# MatMulAlignInputsFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:49:30.618Z pushedAt=2026-10-15T12:44:18.387Z -->

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
