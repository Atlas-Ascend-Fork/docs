# ZInplaceAddLayerNormFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:52:51.463Z pushedAt=2026-11-16T06:27:04.487Z nl=2 -->

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
