# PadDepthwiseConv2dFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:50:56.836Z pushedAt=2026-10-15T12:44:18.411Z -->

## Description

Fuses the PADD+DepthwiseConv2D operators into the DepthwiseConv2D operator.

![](../figures/PadDepthwiseConv2dFusionPass_1.png)

After:

![](../figures/PadDepthwiseConv2dFusionPass_2.png)

## Constraints

- Dynamic shapes are not supported.
- The PadD operator cannot be connected to multiple DepthwiseConv2D structures.
- Before fusion, DepthwiseConv2D must have valid padding attributes.
- The PadD operator supports padding only in the H or W dimension of DepthwiseConv2D. After fusion, the padding size must be within the range of [0, 255], and the values of `pad_top` and `pad_bottom` must be less than `kernel_h`.

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->

<!-- npu="310b" id2 -->
Atlas 200I/500 A2 inference products
<!-- end id2 -->

<!-- npu="910" id3 -->
Atlas training products
<!-- end id3 -->

<!-- npu="910b" id4 -->
Atlas A2 products
<!-- end id4 -->

<!-- npu="A3" id5 -->
Atlas A3 products
<!-- end id5 -->

<!-- npu="950" id7 -->
Ascend 950PR&950DT products
<!-- end id7 -->
