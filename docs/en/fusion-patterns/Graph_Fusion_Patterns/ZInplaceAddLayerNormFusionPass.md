# ZInplaceAddLayerNormFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:58:03.184Z pushedAt=2026-10-15T12:44:18.523Z -->

## Description

Reuses the input address *x1* of AddLayerNorm as the output address *y*, input address *x2* as the output address *x*, and converts the operator to InplaceAddLayerNorm.

![](../figures/ZInplaceAddLayerNormFusionPass_01.png)

## Constraints

- The input types of the AddLayerNorm operator cannot be different before fusion.
- AddLayerNorm does not support being called as a custom operator integrated into a graph.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->

<!-- npu="A3" id2 -->
Atlas A3 products
<!-- end id2 -->
