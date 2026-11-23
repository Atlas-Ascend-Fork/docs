# TfMergeWeightQuantFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:51:34.094Z pushedAt=2026-11-16T06:27:04.449Z nl=2 -->

## Description

In quantization use cases, for the matched Cube operators (including Conv2D, DepthwiseConv2D, Conv3D, Deconvolution, Conv2DTransposeD, MatMulV2, and BatchMatMulV2) in the following graph structures, performs the operations shown in the following figures.

If AscendWeightQuant has a Sub input node, fuses Sub.

If AscendWeightQuant does not have a Sub input node, updates the format of AscendWeightQuant to HWCN.

If a Cube operator is followed by a BiasAdd node, fuses the BiasAdd node.

Fusion pattern 1

![](../figures/TfMergeWeightQuantFusionPass_1.png)

Fusion pattern 2

![](../figures/TfMergeWeightQuantFusionPass_2.png)

Fusion pattern 3

![](../figures/TfMergeWeightQuantFusionPass_3.png)

Fusion pattern 4

![](../figures/TfMergeWeightQuantFusionPass_4.png)

Fusion pattern 5

![](../figures/TfMergeWeightQuantFusionPass_5.png)

Fusion pattern 6

![](../figures/TfMergeWeightQuantFusionPass_6.png)

## Constraints

If the fusion condition contains an AscendWeightQuant operator, the AscendWeightQuant operator requires a minimum of two inputs.

The number of outputs of Split must match the number of inputs to Concat, and outputs of Split must be connected to inputs of Concat.

## Applicable Products

<!-- npu="950" id1 -->
Ascend 950PR&950DT products
<!-- end id1 -->
