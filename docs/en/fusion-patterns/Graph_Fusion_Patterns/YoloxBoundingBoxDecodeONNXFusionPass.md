# YoloxBoundingBoxDecodeONNXFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:57:26.707Z pushedAt=2026-10-15T12:44:18.514Z -->

## Description

Fuses the StridedSliceD, Mul, Exp, GatherV2, Add, Muls, Sub, Unsqueeze, and ConcatD operators into YoloxBoundingBoxDecode, to improve the computing performance.

![](../figures/YoloxBoundingBoxDecodeONNXFusionPass_1.png)

After:

![](../figures/YoloxBoundingBoxDecodeONNXFusionPass_2.png)

## Constraints

None

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->
