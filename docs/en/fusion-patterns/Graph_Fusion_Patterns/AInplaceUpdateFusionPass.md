# AInplaceUpdateFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:42:06.242Z pushedAt=2026-11-16T06:27:04.203Z nl=2 -->

## Description

Splits the InplaceUpdate operator on the network into the TensorMove and ScatterUpdate operators.

![](../figures/AInplaceUpdateFusionPass_1.png)

## Constraints

The InplaceUpdate operator exists on the network.

## Applicable Products

<!-- npu="310b" id1 -->
Atlas 200I/500 A2 inference products
<!-- end id1 -->

<!-- npu="310p" id2 -->
Atlas inference products
<!-- end id2 -->

<!-- npu="910" id3 -->
Atlas training products
<!-- end id3 -->

<!-- npu="910b" id4 -->
Atlas A2 products
<!-- end id4 -->

<!-- npu="A3" id5 -->
Atlas A3 products
<!-- end id5 -->

<!-- npu="950" id6 -->
Ascend 950PR&950DT products
<!-- end id6 -->
