# BatchMatmulConfusiontransposeUbFusion

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:53:34.633Z pushedAt=2026-11-16T06:27:04.510Z nl=2 -->

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
