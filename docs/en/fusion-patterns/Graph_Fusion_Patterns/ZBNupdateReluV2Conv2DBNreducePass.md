# ZBNupdateReluV2Conv2DBNreducePass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:52:33.258Z pushedAt=2026-11-16T06:27:04.477Z nl=2 -->

## Description

Fuses the BNTrainingUpdate+ReluV2+Conv2D+BNTrainingReduce operators into one Conv2D operator to improve computing performance.

![](../figures/ZBNupdateReluV2Conv2DBNreducePass_1.png)

## Constraints

The Conv2D node with bias is not supported.

## Applicable Products

<!-- npu="910" id1 -->
Atlas training products
<!-- end id1 -->
