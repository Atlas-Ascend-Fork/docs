# TbePool2dQuantFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T07:07:05.083Z pushedAt=2026-10-15T12:44:18.681Z -->

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
