# TbeElemwiseQuantFusionPass

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T07:06:03.463Z pushedAt=2026-10-15T12:44:18.662Z -->

## Description

Performs UB fusion on the Elemwise/Broadcast and Quant operators.

![](../figures/TbeElemwiseQuantFusionPass_01.png)

## Constraints

- The Elemwise/Broadcast operator type cannot be Eltwise.
- The Elemwise/Broadcast operator must have dual inputs.
- Dynamic shapes are not supported.
