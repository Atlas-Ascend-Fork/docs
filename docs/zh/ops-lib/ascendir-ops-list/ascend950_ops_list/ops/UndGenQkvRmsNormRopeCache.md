# UndGenQkvRmsNormRopeCache

```c
REG_OP(UndGenQkvRmsNormRopeCache)
    .INPUT(und_qkv, TensorType({DT_BF16}))
    .INPUT(und_weights_q, TensorType({DT_BF16}))
    .INPUT(und_weights_k, TensorType({DT_BF16}))
    .INPUT(cos_sin_cache, TensorType({DT_FLOAT}))
    .INPUT(k_cache, TensorType({DT_BF16}))
    .INPUT(v_cache, TensorType({DT_BF16}))
    .INPUT(slot_mapping, TensorType({DT_INT64}))
    .INPUT(positions, TensorType({DT_INT64}))
    .OPTIONAL_INPUT(gen_qkv, TensorType({DT_BF16}))
    .OPTIONAL_INPUT(gen_weights_q, TensorType({DT_BF16}))
    .OPTIONAL_INPUT(gen_weights_k, TensorType({DT_BF16}))
    .OPTIONAL_INPUT(cat_indices, TensorType({DT_INT64}))
    .OUTPUT(q, TensorType({DT_BF16}))
    .OUTPUT(k_cache, TensorType({DT_BF16}))
    .OUTPUT(v_cache, TensorType({DT_BF16}))
    .REQUIRED_ATTR(num_heads_q, Int)
    .REQUIRED_ATTR(num_heads_k, Int)
    .REQUIRED_ATTR(num_heads_v, Int)
    .ATTR(norm_eps, Float, 1e-6f)
    .ATTR(mrope_section, ListInt, {})
    .OP_END_FACTORY_REG(UndGenQkvRmsNormRopeCache)
```

## Brief

Fused QKV pre-processing for multimodal inference: concatenates the undecoded and generated QKV
segments through cat_indices, applies RMSNorm and MRoPE on Q and K per token, outputs Q and scatters
K/V into the paged KV cache according to slot_mapping.

## Inputs

Twelve inputs, including:
- und_qkv: A tensor, support BF16, shape [und_len, N, D], N = Hq + Hk + Hv.
- und_weights_q: A tensor, support BF16, shape [D], the RMSNorm weight of Q for the undecoded segment.
- und_weights_k: A tensor, support BF16, shape [D], the RMSNorm weight of K for the undecoded segment.
- cos_sin_cache: A tensor, support FP32, shape [max_pos, D], the first D/2 columns are cos and
the last D/2 columns are sin.
- k_cache: A tensor, support BF16, shape [Bn, Bs, Hk, D], the paged KV cache of K, updated in place.
- v_cache: A tensor, support BF16, shape [Bn, Bs, Hv, D], the paged KV cache of V, updated in place.
- slot_mapping: A tensor, support INT64, shape [T], slot = block_num * Bs + row_idx.
- positions: A tensor, support INT64, shape [3, T], the time/height/width positions of MRoPE.
- gen_qkv: An optional tensor, support BF16, shape [gen_len, N, D].
- gen_weights_q: An optional tensor, support BF16, shape [D], the RMSNorm weight of Q for the
generated segment.
- gen_weights_k: An optional tensor, support BF16, shape [D], the RMSNorm weight of K for the
generated segment.
- cat_indices: An optional tensor, support INT64, shape [T], maps each output token to its source token.

## Outputs

Three outputs, including:
- q: A tensor, support BF16, shape [T, Hq, D], T = und_len + gen_len.
- k_cache: A tensor, support BF16, shape [Bn, Bs, Hk, D], shares the address with the input k_cache.
- v_cache: A tensor, support BF16, shape [Bn, Bs, Hv, D], shares the address with the input v_cache.

## Attributes

- num_heads_q: A required scalar, the head number of Q.
- num_heads_k: A required scalar, the head number of K.
- num_heads_v: A required scalar, the head number of V.
- norm_eps: An optional scalar, the epsilon of RMSNorm. Defaults to 1e-6.
- mrope_section: An optional scalar list of length 3, the three-axis section of MRoPE.
Defaults to (), which degenerates to the standard RoPE.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 und_qkv: bfloat16
- input1 und_weights_q: bfloat16
- input2 und_weights_k: bfloat16
- input3 cos_sin_cache: float32
- input4 k_cache: bfloat16
- input5 v_cache: bfloat16
- input6 slot_mapping: int64
- input7 positions: int64
- input8 gen_qkv: bfloat16
- input9 gen_weights_q: bfloat16
- input10 gen_weights_k: bfloat16
- input11 cat_indices: int64
- output0 q: bfloat16
- output1 k_cache: bfloat16
- output2 v_cache: bfloat16

## Attention Constraints

- D is fixed to 128, and (num_heads_q, num_heads_k, num_heads_v) supports (8,1,1) and (16,2,2) only.
- k_cache and v_cache must be contiguous, and their capacity must satisfy Bn * Bs >= T.
- The four optional inputs must be either all provided or all absent within one call.


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
