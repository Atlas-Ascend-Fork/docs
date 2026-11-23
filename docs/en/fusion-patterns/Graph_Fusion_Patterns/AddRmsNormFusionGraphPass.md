# AddRmsNormFusionGraphPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:41:27.238Z pushedAt=2026-11-16T06:27:04.188Z nl=2 -->

## Description

Fuses the Add and RmsNorm operators that comply with the graph fusion pattern into the fused operator AddRmsNorm. The output of the Add operator is used as the first input of the RmsNorm operator.

![](../figures/AddRmsNormFusionGraphPass_1.png)

## Constraints

- The shape and dtype of the inputs X1 and X2 of the Add operator must be the same.
- The format can only be ND.

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
