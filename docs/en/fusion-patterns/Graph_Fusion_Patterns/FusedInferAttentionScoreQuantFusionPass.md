# FusedInferAttentionScoreQuantFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:46:19.142Z pushedAt=2026-11-16T06:27:04.319Z nl=2 -->

## Description

Fuses FusedInferAttentionScore+AscendQuant into the FusedInferAttentionScore operator in quantization use cases. The `scale` and `offset` parameters of `quant` are converted into the input parameters `quant_scale2` and `quant_offset2` of FIA.

![](../figures/FusedInferAttentionScoreQuantFusionPass_1.png)

## Constraints

- FusedInferAttentionScore supports only fp16 output.
- AscendQuant supports only fp16 input and int8 output.
- `quant_scale2` and `quant_offset2` of the FusedInferAttentionScore operator must be empty.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->

<!-- npu="A3" id2 -->
Atlas A3 products
<!-- end id2 -->
