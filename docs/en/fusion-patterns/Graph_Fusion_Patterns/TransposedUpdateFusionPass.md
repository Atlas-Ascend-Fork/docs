# TransposedUpdateFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:51:56.829Z pushedAt=2026-11-16T06:27:04.459Z nl=2 -->

## Description

Changes the TransposeD operator in the graph that fits the graph fusion pattern to the Transpose operator when the `check_supported` function in the TransposeD operator returns `True`.

![](../figures/TransposedUpdateFusionPass_1.png)

## Constraints

- Fusion is performed when `check_supported` returns `True`.
- This fusion pattern cannot be disabled.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
