# ZSplitVFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:58:41.960Z pushedAt=2026-10-15T12:44:18.532Z -->

## Description

Decomposes a SplitV node with output count exceeding the limit into a hierarchical cascade of SplitV nodes.

Fusion pattern when the `size_splits` input is a constant:

![](../figures/ZSplitVFusionPass_1.png)

Fusion pattern when the `size_splits` input is not a constant:

![](../figures/ZSplitVFusionPass_2.png)

## Constraints

- This fusion pattern takes effect when `num_split` exceeds the maximum output limit. The SplitV node is split into a multi-layer cascaded SplitV node structure.
- If `num_split` does not exceed the maximum output limit, this fusion pattern does not take effect, and the original SplitV node structure is retained.
- This fusion pattern cannot be disabled.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
