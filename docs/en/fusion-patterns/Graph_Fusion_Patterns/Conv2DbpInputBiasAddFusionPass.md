# Conv2DbpInputBiasAddFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:44:06.819Z pushedAt=2026-11-16T06:27:04.260Z nl=2 -->

## Description

Fuses the Conv2DBackpropInput and BiasAdd operators into the Conv2DTransposeD operator.

![](../figures/Conv2DbpInputBiasAddFusionPass_1.png)

After:

![](../figures/Conv2DbpInputBiasAddFusionPass_2.png)

## Constraints

None.
