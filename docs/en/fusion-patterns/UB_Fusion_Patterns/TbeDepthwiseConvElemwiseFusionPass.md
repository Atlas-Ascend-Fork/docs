# TbeDepthwiseConvElemwiseFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T07:05:25.993Z pushedAt=2026-10-15T12:44:18.645Z -->

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
