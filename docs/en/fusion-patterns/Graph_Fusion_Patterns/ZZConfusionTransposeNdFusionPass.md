# ZZConfusionTransposeNdFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:53:10.237Z pushedAt=2026-11-16T06:27:04.497Z nl=2 -->

## Description

Replaces the ConfusionTransposeD operator in the ND format with the Transpose operator in static scenarios.

![](../figures/ZZConfusionTransposeNdFusionPass_1.png)

## Constraints

- The input and output formats must be ND.
- Only static shapes are supported.
- The value of the `perm` attribute must be within the range of `[0, input rank]`.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
