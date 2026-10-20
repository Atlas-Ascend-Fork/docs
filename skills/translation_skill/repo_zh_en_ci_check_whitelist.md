# 开源仓中英文校验放通目录

本文档用于配置开源仓内的白名单规则：指定哪些中英文Markdown文件的修改不会被CI流程拦截。下表中的放通目录即为CI豁免目录，主要包含产品文档、Skill等相关文件。

| 开源仓 | 是否配置中英文CI拦截 | 放通目录<br>（如下目录不进行中英文CI校验，只修改英文md不再进行拦截） |
| --- | --- | --- |
| [https://gitcode.com/cann/asc-devkit](https://gitcode.com/cann/asc-devkit) | 是，已完成拦截 | **产品文档：**<br>docs/en/api<br>docs/en/guide<br>docs/zh/api<br>docs/zh/guide<br>docs/zh/vitepress<br>**skill等相关目录：**<br>.agent<br>.claude<br>.codex<br>.opencode |
| [https://gitcode.com/cann/runtime](https://gitcode.com/cann/runtime) | 是，已完成拦截 | **产品文档：**<br>docs<br>python/docs<br>**skill等相关目录：**<br>.claude |
| [https://gitcode.com/cann/ge](https://gitcode.com/cann/ge) | 是，已完成拦截 | **产品文档：**<br>docs/zh/api<br>docs/zh/user_guides/graph_dev<br>docs/zh/user_guides/env_vars<br>docs/zh/user_guides/atc_tools<br>docs/zh/user_guides/llm_datadist<br>docs/zh/user_guides/dflow<br>docs/en/api<br>docs/en/user_guides/graph_dev<br>docs/en/user_guides/env_vars<br>docs/en/user_guides/atc_tools<br>docs/en/user_guides/llm_datadist<br>docs/en/user_guides/dflow<br>**skill等相关目录：**<br>.claude<br>.opencode |
| [https://gitcode.com/cann/metadef](https://gitcode.com/cann/metadef) | 是，已完成拦截 | **产品文档：**<br>docs/zh/api<br>docs/en/api<br>**skill等相关目录：**<br>.claude |
| [https://gitcode.com/cann/hixl](https://gitcode.com/cann/hixl) | 是，已完成拦截 | **产品文档：**<br>docs/zh/api<br>docs/zh/guide<br>docs/en/api<br>docs/en/guide<br>**skill等相关目录：**<br>.agents<br>.claude<br>.codex<br>.opencode<br>AGENTS.md<br>CLAUDE.md |
| [https://gitcode.com/cann/hccl](https://gitcode.com/cann/hccl) | 是，已完成拦截 | **产品文档：**<br>docs/zh/api_ref<br>docs/zh/user_guide<br>docs/en/api_ref<br>docs/en/user_guide<br>**skill等相关目录：**<br>.agents |
| [https://gitcode.com/cann/hcomm](https://gitcode.com/cann/hcomm) | 是，已完成拦截 | **产品文档：**<br>docs/zh/api_ref<br>docs/zh/comm_op_dev_guide<br>docs/en/api_ref<br>docs/en/comm_op_dev_guide<br>**skill等相关目录：**<br>.agents |
| [https://gitcode.com/cann/graph-autofusion](https://gitcode.com/cann/graph-autofusion) | 是，已完成拦截 | **skill等相关目录：**<br>.claude<br>.opencode<br>AGENTS.md |
| [https://gitcode.com/cann/pypto](https://gitcode.com/cann/pypto) | 是，已完成拦截 | **产品文档：**<br>docs/zh/api<br>docs/zh/guide<br>docs/en/api<br>docs/en/guide<br>**skill等相关目录：**<br>.opencode<br>.agents<br>AGENTS.md |
| [https://gitcode.com/cann/driver](https://gitcode.com/cann/driver) | 是，已完成拦截 | **产品文档：**<br>docs/zh/Ascend_910B_DCMI_API<br>docs/zh/Ascend_910_93_DCMI_API<br>docs/zh/Ascend_950_DCMI_API<br>docs/zh/Ascend_950_HCCN_Tool<br>docs/zh/Ascend_950_npu-smi<br>docs/zh/Ascend_950_upgrade-tool<br>docs/zh/msnpureport<br>docs/zh/nda<br>docs/en/Ascend_910B_DCMI_API<br>docs/en/Ascend_910_93_DCMI_API<br>docs/en/Ascend_950_DCMI_API<br>docs/en/Ascend_950_HCCN_Tool<br>docs/en/Ascend_950_npu-smi<br>docs/en/Ascend_950_upgrade-tool<br>docs/en/nda<br>docs/en/msnpureport |
| [https://gitcode.com/cann/asc-tools](https://gitcode.com/cann/asc-tools) | 新增拦截 | **产品文档：**<br>docs/zh/operator_compilation_tool<br>docs/en/operator_compilation_tool<br>**skill等相关目录：**<br>skills |
| [https://gitcode.com/cann/oam-tools](https://gitcode.com/cann/oam-tools) | 是，已完成拦截 | **产品文档：**<br>docs <br>**skill等相关目录：**<br>skills<br>.agent<br>.claude<br>.opencode |
| [https://gitcode.com/cann/amct](https://gitcode.com/cann/amct) | 是，已完成拦截 | **产品文档：**<br>docs<br>**skill等相关目录：**<br>.claude<br>.opencode<br>AGENTS.md<br>.agent |
| [https://gitcode.com/cann/tensorflow](https://gitcode.com/cann/tensorflow) | 是，已完成拦截 | **无放通目录，全部拦截** |
| [https://gitcode.com/cann/pto-isa](https://gitcode.com/cann/pto-isa) | / | / |
| [https://gitcode.com/cann/opbase](https://gitcode.com/cann/opbase) | / | / |
| [https://gitcode.com/cann/ops-cv](https://gitcode.com/cann/ops-cv) | / | / |
| [https://gitcode.com/cann/ops-math](https://gitcode.com/cann/ops-math) | / | / |
| [https://gitcode.com/cann/ops-nn](https://gitcode.com/cann/ops-nn) | / | / |
| [https://gitcode.com/cann/ops-transformer](https://gitcode.com/cann/ops-transformer) | / | / |
| [https://gitcode.com/cann/docs](https://gitcode.com/cann/docs) | 是，已完成拦截 | **产品文档：**<br>docs/zh/app-dev<br>docs/zh/troubleshooting<br>docs/en/app-dev<br>docs/en/troubleshooting |
| [https://gitcode.com/cann/pypto-vscode](https://gitcode.com/cann/pypto-vscode) | 是，已完成拦截 | **产品文档：**<br>docs/zh |
| [https://gitcode.com/cann/asc-comm](https://gitcode.com/cann/asc-comm) | 是，已完成拦截 | **产品文档：**<br>docs/zh/api <br>docs/zh/guide <br>docs/zh/programming_model <br>docs/zh/index.md <br>docs/en/api <br>docs/en/guide <br>docs/en/programming_model <br>docs/en/index.md |
