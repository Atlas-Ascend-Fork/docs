# TensorScatterUpdateFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:55:35.371Z pushedAt=2026-10-15T12:44:18.489Z -->

## Description

Splits the TensorScatterUpdate operator that fits the graph fusion pattern into the TensorMove and ScatterNdUpdate operators when the input and output data types are not bool or int32.

![](../figures/TensorScatterUpdateFusionPass_1.png)

## Constraints

- This fusion pattern does not take effect when the data type of input x is bool or int32.
- This fusion pattern cannot be disabled.

<!-- npu="950" id3 -->
In use cases involving Ascend 950PR&950DT products, the following constraints also apply.

- The ScatterNdUpdate operator AI Core implementation supports the following data types: int64, int8, float32, float16, bfloat16, and bool. Therefore, the fused operator of any of these six data types will be executed on the AI Core, and on the AI CPU if it is of other data types.
- This fusion pattern does not take effect when the data type is String or complex128, since these types are not supported by TensorMove or ScatterNdUpdate.

<!-- end id3 -->
## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->

<!-- npu="950" id2 -->
Ascend 950PR&950DT products
<!-- end id2 -->