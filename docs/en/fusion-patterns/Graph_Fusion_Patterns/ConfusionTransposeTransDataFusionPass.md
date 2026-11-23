# ConfusionTransposeTransDataFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:43:46.354Z pushedAt=2026-11-16T06:27:04.252Z nl=2 -->

## Description

Fuses ConfusionTransposeD(NHWC->NCHW) and TransData(NCHW->5HD) into the TransData(NHWC->5HD) operator to reduce one ConfusionTransposeD operation during the graph fusion phase.

![](../figures/ConfusionTransposeTransDataFusionPass_1.png)

## Constraints

- Only static subgraphs are supported.
- Only the ConfusionTransposeD(NHWC->NCHW) + TransData(NCHW->5HD) scenario is supported.
