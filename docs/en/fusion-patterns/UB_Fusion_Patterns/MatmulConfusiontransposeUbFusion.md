# MatmulConfusiontransposeUbFusion

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T07:01:05.209Z pushedAt=2026-10-15T12:44:18.564Z -->

## Description

Performs UB fusion on MatMul and ConfusionTransposeD in the subgraph that meets the following pattern.

![](../figures/MatmulConfusiontransposeUbFusion_1.png)

## Constraints

Dynamic shapes are not supported.
