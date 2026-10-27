# TbeEltwiseFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T07:06:23.840Z pushedAt=2026-10-15T12:44:18.668Z -->

## Description

Performs UB fusion on the ElemWise/Broadcast nodes in the subgraphs that meet the following pattern. A maximum of six consecutive ElemWise/Broadcast nodes are supported.

![](../figures/TbeEltwiseFusionPass_1.png)

## Constraints

Dynamic shapes are not supported.

## Applicable Products

<!-- npu="310b" id1 -->
Atlas 200I/500 A2 inference products
<!-- end id1 -->

<!-- npu="310p" id2 -->
Atlas inference products
<!-- end id2 -->

<!-- npu="910" id3 -->
Atlas training products
<!-- end id3 -->

<!-- npu="A3" id4 -->
Atlas A3 products
<!-- end id4 -->
