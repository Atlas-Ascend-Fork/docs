# SubFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:55:14.821Z pushedAt=2026-10-15T12:44:18.480Z -->

## Description

Fuses the Sub operator that fits the graph fusion pattern into a Const node when the following constraints are met. The Const node's value is set to all zeros, and its shape is consistent with the output shape of the Sub operator.

![](../figures/SubFusionPass_1.png)

## Constraints

- The fusion pattern does not take effect when the two inputs of Sub are not from the same output of the same node.
- The fusion pattern does not take effect when the input of Sub has a dynamic shape.
- The fusion pattern does not take effect when the data type of Sub is not float16, float32, uint8, int8, uint16, int16, int32, int64, double, complex64, or complex128.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
