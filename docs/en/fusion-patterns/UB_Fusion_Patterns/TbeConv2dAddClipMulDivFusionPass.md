# TbeConv2dAddClipMulDivFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T07:02:52.450Z pushedAt=2026-10-15T12:44:18.603Z -->

## Description

Fuses the Conv2D+Add+Clip+Mul+Div (optional) operators into one operator.

![](../figures/TbeConv2dAddClipMulDivFusionPass.png)

## Constraints

None

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
