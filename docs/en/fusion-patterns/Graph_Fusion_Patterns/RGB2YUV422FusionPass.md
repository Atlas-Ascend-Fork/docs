# RGB2YUV422FusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:52:45.297Z pushedAt=2026-10-15T12:44:18.441Z -->

## Description

Splits RGB2YUV422 into two operators: Aipp+YUV4442YUV422, because the RGB2YUV422 operator and the `load_image` operator in this operator support different product forms.

![](../figures/RGB2YUV422FusionPass_1.png)

## Constraints

- The input shape of RGB2YUV422 is three dimensions, and the last dimension must be 3.
- After the RGB2YUV422 input is reshaped into the NHWC format, ensure that H and W are less than or equal to 4096.
- The value range of the first two dimensions of the input shape of RGB2YUV422 is `[2, 4096]`.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->

<!-- npu="A3" id2 -->
Atlas A3 products
<!-- end id2 -->
