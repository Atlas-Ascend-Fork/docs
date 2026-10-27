# ARefreshCubeC0FusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:39:48.974Z pushedAt=2026-10-15T12:44:18.234Z -->

## Description

Corrects the c0 value of cube operators when their inputs and outputs use heavy (private) formats.

## Constraints

- Cube operators include AvgPool, AvgPoolV2, BatchMatMulV2, Conv2D, Conv2DTransposeD, Conv3D, Deconvolution, DepthwiseConv2D, FullyConnection, MatMulV2, MaxPool, Pooling, and QuantBatchMatmulV3.
- The input and output data types are float before conversion.
- This fusion pattern cannot be disabled.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
