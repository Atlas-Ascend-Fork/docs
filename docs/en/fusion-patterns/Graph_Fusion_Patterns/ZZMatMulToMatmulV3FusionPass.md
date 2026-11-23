# ZZMatMulToMatmulV3FusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:53:13.304Z pushedAt=2026-11-16T06:27:04.499Z nl=2 -->

## Description

Converts the MatmulV2 operator that fits the graph fusion pattern into the MatmulV3 operator.

![](../figures/ZZMatMulToMatmulV3FusionPass_1.png)

## Constraints

The fusion pattern does not take effect if any of the following conditions are met:

- The platform does not support l0c2out or out2l1_nd2nz, but supports l0c2ub and fix_pipe_l0c2ub.
- Any input or output dimension is below 2, the shape is dynamic, and the input or output data type is not float16, bfloat16, or float32.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
