# 算子原型注释审查 Skill 安装指南

## 前置要求

- Python 3.8 或更高版本
- Python `requests` 库（`pip install requests`）
- OpenCode 已安装并配置
- GitCode 账号及 Personal Access Token

## 安装步骤

### 1. 放置 Skill 文件

```bash
cp -r skills/regop-comment-review ~/.config/opencode/skills/
```

### 2. 配置 Token

在 `~/.config/opencode/skills/regop-comment-review/config/` 目录下创建 `gitcode-config.json`：

```bash
mkdir -p ~/.config/opencode/skills/regop-comment-review/config
cp ~/.config/opencode/skills/regop-comment-review/config/gitcode-config.example.json \
   ~/.config/opencode/skills/regop-comment-review/config/gitcode-config.json
```

编辑配置文件，填入 Token：

```json
{
  "token": "your-gitcode-token"
}
```

获取 Token 方式：

1. 登录 GitCode
2. 进入个人设置 → 访问令牌
3. 创建新令牌，勾选相关权限

### 3. 验证安装

在 OpenCode 中加载 skill 并验证：

```bash
/skills regop-comment-review
```

## 安全说明

**Token 不暴露给 LLM**：

- Token 存储在本 skill 的 `gitcode-config.json` 中。
- API 调用通过本 skill 自带的 `scripts/api_client.py --config <path>` 执行。
- LLM 只知道配置文件路径，无法获取 Token 内容。

## 目录结构

```text
regop-comment-review/
├── SKILL.md                    # Skill 定义文件（含原型注释审查规则）
├── README.md                   # 介绍文档
├── INSTALL.md                  # 安装指南
├── scripts/
│   ├── api_client.py           # GitCode API 调用封装（Token 不暴露）
│   └── get_config.py           # 配置读取工具
├── config/
│   ├── gitcode-config.json      # Token 配置（需手动创建）
│   └── gitcode-config.example.json
├── references/
│   ├── field-spec.md           # 算子原型注释字段规范全文（评审权威依据）
│   └── writing-example.md      # 头文件注释写作样例（标准写法参考）
└── evals/
    └── evals.json              # 测试用例
```

## 快速开始

1. 在 OpenCode 中加载 skill

2. 获取 PR 的远程引用并创建本地分支

   ```bash
   git fetch origin refs/merge-requests/<pr_number>/head:pr_<pr_number>
   git checkout pr_<pr_number>
   ```

3. 开始审查

   ```bash
   请审查 PR <pr_number>
   ```

## 常见问题

### Q: Token 配置在哪里？

A: 在 `~/.config/opencode/skills/regop-comment-review/config/gitcode-config.json` 中。

### Q: 为什么不切换分支就看不到 PR 的新文件？

A: PR 的文件在独立的分支上，必须通过 `git checkout` 切换到该分支才能看到新增的文件。

### Q: PR 中同时包含 .md 和 .h 变更怎么办？

A: `.h` 原型头文件注释变更由本 skill 审查；`.md` 文档变更由 md-review-skill 审查，两者互补。

### Q: .md 文档的质检和通用 Markdown 质检找谁？

A: `.md` 文档质检用 md-review-skill 或 api-doc-qc-aclnn；本 skill 仅针对算子原型头文件中的注释块。
