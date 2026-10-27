# MatMulFastgelugradUbFusion

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T07:01:15.556Z pushedAt=2026-10-15T12:44:18.569Z -->

## Description

Performs UB fusion on MatMul/GEMM and Elemwise in the subgraphs that meet the following patterns.

![](../figures/MatMulFastgelugradUbFusion_1.png)

## Constraints

Dynamic shapes are not supported.
