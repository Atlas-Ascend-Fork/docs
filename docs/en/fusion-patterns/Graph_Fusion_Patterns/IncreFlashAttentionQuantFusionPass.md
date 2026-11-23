# IncreFlashAttentionQuantFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:46:57.585Z pushedAt=2026-11-16T06:27:04.328Z nl=2 -->

## Description

Fuses IncreFlashAttention+AscendQuant into the IncreFlashAttention operator in the quantization scenario. The `scale` and `offset` parameters of `quant` are converted into the input parameters `quant_scale2` and `quant_offset2` of `ifa`.

![](../figures/IncreFlashAttentionQuantFusionPass_1.png)

## Constraints

- The output of IncreFlashAttention must be fp16.
- The input of AscendQuant must be fp16, and the output must be int8.
- `quant_scale2` and `quant_offset2` of the IncreFlashAttention operator must be empty.
- The IncreFlashAttention operator can have only one output.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->

<!-- npu="A3" id2 -->
Atlas A3 products
<!-- end id2 -->
