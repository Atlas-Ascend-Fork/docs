# NPU_COLLECT_PATH

<!-- md-trans-meta sourceCommit=0eadb61a993b384a333d3a93ddf2a83b6daba48f translatedAt=2026-10-16T07:29:05.725Z pushedAt=2026-10-20T07:59:38.329Z nl=2 -->

## Function Description

In a problem reproduction scenario, this environment variable specifies the path for saving fault information (including dump graphs, AI Core operator exception data, and operator build information). It can be configured as an absolute path or a relative path (relative to the path of the program or command being executed). The execution user must have read, write, and execute permissions on this path. If the path does not exist, the system automatically creates the directories in the path.

**Note** that the following points must be considered when using this environment variable:

- Setting this environment variable automatically enables exception operator dump data collection by default. If the operator input or output contains sensitive user information, there is a risk of information leakage.
- After setting this environment variable, converting a model adds debugging information when building the OM model, which increases the size of the OM model file. If memory planning is a concern or memory resources are limited, delete this environment variable promptly after debugging is complete.
- Setting this environment variable collects only L1 exception dump information. It does not collect model dump information, single-operator dump information, overflow operator dump information, or L0 exception dump information.

    The directories for storing L1 exception dump information, in descending order of priority, are: **NPU_COLLECT_PATH** -\> **ASCEND_WORK_PATH** -\> default path (extra-info directory in the current path of the program being executed)

    L1 exception dump is a normal exception dump, while L0 exception dump is a lite exception dump (that is, a lightweight exception dump). Both export information such as operator input and output and workspace data. However, compared with L0 exception dump, L1 exception dump contains more information. When L1 exception dump is enabled, information such as the dtype of each tensor is printed in the host application log file (that is, the plog), and the operator name and kernel related to the operator are also printed.

- Setting this environment variable causes operators to be built online during model compilation, instead of using the prebuilt operator binary files.

    The directories for storing online-built operator information (.o and .json files), in descending order of priority, are: **NPU_COLLECT_PATH** -\> **ASCEND_CACHE_PATH** -\> default path (the **$\{HOME\}/atc_data** directory)

## Configuration Example

```bash
export NPU_COLLECT_PATH=$HOME/demo/
```

## Constraints

- When a single-operator API (for example, an aclnn API) is called, the compiled operator binary file is used, and online operator build is not involved.
- If the **NPU_COLLECT_PATH** environment variable is configured, in graph mode, operator build files, including .o and .json files, cannot be generated in the path specified by this environment variable for the following operators:

    MatMulAllReduce

    MatMulAllReduceAddRmsNorm

    AllGatherMatMul

    MatMulReduceScatter

    AlltoAllAllGatherBatchMatMul

    BatchMatMulReduceScatterAlltoAll

- If the **NPU_COLLECT_PATH** environment variable is configured, enabling the switch for detecting whether Global Memory is out of bounds is not supported. Otherwise, the compiled model file or operator kernel package will report an error when used. The switch for detecting whether Global Memory is out of bounds can be enabled in the following ways:
  - When using the ATC model conversion tool, configure **oom** in the configuration file specified by the **--op_debug_config** parameter. For detailed configuration, see [*ATC Offline Model Build Tool*](https://hiascend.com/document/redirect/cannCommunityATC).
  <!-- npu="950,A3,910b,910,310p,310b" id1 -->
  - When using the **op_compiler** operator build tool, configure **oom** in the configuration file specified by the **--op_debug_config** parameter. For detailed configuration, see [*Operator Build Tool*](https://hiascend.com/document/redirect/CannCommunityopcompiler).
  <!-- end id1 -->
  - When building graphs in Ascend Graph mode, configure **oom** in the configuration file specified by the **op_debug_config** or **OP_DEBUG_CONFIG** parameter. For detailed configuration, see [*Graph Development*](https://hiascend.com/document/redirect/CannCommunityGraphguide).
  <!-- npu="950,A3,910b,910,310p" id2 -->
  - When migrating a training script developed based on the TensorFlow Python API to an AI processor for training, configure **oom** in the configuration file specified by the **op_debug_config** parameter. For detailed configuration, see [*TensorFlow Product Documentation*](https://www.hiascend.com/document/detail/en/TensorFlowCommunity/latest/index/index.html).
  <!-- end id2 -->
