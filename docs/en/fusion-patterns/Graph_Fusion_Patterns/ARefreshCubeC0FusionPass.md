# ARefreshCubeC0FusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:42:25.929Z pushedAt=2026-11-16T06:27:04.210Z nl=2 -->

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
