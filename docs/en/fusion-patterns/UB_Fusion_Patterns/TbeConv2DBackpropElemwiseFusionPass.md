# TbeConv2DBackpropElemwiseFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:55:28.100Z pushedAt=2026-11-16T06:27:04.567Z nl=2 -->

## Description

Performs UB fusion on DX+ElementWise+ElementWise1 (optional).

![](../figures/TbeConv2DBackpropElemwiseFusionPass_1.png)

## Constraints

- If only ElementWise exists, ReluGradV2 is supported. If ElementWise1 exists, ElementWise supports AddN and Add, and ElementWise1 supports ReluGradV2.
- DX supports Conv2DBackpropInputD, Conv2DTransposeD, and Deconvolution.
- DX supports only non-FP32 types.
- This UB fusion pattern applies to DX non-quantization use cases.
