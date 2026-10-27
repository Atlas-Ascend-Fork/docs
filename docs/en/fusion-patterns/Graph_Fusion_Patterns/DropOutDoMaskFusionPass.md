# DropOutDoMaskFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:45:33.091Z pushedAt=2026-10-15T12:44:18.321Z -->

## Description

Replaces the DropOutDoMaskV3D operator with DropOutDoMask.

After fusion, the DropOutDoMaskV3D operator is replaced with the DropOutDoMask operator. The DropOutDoMask operator can be implemented through the DSL branch using the Elemwise template and supports UB fusion.

![](../figures/DropOutDoMaskFusionPass_1.png)

After:

![](../figures/DropOutDoMaskFusionPass_2.png)

## Constraints

- When the DSA module is supported, the fusion patterns take effect and must be enabled.
- Fusion patterns must be enabled when the DropOutDoMask operator is used for UB fusion.
- One of the parent nodes of DropOutDoMaskV3D must be DSAGenBitMask, which is used as the mask input.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->

<!-- npu="A3" id2 -->
Atlas A3 products
<!-- end id2 -->
