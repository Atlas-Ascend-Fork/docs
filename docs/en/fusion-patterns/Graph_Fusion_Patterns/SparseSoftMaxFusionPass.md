# SparseSoftMaxFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:50:55.200Z pushedAt=2026-11-16T06:27:04.435Z nl=2 -->

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
