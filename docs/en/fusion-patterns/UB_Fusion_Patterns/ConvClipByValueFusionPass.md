# ConvClipByValueFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:53:58.285Z pushedAt=2026-11-16T06:27:04.521Z nl=2 -->

## Description

The following fusion pattern is supported:

Fuses the Conv2D+Elemwise (ClipByValue type) operators into one operator.

![](../figures/ConvClipByValueFusionPass_1.png)

## Constraints

- The number of Elemwise operators is 1 to 3. The first Elemwise operator must be of the ClipByValue type, and the last two Elemwise operators must be of the Relu or Add type.
- The number of the output channels of the Conv2D operator must be an integer multiple of 16.

## Applicable Products

<!-- npu="310b" id1 -->
Atlas 200I/500 A2 inference products
<!-- end id1 -->

<!-- npu="310p" id2 -->
Atlas inference products
<!-- end id2 -->

<!-- npu="910" id3 -->
Atlas training products
<!-- end id3 -->
