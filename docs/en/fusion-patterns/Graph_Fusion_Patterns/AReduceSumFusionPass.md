# AReduceSumFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:39:20.416Z pushedAt=2026-10-15T12:44:18.228Z -->

## Description

Changes the ReduceSum operator that fits the graph fusion pattern to the Reshape operator in static scenarios.

![](../figures/AReduceSumFusionPass_1.png)

## Constraints

- The fusion pattern does not take effect in dynamic scenarios.
- The axis is not an empty tensor, the axis size does not exceed the range of the input dimension, and the axis specified by the input parameter axis in the input shape is 1.
- This fusion pattern cannot be disabled.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
