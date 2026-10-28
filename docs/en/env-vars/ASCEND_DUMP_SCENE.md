# ASCEND_DUMP_SCENE

<!-- md-trans-meta sourceCommit=80afc5e236fbcff31e1f90e91c7213c8a3080eb0 translatedAt=2026-10-23T09:24:08.003Z pushedAt=2026-10-26T01:04:48.429Z nl=2 -->

## Function Description

Enables exception dump when reproducing issue scenarios, and exports the input and output data, workspace information, and tiling information of the abnormal operator.

The value can be:

- **aic_err_brief_dump**: Indicates lightweight exception dump, which is used to export the input & output and workspace data of the AI Core error operator.
- **aic_err_norm_dump**: Indicates normal exception dump, which additionally exports shape, data type, format, and attribute information on the basis of lightweight exception dump.
- **aic_err_detail_dump**: Additionally exports the internal storage, registers, and call stack information of the AI Core on the basis of lightweight exception dump.

    Note the following when configuring this option:

  - This option is supported only on the following models:

    <!-- npu="910b" id1 -->
    Atlas A2 products
    <!-- end id1 -->

    <!-- npu="A3" id2 -->
    Atlas A3 products
    <!-- end id2 -->

  - During dump file export, the AI Core where the abnormal operator resides is paused, which may affect the normal execution of other service processes on the device. After the dump file is exported, the AI Core is automatically resumed.
  - After the dump file is exported, the user service process on the host side is forcibly terminated. Errors during the forced termination can be excluded from the input for AI Core issue analysis.
  - After the **aic_err_detail_dump** option is configured, if a dump file is generated but it is not a **\*.core** file, the function corresponding to **aic_err_detail_dump** has not been started successfully, and the system automatically switches to dumping based on the **aic_err_brief_dump** option.

## Configuration Example

```bash
export ASCEND_DUMP_SCENE=aic_err_brief_dump
```

## Constraints

- There are multiple ways to enable the abnormal operator dump function. The priorities in descending order are as follows: **ASCEND_DUMP_SCENE** environment variable \> **NPU_COLLECT_PATH** environment variable \> configuration file (**aclInit** API and **aclmdlSetDump** API).
- For the storage path of dump information exported through this environment variable, the priorities in descending order are as follows: **ASCEND_DUMP_PATH** environment variable \> **ASCEND_WORK_PATH** environment variable \> default path (current execution directory of the application).

## Supported Models

Supported on all chips
