# LayerNormSpecialTrainingFusionPass

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T06:49:16.698Z pushedAt=2026-10-15T12:44:18.381Z -->

## Description

Fuses the Mean/SquaredDifference/Add/Rsqrt/RsqrtGrad/Mul/Sub/AddN operator into a LayerNorm operator and two LayerNormGrad operators to improve the computing performance. See the following figure.

![](../figures/LayerNormSpecialTrainingFusionPass_01.png)

## Constraints

None
