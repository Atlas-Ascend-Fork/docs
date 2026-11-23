# GemmTransFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:46:36.620Z pushedAt=2026-11-16T06:27:04.326Z nl=2 -->

## Description

Fuses the Transpose+Gemm operators into the GemmTrans operator.

![](../figures/GemmTransFusionPass_1.png)

After:

![](../figures/GemmTransFusionPass_2.png)

## Constraints

The input format of Transpose must be ND, and non-alignment scenarios are not supported.

## Applicable Products

<!-- npu="310b" id1 -->
Atlas 200I/500 A2 inference products
<!-- end id1 -->
