# PadFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:49:05.261Z pushedAt=2026-11-16T06:27:04.401Z nl=2 -->

## Description

Fuses the Pad operator that fits the graph fusion pattern into the PadD operator when the input `paddings` is a const node, and converts the input into an attribute.

![](../figures/PadFusionPass_1.png)

## Constraints

If the data type of input x is not within `{float16,float,int32}`, graph fusion is not performed.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
