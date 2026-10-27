# TbeConv3dDxElemwisePass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T07:04:00.508Z pushedAt=2026-10-15T12:44:18.623Z -->

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
