# AvgPoolV2GradFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:42:43.519Z pushedAt=2026-11-16T06:27:04.219Z nl=2 -->

Changes the AvgPoolV2Grad operator into the AvgPoolV2GradD operator.

![](../figures/AvgPoolV2GradFusionPass_1.png)

## Constraints

The input `ori_input_shape` of AvgPoolV2Grad must be a const node or a data node with a value.
