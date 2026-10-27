# BatchMatmulConfusiontransposeUbFusion

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T07:00:02.906Z pushedAt=2026-10-15T12:44:18.549Z -->

## Description

Performs UB fusion on batch_matmul and batchmatmul_transpose in a subgraph that meets the following pattern:

![](../figures/BatchMatmulConfusiontransposeUbFusion_1.png)

## Constraints

Dynamic scenarios are not supported.

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
