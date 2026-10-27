# CubeTransFixpipeFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:44:38.213Z pushedAt=2026-10-15T12:44:18.307Z -->

## Description

Moves transdata downward to fuse with Fixpipe when the following structure is matched.

![](../figures/CubeTransFixpipeFusionPass_1.png)

## Constraints

- Only static scenarios are supported.
- The Cube operator must have FixpipeAbility configured. For details, see [FixPipeAbilityProcessPass](FixPipeAbilityProcessPass.md).
- The data type of the Cube node must be float32.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
