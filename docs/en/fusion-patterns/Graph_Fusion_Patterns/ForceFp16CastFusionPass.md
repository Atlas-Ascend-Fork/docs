# ForceFp16CastFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:46:11.490Z pushedAt=2026-11-16T06:27:04.311Z nl=2 -->

## Description

For cast operators, when converting input and output data types between int32 and fp32 (either int32->fp32 or fp32->int32), set `attr_keep_dtype` to improve the precision.

![](../figures/ForceFp16CastFusionPass_1.png)

## Constraints

For cast operators, this fusion pattern is enabled when data types for the input and output are converted between int32 and fp32 (either int32->fp32 or fp32->int32).

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
