# RotaryMul2RotaryPositionEmbeddingFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:49:55.688Z pushedAt=2026-11-16T06:27:04.407Z nl=2 -->

## Description

Fuses the RotaryMul operator into the RotaryPositionEmbedding operator.

![](../figures/RotaryMul2RotaryPositionEmbeddingFusionPass_1.png)

## Constraints

You are advised not to disable this pattern. Otherwise, the RotaryMul Ascend IR function will be unavailable.

## Applicable Products

<!-- npu="950" id1 -->
Ascend 950PR&950DT products
<!-- end id1 -->
