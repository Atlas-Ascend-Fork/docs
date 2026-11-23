# TbeConv2dAddClipMulDivFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:55:06.286Z pushedAt=2026-11-16T06:27:04.554Z nl=2 -->

## Description

Fuses the Conv2D+Add+Clip+Mul+Div (optional) operators into one operator.

![](../figures/TbeConv2dAddClipMulDivFusionPass.png)

## Constraints

None.

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
