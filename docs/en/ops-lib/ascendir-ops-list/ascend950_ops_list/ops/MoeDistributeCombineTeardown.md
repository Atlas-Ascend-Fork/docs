# MoeDistributeCombineTeardown

```c
REG_OP(MoeDistributeCombineTeardown)
    .INPUT(expand_x, TensorType({DT_FLOAT16, DT_BF16}))
    .INPUT(quant_expand_x, TensorType({DT_INT8}))
    .INPUT(expert_ids, TensorType({DT_INT32}))
    .INPUT(expand_idx, TensorType({DT_INT32}))
    .INPUT(expert_scales, TensorType({DT_FLOAT}))
    .INPUT(comm_cmd_info, TensorType({DT_INT32}))
    .OPTIONAL_INPUT(x_active_mask, TensorType({DT_BOOL}))
    .OPTIONAL_INPUT(shared_expert_x, TensorType({DT_FLOAT16, DT_BF16}))
    .OUTPUT(x_out, TensorType({DT_FLOAT16, DT_BF16}))
    .REQUIRED_ATTR(group_ep, String)
    .REQUIRED_ATTR(ep_world_size, Int)
    .REQUIRED_ATTR(ep_rank_id, Int)
    .REQUIRED_ATTR(moe_expert_num, Int)
    .ATTR(expert_shard_type, Int, 0)
    .ATTR(shared_expert_num, Int, 1)
    .ATTR(shared_expert_rank_num, Int, 0)
    .ATTR(global_bs, Int, 0)
    .ATTR(comm_quant_mode, Int, 0)
    .ATTR(comm_type, Int, 0)
    .ATTR(comm_alg, String, "")
    .OP_END_FACTORY_REG(MoeDistributeCombineTeardown)
```

## Brief

MoeDistributeCombineTeardown operator interface implementation.

## Inputs

Eight inputs, including:
- expand_x: A tensor. Support dtype: float16, bfloat16, dimension must be 2, Support Shape: (A, H), support format:
ND.
- quant_expand_x: A tensor. Support dtype: int8, dimension must be 2, Support Shape: (A, tokenMsgSize), support
format: ND.
- expert_ids: A tensor. Support dtype: int32, dimension must be 2, Support Shape: (BS, K), support format: ND.
- expand_idx: A tensor. Support dtype: int32, dimension must be 1, Support Shape: (BS * K, ), support format: ND.
- expert_scales: A tensor. Support dtype: float32, dimension must be 2, Support Shape: (BS, K), support format: ND.
- comm_cmd_info: A tensor. Support dtype: int32, dimension must be 1, Call the
`aclnnMoeDistributeCombineSetupTeardownCalcOutputSize` API to obtain the Shape, support format: ND.
- x_active_mask: An optional tensor. Support dtype: bool, dimension must be 1, Support Shape: (BS, ) support
format: ND.
- shared_expert_x: An optional tensor. Dtype should be same with expand_x, dimension must be 2 or 3, Support Shape:
(BS, H) or (a, b, H), where a * b = BS, support format: ND.

## Outputs

One outputs, including:
- x_out: A tensor. Result of combine. Dtype should be same with expand_x, Support Shape: (BS, H), support format:
ND.

## Attributes

- group_ep: Input ep comm group name, ep means experts parallelism, dtype: String.
- ep_world_size: Input ep comm world size, dtype: Int64.
- ep_rank_id: Input ep comm rank Id, dtype: Int64.
- moe_expert_num: Input moe expert num, dtype: Int64.
- expert_shard_type: Input moe shard type, dtype: Int64. Default: 0.
- shared_expert_num: Input shared expert num, dtype: Int64. Default: 1.
- shared_expert_rank_num: Input shared expert rank num, dtype: Int64. Default: 0.
- global_bs: Input global batch size, dtype: Int64. Default: 0.
- comm_quant_mode: communication quantization mode, 1 for enable, 0 for disable, dtype: Int64. Default: 0.
- comm_type: type of communication, dtype: Int64. Default: 0.
- comm_alg: Input comm alg type, dtype: String. Default: "".

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 expand_x: bfloat16,float16
- input1 quant_expand_x: int8
- input2 expert_ids: int32
- input3 expand_idx: int32
- input4 expert_scales: float32
- input5 comm_cmd_info: int32
- input6 x_active_mask: bool
- input7 shared_expert_x: bfloat16,float16


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
