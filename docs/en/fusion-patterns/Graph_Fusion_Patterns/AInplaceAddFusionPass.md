# AInplaceAddFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:38:24.629Z pushedAt=2026-10-15T12:44:18.211Z -->

## Description

Splits the InplaceAdd operator on the network into the TensorMove and ScatterAdd operators.

![](../figures/AInplaceAddFusionPass_1.png)

## Constraints

The InplaceAdd operator exists on the network.

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
