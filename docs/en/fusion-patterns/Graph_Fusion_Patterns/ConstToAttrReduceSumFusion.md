# ConstToAttrReduceSumFusion

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:42:25.494Z pushedAt=2026-10-15T12:44:18.276Z -->

## Description

Changes the ReduceSum operator that fits the graph fusion pattern to the ReduceSumD operator in static scenarios.

![](../figures/ConstToAttrReduceSumFusion_1.png)

## Constraints

- The input data type can only be float16, float32, or bfloat16.
- The fusion pattern does not take effect when the axis is an empty tensor.
- The fusion pattern does not take effect in dynamic scenarios.
- This fusion pattern is enabled by default and cannot be disabled.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
