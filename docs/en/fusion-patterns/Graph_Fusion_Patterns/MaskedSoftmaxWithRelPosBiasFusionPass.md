# MaskedSoftmaxWithRelPosBiasFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:47:49.542Z pushedAt=2026-11-16T06:27:04.351Z nl=2 -->

## Description

Fuses Mul, Add, Reshape, and Softmax that meet the following conditions into the MaskedSoftmaxWithRelPosBias operator.

**Pattern 1:**

![](../figures/MaskedSoftmaxWithRelPosBiasFusionPass_1.png)

**Pattern 2:**

![](../figures/MaskedSoftmaxWithRelPosBiasFusionPass_2.png)

**Pattern 3**

![](../figures/MaskedSoftmaxWithRelPosBiasFusionPass_3.png)

**Pattern 4**

![](../figures/MaskedSoftmaxWithRelPosBiasFusionPass_4.png)

## Constraints

The input supports only four or five dimensions. Each fusion mode has the corresponding input shape, which is the base for constructing an operator. B, W, N, S1, and S2 indicate the dimensions of each shape, and `scale` indicates that the input is a scalar.

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->

<!-- npu="910b" id2 -->
Atlas A2 products
<!-- end id2 -->

<!-- npu="A3" id3 -->
Atlas A3 products
<!-- end id3 -->
