# ZSplitFusionPassV2

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:58:03.650Z pushedAt=2026-10-15T12:44:18.526Z -->

## Description

Decomposes a Split node with output count exceeding the limit into a hierarchical cascade of Split/SplitV nodes.

Even decomposition

![](../figures/ZSplitFusionPassV2_1.png)

Uneven decomposition

![](../figures/ZSplitFusionPassV2_2.png)

## Constraints

- This fusion pattern takes effect when `num_split` of Split exceeds the maximum output limit.
- This fusion pattern cannot be disabled.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
