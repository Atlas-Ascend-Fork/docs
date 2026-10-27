# Resnet50DbnDwFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:52:54.263Z pushedAt=2026-10-15T12:44:18.444Z -->

## Description

Fuses the BNTrainingReduceGrad+Conv2DBackpropFilterD operators into the FusedDbnDw operator.

![](../figures/Resnet50DbnDwFusionPass_1.png)

After:

![](../figures/Resnet50DbnDwFusionPass_2.png)

## Constraints

Non-common fusion. This fusion is performed only for specific shapes on the ResNet-50 network.

## Applicable Products

<!-- npu="910" id1 -->
Atlas training products
<!-- end id1 -->
