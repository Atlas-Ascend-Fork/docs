# CANN Product Documentation

English | [简体中文](./README.md)

## Introduction

This repository hosts the source files of the public documents on the [CANN document center](https://www.hiascend.com/cann/document). Documents that are closely related to specific components are maintained separately in the repositories of those components.

## Contributing

You are welcome to contribute to the documentation! For details, see the [Contribution Guidelines](./CONTRIBUTION_en.md). Make sure that you follow the document writing specifications and submit changes according to the process rules. If you have any comments or suggestions on the documentation, submit an issue.

## Directory Structure

The key directory structure is as follows:

```txt
cann_docs/
├── .gitcode/                   # CI workflow configurations
│   └── workflows/              # PR pipeline and static check configurations
├── docs/                       # Documents
│   ├── zh/                     # Chinese documents
│   │   ├── app-dev             # Application development
│   │   ├── common-ref          # Common references (glossary, headers and libraries, etc.)
│   │   ├── env-vars            # Environment variable reference
│   │   ├── fusion-patterns     # Graph fusion and UB fusion rule reference
│   │   ├── ops-lib             # Operator library public documents
│   │   ├── profiling           # Performance profiling
│   │   └── troubleshooting     # Troubleshooting
│   └── en/                     # English documents
│       ├── common-ref          # Common references (glossary, headers and libraries, etc.)
│       ├── env-vars            # Environment variable reference
│       ├── fusion-patterns     # Graph fusion and UB fusion rule reference
│       └── troubleshooting     # Troubleshooting
├── scripts/                    # CI and site configuration scripts
│   ├── ci/                     # CI configurations
│   └── site/                   # Document center site configurations
├── specification/              # Document writing specifications
├── writing_template/           # Document writing templates
└── README.md
```

## Documentation Processing Skills

The documentation processing skills are as follows:

- [Document general quality check skill](https://gitcode.com/cann/cannbot-skills/tree/master/infra/docs-common-review)
- [Diagram drawing and editing skill](https://gitcode.com/cann/cannbot-skills/tree/master/infra/docs-diagram-draw)
- [Document translation skill](https://gitcode.com/cann/cannbot-skills/tree/master/infra/docs-translation)
- [Auto-modification skill for fixed items on repository branches](https://gitcode.com/cann/cannbot-skills/tree/master/infra/docs-branch-update)

## cann-docs-raw Package

The [cann-docs-raw](https://ascend.devcloud.huaweicloud.com/artifactory/cann-run-mirror/cann-docs/) package collects the Markdown source files, header files, and samples of the product documentation. The Markdown source files are tag-cleaned to facilitate Agent reading and usage.
