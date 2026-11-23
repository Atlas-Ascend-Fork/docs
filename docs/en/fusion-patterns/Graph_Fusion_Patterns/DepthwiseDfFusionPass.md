# DepthwiseDfFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:45:28.666Z pushedAt=2026-11-16T06:27:04.293Z nl=2 -->

## Description

Adds the TransposeD operator before the DepthwiseConv2DbackpropInput convolution operator to improve computing performance.

Before: ![](../figures/DepthwiseDfFusionPass_1.png) After:

![](../figures/DepthwiseDfFusionPass_2.png)

## Constraints

This fusion takes effect only when the filter format is NCHW.
