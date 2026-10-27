# GemmTransFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:47:34.353Z pushedAt=2026-10-15T12:44:18.353Z -->

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
