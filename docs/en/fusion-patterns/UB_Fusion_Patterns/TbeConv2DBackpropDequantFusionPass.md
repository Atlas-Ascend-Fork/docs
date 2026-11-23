# TbeConv2DBackpropDequantFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:55:23.974Z pushedAt=2026-11-16T06:27:04.562Z nl=2 -->

## Description

Performs UB fusion on DX+AscendDequant.

![](../figures/TbeConv2DBackpropDequantFusionPass_1.png)

## Constraints

- DX and AscendDequant are mandatory.
- DX supports Conv2DBackpropInputD, Conv2DTransposeD, and Deconvolution.

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
