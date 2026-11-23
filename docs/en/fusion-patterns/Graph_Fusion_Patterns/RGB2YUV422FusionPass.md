# RGB2YUV422FusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:49:57.976Z pushedAt=2026-11-16T06:27:04.409Z nl=2 -->

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
