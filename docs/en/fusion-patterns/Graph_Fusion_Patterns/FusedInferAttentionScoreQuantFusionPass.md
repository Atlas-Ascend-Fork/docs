# FusedInferAttentionScoreQuantFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:47:10.946Z pushedAt=2026-10-15T12:44:18.341Z -->

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
