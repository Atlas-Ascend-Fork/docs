# InterleaveRope2RotaryPositionEmbeddingFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:49:04.355Z pushedAt=2026-10-15T12:44:18.375Z -->

## Description

Fuses the InterleaveRope operator into the RotaryPositionEmbedding operator, as shown in the following fusion.

![](../figures/InterleaveRope2RotaryPositionEmbeddingFusionPass_1.png)

## Constraints

You are advised not to disable this pattern. Otherwise, the InterleaveRope Ascend IR function will be unavailable.

## Applicable Products

<!-- npu="950" id1 -->
Ascend 950PR&950DT products
<!-- end id1 -->
