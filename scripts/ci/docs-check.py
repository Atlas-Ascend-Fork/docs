#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
docs-check.py —— 文档(手册)维度的索引驱动批量检查

用法:
    python3 docs-check.py <docs-index.json路径或URL> <用户工作区目录> [--keep-temp]

工作区布局(脚本自动创建三个子目录, 所有产物集中于此):
    <工作区>/src/         # 各仓克隆落位(已有克隆则直接复用, 不覆盖——支持本地修改后测试)
    <工作区>/output/      # 最终产物: {手册名称}/StaticCheck.csv + {仓}_output.md + docs_check_summary.csv
    <工作区>/build/       # 中间产物: 远端下载(docs-index/config_template) + manifest/跨仓边/引擎日志

索引配置:
    - 路径: 本地文件路径或 http URL(自动下载到 build/docs-index.json)
    - documents: [{name, repo, branch, entry, id?}, ...]  按文档(手册)维度组织
      数据来源: README.md「CANN产品文档源文件」章节的程序化映射(name=链接文本)
    - traverse: {maxDepth, maxFilesPerRepo}  串接防御性参数
    - 配置文件只读, 脚本不回写

文档模型:
    - 一个文档 = 一个检查任务 = 入口索引文件出发的完整菜单树(可跨仓) + 点状纳入的跨仓正文
    - 仓是文档的宿主属性, 文件集可跨仓

串接规则(索引树驱动——只解析索引文件中的链接, 正文文件的链接一律不解析):
    - 索引文件 = 入口索引 ∪ submenu 边目标(仓内/跨仓, 结构传播)
    - 索引文件中的.md链接逐条分流:
       - 带<a name="sub_menu">标记 → 目标是子索引 → 入队展开(跨仓目标仓缺失则自动浅克隆;
         若目标已是其他声明文档的入口则去重不展开)
       - 无标记 → 目标是正文 → 纳入受检集, 不再解析其链接(正文互链/正文跨链均不串接)
    - 正文文件: 仅作为受检对象, 链接有效性由引擎检查
    - 防环防泄漏: (repo, path)全局去重 + maxDepth(索引树深度) + maxFilesPerRepo(按文档×仓计数)

处理逻辑(六阶段):
    1. 获取index配置: 读docs-index.json(文档清单+traverse参数)
    2. 逐文档串接索引树: 入口+submenu子索引展开, 遇到跨仓目标仓缺失则直接浅克隆;
       跨仓链接声明分支与手册分支(入口声明)不一致 → branch-mismatch报错(拦截级)
    3. 仓维度汇总待检集: 按 {仓: 文件集} 归并(全文档并集)并记录文件→手册归属
    4. 检查: 引擎逐仓执行一次(docPath=该仓全部受检文件的精确正则)
    5. 按手册归档: 引擎结果按文件归属拆分回各手册 + Index-Traverse串接报错行 → {手册}/StaticCheck.csv
"""
import copy
import csv
import json
import os
import posixpath
import re
import subprocess
import sys
import urllib.request
from collections import deque
from datetime import datetime
from urllib.parse import unquote

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_ENGINE = os.path.join(SCRIPT_DIR, "docs-ci-v2.js")

# ---- 远端资源配置(http开头=远程, 否则视为本地路径) ----
RAW_BASE = "https://raw.gitcode.com/cann/.gitcode/raw/master/actions/staticcheck/dist/staticcheck/docs-ci"
CONFIG_TEMPLATE_URL = "%s/.doctools/config.json" % RAW_BASE    # 统一config: 远端(运行时下载后按文档×仓注入)
URL_WHITELIST_URL = "%s/.doctools/url.whitelist.json" % RAW_BASE  # 白名单: 默认远端(引擎自行拉取)
MARKDOWNLINT_CONFIG_URL = "%s/.doctools/markdownlint.config.json" % RAW_BASE  # markdownlint规则(引擎自行拉取)
CODESPELL_WHITELIST_URL = "%s/.doctools/whitelist_words.txt" % RAW_BASE  # codespell白名单(引擎自行拉取)
ENGINE_URL = "%s/docs-ci-v2.js" % RAW_BASE                    # 引擎: 本地缺失时下载


CHECK_ITEMS = ["link-validity-check", "resource-existence-check", "tag-closed-check", "markdownlint", "codespell-check"]
CSV_HEADER = ["检查类型", "检测结果", "是否拦截", "严重程度", "文件路径", "错误位置", "错误信息", "错误内容"]
SUMMARY_HEADER = ["文档", "宿主仓", "状态", "错误数量", "受检文件数", "跨仓文件数"]
LANJIE_TOOLS = ["StaticCheck_link_validity", "StaticCheck_resource_existence", "StaticCheck_tag_closed", "StaticCheck_compliance"]

# 自动克隆(跨仓目标/宿主仓缺失即浅克隆, 无配置开关)
CLONE_URL = "https://gitcode.com/cann/{repo}.git"
CLONE_DEPTH = 1
MAX_DEPTH = 10               # 串接最大索引树深度
MAX_FILES_PER_REPO = 10000   # 单文档单仓受检文件数上限
# 跨仓md链接(gitcode blob形态): 仓/分支/路径
GITCODE_MD_RE = re.compile(r"^https://gitcode\.com/cann/([^/]+)/blob/([^/]+)/(.+?\.md)$", re.I)
LINK_RE = re.compile(r"\]\(\s*([^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")
MENU_ANCHOR_RE = re.compile(r"name=\"sub_menu\"")
# 拦截级串接错误(置文档状态"未通过"); truncated为警告级
BLOCKING_CODES = {"entry-missing", "read-failed", "cross-target-missing", "clone-failed", "branch-mismatch", "engine-failed"}


def norm_tool(check_type):
    """link-validity-check -> StaticCheck_link_validity"""
    return "StaticCheck_" + check_type.replace("-", "_")


def http_download(url, dest):
    """下载远端文件到本地(原子写入: 先写.tmp, 成功后rename)"""
    tmp = dest + ".tmp"
    req = urllib.request.Request(url, headers={"User-Agent": "docs-check"})
    with urllib.request.urlopen(req, timeout=300) as r, open(tmp, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
    os.rename(tmp, dest)


def ensure_engine():
    """引擎本地缺失时从远端下载"""
    if os.path.isfile(LOCAL_ENGINE):
        return LOCAL_ENGINE
    if not ENGINE_URL.startswith("http"):
        return None
    print("[info] 本地无引擎, 从远端下载: %s" % ENGINE_URL)
    http_download(ENGINE_URL, LOCAL_ENGINE)
    return LOCAL_ENGINE if os.path.isfile(LOCAL_ENGINE) else None


def load_config_template(build_dir):
    """读取统一配置模板: http链接则下载到build目录, 否则读本地文件"""
    if CONFIG_TEMPLATE_URL.startswith("http"):
        dest = os.path.join(build_dir, "config_template.json")
        print("[info] 从远端下载配置模板: %s" % CONFIG_TEMPLATE_URL)
        http_download(CONFIG_TEMPLATE_URL, dest)
        with open(dest, encoding="utf-8") as f:
            return json.load(f)
    with open(CONFIG_TEMPLATE_URL, encoding="utf-8") as f:
        return json.load(f)


def get_branch(repo):
    r = subprocess.run(["git", "-C", repo, "rev-parse", "--abbrev-ref", "HEAD"],
                       capture_output=True, text=True)
    branch = r.stdout.strip()
    if r.returncode != 0 or not branch or branch == "HEAD":
        return "master"
    return branch


def load_docs_index(index_path, build_dir):
    """读取文档索引配置(支持本地路径与http URL), 校验documents段并补齐id"""
    if index_path.startswith("http"):
        dest = os.path.join(build_dir, "docs-index.json")
        print("[info] 从远端下载索引配置: %s" % index_path)
        http_download(index_path, dest)
        index_path = dest
    if not os.path.isfile(index_path):
        print("[error] 缺少文档索引配置: %s" % index_path)
        sys.exit(1)
    with open(index_path, encoding="utf-8") as f:
        data = json.load(f)
    docs = data.get("documents")
    if not isinstance(docs, list) or not docs:
        print("[error] 文档索引配置缺少documents段: %s" % index_path)
        sys.exit(1)
    for d in docs:
        for key in ("name", "repo", "entry"):
            if not d.get(key):
                print("[error] 文档索引缺少 %s 字段: %s" % (key, d))
                sys.exit(1)
        if not d.get("id"):
            d["id"] = "%s_%s" % (d["repo"], d["entry"].strip()[:-3].replace("/", "_"))
    return data


def crawl_document(doc, state, workspace, src_dir, declared_entries, errors, edges,
                   max_depth=MAX_DEPTH, max_files_per_repo=MAX_FILES_PER_REPO):
    """串接单个手册的受检文件集(索引树驱动; 遇跨仓目标仓缺失则内联浅克隆)
    state: {queue, visited, files} — 跨手册持续
    分支一致性: 跨仓链接(submenu/正文)声明分支须等于手册分支(文档声明, 默认master);
               不一致 → branch-mismatch拦截级错误: submenu不再克隆不展开, 正文不纳入"""
    manual_branch = doc.get("branch") or "master"
    entry_repo = doc["repo"]
    entry_path = posixpath.normpath(doc["entry"].strip())

    seen_errors = set()

    def add_error(code, repo, path, detail):
        key = (code, repo, path)
        if key not in seen_errors:
            seen_errors.add(key)
            errors.append({"code": code, "repo": repo, "path": path, "detail": detail})

    def add_edge(etype, status, src_repo, src_path, dst_repo, dst_path):
        edges.append({"etype": etype, "status": status,
                      "src": "%s:%s" % (src_repo, src_path), "dst": "%s:%s" % (dst_repo, dst_path)})

    def add_file(repo, path):
        if len(state["files"].get(repo, set())) >= max_files_per_repo:
            add_error("truncated", repo, path,
                      "受检文件数达到上限%d, 该仓超出部分不再纳入" % max_files_per_repo)
            return
        state["files"].setdefault(repo, set()).add(path)

    def cross_ready(tgt_repo, tgt_path, tgt_branch, kind, src_repo, src_path, depth):
        """跨仓目标处理: 分支校验→自动浅克隆→存在性校验→纳入/展开"""
        if tgt_branch != manual_branch:
            add_error("branch-mismatch", tgt_repo, tgt_path,
                      "跨仓链接声明分支%s与手册分支%s不一致, 不克隆不纳入" % (tgt_branch, manual_branch))
            add_edge(kind, "branch-mismatch", src_repo, src_path, tgt_repo, tgt_path)
            return
        if not ensure_repo(tgt_repo, tgt_branch, workspace, src_dir, errors, doc["id"]):
            add_edge(kind, "clone-failed", src_repo, src_path, tgt_repo, tgt_path)
            return
        if not os.path.isfile(os.path.join(workspace[tgt_repo], tgt_path)):
            add_error("cross-target-missing", tgt_repo, tgt_path, "跨仓目标文件不存在(分支%s)" % tgt_branch)
            add_edge(kind, "target-missing", src_repo, src_path, tgt_repo, tgt_path)
        elif kind == "submenu":
            state["queue"].append((tgt_repo, tgt_path, depth))
            add_edge("submenu", "expanded", src_repo, src_path, tgt_repo, tgt_path)
        else:
            add_file(tgt_repo, tgt_path)
            add_edge("body", "included", src_repo, src_path, tgt_repo, tgt_path)

    if not ensure_repo(entry_repo, manual_branch, workspace, src_dir, errors, doc["id"]):
        return  # 宿主仓克隆失败, 串接无法开始

    # ---- 处理索引队列 ----
    queue = state["queue"]
    while queue:
        repo, path, depth = queue.popleft()
        if (repo, path) in state["visited"]:
            continue
        state["visited"].add((repo, path))
        full = os.path.join(workspace[repo], path)
        if not os.path.isfile(full):
            if (repo, path) == (entry_repo, entry_path):
                add_error("entry-missing", repo, path, "入口文件不存在(声明于docs-index.json)")
            else:
                add_error("cross-target-missing", repo, path, "submenu子索引文件不存在")
            continue
        add_file(repo, path)
        try:
            with open(full, encoding="utf-8") as f:
                text = f.read()
        except (OSError, UnicodeDecodeError) as e:
            add_error("read-failed", repo, path,
                      "md文件读取失败: %s" % str(e).splitlines()[-1][:120])
            continue
        base_dir = posixpath.dirname(path)
        for line in text.splitlines():
            for raw in LINK_RE.findall(line):
                frag = unquote(raw.split("#", 1)[0].strip())
                if not frag:
                    continue
                g = GITCODE_MD_RE.match(frag)
                if g:
                    tgt_repo, tgt_branch = g.group(1), g.group(2)
                    tgt_path = posixpath.normpath(unquote(g.group(3)))
                    is_cross = tgt_repo != repo
                elif frag.lower().endswith(".md"):
                    tgt_repo, tgt_branch, is_cross = repo, None, False
                    tgt_path = posixpath.normpath(posixpath.join(base_dir, frag))
                else:
                    continue
                if not tgt_path or tgt_path.startswith("../") or tgt_path == "..":
                    continue
                kind = "submenu" if MENU_ANCHOR_RE.search(line) else "body"
                if (tgt_repo, tgt_path) != (entry_repo, entry_path) and (tgt_repo, tgt_path) in declared_entries:
                    add_edge(kind, "dedup-declared", repo, path, tgt_repo, tgt_path)
                    continue
                if is_cross:
                    if kind == "submenu" and depth >= max_depth:
                        add_error("truncated", repo, tgt_path,
                                  "串接深度达到上限%d, 该分支不再展开" % max_depth)
                        add_edge(kind, "depth-truncated", repo, path, tgt_repo, tgt_path)
                        continue
                    cross_ready(tgt_repo, tgt_path, tgt_branch, kind, repo, path, depth + 1)
                elif kind == "submenu":
                    # 仓内submenu → 子索引入队展开(缺失报结构断链)
                    if not os.path.isfile(os.path.join(workspace[repo], tgt_path)):
                        add_error("cross-target-missing", repo, tgt_path, "submenu子索引文件不存在")
                    elif depth < max_depth:
                        queue.append((repo, tgt_path, depth + 1))
                elif os.path.isfile(os.path.join(workspace[repo], tgt_path)):
                    # 仓内正文 → 纳入受检集
                    add_file(repo, tgt_path)


def ensure_repo(repo, branch, workspace, src_dir, errors, doc_id):
    """仓缺失则浅克隆(分支取链接声明); 成功登记workspace。返回True=就绪"""
    if repo in workspace:
        return True
    local = os.path.join(src_dir, repo)
    if os.path.isdir(os.path.join(local, ".git")):
        workspace[repo] = local  # 已有本地克隆(用户预置/上次运行), 直接复用
        return True
    url = CLONE_URL.format(repo=repo)
    dest = os.path.join(src_dir, repo)
    cmd = ["git", "clone", "--depth", str(CLONE_DEPTH), "-b", branch or "master", url, dest]
    print("    [info] 自动克隆: %s (%s)" % (url, branch or "master"))
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=900, check=True)
        workspace[repo] = dest
        return True
    except subprocess.CalledProcessError as e:
        tail = ((e.stderr or "").strip().splitlines() or [""])[-1]
        errors.append({"code": "clone-failed", "repo": repo, "path": "-", "detail": "git clone失败: %s" % tail})
        return False
    except subprocess.TimeoutExpired:
        errors.append({"code": "clone-failed", "repo": repo, "path": "-", "detail": "git clone超时(900s)"})
        return False


def build_docpath(files):
    """受检文件清单 -> 精确匹配docPath正则(引擎仅支持docPath圈定检查范围)"""
    if not files:
        return r"(?!x)x"
    return "^(?:%s)$" % "|".join(re.escape(f) for f in files)


def run_check(engine, config_tpl, repo_path, repo_name, branch, files, build_dir, report_dir, out_prefix):
    """构造该文档×仓运行配置并执行引擎:
       注入受检文件集(docPath精确正则)/白名单 -> node执行docs-ci-v2.js
       中间产物(配置/result/日志)落build目录, 引擎原始输出落手册归档目录
       返回 (result.json路径, 耗时秒, 退出码)"""
    cfg = copy.deepcopy(config_tpl)
    base = cfg["config"]["base"]
    base["docPath"] = build_docpath(files)
    base["linkValidityCheckRemoteWhitelistUrl"] = URL_WHITELIST_URL
    base["resourceExistenceCheckRemoteWhitelistUrl"] = URL_WHITELIST_URL
    base["markdownlintRemoteConfigUrl"] = MARKDOWNLINT_CONFIG_URL
    base["codespellCheckRemoteWhitelistUrl"] = CODESPELL_WHITELIST_URL
    base["ci"] = list(CHECK_ITEMS)
    cfg["repo"] = {
        "cann/" + repo_name: {
            "extendConfig": "base",
            "branches": {branch: {"ci": list(CHECK_ITEMS)}},
        }
    }
    run_cfg = os.path.join(build_dir, "run_config_%s.json" % out_prefix)
    with open(run_cfg, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False)
    result_json = os.path.join(build_dir, "%s_result.json" % out_prefix)
    output_md = os.path.join(report_dir, "%s_output.md" % repo_name)
    cmd = [
        "node", engine,
        "--repoPath=%s" % repo_path,
        "--checkAll=true",
        "--targetOwnerRepo=cann/%s" % repo_name,
        "--targetBranch=%s" % branch,
        "--outputCount=20000",
        "--concurrency=8",
        "--ciConfigUrl=%s" % run_cfg,
        "--outputJson=true",
        "--outputJsonPath=%s" % result_json,
        "--outputPath=%s" % output_md,
    ]
    start = datetime.now()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=3600)
    elapsed = (datetime.now() - start).total_seconds()
    with open(os.path.join(build_dir, "%s_engine.log" % out_prefix), "w", encoding="utf-8") as f:
        f.write(r.stdout or "")
        f.write("\n---STDERR---\n")
        f.write(r.stderr or "")
    return result_json, elapsed, r.returncode


def parse_result(result_json, repo_tag):
    """解析result.json -> 告警明细行(文件路径加 cann/{repo}: 前缀标识跨仓归属)"""
    rows = []
    if not os.path.isfile(result_json):
        return rows
    with open(result_json, encoding="utf-8") as f:
        data = json.load(f)
    for w in data:
        check_type = w.get("checkType", "")
        if check_type not in CHECK_ITEMS:
            continue
        tool = norm_tool(check_type).replace("_check", "")
        rows.append([
            tool,
            "不通过",
            "拦截" if tool in LANJIE_TOOLS else "不拦截",
            "严重",
            "%s:%s" % (repo_tag, w.get("filePath", "")),
            w.get("position", ""),
            w.get("message", ""),
            w.get("content", ""),
        ])
    return rows


def build_traverse_rows(errors):
    """串接异常 -> Index-Traverse 明细行(排序: 拦截级在前, 警告级在后)"""
    rows = []
    for e in sorted(errors, key=lambda x: (x["code"] not in BLOCKING_CODES, x["repo"], x["path"])):
        blocking = e["code"] in BLOCKING_CODES
        msg = {
            "entry-missing": "入口文件不存在",
            "read-failed": "md文件读取失败",
            "cross-target-missing": "串接目标文件不存在",
            "clone-failed": "仓库自动克隆失败",
            "branch-mismatch": "跨仓链接分支与手册分支不一致",
            "engine-failed": "引擎执行失败, 检查结果不可信",
            "truncated": "串接达到上限截断",
        }.get(e["code"], e["code"])
        rows.append([
            "Index-Traverse",
            "不通过",
            "拦截" if blocking else "不拦截",
            "严重" if blocking else "警告",
            "%s:%s" % (e["repo"], e["path"]),
            "-",
            msg,
            e["detail"],
        ])
    return rows


TAG_CHECK_JS_URL = "%s/js/tag_check.js" % RAW_BASE  # 标签合法性检查脚本(引擎外独立JS)

def check_tags(files, repo_path, repo_name, build_dir):
    """标签合法性检查(TG-01~TG-08): 下载远端js/tag_check.js, 逐文件调用, 解析JSON结果
    返回 compliance 行列表(八列)"""
    js_path = os.path.join(build_dir, "tag_check.js")
    if not os.path.isfile(js_path):
        http_download(TAG_CHECK_JS_URL, js_path)
    result_json = os.path.join(build_dir, "tag_check_result.json")
    rows = []
    for path in files:
        if os.path.isfile(result_json):
            os.remove(result_json)
        subprocess.run(["node", js_path, os.path.join(repo_path, path),
                        build_dir, repo_name], capture_output=True, timeout=30)
        if not os.path.isfile(result_json):
            continue
        for item in json.load(open(result_json, encoding="utf-8")):
            rows.append([
                "StaticCheck_compliance", "不通过", "拦截",
                item.get("rule_level", "严重"),
                "cann/%s:%s" % (repo_name, item.get("location", path).replace(repo_path + "/", "")),
                "第 %s 行" % item.get("line_number", "N/A"),
                item.get("rule_item", ""),
                item.get("description", ""),
            ])
    if os.path.isfile(result_json):
        os.remove(result_json)
    return rows


def check_encoding(full_path):
    """编码格式检查(EC-01/EC-02): UTF-8无BOM"""
    with open(full_path, "rb") as f:
        if f.read(3) == b"\xef\xbb\xbf":
            return "文件含UTF-8 BOM, 请转换为无BOM的纯UTF-8格式"
    try:
        open(full_path, encoding="utf-8").read()
    except UnicodeDecodeError:
        return "文件编码不是UTF-8, 请转换为纯UTF-8格式"
    return None


def csv_escape(s):
    """CSV公式注入防护: 首字符为 =+-@\t\r 时前缀单引号, 阻止Excel解析为公式(CWE-1236)"""
    if s and s[0] in ('=', '+', '-', '@', '\t', '\r'):
        return "'" + s
    return s


def write_csv(doc_dir, rows):
    """手册归档目录下写 StaticCheck.csv: Index-Traverse行 + 引擎结果行; 无告警检查项补'通过'行"""
    engine_rows = [r for r in rows if r[0] != "Index-Traverse"]
    data = [list(CSV_HEADER)]
    data.extend(r for r in rows if r[0] == "Index-Traverse")
    data.extend(engine_rows)
    hit_tools = {r[0] for r in engine_rows}
    for item in CHECK_ITEMS:
        tool = norm_tool(item).replace("_check", "")
        if tool not in hit_tools:
            data.append([tool, "通过", "", "", "", "", "", ""])
    os.makedirs(doc_dir, exist_ok=True)
    path = os.path.join(doc_dir, "StaticCheck.csv")
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow([csv_escape(c) if isinstance(c, str) else c for c in row])
    return path


def write_manifest(doc_id, doc, files, build_dir):
    """受检文件清单(build中间产物): 按宿主仓分节(入口仓在前), 每行一个仓库根相对路径"""
    path = os.path.join(build_dir, "%s_manifest.txt" % doc_id)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# 文档: %s (id=%s, 入口: cann/%s:%s)\n" % (doc["name"], doc_id, doc["repo"], doc["entry"]))
        ordered = [doc["repo"]] + sorted(r for r in files if r != doc["repo"])
        for repo in ordered:
            if not files[repo]:
                continue
            tag = "宿主仓" if repo == doc["repo"] else "跨仓"
            f.write("## cann/%s (%d 个文件, %s)\n" % (repo, len(files[repo]), tag))
            f.write("".join(p + "\n" for p in files[repo]))
    return path


def write_edges(edges, build_dir):
    """跨仓边审计清单(build中间产物): [类型/状态] 源仓:源文件 -> 目标仓:目标文件"""
    path = os.path.join(build_dir, "cross_repo_edges.txt")
    with open(path, "w", encoding="utf-8") as f:
        for e in edges:
            f.write("[%s/%s] %s -> %s\n" % (e["etype"], e["status"], e["src"], e["dst"]))
    return path


def write_summary_csv(summary, out_dir):
    """总报告CSV: 文档/宿主仓/状态/错误数量/受检文件数/跨仓文件数 六列"""
    path = os.path.join(out_dir, "docs_check_summary.csv")
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(SUMMARY_HEADER)
        writer.writerows(summary)
    return path


def cleanup_temp(prefix, build_dir):
    """删除文档×仓中间产物(运行时配置/结构化结果/引擎日志), 保留清单/边审计/引擎输出"""
    for pattern in ("run_config_%s.json", "%s_result.json", "%s_engine.log"):
        p = os.path.join(build_dir, pattern % prefix)
        if os.path.isfile(p):
            os.remove(p)


def main():
    keep_temp = "--keep-temp" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        sys.exit(2)
    index_path = os.path.abspath(args[0])        # 入参1: 文档索引配置路径
    workspace_dir = os.path.abspath(args[1])     # 入参2: 用户工作区(脚本在其下自建src/output/build)
    src_dir = os.path.join(workspace_dir, "src")
    out_dir = os.path.join(workspace_dir, "output")
    build_dir = os.path.join(workspace_dir, "build")
    for d in (src_dir, out_dir, build_dir):
        os.makedirs(d, exist_ok=True)
    docs_index = load_docs_index(index_path, build_dir)
    documents = docs_index["documents"]
    traverse = docs_index.get("traverse", {})
    max_depth = int(traverse.get("maxDepth", MAX_DEPTH))
    max_files_per_repo = int(traverse.get("maxFilesPerRepo", MAX_FILES_PER_REPO))
    declared_entries = {(d["repo"], posixpath.normpath(d["entry"].strip())) for d in documents}
    engine = ensure_engine()
    if not engine or not os.path.isfile(engine):
        print("[error] 检查引擎不可用(本地无且远端下载失败): %s" % LOCAL_ENGINE)
        sys.exit(1)
    if not URL_WHITELIST_URL.startswith("http") and not os.path.isfile(URL_WHITELIST_URL):
        print("[error] 缺少白名单: %s" % URL_WHITELIST_URL)
        sys.exit(1)

    workspace = {}  # 运行内仓注册表(ensure_repo登记); 每次运行全新克隆
    errors_by_doc = {doc["id"]: [] for doc in documents}
    edges = []
    print("工作区: %s (src已克隆 %d 仓) | 文档索引: %d 个文档" % (
        workspace_dir, len(workspace), len(documents)))
    print("检查项: %s" % ", ".join(CHECK_ITEMS))
    print()

    # ---- 阶段2/3: 逐文档串接索引树(遇跨仓目标仓缺失则内联浅克隆) ----
    states = {doc["id"]: {"queue": deque([(doc["repo"], posixpath.normpath(doc["entry"].strip()), 0)]),
                          "visited": set(), "files": {doc["repo"]: set()}}
              for doc in documents}
    for doc in documents:
        crawl_document(doc, states[doc["id"]], workspace, src_dir,
                       declared_entries, errors_by_doc[doc["id"]], edges,
                       max_depth=max_depth, max_files_per_repo=max_files_per_repo)

    # ---- 阶段4: 仓维度汇总待检集 + 文件→手册归属 ----
    repo_files = {}
    file_docs = {}
    for doc in documents:
        for repo, paths in states[doc["id"]]["files"].items():
            for p in paths:
                repo_files.setdefault(repo, set()).add(p)
                file_docs.setdefault((repo, p), []).append(doc)
    n_total = sum(len(v) for v in repo_files.values())
    print(">>> 阶段4: 串接收敛 — %d 仓 %d 文件, 跨仓边 %d 条" % (len(repo_files), n_total, len(edges)))
    print()

    # ---- 阶段5: 检查(每仓一次, 受检集为该仓全部手册的并集) ----
    config_tpl = load_config_template(build_dir)
    rows_by_repo = {}
    engine_failed_repos = set()
    for repo in sorted(repo_files):
        files = sorted(repo_files[repo])
        repo_path = workspace[repo]
        branch = get_branch(repo_path)
        result_json, elapsed, rc = run_check(engine, config_tpl, repo_path, repo, branch,
                                             files, build_dir, out_dir, repo)
        rows = parse_result(result_json, "cann/%s" % repo)
        # 编码格式检查(Python原生, 逐文件)
        for fp in files:
            enc_err = check_encoding(os.path.join(repo_path, fp))
            if enc_err:
                rows.append(["StaticCheck_compliance", "不通过", "拦截", "严重",
                             "cann/%s:%s" % (repo, fp), "-", "EC 编码格式", enc_err])
        # 标签合法性检查(远端JS, 逐文件)
        tag_rows = check_tags(files, repo_path, repo, build_dir)
        rows.extend(tag_rows)
        rows_by_repo[repo] = rows
        if rc != 0 or not os.path.isfile(result_json):
            engine_failed_repos.add(repo)
            print("    [%s] [error] 引擎执行失败(退出码%d, 结果文件%s)——该仓所有手册将标记为未通过" % (
                repo, rc, "缺失" if not os.path.isfile(result_json) else "异常"))
        print("    [%s] 分支: %s | 文件: %d | 耗时: %.1fs | 引擎退出码: %d | 错误: %d" % (
            repo, branch, len(files), elapsed, rc, len(rows)))
        if not keep_temp:
            cleanup_temp(repo, build_dir)
    # 引擎结果按文件归属拆回手册
    rows_by_doc = {doc["id"]: [] for doc in documents}
    for repo, rows in rows_by_repo.items():
        for row in rows:
            p = row[4].split(":", 1)[1] if ":" in row[4] else ""
            for doc in file_docs.get((repo, p), []):
                rows_by_doc[doc["id"]].append(row)
    if engine_failed_repos:
        for doc in documents:
            doc_repos = {r for r in states[doc["id"]]["files"] if states[doc["id"]]["files"][r]}
            if doc_repos & engine_failed_repos:
                failed = sorted(doc_repos & engine_failed_repos)
                errors_by_doc[doc["id"]].append({
                    "code": "engine-failed", "repo": ",".join(failed), "path": "-",
                    "detail": "引擎执行失败(退出码非0或结果文件缺失), 该仓检查结果不可信"})
    print()

    # ---- 阶段6: 按手册归档问题列表 ----
    summary = []
    for doc in documents:
        doc_id, name = doc["id"], doc["name"]
        doc_dir = os.path.join(out_dir, name)
        entry_repo = doc["repo"]
        state = states[doc_id]
        files = {r: sorted(p) for r, p in state["files"].items()}
        n_files = sum(len(v) for v in files.values())
        n_cross = n_files - len(files.get(entry_repo, set()))
        csv_rows = build_traverse_rows(errors_by_doc[doc_id])
        blocking = sum(1 for r in csv_rows if r[2] == "拦截")
        engine_errors = len(rows_by_doc[doc_id])
        csv_rows.extend(rows_by_doc[doc_id])
        status = "未通过" if (blocking or engine_errors) else "通过"
        if n_files == 0:
            status = "未通过" if blocking else "跳过(无受检文件)"
        write_csv(doc_dir, csv_rows)
        if n_files:
            write_manifest(doc_id, doc, files, build_dir)
        print(">>> [%s] %s | 受检 %d 个文件(跨仓 %d) | 错误: %d | 归档: %s/StaticCheck.csv" % (
            name, status, n_files, n_cross, engine_errors + blocking, name))
        summary.append([name, entry_repo, status, engine_errors + blocking, n_files, n_cross])

    edges_path = write_edges(edges, build_dir)
    summary_csv = write_summary_csv(summary, out_dir)
    tpl_cache = os.path.join(build_dir, "config_template.json")
    if not keep_temp and os.path.isfile(tpl_cache):
        os.remove(tpl_cache)
    print()
    print("=" * 72)
    print("| 文档 | 宿主仓 | 状态 | 错误数量 | 受检文件数 | 跨仓文件数 |")
    print("| --- | --- | --- | --- | --- | --- |")
    for row in summary:
        print("| %s | %s | %s | %d | %d | %d |" % tuple(row))
    failed = sum(1 for r in summary if r[2] == "未通过")
    skipped = sum(1 for r in summary if r[2].startswith("跳过"))
    print("=" * 72)
    print("汇总: %d文档, 未通过 %d, 跳过 %d; 报告: %s | 跨仓边: %s (%d条)" % (
        len(summary), failed, skipped, summary_csv, os.path.basename(edges_path), len(edges)))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
