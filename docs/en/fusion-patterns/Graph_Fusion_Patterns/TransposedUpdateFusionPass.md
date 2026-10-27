# TransposedUpdateFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:56:21.562Z pushedAt=2026-10-15T12:44:18.499Z -->

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
