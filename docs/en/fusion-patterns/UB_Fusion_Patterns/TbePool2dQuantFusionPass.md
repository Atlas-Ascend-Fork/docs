# TbePool2dQuantFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:57:42.771Z pushedAt=2026-11-16T06:27:04.631Z nl=2 -->

## Description

Fuses the Pool2D+Quant+strided_write operators into one operator.

![](../figures/TbePool2dQuantFusionPass_1.png)

## Constraints

The strided_write operator will be optimized during fusion. Therefore, the fusion pattern must not be disabled separately.

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
