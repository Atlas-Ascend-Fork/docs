# Resnet50DbnDwFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:49:52.831Z pushedAt=2026-11-16T06:27:04.405Z nl=2 -->

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
