# AddRmsNormFusionGraphPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:37:38.078Z pushedAt=2026-10-15T12:44:18.203Z -->

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
Ascend 950PR/950DT products
<!-- end id3 -->
