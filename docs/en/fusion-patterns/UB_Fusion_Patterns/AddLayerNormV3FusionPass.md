# AddLayerNormV3FusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:53:18.811Z pushedAt=2026-11-16T06:27:04.502Z nl=2 -->

## Description

Performs UB fusion on the RealDiv+Add+LayerNormV3 structure or the Add+LayerNormV3 structure.

![](../figures/AddLayerNormV3FusionPass_1.png)

Or

![](../figures/AddLayerNormV3FusionPass_2.png)

## Constraints

- This pattern supports only static use cases on Atlas inference accelerator cards, with data format being ND; other use cases are not supported;
- This pattern applies only when the last axis of LayerNormV3 is 320, 640, 768, 1024, 1280, or 1536.

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->
