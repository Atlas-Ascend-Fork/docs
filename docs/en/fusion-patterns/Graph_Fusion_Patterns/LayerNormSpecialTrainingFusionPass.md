# LayerNormSpecialTrainingFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:47:41.461Z pushedAt=2026-11-16T06:27:04.348Z nl=2 -->

## Description

Fuses the Mean/SquaredDifference/Add/Rsqrt/RsqrtGrad/Mul/Sub/AddN operator into a LayerNorm operator and two LayerNormGrad operators to improve the computing performance. See the following figure.

![](../figures/LayerNormSpecialTrainingFusionPass_01.png)

## Constraints

None.
