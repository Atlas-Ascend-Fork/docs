# TbeElemwiseQuantFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:57:09.070Z pushedAt=2026-11-16T06:27:04.614Z nl=2 -->

## Description

Performs UB fusion on the Elemwise/Broadcast and Quant operators.

![](../figures/TbeElemwiseQuantFusionPass_01.png)

## Constraints

- The Elemwise/Broadcast operator type cannot be Eltwise.
- The Elemwise/Broadcast operator must have dual inputs.
- Dynamic shapes are not supported.
