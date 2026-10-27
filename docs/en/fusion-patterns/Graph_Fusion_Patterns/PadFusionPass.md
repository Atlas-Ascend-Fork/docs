# PadFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:51:12.245Z pushedAt=2026-10-15T12:44:18.417Z -->

## Description

Fuses the Pad operator that fits the graph fusion pattern into the PadD operator when the input `paddings` is a const node, and converts the input into an attribute.

![](../figures/PadFusionPass_1.png)

## Constraints

If the data type of input x is not within `{float16,float,int32}`, graph fusion is not performed.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
