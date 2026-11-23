# MatMulAlignInputsFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:47:55.384Z pushedAt=2026-11-16T06:27:04.354Z nl=2 -->

## Description

When the inner axis of the input shape of the matmul operator is not 512-byte aligned, the MTE efficiency is low and the performance is poor. This graph fusion aligns the input shape of matmul to solve the performance problem.

![](../figures/MatMulAlignInputsFusionPass_1.png)

## Constraints

Applies only to the static scenario where the input DType is Float32 and the input does not have bias.

This non-common fusion is performed only in certain cases.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->

<!-- npu="A3" id2 -->
Atlas A3 products
<!-- end id2 -->
