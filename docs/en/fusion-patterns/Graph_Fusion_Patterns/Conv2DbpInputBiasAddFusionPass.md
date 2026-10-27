# Conv2DbpInputBiasAddFusionPass

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T06:42:46.359Z pushedAt=2026-10-15T12:44:18.281Z -->

## Description

Fuses the Conv2DBackpropInput and BiasAdd operators into the Conv2DTransposeD operator.

![](../figures/Conv2DbpInputBiasAddFusionPass_1.png)

After:

![](../figures/Conv2DbpInputBiasAddFusionPass_2.png)

## Constraints

None
