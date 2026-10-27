# TbeConv2DReluv2Pass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T07:03:52.318Z pushedAt=2026-10-15T12:44:18.632Z -->

## Description

Fuses the Conv2D+ReluV2 operators into one Conv2D operator.

![](../figures/TbeConv2DReluv2Pass_1.png)

## Constraints

- The data type of output 1 of Conv2D must be float16.
- ReluV2 must have two outputs.

## Applicable Products

<!-- npu="910" id1 -->
Atlas training products
<!-- end id1 -->
