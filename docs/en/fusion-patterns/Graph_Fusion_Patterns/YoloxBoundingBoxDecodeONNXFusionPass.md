# YoloxBoundingBoxDecodeONNXFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:52:34.425Z pushedAt=2026-11-16T06:27:04.480Z nl=2 -->

## Description

Fuses the StridedSliceD, Mul, Exp, GatherV2, Add, Muls, Sub, Unsqueeze, and ConcatD operators into YoloxBoundingBoxDecode, to improve the computing performance.

![](../figures/YoloxBoundingBoxDecodeONNXFusionPass_1.png)

After:

![](../figures/YoloxBoundingBoxDecodeONNXFusionPass_2.png)

## Constraints

None.

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->
