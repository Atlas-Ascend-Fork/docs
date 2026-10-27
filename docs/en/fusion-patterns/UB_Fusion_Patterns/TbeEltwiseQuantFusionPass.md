# TbeEltwiseQuantFusionPass

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T07:06:33.004Z pushedAt=2026-10-15T12:44:18.674Z -->

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
