# BatchMatMulDequantElemwiseFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:42:45.275Z pushedAt=2026-11-16T06:27:04.222Z nl=2 -->

## Description

Fuses BatchMatMul/MatMul, AscendDequant, and Elemwise into the BatchMatMul operator in quantization use cases. The Elemwise operator is broadcast to MatMul.

![](../figures/BatchMatMulDequantElemwiseFusionPass_1.png)

## Constraints

- The two inputs of Elemwise must have the same dimensions and both have the **batch** axis. Elemwise can be broadcast to the MatMul shape only on the **batch** axis.
- Elemwise supports only the Add and Sub operators.
- The input format of Elemwise must be FRACTAL_NZ.

## Applicable Products

<!-- npu="310b" id1 -->
Atlas 200I/500 A2 inference products
<!-- end id1 -->
