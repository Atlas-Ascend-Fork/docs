# TbeBatchMatMulQuantFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:55:05.405Z pushedAt=2026-11-16T06:27:04.557Z nl=2 -->

## Description

Performs UB fusion on BatchMatMul/GEMM and AscendDequant/AscendQuant/Elemwise in the subgraphs that meet the following patterns.

Pattern 1:

![](../figures/TbeBatchMatMulQuantFusionPass_1.png)

Pattern 2:

![](../figures/TbeBatchMatMulQuantFusionPass_2.png)

## Constraints

- BatchMatMul can be MatMul, MatMulV2, BatchMatMul, and BatchMatMulV2.
- Dynamic shapes are not supported.
- The Elemwise node must be FastGeluV2.

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
