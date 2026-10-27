# ConfusionTransposeTransDataFusionPass

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T06:42:17.311Z pushedAt=2026-10-15T12:44:18.271Z -->

## Description

Fuses ConfusionTransposeD(NHWC->NCHW) and TransData(NCHW->5HD) into the TransData(NHWC->5HD) operator to reduce one ConfusionTransposeD operation during the graph fusion phase.

![](../figures/ConfusionTransposeTransDataFusionPass_1.png)

## Constraints

- Only static subgraphs are supported.
- Only the ConfusionTransposeD(NHWC->NCHW) + TransData(NCHW->5HD) scenario is supported.
