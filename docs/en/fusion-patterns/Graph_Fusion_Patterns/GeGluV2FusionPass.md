# GeGluV2FusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:47:16.070Z pushedAt=2026-10-15T12:44:18.347Z -->

## Description

Fuses small operators (SplitVD + Gelu + Mul) into the large operator GeGluV2.

![](../figures/GeGluV2FusionPass_1.png)

## Constraints

Only the scenario where the split axis of the SplitVD node is greater than 512 is supported.

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->

<!-- npu="910b" id3 -->
Ascend_xxx_B in Atlas A2 products
<!-- end id3 -->

<!-- npu="A3" id2 -->
Atlas A3 products
<!-- end id2 -->
