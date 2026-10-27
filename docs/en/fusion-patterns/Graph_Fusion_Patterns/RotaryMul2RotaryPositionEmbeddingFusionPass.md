# RotaryMul2RotaryPositionEmbeddingFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:52:41.851Z pushedAt=2026-10-15T12:44:18.439Z -->

## Description

Fuses the RotaryMul operator into the RotaryPositionEmbedding operator.

![](../figures/RotaryMul2RotaryPositionEmbeddingFusionPass_1.png)

## Constraints

You are advised not to disable this pattern. Otherwise, the RotaryMul Ascend IR function will be unavailable.

## Applicable Products

<!-- npu="950" id1 -->
Ascend 950PR&950DT products
<!-- end id1 -->
