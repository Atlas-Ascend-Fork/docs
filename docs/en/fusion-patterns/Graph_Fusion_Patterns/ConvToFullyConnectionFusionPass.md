# ConvToFullyConnectionFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:44:44.070Z pushedAt=2026-10-15T12:44:18.310Z -->

## Description

Fuses the Conv operator into the FullyConnection operator to improve computation performance:

Before: ![](../figures/ConvToFullyConnectionFusionPass_1.png) After: ![](../figures/ConvToFullyConnectionFusionPass_2.png)

## Constraints

- Dynamic shapes are not supported.
- int4 and int8 data types are not supported.
<!-- npu="910b" id1 -->
- For Atlas A2 products, the float32 data type does not support the case where the N axis of the filter is not aligned to 16.
<!-- end id1 -->
- The number of conv2d output nodes can only be 1, the `input` and `filter` sizes must be equal on the HWC axes, the `group` attribute must be 1, and the `pad` attribute must be \[0,0,0,0\].
- conv2d followed by a quant or requant operator is not supported.
- conv2d followed by a dequant+sigmoid operator cascade is not supported.

## Applicable Products

<!-- npu="310b" id2 -->
Atlas 200I/500 A2 inference products
<!-- end id2 -->

<!-- npu="310p" id3 -->
Atlas inference products
<!-- end id3 -->

<!-- npu="910" id4 -->
Atlas training products
<!-- end id4 -->

<!-- npu="910b" id5 -->
Atlas A2 products
<!-- end id5 -->

<!-- npu="A3" id6 -->
Atlas A3 products
<!-- end id6 -->
