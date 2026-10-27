# RotaryMulGrad2RotaryPositionEmbeddingGradFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:53:23.960Z pushedAt=2026-10-15T12:44:18.449Z -->

## Description

Fuses the RotaryMulGrad operator into the RotaryPositionEmbeddingGrad operator, as shown in the following fusion.

- needBackward == true

  ![](../figures/RotaryMulGrad2RotaryPositionEmbeddingGradFusionPass_1.png)

- needBackward == false

  ![](../figures/RotaryMulGrad2RotaryPositionEmbeddingGradFusionPass_2.png)

## Constraints

You are advised not to disable this pattern. Otherwise, the RotaryMulGrad Ascend IR function will be unavailable.

## Applicable Products

<!-- npu="950" id1 -->
Ascend 950PR&950DT products
<!-- end id1 -->