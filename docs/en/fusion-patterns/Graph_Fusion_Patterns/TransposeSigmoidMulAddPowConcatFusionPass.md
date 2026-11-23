# TransposeSigmoidMulAddPowConcatFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:52:15.088Z pushedAt=2026-11-16T06:27:04.467Z nl=2 -->

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

None.

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->
