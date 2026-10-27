# ZBNupdateReluV2Conv2DBNreducePass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:57:30.581Z pushedAt=2026-10-15T12:44:18.516Z -->

## Description

Fuses the BNTrainingUpdate+ReluV2+Conv2D+BNTrainingReduce operators into one Conv2D operator to improve computing performance.

![](../figures/ZBNupdateReluV2Conv2DBNreducePass_1.png)

## Constraints

The Conv2D node with bias is not supported.

## Applicable Products

<!-- npu="910" id1 -->
Atlas training products
<!-- end id1 -->
