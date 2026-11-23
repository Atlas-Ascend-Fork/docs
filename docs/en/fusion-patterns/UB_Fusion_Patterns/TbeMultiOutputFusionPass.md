# TbeMultiOutputFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:57:38.321Z pushedAt=2026-11-16T06:27:04.628Z nl=2 -->

## Description

Performs UB fusion on the ElemWise nodes in the subgraphs that meet the following patterns.

The number in the parentheses indicates the value range of the number of ElemWise nodes. `head` indicates that the current node is the first node for matching.

![](../figures/TbeMultiOutputFusionPass_1.png)

or

![](../figures/TbeMultiOutputFusionPass_2.png)

## Constraints

None.
