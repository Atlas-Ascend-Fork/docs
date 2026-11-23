# MatmulConfusiontransposeUbFusion

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:54:00.457Z pushedAt=2026-11-16T06:27:04.526Z nl=2 -->

## Description

Performs UB fusion on MatMul and ConfusionTransposeD in the subgraph that meets the following pattern.

![](../figures/MatmulConfusiontransposeUbFusion_1.png)

## Constraints

Dynamic shapes are not supported.
