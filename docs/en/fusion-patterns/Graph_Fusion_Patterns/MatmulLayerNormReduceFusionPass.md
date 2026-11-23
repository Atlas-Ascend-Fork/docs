# MatmulLayerNormReduceFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:48:13.187Z pushedAt=2026-11-16T06:27:04.365Z nl=2 -->

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
