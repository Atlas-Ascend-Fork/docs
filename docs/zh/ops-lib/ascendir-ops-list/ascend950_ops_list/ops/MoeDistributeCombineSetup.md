# MoeDistributeCombineSetup

```c
REG_OP(MoeDistributeCombineSetup)
    .INPUT(expand_x, TensorType({DT_BF16, DT_FLOAT16}))
    .INPUT(expert_ids, TensorType({DT_INT32}))
    .INPUT(assist_info_for_combine, TensorType({DT_INT32}))
    .OUTPUT(quant_expand_x, TensorType({DT_INT8}))
    .OUTPUT(comm_cmd_info, TensorType({DT_INT32}))
    .REQUIRED_ATTR(group_ep, String)
    .REQUIRED_ATTR(ep_world_size, Int)
    .REQUIRED_ATTR(ep_rank_id, Int)
    .REQUIRED_ATTR(moe_expert_num, Int)
    .ATTR(expert_shard_type, Int, 0)
    .ATTR(shared_expert_num, Int, 1)
    .ATTR(shared_expert_rank_num, Int, 0)
    .ATTR(comm_quant_mode, Int, 0)
    .ATTR(global_bs, Int, 0)
    .ATTR(comm_type, Int, 0)
    .ATTR(comm_alg, String, "")
    .OP_END_FACTORY_REG(MoeDistributeCombineSetup)
```

## Brief

MoeDistributeCombineSetup operator interface implementation.

## Inputs

Three inputs, including:
- expand_x: A tensor. Support dtype: float16, bfloat16, dimension must be 2. Shape supports (A, H), support format:
ND.
- expert_ids: A tensor. Support dtype: int32, indicates top k experts of each token, dimension must be 2. Shape
supports (BS, K), support format: ND.
- assist_info_for_combine: A tensor. Support dtype: int32, dimension must be 1. Shape supports (N, ), support
format: ND.

## Outputs

Two outputs, including:
- quant_expand_x: A tensor. Result of quantized expand_x. Support dtype: int8, dimension must be 2. Shape supports
(A, H), support format: ND.
- comm_cmd_info: A tensor. Communication command info. Support dtype: int32, dimension must be 1. Shape supports
(N, ), support format: ND.

## Attributes

- group_ep: Required. Input ep comm group name, ep means experts parallelism, dtype: String.
- ep_world_size: Required. Input ep comm world size, dtype: int64.
- ep_rank_id: Required. Input ep comm rank Id, dtype: int64.
- moe_expert_num: Required. Input moe expert num, dtype: int64.
- expert_shard_type: Input moe shard type, dtype: int64. Default: 0.
- shared_expert_num: Input shared expert num, dtype: int64. Default: 1.
- shared_expert_rank_num: Input shared expert rank num, dtype: int64. Default: 0.
- comm_quant_mode: Input quant mode. The options are 0 (non-quantization), 1 (static quantization), and 2 (dynamic
quantization). dtype: int64. Default: 0.
- global_bs: Input global batch size, dtype: int64. Default: 0.
- comm_type: Input comm type, dtype: int64. Default: 0.
- comm_alg: Input comm algorithm, dtype: String. Default: "".

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 expand_x: bfloat16,float16
- input1 expert_ids: int32
- input2 assist_info_for_combine: int32
- output0 quant_expand_x: int8
- output1 comm_cmd_info: int32


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
