# IndexByTensorStaticFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:48:22.563Z pushedAt=2026-10-15T12:44:18.364Z -->

## Description

Converts the IndexByTensor operator into the Index operator during static shape in PyTorch graph mode, to ensure that the graph sink is not damaged.

![](../figures/IndexByTensorStaticFusionPass_1.png)

## Constraints

Only static shapes are supported.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->

<!-- npu="A3" id2 -->
Atlas A3 products
<!-- end id2 -->

<!-- npu="950" id3 -->
Ascend 950PR&950DT products
<!-- end id3 -->
