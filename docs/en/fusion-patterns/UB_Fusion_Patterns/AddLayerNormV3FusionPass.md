# AddLayerNormV3FusionPass

<!-- md-trans-meta sourceCommit=067605f577cb8d67fb272f6aa2f339a50f346779 translatedAt=2026-10-09T06:59:41.794Z pushedAt=2026-10-15T12:44:18.547Z -->

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
