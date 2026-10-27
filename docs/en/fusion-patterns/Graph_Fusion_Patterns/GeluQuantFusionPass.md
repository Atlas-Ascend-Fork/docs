# GeluQuantFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:47:12.989Z pushedAt=2026-10-15T12:44:18.344Z -->

## Description

Fuses the small operators (Gelu + AscendQuantV2) or (Gelu + DynamicQuant) into the large operator GeluQuant.

![](../figures/GeluQuantFusionPass_1.png)

Or

![](../figures/GeluQuantFusionPass_2.png)

## Constraints

- The shape of the Gelu input parameter must be greater than or equal to two dimensions.
- The Gelu output connects to only one node AscendQuantV2 or DynamicQuant.
- The type of output `y` of the AscendQuantV2 or DynamicQuant operator is int8.
- When Gelu and the downstream AscendQuantV2 operator are fused, set `sqrt_mode` of AscendQuantV2 to `false`, `round_mode` of AscendQuantV2 to `round`, and `dst_type` of AscendQuantV2 to `int8`.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
