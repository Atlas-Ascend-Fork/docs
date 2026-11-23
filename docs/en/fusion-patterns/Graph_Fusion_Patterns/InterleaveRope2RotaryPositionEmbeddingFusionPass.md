# InterleaveRope2RotaryPositionEmbeddingFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:48:06.982Z pushedAt=2026-11-16T06:27:04.359Z nl=2 -->

## Description

Fuses the InterleaveRope operator into the RotaryPositionEmbedding operator, as shown in the following fusion.

![](../figures/InterleaveRope2RotaryPositionEmbeddingFusionPass_1.png)

## Constraints

You are advised not to disable this pattern. Otherwise, the InterleaveRope Ascend IR function will be unavailable.

## Applicable Products

<!-- npu="950" id1 -->
Ascend 950PR&950DT products
<!-- end id1 -->
