---
name: link-version-npu-remove
description: 替换文档链接版本号并删除 NPU 条件内容块。将 https://gitcode.com/ 开头链接中的 master 替换为用户指定版本号（示例格式 9.3.0-beta.1），将 https://www.hiascend.com/document/ 开头链接中的 latest 替换为用户指定版本号（示例格式 930beta1），Ascend/triton-ascend、Ascend/torchair、Ascend/ModelZoo-PyTorch 前缀除外；同时删除 Markdown 文档中特定 NPU 型号的条件内容块（npu 条件注释块），默认删除 IPV350，用户可交互式指定要删除的 NPU 型号（支持多个）。当用户要求替换链接版本号、更新文档链接版本、批量修改 gitcode/hiascend 链接版本、删除 NPU 条件内容、清理特定芯片型号（IPV350、310p、A3、910 等）内容、或同时执行两类处理时使用。所有参数通过交互方式由用户输入。
---

# 链接版本号替换 + NPU 条件内容删除

对 Markdown 文档执行两类处理，全部参数通过 question 工具交互式获取：

1. 链接版本号替换：把 `https://gitcode.com/` 链接中的 `master`、`https://www.hiascend.com/document/` 链接中的 `latest` 替换为用户指定的版本号。
2. NPU 条件内容块删除：删除特定 NPU 型号的条件内容块，默认 `IPV350`，由用户交互式指定要删除的型号（支持一次删除多个）。

## 功能一：链接版本号替换

把文档中两类链接的版本号替换为用户交互输入指定的版本。只处理下面两类链接，其余链接一律保持原样：

| 链接开头 | 被替换的路径段 | 版本号示例格式 |
| --- | --- | --- |
| `https://gitcode.com/` | `master` | `9.3.0-beta.1` |
| `https://www.hiascend.com/document/` | `latest` | `930beta1` |

gitcode 类排除清单：以下列前缀开头的链接，即使含有 `master` 路径段也一律不替换：

| 排除前缀 | 处理方式 |
| --- | --- |
| `https://gitcode.com/Ascend/triton-ascend/` | 保持原样，汇报时提醒用户自行修改 |
| `https://gitcode.com/Ascend/torchair/` | 保持原样，汇报时提醒用户自行修改 |
| `https://gitcode.com/Ascend/ModelZoo-PyTorch/` | 保持原样，无需任何修改 |

替换规则（严格按完整路径段匹配）：

- gitcode 类：仅把链接中作为完整路径段的 `master` 替换为用户输入的版本号。完整路径段指 `master` 前后紧邻 `/`、字符串开头或结尾。
  - 例：`https://gitcode.com/ascend/metadef/blob/master/README.md` → `https://gitcode.com/ascend/metadef/blob/9.3.0-beta.1/README.md`
  - 链接中不含 `master` 路径段时保持原样。
- gitcode 排除清单：以 `https://gitcode.com/Ascend/triton-ascend/`、`https://gitcode.com/Ascend/torchair/`、`https://gitcode.com/Ascend/ModelZoo-PyTorch/` 开头的链接，其中的 `master` 一律不替换，按“保持原样”计入统计。
- hiascend 文档类：仅把链接中作为完整路径段的 `latest` 替换为用户输入的版本号。
  - 例：`https://www.hiascend.com/document/detail/zh/canncommercial/latest/instg/instg_0000.html` → `https://www.hiascend.com/document/detail/zh/canncommercial/930beta1/instg/instg_0000.html`
  - 链接中不含 `latest` 路径段时保持原样。
- 只替换 URL 本身；URL 之外的文本，以及锚点（`#`）、查询参数（`?`）中出现的 master/latest 不动。
- 禁止子串误替换：`masterpiece`、`latestVersion` 之类不构成完整路径段的匹配一律不改。
- 匹配区分大小写，只替换小写的 `master`、`latest`。

## 功能二：NPU 条件内容块删除

删除 Markdown 文档中特定 NPU 产品线的内容块。处理三种情况：
1. 纯目标 NPU 块：整块删除（含 opener/closer/内容）
2. 混合块（如 `<!-- npu="A3,910,310p" id3 -->` 与 `<!-- end id3 -->`）：从 npu 列表中移除目标 NPU（此处的产品型号以及id后的数字都为示例）
3. 混合块内部嵌套的目标 NPU 子块：删除子块，保留外层块
4. 多余空行自动合并

默认删除 `IPV350`；实际执行时通过交互式提问由用户指定要删除的 NPU 型号，支持一次指定多个（逗号分隔），逐个型号执行删除。

### 脚本调用

使用本 skill 目录下的 `remove_npu_content.py`（与本 SKILL.md 同目录；若缺失，按下方“脚本内容”小节重新保存）：

```bash
python remove_npu_content.py <目标目录> [--npu <目标NPU名称>]
```

**参数说明：**
- `<目标目录>`：必填，要处理的 Markdown 文件所在目录路径
- `--npu <名称>`：可选，要删除的 NPU 名称，默认为 `IPV350`

**示例：**

```bash
# 删除 IPV350 相关内容（默认）
python remove_npu_content.py D:\docs\user_guides

# 删除其他 NPU 相关内容
python remove_npu_content.py /path/to/docs --npu 310p
python remove_npu_content.py /path/to/docs --npu A3
```

用户指定多个型号时逐个运行，例如 `--npu IPV350` 与 `--npu 310p` 各运行一次。

### 脚本内容

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os
import sys
import argparse


def create_arg_parser():
    parser = argparse.ArgumentParser(
        description='删除 Markdown 中特定 NPU 的条件内容块',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python remove_npu_content.py D:\\docs\\user_guides
  python remove_npu_content.py /path/to/docs --npu 310p
  python remove_npu_content.py /path/to/docs --npu A3
"""
    )
    parser.add_argument('target_dir', help='要处理的目录路径')
    parser.add_argument('--npu', default='IPV350', help='要删除的 NPU 名称（默认: IPV350）')
    return parser


OPENER = re.compile(r'<!--\s*npu="([^"]*)"\s+(id\d+)\s*-->')
CLOSER = re.compile(r'<!--\s*end\s+(id\d+)\s*-->')


def process_file(filepath, target_npu):
    raw = open(filepath, 'rb').read()
    newline = '\r\n' if b'\r\n' in raw else '\n'
    content = raw.decode('utf-8')
    lines = content.split(newline)

    for _ in range(20):
        prev = list(lines)
        lines = remove_inner_target_only(lines, target_npu)
        lines = remove_target_from_mixed(lines, target_npu)
        lines = remove_standalone_target_only(lines, target_npu)
        if lines == prev:
            break

    lines = collapse_blank_lines(lines)
    new_content = newline.join(lines)
    if new_content != content:
        with open(filepath, 'wb') as f:
            f.write(new_content.encode('utf-8'))
        return True
    return False


def remove_inner_target_only(lines, target_npu):
    result = []
    depth = 0
    target_open_depth = 0
    target_skip = False
    for line in lines:
        stripped = line.strip()
        m_open = OPENER.match(stripped)
        m_close = CLOSER.match(stripped)

        if m_open:
            npus = [n.strip() for n in m_open.group(1).split(',')]
            if depth > 0 and not target_skip and npus == [target_npu]:
                target_open_depth = depth
                target_skip = True
                depth += 1
                continue
            result.append(line)
            depth += 1
        elif m_close:
            if target_skip and depth == target_open_depth + 1:
                target_skip = False
                target_open_depth = 0
                depth -= 1
                continue
            depth -= 1
            result.append(line)
        else:
            if target_skip:
                continue
            result.append(line)
    return result


def remove_target_from_mixed(lines, target_npu):
    result = []
    for line in lines:
        m = OPENER.match(line.strip())
        if m:
            npus = [n.strip() for n in m.group(1).split(',')]
            if target_npu in npus and len(npus) > 1:
                npus.remove(target_npu)
                new_npus = ','.join(npus)
                line = re.sub(r'npu="[^"]*"', f'npu="{new_npus}"', line, count=1)
        result.append(line)
    return result


def remove_standalone_target_only(lines, target_npu):
    result = []
    i = 0
    while i < len(lines):
        m_open = OPENER.match(lines[i].strip())
        if m_open and [n.strip() for n in m_open.group(1).split(',')] == [target_npu]:
            block_id = m_open.group(2)
            j = i + 1
            depth = 1
            while j < len(lines):
                sj = lines[j].strip()
                if OPENER.match(sj) and OPENER.match(sj).group(2) == block_id:
                    depth += 1
                elif CLOSER.match(sj) and CLOSER.match(sj).group(1) == block_id:
                    depth -= 1
                    if depth == 0:
                        i = j + 1
                        break
                j += 1
            else:
                result.append(lines[i])
                i += 1
            continue
        result.append(lines[i])
        i += 1
    return result


def collapse_blank_lines(lines):
    result = []
    for line in lines:
        if line.strip() == '' and result and result[-1].strip() == '':
            continue
        result.append(line)
    while result and result[-1].strip() == '':
        result.pop()
    result.append('')
    return result


if __name__ == '__main__':
    parser = create_arg_parser()
    args = parser.parse_args()

    base_dir = args.target_dir
    target_npu = args.npu

    if not os.path.isdir(base_dir):
        print(f"错误：目录不存在: {base_dir}")
        sys.exit(1)

    print(f"目标目录: {base_dir}")
    print(f"目标 NPU: {target_npu}")
    print()

    modified_count = 0
    for dirpath, dirnames, filenames in os.walk(base_dir):
        for filename in sorted(filenames):
            if not filename.endswith('.md'):
                continue
            filepath = os.path.join(dirpath, filename)
            raw = open(filepath, 'rb').read()
            if target_npu.encode() not in raw:
                continue
            relpath = os.path.relpath(filepath, base_dir)
            if process_file(filepath, target_npu):
                print(f"  MODIFIED: {relpath}")
                modified_count += 1
            else:
                print(f"  no change:  {relpath}")

    print(f"\n{modified_count} files modified")
```

## 执行流程

1. 确定处理对象
   - 用户已指定文件或目录：以指定对象为准；目录则递归处理其中全部 `.md` 文件。
   - NPU 条件内容删除以目录为单位执行；用户指定单个文件时，询问是否对该文件所在目录执行 NPU 删除，用户不同意则仅执行链接替换。
   - 用户未指定对象但给了一段文本：仅执行链接版本号替换，直接输出结果，不落盘（NPU 删除不适用于纯文本）。
   - 用户未指定任何对象：用 question 工具询问要处理哪个文件或目录。

2. 扫描并分类
   - 逐行扫描所有 URL（包括 Markdown 链接、HTML href、反引号内的裸链接），按前缀分类：
     - gitcode 类：以 `https://gitcode.com/` 开头；
     - hiascend 文档类：以 `https://www.hiascend.com/document/` 开头；
     - 其他类：一律不做任何修改，也不为其提问。
   - gitcode 类中命中排除清单（`Ascend/triton-ascend/`、`Ascend/torchair/`、`Ascend/ModelZoo-PyTorch/` 前缀）的链接单独记录；若 gitcode 类只出现排除清单中的链接，则视为没有需要替换的 gitcode 链接。
   - 扫描 NPU 条件内容块：统计所有`<!-- npu="A3" id2 -->` 与 `<!-- end id2 -->` 注释（此处的产品型号以及id后的数字都为示例），提取去重后的 NPU 型号列表（如 IPV350、910、310p、A3）及出现次数。
   - 记录每类是否出现及出现次数。

3. 交互式获取参数（必须用 question 工具，禁止自行猜测、编造或推导版本号或 NPU 型号）
   - 在同一次 question 调用中提出实际需要的问题：
     - 存在可替换的 gitcode 链接时：“gitcode 链接中的 master 要替换为哪个版本号？（示例格式：9.3.0-beta.1）”
     - 存在 hiascend 文档链接时：“hiascend 文档链接中的 latest 要替换为哪个版本号？（示例格式：930beta1）”
     - 存在 NPU 条件内容块时：“要删除哪些 NPU 型号？”，multiple=true，选项由扫描到的型号生成（`IPV350` 排最前并标注“默认”，其余按出现次数降序排列），另加“跳过 NPU 内容删除”选项；用户也可自行输入，多个型号用逗号分隔
   - 版本号原样使用用户输入，不做格式转换、不做自动推断（例如不得把 9.3.0-beta.1 自动转成 930beta1）。
   - NPU 型号原样使用用户输入，不做格式转换；未检测到 NPU 条件内容块时跳过 NPU 提问，也不做 NPU 删除；用户选择“跳过 NPU 内容删除”时同样不执行。
   - 两个版本号只有用户明确说明共用同一个版本号时，才允许复用同一输入；否则必须分开提问。
   - 某类处理对象未出现时，跳过对应提问，也不做该类处理。

4. 执行处理（先 NPU 删除，后链接替换；NPU 块内可能包含链接，先删除可避免对即将删除的内容做无谓替换，使汇报的链接替换数与最终文档一致）
   - NPU 条件内容删除：对用户指定的每个 NPU 型号，依次运行 `python remove_npu_content.py <目标目录> --npu <型号>`（脚本位于本 skill 目录下）。
   - 链接版本号替换：按“功能一”的规则执行完整路径段替换。
   - 两类处理写回时均不得改变文件编码、BOM 与换行符，除处理目标外不做任何其他改动（不重排格式、不改换行、不增删内容）。

5. 写回并汇报
   - 链接替换：每类链接替换处数、保持原样处数，并附修改前后对照表；单独列出实际出现的 `Ascend/triton-ascend/` 与 `Ascend/torchair/` 链接及所在文件，明确提示这两类需要用户自行修改；`Ascend/ModelZoo-PyTorch/` 链接保持 master 即为正确状态，无需提示修改。
   - NPU 删除：每个型号修改的文件数及清单（脚本输出的 MODIFIED 列表）；可通过 grep 验证无残留：`grep -r "<目标NPU>" <目标目录> --include="*.md"` 应返回空结果。
   - 未发现任何可处理内容时，明确告知用户，不做任何修改。

## 注意事项
- 不要把处理范围扩大到用户未要求的其他文件。
- 原有两个 skill（link-version-replace、remove-npu-conditional-content）保持不变，本 skill 为合并后的独立入口。
- 处理完成后不需要额外运行任何检查或 lint，除非用户要求（NPU 删除的 grep 残留验证除外）。
