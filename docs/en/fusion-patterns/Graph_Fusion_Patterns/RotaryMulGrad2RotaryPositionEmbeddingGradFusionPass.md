# RotaryMulGrad2RotaryPositionEmbeddingGradFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:50:11.433Z pushedAt=2026-11-16T06:27:04.412Z nl=2 -->

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