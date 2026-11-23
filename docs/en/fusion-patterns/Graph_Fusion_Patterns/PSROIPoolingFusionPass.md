# PSROIPoolingFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:49:11.411Z pushedAt=2026-11-16T06:27:04.388Z nl=2 -->

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
