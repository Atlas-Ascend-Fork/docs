# PSROIPoolingFusionPass

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T06:51:39.632Z pushedAt=2026-10-15T12:44:18.425Z -->

## Description

If the input of PSROIPooling is Conv2D, inserts the SwapCo operator as the Filter and Bias output of Conv2D. If the input of PSROIPooling is not Conv2D, inserts the SwapCi operator as the input of PSROIPooling.

![](../figures/PSROIPoolingFusionPass_1.png)

After:

![](../figures/PSROIPoolingFusionPass_2.png)

Or

![](../figures/PSROIPoolingFusionPass_3.png)

After:

![](../figures/PSROIPoolingFusionPass_4.png)

## Constraints

The precursor node of PSROIPooling must be connected to input0, and the rois parameter of input1 must be specified.
