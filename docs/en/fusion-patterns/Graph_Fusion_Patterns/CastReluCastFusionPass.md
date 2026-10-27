# CastReluCastFusionPass

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T06:41:23.555Z pushedAt=2026-10-15T12:44:18.260Z -->

## Description

Fuses the Cast+Relu+Cast operators into the Relu operator, that is, removes the Cast operators before and after Relu.

![](../figures/CastReluCastFusionPass_1.png)

## Constraints

The data type of ReLU is fp32. The input data type of the front cast must be the same as the output data type of the rear cast, such as converting both from fp16 to fp32 or fp32 to fp16.
