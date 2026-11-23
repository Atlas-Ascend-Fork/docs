# MatMulFastgelugradUbFusion

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:54:18.946Z pushedAt=2026-11-16T06:27:04.532Z nl=2 -->

## Description

Performs UB fusion on MatMul/GEMM and Elemwise in the subgraphs that meet the following patterns.

![](../figures/MatMulFastgelugradUbFusion_1.png)

## Constraints

Dynamic shapes are not supported.
