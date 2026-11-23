# TbeConv2dAddRelu6MulMulFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:55:25.202Z pushedAt=2026-11-16T06:27:04.564Z nl=2 -->

## Description

Two fusion patterns are supported:

Fuses Conv2D/DepthwiseConv2D+Add+Relu6+Mul+Mul into one operator.

![](../figures/TbeConv2dAddRelu6MulMulFusionPass_1.png)

Fuses Conv2D/DepthwiseConv2D+Dequant+Add+Relu6+Mul+Mul+Quant into one operator.

![](../figures/TbeConv2dAddRelu6MulMulFusionPass_2.png)

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
