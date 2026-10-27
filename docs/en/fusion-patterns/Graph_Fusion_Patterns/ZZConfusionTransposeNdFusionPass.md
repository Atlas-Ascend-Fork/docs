# ZZConfusionTransposeNdFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:58:31.767Z pushedAt=2026-10-15T12:44:18.530Z -->

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
