# SoftmaxSmallOpFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:50:36.365Z pushedAt=2026-11-16T06:27:04.427Z nl=2 -->

## Description

Identifies and fuses small operators such as ReduceMaxD and Sub into the SoftmaxV2 operator.

This fusion pattern is disabled by default.

Before: ![](../figures/SoftmaxSmallOpFusionPass_1.png) After: ![](../figures/SoftmaxSmallOpFusionPass_2.png)

## Constraints

- Dynamic shapes are not supported.
- For the input parameters of ReduceMaxD and ReduceSumD:
  - `axes` must be the same.
  - `keep_dims` must be `true`.

- The fusion pattern does not take effect if the reduce axis is set to `1` and the AReduceSumFusionPass fusion pattern is enabled.
- The current fusion pattern does not take effect if there is more than one reduce axis and the tail axis is included, the data type is FLOAT32, and ReduceMaxDFusionPass fusion pattern is enabled.
<!-- npu="910b" id2 -->
- Data type constraints:
  - Atlas A2 products: Supported data types are FLOAT32, FLOAT16, and BFLOAT16.
<!-- end id2 -->

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
