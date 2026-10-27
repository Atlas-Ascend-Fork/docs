# TransposeSigmoidMulAddPowConcatFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:57:00.564Z pushedAt=2026-10-15T12:44:18.508Z -->

## Description

Fuses the sigmoid structures of yolov3, yolov5, and yolov7 models which have no NMS postprocessing operator into one operator.

**Pattern 1:**

![](../figures/TransposeSigmoidMulAddPowConcatFusionPass_1.png)

After:

![](../figures/TransposeSigmoidMulAddPowConcatFusionPass_4.png)

**Pattern 2:**

![](../figures/TransposeSigmoidMulAddPowConcatFusionPass_3.png)

After:

![](../figures/TransposeSigmoidMulAddPowConcatFusionPass_4.png)

## Constraints

None

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->
