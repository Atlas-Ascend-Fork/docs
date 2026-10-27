# ATbeMatMulElemwiseFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:59:33.692Z pushedAt=2026-10-15T12:44:18.542Z -->

## Description

Performs UB fusion on MatMul/GEMM and Elemwise in the subgraphs that meet the following patterns.

![](../figures/ATbeMatMulElemwiseFusionPass_1.png)

or

![](../figures/ATbeMatMulElemwiseFusionPass_2.png)

## Constraints

Dynamic shapes are not supported.

## Applicable Products

<!-- npu="310b" id1 -->
Atlas 200I/500 A2 inference products
<!-- end id1 -->

<!-- npu="310p" id2 -->
Atlas inference products
<!-- end id2 -->

<!-- npu="910" id3 -->
Atlas training products
<!-- end id3 -->
