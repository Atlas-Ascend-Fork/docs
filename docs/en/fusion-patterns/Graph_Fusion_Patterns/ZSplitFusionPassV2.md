# ZSplitFusionPassV2

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:52:53.603Z pushedAt=2026-11-16T06:27:04.490Z nl=2 -->

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
