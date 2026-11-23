# CubeTransFixpipeFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:45:11.254Z pushedAt=2026-11-16T06:27:04.289Z nl=2 -->

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
