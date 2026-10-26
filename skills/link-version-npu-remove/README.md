# link-version-npu-remove 使用说明

文档后处理合并技能：一次任务中同时完成**链接版本号替换**与 **NPU 条件内容块删除**。

## 1. 启用方式

skill 位于 opencode 全局技能目录，**重启 opencode 后自动生效**，无需任何配置。

## 2. 触发方式

在 opencode 对话中直接用自然语言描述需求即可，例如：

```
帮我处理 D:\docs\zh 目录下的链接，并把 IPV350 的内容删掉
替换 D:\docs\zh 里 gitcode 链接的 master 为 9.3.0-beta.1(仅为示例)
清理 D:\docs\user_guides 中的 310p 芯片内容
处理一下 D:\docs\zh（不指定参数，由 skill 扫描后交互式询问）
```

## 3. 交互流程

skill 会先扫描目标目录，然后**一次性**弹出实际需要的问题（没检测到的处理项不提问）：

| 问题 | 何时出现 | 说明 |
| --- | --- | --- |
| gitcode 链接中的 master 替换为哪个版本号？ | 存在含 `master` 的 gitcode 链接 | 示例格式 `9.3.0-beta.1` |
| hiascend 文档链接中的 latest 替换为哪个版本号？ | 存在含 `latest` 的 hiascend 链接 | 示例格式 `930beta1` |
| 要删除哪些 NPU 型号？ | 存在`<!-- npu="A3" id2 -->` 与 `<!-- end id2 -->`  条件块（此处的产品型号以及id后的数字都为示例） | **多选**，选项来自文档中实际检测到的型号，`IPV350` 排最前（默认）；也可自行输入多个型号（逗号分隔），或选择"跳过 NPU 内容删除" |

执行顺序：先删 NPU 内容块，后替换链接版本号，最后统一汇报（替换处数、对照表、删除文件清单）。

## 4. 处理规则摘要

**链接版本号替换：**

| 链接类型 | 替换内容 |
| --- | --- |
| `https://gitcode.com/...` | 完整路径段 `master` → 指定版本号 |
| `https://www.hiascend.com/document/...` | 完整路径段 `latest` → 指定版本号 |

- 排除清单（不替换 `master`）：`Ascend/triton-ascend/`、`Ascend/torchair/`（提醒用户自行修改）、`Ascend/ModelZoo-PyTorch/`（保持 master 即正确）
- 只替换 URL 中的完整路径段；锚点（`#`）、查询参数（`?`）及正文中出现的 master/latest 不动，无子串误替换

**NPU 条件内容块删除：**

- 整块删除纯目标型号块（含 `<!-- npu="A3" id1 -->` 与 `<!-- end id1 -->`）（此处的产品型号以及id后的数字都为示例）
- 混合块（如 `npu="910,IPV350"`）仅从列表中移除目标型号
- 嵌套块只删内层目标子块，保留外层
- 多余空行自动合并

## 5. 直接运行脚本（可选）

不经过 opencode 交互，也可手动执行 NPU 删除部分（如下脚本仅限NPU删除）：

```bash
# 删除 IPV350 相关内容（默认）
python remove_npu_content.py D:\docs\user_guides

# 删除其他 NPU 相关内容
python remove_npu_content.py /path/to/docs --npu 310p
python remove_npu_content.py /path/to/docs --npu A3
```

执行后可用 grep 验证无残留：

```bash
grep -r "IPV350" <目标目录> --include="*.md"   # 应返回空
```

## 6. 注意事项

- 两类处理均**不改变文件编码、BOM 与换行符**，除处理目标外不做任何其他改动。
- 链接版本号与 NPU 型号全部由用户交互输入，skill 不会自行猜测或推导。
- NPU 删除以目录为单位；指定单个文件时 skill 会询问是否对其所在目录执行。
