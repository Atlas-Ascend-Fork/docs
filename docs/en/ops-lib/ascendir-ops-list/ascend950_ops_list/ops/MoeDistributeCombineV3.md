# MoeDistributeCombineV3

```c
REG_OP(MoeDistributeCombineV3)
    .INPUT(context, TensorType({DT_INT32}))
    .INPUT(expand_x, TensorType({DT_BF16, DT_FLOAT16, DT_INT32}))
    .INPUT(expert_ids, TensorType({DT_INT32}))
    .INPUT(assist_info_for_combine, TensorType({DT_INT32}))
    .INPUT(ep_send_counts, TensorType({DT_INT32}))
    .INPUT(expert_scales, TensorType({DT_FLOAT}))
    .OPTIONAL_INPUT(tp_send_counts, TensorType({DT_INT32}))
    .OPTIONAL_INPUT(x_active_mask, TensorType({DT_BOOL}))
    .OPTIONAL_INPUT(activation_scale, TensorType({DT_FLOAT}))
    .OPTIONAL_INPUT(weight_scale, TensorType({DT_FLOAT}))
    .OPTIONAL_INPUT(group_list, TensorType({DT_INT64}))
    .OPTIONAL_INPUT(expand_scales, TensorType({DT_FLOAT}))
    .OPTIONAL_INPUT(shared_expert_x, TensorType({DT_BF16, DT_FLOAT16, DT_INT32}))
    .OPTIONAL_INPUT(elastic_info, TensorType({DT_INT32}))
    .OPTIONAL_INPUT(ori_x, TensorType({DT_BF16, DT_FLOAT16, DT_INT32}))
    .OPTIONAL_INPUT(const_expert_alpha_1, TensorType({DT_BF16, DT_FLOAT16, DT_INT32}))
    .OPTIONAL_INPUT(const_expert_alpha_2, TensorType({DT_BF16, DT_FLOAT16, DT_INT32}))
    .OPTIONAL_INPUT(const_expert_v, TensorType({DT_BF16, DT_FLOAT16, DT_INT32}))
    .OPTIONAL_INPUT(performance_info, TensorType({DT_INT64}))
    .OUTPUT(x, TensorType({DT_BF16, DT_FLOAT16}))
    .REQUIRED_ATTR(ep_world_size, Int)
    .REQUIRED_ATTR(ep_rank_id, Int)
    .REQUIRED_ATTR(moe_expert_num, Int)
    .REQUIRED_ATTR(ccl_buffer_size, Int)
    .ATTR(tp_world_size, Int, 0)
    .ATTR(tp_rank_id, Int, 0)
    .ATTR(expert_shard_type, Int, 0)
    .ATTR(shared_expert_num, Int, 1)
    .ATTR(shared_expert_rank_num, Int, 0)
    .ATTR(global_bs, Int, 0)
    .ATTR(out_dtype, Int, 0)
    .ATTR(comm_quant_mode, Int, 0)
    .ATTR(group_list_type, Int, 0)
    .ATTR(comm_alg, String, "")
    .ATTR(zero_expert_num, Int, 0)
    .ATTR(copy_expert_num, Int, 0)
    .ATTR(const_expert_num, Int, 0)
    .OP_END_FACTORY_REG(MoeDistributeCombineV3)
```

## Brief

MoeDistributeCombineV3 operator interface implementation.

## Inputs

- context: A tensor. Support dtype: int32, dimension must be 1, Support Shape (2052, ), support format: ND.
- expand_x: A tensor. Support dtype: float16, bfloat16, int32, dimension must be 2, Support Shape: (A * world_size,
H), support format: ND.
- expert_ids: A tensor. Support dtype: int32, dimension must be 2, Support Shape: (BS, K), support format: ND.
- assist_info_for_combine: A tensor. Support dtype: int32, dimension must be 1, Support Shape: (A * 128), support
format: ND.
- ep_send_counts: A tensor. Support dtype: int32, Support Shape: (moe_expert_num + 2 * globalBs * K * server_num, ),
where sever_num is num of host server used. support format: ND.
- expert_scales: A tensor. Support dtype: float32, Support Shape: (BS, K), support format: ND.
- tp_send_counts: A tensor. Support dtype: int32, Support Shape: (Bs, K), support format: ND.
- x_active_mask: An optional tensor. Support dtype: bool, Support Shape: (Bs, ) or (Bs, K), support format: ND.
- activation_scale: An optional tensor. Support dtype: float32, support format: ND.
- weight_scale: An optional tensor. Support dtype: float32, Support Shape: (A, ), support format: ND.
- group_list: An optional tensor. Support dtype: int64, support format: ND.
- expand_scales: A tensor. Support dtype: float32, Support Shape: (A, ), support format: ND.
- shared_expert_x: A tensor. Support dtype: float16, bfloat16, int32, Support Shape: (Bs, H) or (dim0, dim1,
H）where dim0 * dim1 equal to Bs, support format: ND.
- elastic_info: An optional tensor. Support dtype: int32, Support Shape: (4 + 2 * ep_world_size, ) support format:
ND.
- ori_x: A tensor, reserved. Support dtype: float16, bfloat16, int32, support format: ND.
- const_expert_alpha_1: A tensor, reserved. Support dtype: float16, bfloat16, int32, support format: ND.
- const_expert_alpha_2: A tensor, reserved. Support dtype: float16, bfloat16, int32, support format: ND.
- const_expert_v : A tensor, reserved. Support dtype: float16, bfloat16, int32, support format : ND.
- performance_info: A tensor. Support dtype: int64, Support Shape: (ep_world_size) support format: ND.

## Outputs

One outputs, including:
x: A tensor. Result of combine. Support dtype: float16,bfloat16,  Support Shape: (BS, H), support format: ND.

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
- global_bs: Input global batch size, dtype: int64. The options are : 0 or (Bs * ep_world_size) when Bs is uniform
across ranks; (maxBs * ep_world_size) when Bs is different across ranks, maxBs is the largest possible Bs. Default: 0.
- out_dtype: Dtype of output, 0 for bfloat16, 1 for float16, dtype: Int64.
- comm_quant_mode: Communication quantization mode, 1 for enable, 0 for disable, dtype: Int64.
- group_list_type: Type of input group_list, dtype: Int64.
- comm_alg: Input comm alg type, dtype: String. Support: (nullptr, "fullmesh_v1", "fullmesh_v2"). Default: "".
- zero_expert_num: Input zero expert num, dtype: int64. Support Range: [0, MAX_INT32)，MAX_INT32 = 2^31 - 1.
Default: 0.
- copy_expert_num: Input copy expert num, dtype: int64. Support Range: [0, MAX_INT32)，MAX_INT32 = 2^31 - 1,
Default: 0.
- const_expert_num: Input const expert num, dtype: int64. Support: 0, Default: 0.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 context: int32
- input1 expand_x: bfloat16,float16,int32
- input2 expert_ids: int32
- input3 assist_info_for_combine: int32
- input4 ep_send_counts: int32
- input5 expert_scales: float32
- input6 tp_send_counts: int32
- input7 x_active_mask: bool
- input8 activation_scale: float32
- input9 weight_scale: float32
- input10 group_list: int64
- input11 expand_scales: float32
- input12 shared_expert_x: bfloat16,float16,int32
- input13 elastic_info: int32
- input14 ori_x: bfloat16,float16,int32
- input15 const_expert_alpha_1: bfloat16,float16,int32
- input16 const_expert_alpha_2: bfloat16,float16,int32
- input17 const_expert_v: bfloat16,float16,int32
- input18 performance_info: int64
- output0 x: bfloat16,float16


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
