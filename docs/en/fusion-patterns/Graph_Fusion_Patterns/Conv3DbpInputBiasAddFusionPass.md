# Conv3DbpInputBiasAddFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:44:24.738Z pushedAt=2026-11-16T06:27:04.267Z nl=2 -->

## Description

Fuses the Conv3DBackpropInput+BiasAdd operators into the Conv3DTransposeD operator. The BiasAdd input is used as the input bias of Conv3DTransposeD.

![](../figures/Conv3DbpInputBiasAddFusionPass_1.png)

## Constraints

The output format of the Conv3DTransposeD operator is FLOAT16.
