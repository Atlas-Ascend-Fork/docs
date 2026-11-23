# TbeConv2DReluv2Pass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:55:44.867Z pushedAt=2026-11-16T06:27:04.572Z nl=2 -->

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
