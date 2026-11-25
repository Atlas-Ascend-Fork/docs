# CANN产品文档

简体中文 | [English](./README_en.md)

## 简介

本仓库托管[CANN文档中心](https://www.hiascend.com/cann/document)公共文档的源文件，而与各组件密切关联的文档则由各组件仓库单独维护。

## 贡献

欢迎您参与文档贡献！详细请参考[贡献指南](./CONTRIBUTION.md)，请您务必遵守文档写作规范，并按照流程规则提交。如果您对文档有任何意见或建议，请在Issues中提交。

## 目录说明

关键目录结构如下：

```txt
cann_docs/
├── .gitcode/                   # CI工作流配置
│   └── workflows/              # PR流水线与静态检查配置
├── docs/                       # 文档源文件
│   ├── zh/                     # 中文文档
│   │   ├── app-dev             # 应用开发
│   │   ├── common-ref          # 公共参考（术语表、头文件与库等）
│   │   ├── env-vars            # 环境变量参考
│   │   ├── fusion-patterns     # 图融合和UB融合规则参考
│   │   ├── ops-lib             # 算子库公共
│   │   ├── profiling           # 性能调优
│   │   └── troubleshooting     # 故障处理
│   └── en/                     # 英文文档
│       ├── common-ref          # 公共参考（术语表、头文件与库等）
│       ├── env-vars            # 环境变量参考
│       ├── fusion-patterns     # 图融合和UB融合规则参考
│       └── troubleshooting     # 故障处理
├── scripts/                    # CI与站点配置脚本
│   ├── ci/                     # CI配置
│   └── site/                   # 文档中心站点配置
├── skills/                     # 文档处理技能（链接/NPU标签处理、文档审查等）
├── specification/              # 文档写作规范
├── writing_template/           # 文档写作模板
└── README.md
```

## 模板和规范

常用模板和规范如下：

- 写作模板和规范
  - [文档写作规范](./specification/document_writing_specs.md)
  - [API参考写作模板](./writing_template/API_reference.md) 

- 绘图模板和规范
  - [绘图规范](./specification/drawing_specs.md) 
  - [绘图模板（draw.io）](./writing_template/drawing_template_drawio.xml) 
  - [绘图模板（Mermaid）](./writing_template/drawing_template_mermaid.md) 

## cann-docs-raw包

[cann-docs-raw](https://ascend.devcloud.huaweicloud.com/artifactory/cann-run-mirror/cann-docs/) 包汇总了产品文档的Markdown源文件、头文件和样例，并对Markdown源文件进行了标签清洗，便于Agent读取和使用。
