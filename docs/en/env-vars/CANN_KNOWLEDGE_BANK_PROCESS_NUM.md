# CANN_KNOWLEDGE_BANK_PROCESS_NUM

<!-- md-trans-meta sourceCommit=96217e9acd4da744a739b8f94b020fbe0cc7fcca translatedAt=2026-10-16T07:27:05.181Z pushedAt=2026-10-20T07:59:38.325Z nl=2 -->

## Function Description

The **CANN_KNOWLEDGE_BANK_PROCESS_NUM** environment variable is used to set the number of processes used by the knowledge base management module to query the knowledge base.

The value range is \[0, 8\]. The default value is **8** (that is, during the operator compilation phase, 8 processes are started by default to query the knowledge base).

The more processes are started, the more host memory is consumed and the faster the compilation.

The fewer processes are started, the less host memory is consumed and the slower the compilation.

When **CANN_KNOWLEDGE_BANK_PROCESS_NUM** is set to **0**, the knowledge base management module is not started and the knowledge base is not queried.

## Configuration Example

```bash
export CANN_KNOWLEDGE_BANK_PROCESS_NUM=5
```

## Constraints

None

## Supported Models

Supported on all chips
