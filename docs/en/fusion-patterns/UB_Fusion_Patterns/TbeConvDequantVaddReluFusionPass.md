# TbeConvDequantVaddReluFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T07:04:26.989Z pushedAt=2026-10-15T12:44:18.627Z -->

## Description

Fuses the operators into one Conv2D fusion operator in the following three modes:

![](../figures/TbeConvDequantVaddReluFusionPass_1.png)

Or

![](../figures/TbeConvDequantVaddReluFusionPass_2.png)

Or

![](../figures/TbeConvDequantVaddReluFusionPass_3.png)

## Constraints

The ReLU node does not support PReLU.

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->

<!-- npu="910" id2 -->
Atlas training products
<!-- end id2 -->
