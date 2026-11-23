# MatmulCastFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:48:09.734Z pushedAt=2026-11-16T06:27:04.362Z nl=2 -->

## Description

Fuses the MatMul/MatMulV2/BatchMatMul/BatchMatMulV2 and cast operators into the MatMul/MatMulV2/BatchMatMul/BatchMatMulV2 operator.

![](../figures/MatmulCastFusionPass_1.png)

After:

![](../figures/MatmulCastFusionPass_2.png)

## Constraints

This fusion takes effect when the input data type of MatMul is float16 and the output data type of cast is float32.

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->

<!-- npu="910" id2 -->
Atlas training products
<!-- end id2 -->
