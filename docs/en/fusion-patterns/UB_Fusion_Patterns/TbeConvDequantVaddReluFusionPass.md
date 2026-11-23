# TbeConvDequantVaddReluFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:56:10.958Z pushedAt=2026-11-16T06:27:04.588Z nl=2 -->

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
