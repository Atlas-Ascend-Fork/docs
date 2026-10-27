# DepthwiseDfFusionPass

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T06:45:12.357Z pushedAt=2026-10-15T12:44:18.318Z -->

## Description

Adds the TransposeD operator before the DepthwiseConv2DbackpropInput convolution operator to improve computing performance.

Before: ![](../figures/DepthwiseDfFusionPass_1.png) After:

![](../figures/DepthwiseDfFusionPass_2.png)

## Constraints

This fusion takes effect only when the filter format is NCHW.
