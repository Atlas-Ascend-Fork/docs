# TbeEltwiseQuantFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:57:22.405Z pushedAt=2026-11-16T06:27:04.621Z nl=2 -->

## Description

Performs UB fusion on the ElemWise/Broadcast and quant nodes in the subgraphs that meet the following patterns.

![](../figures/TbeEltwiseQuantFusionPass_01.png)

Or

![](../figures/TbeEltwiseQuantFusionPass_02.png)

Or

![](../figures/TbeEltwiseQuantFusionPass_03.png)

## Constraints

- In an ElemWise/Broadcast+ElemWise/Broadcast+Quant use case, a maximum of five ElemWise/Broadcast nodes are supported.
- Dynamic shapes are not supported.
