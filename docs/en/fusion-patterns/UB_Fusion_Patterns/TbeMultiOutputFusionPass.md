# TbeMultiOutputFusionPass

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T07:06:50.394Z pushedAt=2026-10-15T12:44:18.677Z -->

## Description

Performs UB fusion on the ElemWise nodes in the subgraphs that meet the following patterns.

The number in the parentheses indicates the value range of the number of ElemWise nodes. `head` indicates that the current node is the first node for matching.

![](../figures/TbeMultiOutputFusionPass_1.png)

Or

![](../figures/TbeMultiOutputFusionPass_2.png)

## Constraints

None
