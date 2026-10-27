# Conv3DbpInputBiasAddFusionPass

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T06:43:08.917Z pushedAt=2026-10-15T12:44:18.289Z -->

## Description

Fuses the Conv3DBackpropInput+BiasAdd operators into the Conv3DTransposeD operator. The BiasAdd input is used as the input bias of Conv3DTransposeD.

![](../figures/Conv3DbpInputBiasAddFusionPass_1.png)

## Constraints

The output format of the Conv3DTransposeD operator is FLOAT16.
