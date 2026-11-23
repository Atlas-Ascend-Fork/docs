# TbeConv3dDxElemwisePass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:55:47.096Z pushedAt=2026-11-16T06:27:04.575Z nl=2 -->

## Description

Performs UB fusion on Conv3dBackpropInput and Elemwise in the following pattern subgraphs.

![](../figures/TbeConv3dDxElemwisePass_1.png)

Or

![](../figures/TbeConv3dDxElemwisePass_2.png)

Or

![](../figures/TbeConv3dDxElemwisePass_3.png)

## Constraints

- Elemwise can only be set to AddN, and Elemwise1 can only be set to LeakyReluGrad.
- Dynamic shapes are not supported.

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->

<!-- npu="910" id2 -->
Atlas training products
<!-- end id2 -->
