# MoeReRoutingV2

```c
REG_OP(MoeReRoutingV2)
    .INPUT(tokens, TensorType({DT_FLOAT16, DT_BF16, DT_INT8, DT_FLOAT8_E5M2, DT_FLOAT8_E4M3FN, DT_HIFLOAT8,
                               DT_FLOAT4_E2M1, DT_FLOAT4_E1M2}))
    .INPUT(expert_token_num_per_rank, TensorType({DT_INT32, DT_INT64}))
    .OPTIONAL_INPUT(per_token_scales, TensorType({DT_FLOAT, DT_FLOAT8_E8M0}))
    .OPTIONAL_INPUT(expert_topk_weight, TensorType({DT_FLOAT}))
    .OUTPUT(permute_tokens, TensorType({DT_FLOAT16, DT_BF16, DT_INT8, DT_FLOAT8_E5M2, DT_FLOAT8_E4M3FN, DT_HIFLOAT8,
                                        DT_FLOAT4_E2M1, DT_FLOAT4_E1M2}))
    .OUTPUT(permute_per_token_scales, TensorType({DT_FLOAT, DT_FLOAT8_E8M0}))
    .OUTPUT(permute_token_idx, TensorType({DT_INT32}))
    .OUTPUT(expert_token_num, TensorType({DT_INT32, DT_INT64}))
    .OUTPUT(permute_topk_weight, TensorType({DT_FLOAT}))
    .ATTR(expert_token_num_type, Int, 1)
    .ATTR(idx_type, Int, 0)
    .OP_END_FACTORY_REG(MoeReRoutingV2)
```

## Brief

Rearrange tokens from rank order to expert order, and optionally rearrange topk weight

## Inputs

- tokens: A 2D tensor, represents tokens in rank-order. Type is BFloat16, Float16, DT_FLOAT8_E5M2,
DT_FLOAT8_E4M3FN, Int8, DT_HIFLOAT8, DT_FLOAT4_E2M1 or DT_FLOAT4_E1M2. Shape supports (A, H). Format supports ND.
- expert_token_num_per_rank: A 2D tensor, represents numbers of tokens belong to an expert on specific rank.
Type is Int32 or Int64. Shape supports (N, E). Format supports ND.
- per_token_scales: A 1D, 2D or 3D tensor, optional, represents tokens scale in rank-order.
Type is Float32, DT_FLOAT8_E8M0.
Shape supports (A), (A,S) or (A,K/64,2). Format supports ND. If tokens is FLOAT8,
per_token_scales must be DT_FLOAT8_E8M0.
Ascend 950PR&950DT products support 1D, 2D or 3D (3D only for FP8 tokens).
- expert_topk_weight: A 2D tensor, optional, represents topk weight of each token in rank-order.
Type is Float32. Shape supports (A, 1). Format supports ND. Must be used together with
permute_topk_weight: either both provided or neither.

## Outputs

- permute_tokens: A 2D tensor, represents tokens in expert-order. Type is BFloat16, Float16,
Int8, DT_FLOAT8_E5M2, DT_FLOAT8_E4M3FN, DT_HIFLOAT8, DT_FLOAT4_E2M1 or DT_FLOAT4_E1M2. Shape supports (A, H).
Format supports ND.
- permute_per_token_scales: A 1D, 2D or 3D tensor, represents tokens scale in expert-order.
Type is Float32, DT_FLOAT8_E8M0. Shape supports (A), (A,S) or (A,K/64,2). Format supports ND.
Ascend 950PR&950DT products support 1D, 2D or 3D (3D only for FP8 tokens).
- permute_token_idx: A 1D tensor, represents token idx in rank-order. Type is Int32.
Shape supports (A). Format supports ND.
- expert_token_num: A 1D tensor, represents tokens nums of experts. Type is Int32 or Int64.
Shape supports (E). Format supports ND.
- permute_topk_weight: A 2D tensor, optional, represents topk weight in expert-order, corresponds
one-to-one with permute_tokens. Type is Float32. Shape supports (A, 1). Format supports ND.
Must be used together with expert_topk_weight: either both provided or neither.

## Attributes

- expert_token_num_type: Optional integer, represents the cumsum or count mode. Type is Int. Default: 1. Value
supports 0-cumsum or 1-count, currently only supports "1".
- idx_type: Optional integer, represents the gather or scatter index. Type is Int. Default: 0. Value
supports 0-gather idx or 1-scatter idx. Ascend 950PR&950DT products support "0" or "1".

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 tokens: bfloat16,float4_e1m2,float4_e2m1,float8_e4m3fn,float8_e5m2,float16,hifloat8,int8
- input1 expert_token_num_per_rank: int32,int64
- input2 per_token_scales: float8_e8m0,float32
- input3 expert_topk_weight: float32
- output0 permute_tokens: bfloat16,float4_e1m2,float4_e2m1,float8_e4m3fn,float8_e5m2,float16,hifloat8,int8
- output1 permute_per_token_scales: float8_e8m0,float32
- output2 permute_token_idx: int32
- output3 expert_token_num: int32,int64
- output4 permute_topk_weight: float32


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
