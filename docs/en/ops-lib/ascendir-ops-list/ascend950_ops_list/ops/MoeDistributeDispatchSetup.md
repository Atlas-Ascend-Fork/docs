# MoeDistributeDispatchSetup

```c
REG_OP(MoeDistributeDispatchSetup)
    .INPUT(x, TensorType({DT_BF16, DT_FLOAT16}))
    .INPUT(expert_ids, TensorType({DT_INT32}))
    .OPTIONAL_INPUT(scales, TensorType({DT_FLOAT}))
    .OPTIONAL_INPUT(x_active_mask, TensorType({DT_BOOL}))
    .OUTPUT(y, TensorType({DT_BF16, DT_INT8, DT_FLOAT16}))
    .OUTPUT(expand_idx, TensorType({DT_INT32}))
    .OUTPUT(comm_cmd_info, TensorType({DT_INT32}))
    .REQUIRED_ATTR(group_ep, String)
    .REQUIRED_ATTR(ep_world_size, Int)
    .REQUIRED_ATTR(ep_rank_id, Int)
    .REQUIRED_ATTR(moe_expert_num, Int)
    .ATTR(expert_shard_type, Int, 0)
    .ATTR(shared_expert_num, Int, 1)
    .ATTR(shared_expert_rank_num, Int, 0)
    .ATTR(quant_mode, Int, 0)
    .ATTR(global_bs, Int, 0)
    .ATTR(comm_type, Int, 0)
    .ATTR(comm_alg, String, "")
    .OP_END_FACTORY_REG(MoeDistributeDispatchSetup)
```

## Brief

MoeDistributeDispatchSetup operator interface implementation.

## Inputs

Four inputs, including:
- x: A tensor. Support dtype: float16, bfloat16, dimension must be 2. Shape supports (BS, H), support format: ND.
- expert_ids: A tensor. Support dtype: int32, indicates top k experts of each token, dimension must be 2. Shape
supports (BS, K), support format: ND.
- scales: An optional tensor. Support dtype: float32, dimension must be 2. Shape supports (sharedExpertNum +
moeExpertNum, H)， support format: ND. In non-quantization scenario, the value in scales is nullptr. In dynamic
quantization scenario, the value in scales is nullptr or valid data (indicating the quantization smoothing parameter of
each expert).
- x_active_mask: An optional tensor. Support dtype: bool. Shape supports (BS, ), support format: ND.
The value in x_active_mask can be valid data or nullptr. If the value is nullptr, all tokens participate in
communication. If the value is valid data, tokens where x_active_mask is true participate in communication.

## Outputs

Three outputs, including:
- y: A tensor. Support dtype: float16, bfloat16, int8. Shape supports (BS * K, ), support format: ND.
- expand_idx: A tensor. Support dtype: int32. Shape supports (BS * K, ), support format: ND.
- comm_cmd_info: A tensor. Support dtype: int32. Shape supports (BS * K, ), support format: ND.

## Attributes

- group_ep: Required. Input ep comm group name, ep means experts parallelism. The string length range: [1, 128),
dtype: String.
- ep_world_size: Required. Input ep comm world size, value range: [2, 384], dtype: int64.
- ep_rank_id: Required. Input ep comm rank Id, value range: [0, epWorldSize), dtype: int64.
- moe_expert_num: Required. Input moe expert num, value range: (0, 512] and must satisfy moeExpertNum % (epWorldSize
- SharedExpertRankNum) = 0, dtype: int64.
- expert_shard_type: The shard type of shared expert rank. Only 0 (the shared expert rank is placed before moe
expert rank) is supported currently, dtype: int64. Default: 0.
- shared_expert_num: Input shared expert num, value range: [0, 4], dtype: int64. Default: 1.
- shared_expert_rank_num: Input shared expert rank num, value range: [0, epWorldSize / 2], dtype: int64. Default: 0.
- quant_mode: Input quant mode. The options are 0 (non-quantization), and 2 (dynamic quantization). dtype: int64.
Default: 0.
- global_bs: Input global batch size, dtype: int64. Default: 0.
When the number of Bs at each rank is the same, globalBs = Bs * epWorldSize or globalBs = 0. When the number of Bs at
each rank is different, globalBs = maxBs * epWorldSize.
- comm_type: Communication scheme selection. The options are 0 (AICPU-SDMA), 1 (CCU), and 2 (URMA), only 0 is
supported currently. dtype: int64. Default: 0.
- comm_alg: Communication affinity and memory layout algorithm. Only nullptr is supported currently. dtype: String.
Default: "".

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x: bfloat16,float16
- input1 expert_ids: int32
- input2 scales: float32
- input3 x_active_mask: bool
- output0 y: bfloat16,float8_e4m3fn,float8_e5m2,float16,hifloat8,int8
- output1 expand_idx: int32
- output2 comm_cmd_info: int32


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
