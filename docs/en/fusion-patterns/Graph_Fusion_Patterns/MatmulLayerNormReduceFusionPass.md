# MatmulLayerNormReduceFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:49:57.013Z pushedAt=2026-10-15T12:44:18.392Z -->

## Description

Fuses the structure that meets the following patterns into the MatmulLayerNormReduce+LayerNormUpdate operator.

![](../figures/MatmulLayerNormReduceFusionPass_1.png)

Or

![](../figures/MatmulLayerNormReduceFusionPass_2.png)

## Constraints

It takes effect only on the SDXL network.

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->
