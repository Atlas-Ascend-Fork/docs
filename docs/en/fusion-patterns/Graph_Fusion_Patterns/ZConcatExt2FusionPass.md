# ZConcatExt2FusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:57:52.260Z pushedAt=2026-10-15T12:44:18.521Z -->

## Description

Splits the ConcatV2 operator with multiple inputs into multiple ConcatV2D operators. The number of ConcatV2D operators after fusion is determined based on the actual number of inputs according to a predefined calculation rule.

![](../figures/ZConcatExt2FusionPass_1.png)

After:

![](../figures/ZConcatExt2FusionPass_2.png)

## Constraints

- For static shapes, the maximum number of inputs compiled for a single ConcatV2 operator is 63.
- For dynamic shapes, the maximum number of inputs compiled for a single ConcatV2 operator is 48.
- In binary use cases, the maximum number of inputs compiled for a single ConcatV2 operator is 32.
- The input data type cannot be complex64, complex128, or double.
- This fusion pattern cannot be disabled by default.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
