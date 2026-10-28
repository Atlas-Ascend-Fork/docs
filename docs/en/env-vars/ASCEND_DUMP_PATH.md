# ASCEND_DUMP_PATH

<!-- md-trans-meta sourceCommit=96217e9acd4da744a739b8f94b020fbe0cc7fcca translatedAt=2026-10-23T09:24:06.143Z pushedAt=2026-10-23T09:31:05.746Z nl=2 -->

## Function Description

Sets the storage path of exception operator dump information. The path can be configured as an absolute path or a path relative to the execution program. The specified path supports uppercase and lowercase letters (a-z, A-Z), digits (0-9), underscores (_), hyphens (-), periods (.), and Chinese characters. The execution user must have read, write, and execute permissions. If the path does not exist, the system automatically creates the directories in the path. If no path is specified, the exception operator dump information is stored in the current execution directory of the application by default.

Note the following when using this environment variable:

- When exception operator dump is enabled through the **ASCEND_DUMP_SCENE** environment variable, the priorities in descending order are: **ASCEND_DUMP_PATH** environment variable \> **ASCEND_WORK_PATH** environment variable \> default path (current execution directory of the application).
- When exception operator dump is enabled through a configuration file (**aclInit** API, **aclmdlSetDump** API), the priorities in descending order are: **ASCEND_DUMP_PATH** environment variable \> **ASCEND_WORK_PATH** environment variable \> configuration file path (**dump_path** field) \> default path (current execution directory of the application).
- Setting this environment variable automatically enables the operator kernel data dump function by default. The priorities of the dump information storage paths in descending order are: **ASCEND_DUMP_PATH** environment variable \> **ASCEND_WORK_PATH** environment variable \> configuration file path (**dump_path** field).

## Configuration Example

```bash
export ASCEND_DUMP_PATH=/repo/task001
```

## Constraints

- When enabling exception operator dump, this environment variable must be used together with **ASCEND_DUMP_SCENE**.
- When enabling operator kernel data dump, you only need to configure this environment variable.

## Supported Models

Supported on all chips
