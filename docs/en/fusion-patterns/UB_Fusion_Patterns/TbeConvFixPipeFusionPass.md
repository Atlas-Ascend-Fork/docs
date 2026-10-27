# TbeConvFixPipeFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T07:05:08.014Z pushedAt=2026-10-15T12:44:18.640Z -->

## Description

Performs UB fusion on Conv2d and the Fixpipe node, Elemwise operator (optional), and Quant operator (optional) generated in [FIXPIPEFUSIONPASS](../Graph_Fusion_Patterns/FIXPIPEFUSIONPASS.md).

![](../figures/TbeConvFixPipeFusionPass_1.png)

## Constraints

None

## Applicable Products

<!-- npu="310b" id1 -->
Atlas 200I/500 A2 inference products
<!-- end id1 -->

<!-- npu="910b" id2 -->
Atlas A2 products
<!-- end id2 -->

<!-- npu="A3" id3 -->
Atlas A3 products
<!-- end id3 -->
