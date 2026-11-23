# Conv2DTransposeBatchnormFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:44:08.357Z pushedAt=2026-11-16T06:27:04.262Z nl=2 -->

## Description

Fuses the Conv2DTranspose+BatchNorm/BNInference operators into the Conv2DTransposeD operator, that is, converts the input of BatchNorm or BNInference into the weight and bias inputs of Conv2DTransposeD.

![](../figures/Conv2DTransposeBatchnormFusionPass_1.png)

## Constraints

- The `groups` attribute of Conv2DTranspose must be set to `1`.
- The input type (except input x) of BatchNorm or BNInference must be const.
- Only static scenarios are supported.
- The BatchNorm operator supports only four dimensions.
