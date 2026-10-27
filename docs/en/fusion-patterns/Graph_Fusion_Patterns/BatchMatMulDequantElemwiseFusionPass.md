# BatchMatMulDequantElemwiseFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:40:16.128Z pushedAt=2026-10-15T12:44:18.242Z -->

## Description

Fuses BatchMatMul/MatMul, AscendDequant, and Elemwise into the BatchMatMul operator in quantization use cases. The Elemwise operator is broadcast to MatMul.

![](../figures/BatchMatMulDequantElemwiseFusionPass_1.png)

## Constraints

- The two inputs of Elemwise must have the same dimensions and both have the **batch **axis. Elemwise can be broadcast to the MatMul shape only on the **batch** axis.
- Elemwise supports only the Add and Sub operators.
- The input format of Elemwise must be FRACTAL_NZ.

## Applicable Products

<!-- npu="310b" id1 -->
Atlas 200I/500 A2 inference products
<!-- end id1 -->
