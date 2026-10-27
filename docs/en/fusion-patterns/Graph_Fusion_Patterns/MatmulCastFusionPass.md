# MatmulCastFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:49:46.546Z pushedAt=2026-10-15T12:44:18.389Z -->

## Description

Fuses the MatMul/MatMulV2/BatchMatMul/BatchMatMulV2 and cast operators into the MatMul/MatMulV2/BatchMatMul/BatchMatMulV2 operator.

![](../figures/MatmulCastFusionPass_1.png)

Fused into

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
