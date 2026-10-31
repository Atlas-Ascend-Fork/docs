# MoeDistributeDispatchV3

```c
REG_OP(MoeDistributeDispatchV3)
    .INPUT(context, TensorType({DT_INT32}))
    .INPUT(x, TensorType({DT_BF16, DT_FLOAT16}))
    .INPUT(expert_ids, TensorType({DT_INT32}))
    .OPTIONAL_INPUT(scales, TensorType({DT_FLOAT}))
    .OPTIONAL_INPUT(x_active_mask, TensorType({DT_BOOL}))
    .OPTIONAL_INPUT(expert_scales, TensorType({DT_FLOAT}))
    .OPTIONAL_INPUT(elastic_info, TensorType({DT_INT32}))
    .OPTIONAL_INPUT(performance_info, TensorType({DT_INT64}))
    .OUTPUT(expand_x, TensorType({DT_BF16, DT_INT8, DT_FLOAT16, DT_FLOAT8_E5M2, DT_FLOAT8_E4M3FN, DT_HIFLOAT8}))
    .OUTPUT(dynamic_scales, TensorType({DT_FLOAT, DT_FLOAT8_E8M0}))
    .OUTPUT(assist_info_for_combine, TensorType({DT_INT32}))
    .OUTPUT(expert_token_nums, TensorType({DT_INT64}))
    .OUTPUT(ep_recv_count, TensorType({DT_INT32}))
    .OUTPUT(tp_recv_count, TensorType({DT_INT32}))
    .OUTPUT(expand_scales, TensorType({DT_FLOAT}))
    .REQUIRED_ATTR(ep_world_size, Int)
    .REQUIRED_ATTR(ep_rank_id, Int)
    .REQUIRED_ATTR(moe_expert_num, Int)
    .REQUIRED_ATTR(ccl_buffer_size, Int)
    .ATTR(tp_world_size, Int, 0)
    .ATTR(tp_rank_id, Int, 0)
    .ATTR(expert_shard_type, Int, 0)
    .ATTR(shared_expert_num, Int, 1)
    .ATTR(shared_expert_rank_num, Int, 0)
    .ATTR(quant_mode, Int, 0)
    .ATTR(global_bs, Int, 0)
    .ATTR(expert_token_nums_type, Int, 1)
    .ATTR(comm_alg, String, "")
    .ATTR(zero_expert_num, Int, 0)
    .ATTR(copy_expert_num, Int, 0)
    .ATTR(const_expert_num, Int, 0)
    .ATTR(y_dtype, Int, 28)
    .OP_END_FACTORY_REG(MoeDistributeDispatchV3)
```

## Brief

MoeDistributeDispatchV3 operator interface implementation.

## Inputs

- context: A tensor. Support dtype: int32, dimension must be 1. Shape supports (2052, ), support format: ND.
- x: A tensor. Support dtype: float16,bfloat16, dimension must be 2. Shape supports (BS, H), support format: ND.
- expertIds: A tensor. Support dtype: int32, indicates top k experts of each token, dimension must be 2. Shape
supports (BS, K), support format: ND.
- scales: An optional tensor. Support dtype: float32, dimension must be 2, support format: ND.
- x_active_mask: An optional tensor. Support dtype: bool, Support Shape: (Bs, ) or (Bs, K), support format: ND.
- expert_scales: An optional tensor. Support dtype: float32. Shape supports (BS, K), support format: ND.
- elastic_info: An optional tensor. Support dtype: int32, Support Shape: (4 + 2 * ep_world_size, ) support format:
ND.
- performance_info: An optional tensor. Support dtype: int64, Support Shape: (ep_world_size) support format: ND.

## Outputs

Seven outputs, including:
- expand_x: A tensor. Result of each expert after dispatching. Support dtype:
float16,bfloat16,int8,float8_e4m3,float8_e5m2，hifloat8. Shape supports (A, H), support format: ND.
- dynamic_scales: If quant is enabled, scale value of each token. A tensor. Support dtype: float32,float8_e8m0.
Shape supports (A, ), support format: ND.
- assist_info_for_combine: A tensor. Support dtype: int32. Shape supports (A * 128), support format: ND.
- expert_token_nums: A tensor. Tokens nums of expand_x. Support dtype: int64, support format: ND.
- ep_recv_count: A tensor. Received token nums after dispatching. Support dtype: int32, support format: ND.
- tp_recv_count: A tensor. Received token nums after allgather. Support dtype: int32, support format: ND.
- expand_scales: A tensor. Scales of each token to sum for combine. Support dtype: float32. Shape supports (A, ),
support format: ND.

## Attributes

- ep_world_size: Required. Input ep comm world size, Support Range: [2, 768], dtype: int64.
- ep_rank_id: Required. Input ep comm rank Id, dtype: int64.
- moe_expert_num: Required. Input moe expert num, Support Range: (0, 1024], dtype: int64.
- ccl_buffer_size: Required, Input ccl buffer size, Support Range: [0, MAX_INT32)，MAX_INT32 = 2^31 - 1, dtype:
Int64.
- tp_world_size: Input tp comm world size, dtype: int64. Support Range: [0, 2], Default: 0.
- tp_rank_id: Input tp comm rank Id, dtype: int64. Support Range: [0, 2], Default: 0.
- expert_shard_type: Input moe shard type, dtype: int64. Support Range: [0], Default: 0.
- shared_expert_num: Input shared expert num, dtype: int64. Support Range: [0, 4], Default: 0.
- shared_expert_rank_num: Input shared expert rank num, dtype: int64. Support Range: [0, ep_world_size), Default: 0.
- quant_mode: Input quant mode. The options are 0 (non-quantization), 1 (static quantization), and 2 (dynamic
quantization). dtype: int64.
- global_bs: Input global batch size, dtype: int64. The options are : 0 or (Bs * ep_world_size) when Bs is uniform
across ranks; (maxBs * ep_world_size) when Bs is different across ranks, maxBs is the largest possible Bs. Default: 0.
- expert_token_nums_type: Input expert token nums type, dtype: int64. Support:0, Default: 0.
- comm_alg: Input comm alg type, dtype: String. Support: ("", "fullmesh_v1", "fullmesh_v2"). Default: "".
- zero_expert_num: Input zero expert num, dtype: int64. Support Range: [0, MAX_INT32)，MAX_INT32 = 2^31 - 1.
Default: 0.
- copy_expert_num: Input copy expert num, dtype: int64. Support Range: [0, MAX_INT32)，MAX_INT32 = 2^31 - 1,
Default: 0.
- const_expert_num: Input const expert num, dtype: int64. Support: 0, Default: 0.
- y_dtype: Input y dtype, dtype: int64. Support: 28, Default: 28.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 context: int32
- input1 x: bfloat16,float4_e1m2,float4_e2m1,float8_e4m3fn,float8_e5m2,float16,hifloat8
- input2 expert_ids: int32
- input3 scales: float8_e8m0,float32
- input4 x_active_mask: bool
- input5 expert_scales: float32
- input6 elastic_info: int32
- input7 performance_info: int64
- output0 expand_x: bfloat16,float4_e1m2,float4_e2m1,float8_e4m3fn,float8_e5m2,float16,hifloat8,int8
- output1 dynamic_scales: float8_e8m0,float32
- output2 assist_info_for_combine: int32
- output3 expert_token_nums: int64
- output4 ep_recv_count: int32
- output5 tp_recv_count: int32
- output6 expand_scales: float32


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
