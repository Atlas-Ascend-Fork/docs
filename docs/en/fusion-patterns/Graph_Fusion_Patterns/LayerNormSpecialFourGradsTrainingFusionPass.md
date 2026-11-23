# LayerNormSpecialFourGradsTrainingFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:47:36.441Z pushedAt=2026-11-16T06:27:04.346Z nl=2 -->

## Description

Similar to LayerNormSpecialTrainingFusionPass, fuses the Mean/SquaredDifference/Add/Rsqrt/RsqrtGrad/Mul/Sub/AddN operator into one LayerNorm operator and two LayerNormGrad operators to improve the computing performance. The difference is that the fusion pass matches four backward patterns and fuses two backward LayerNorm structures whose scope names are the same as those of the forward LayerNorm into the LayerNormGrad operator. See the table below.

![](../figures/LayerNormSpecialFourGradsTrainingFusionPass_01.png)

## Constraints

None.
