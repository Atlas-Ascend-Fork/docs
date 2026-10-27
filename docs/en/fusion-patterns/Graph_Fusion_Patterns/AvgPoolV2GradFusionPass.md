# AvgPoolV2GradFusionPass

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T06:39:48.113Z pushedAt=2026-10-15T12:44:18.231Z -->

Changes the AvgPoolV2Grad operator into the AvgPoolV2GradD operator.

![](../figures/AvgPoolV2GradFusionPass_1.png)

## Constraints

The input `ori_input_shape` of AvgPoolV2Grad must be a const node or a data node with a value.
