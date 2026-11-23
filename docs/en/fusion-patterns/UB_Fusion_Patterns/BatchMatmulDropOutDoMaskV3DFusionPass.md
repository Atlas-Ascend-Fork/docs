# BatchMatmulDropOutDoMaskV3DFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:53:36.230Z pushedAt=2026-11-16T06:27:04.513Z nl=2 -->

## Description

Performs UB fusion on BatchMatMul and DropOutDoMaskV3D/Add in a subgraph that meets the following pattern:

![](../figures/BatchMatmulDropOutDoMaskV3DFusionPass_1.png)

## Constraints

- Dynamic shapes are not supported.
- BatchMatMul and BatchMatMulV2 are supported.

## Applicable Products

<!-- npu="310b" id1 -->
Atlas 200I/500 A2 inference products
<!-- end id1 -->

<!-- npu="310p" id2 -->
Atlas inference products
<!-- end id2 -->

<!-- npu="910" id3 -->
Atlas training products
<!-- end id3 -->
