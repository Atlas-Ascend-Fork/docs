# TbeConv2dAddRelu6MulMulFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T07:03:18.619Z pushedAt=2026-10-15T12:44:18.609Z -->

## Description

Two fusion patterns are supported:

Fuses Conv2D/DepthwiseConv2D+Add+Relu6+Mul+Mul into one operator.

![](../figures/TbeConv2dAddRelu6MulMulFusionPass_1.png)

Fuses Conv2D/DepthwiseConv2D+Dequant+Add+Relu6+Mul+Mul+Quant into one operator.

![](../figures/TbeConv2dAddRelu6MulMulFusionPass_2.png)

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
