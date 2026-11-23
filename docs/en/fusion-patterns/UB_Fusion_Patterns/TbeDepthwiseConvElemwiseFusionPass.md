# TbeDepthwiseConvElemwiseFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:56:29.725Z pushedAt=2026-11-16T06:27:04.593Z nl=2 -->

## Description

Performs UB fusion on Elemwise+DepthwiseConvolution in the following pattern.

![](../figures/TbeDepthwiseConvElemwiseFusionPass_1.png)

## Constraints

- The ElementWise type supports only LeakyRelu, and the coefficient is 0.
- The DepthwiseConvolution type supports only DepthwiseConv2D.

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->

<!-- npu="910" id2 -->
Atlas training products
<!-- end id2 -->
