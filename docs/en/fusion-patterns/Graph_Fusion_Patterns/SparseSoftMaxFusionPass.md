# SparseSoftMaxFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:54:45.626Z pushedAt=2026-10-15T12:44:18.473Z -->

## Description

Fuses the SparseSoftmaxCrossEntropyWithLogits operator that fits the graph fusion pattern into the OneHotD and SoftmaxCrossEntropyWithLogits operators.

![](../figures/SparseSoftMaxFusionPass_1.png)

## Constraints

- Dynamic shapes are not supported.
- input0 supports only the float16 and float32 data types.
- input1 supports only the int32 data type.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
