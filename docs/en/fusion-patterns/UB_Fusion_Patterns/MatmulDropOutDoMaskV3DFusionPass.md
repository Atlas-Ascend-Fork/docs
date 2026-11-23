# MatmulDropOutDoMaskV3DFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:54:08.004Z pushedAt=2026-11-16T06:27:04.528Z nl=2 -->

## Description

Performs UB fusion on MatMul and DropOutDoMaskV3D/Add in the following pattern subgraph.

![](../figures/MatmulDropOutDoMaskV3DFusionPass_1.png)

## Constraints

- MatMul must be the MatMulV2 operator.
- Dynamic shapes are not supported.

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
