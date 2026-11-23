# IndexByTensorStaticFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:47:18.730Z pushedAt=2026-11-16T06:27:04.339Z nl=2 -->

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
