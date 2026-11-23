# TbeDxElemwisePass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:56:49.484Z pushedAt=2026-11-16T06:27:04.603Z nl=2 -->

## Description

Performs UB fusion on DX+ElementWise.

![](../figures/TbeDxElemwisePass_1.png)

## Constraints

- ElementWise supports ReLU, Leaky ReLU, PReLU, and Add.
- DX supports Conv2DBackpropInputD, Conv2DTransposeD, and Deconvolution.
- This UB fusion pattern applies to DX non-quantization use cases, mostly for ElementWise.
- Dynamic scenarios are not supported.

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->

<!-- npu="310b" id2 -->
Atlas 200I/500 A2 inference products
<!-- end id2 -->

<!-- npu="910" id3 -->
Atlas training products
<!-- end id3 -->
