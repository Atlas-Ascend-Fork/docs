# ACLNN_CACHE_LIMIT

<!-- md-trans-meta sourceCommit=fe5307907d2087c03797a673819df2784c73d1b4 translatedAt=2026-10-16T07:25:29.277Z pushedAt=2026-10-20T07:59:38.323Z nl=2 -->

## Function Description

This environment variable is used to configure the number of operator information entries cached by the aclnn API on the host side. The cached operator information includes the workspace size, the executor for operator computation, and tiling information.

Value range: \[0,10000000\]. The default value is **10000**. When the value is **0**, the operator information caching function is disabled.

**Generally, it is not recommended to set the ACLNN_CACHE_LIMIT environment variable. Keep the default value.** For dynamic shape scenarios, if the shape range of an operator is large, developers can appropriately increase the value of this environment variable based on service requirements to increase the number of operator cache entries, thereby improving scheduling performance. However, note that increasing the number of operator information cache entries increases the host memory overhead. For details, see [Constraints](#constraints).

## Configuration Example

```bash
export ACLNN_CACHE_LIMIT=10000
```

## Constraints

- The cache of a single operator is managed by thread. Different threads use different caches and do not affect each other. **ACLNN_CACHE_LIMIT** configures the number of operator cache entries per thread. Therefore, the more threads there are, the more operator cache entries there are.

    Each operator cache entry occupies approximately 2 KB of host memory. The total memory occupied by the cache of a single operator is: **ACLNN_CACHE_LIMIT** × Number of threads × 2 KB.

    For example, if there are 10 threads and **ACLNN_CACHE_LIMIT** is set to **100000**, the total memory occupied by the cache of a single operator is: 10 × 100000 × 2 KB = 2 GB.

- The cache of a fusion operator (large kernel operator) is managed in a process-level dedicated memory pool. Each cache entry occupies approximately 20 KB of host memory. The total memory occupied by the fusion operator cache is: **ACLNN_CACHE_LIMIT** × 20 KB.
- Users should set **ACLNN_CACHE_LIMIT** properly based on the total host memory size, the number of threads, and the size of each operator cache entry. Setting it to a too large value may cause excessive host memory usage and degrade scheduling performance.

## Supported Models

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->

<!-- npu="910" id2 -->
Atlas training products
<!-- end id2 -->

<!-- npu="910b" id3 -->
Atlas A2 products
<!-- end id3 -->

<!-- npu="A3" id4 -->
Atlas A3 products
<!-- end id4 -->

<!-- npu="950" id5 -->
Ascend 950PR&950DT products
<!-- end id5 -->
