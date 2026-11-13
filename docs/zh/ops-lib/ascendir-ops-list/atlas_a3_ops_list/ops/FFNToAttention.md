# FFNToAttention

```c
REG_OP(FFNToAttention)
    .INPUT(x, TensorType({DT_FLOAT16, DT_BF16}))
    .INPUT(session_ids, TensorType({DT_INT32}))
    .INPUT(micro_batch_ids, TensorType({DT_INT32}))
    .INPUT(token_ids, TensorType({DT_INT32}))
    .INPUT(expert_offsets, TensorType({DT_INT32}))
    .INPUT(actual_token_num, TensorType({DT_INT64}))
    .OPTIONAL_INPUT(attn_rank_table, TensorType({DT_INT32}))
    .REQUIRED_ATTR(group, String)
    .REQUIRED_ATTR(world_size, Int)
    .REQUIRED_ATTR(token_info_table_shape, ListInt)
    .REQUIRED_ATTR(token_data_shape, ListInt)
    .OP_END_FACTORY_REG(FFNToAttention)
```

## Brief

Fusion op FFNToAttention.

## Inputs

- x:
- session_ids:
- micro_batch_ids:
- token_ids:
- expert_offsets:
- attn_rank_table:

## Attributes

- group:
- world_size:
- quant_mode:
- expert_tokens_cnt_flag_len:

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x: bfloat16,float16
- input1 session_ids: int32
- input2 micro_batch_ids: int32
- input3 token_ids: int32
- input4 expert_offsets: int32
- input5 actual_token_num: int64
- input6 attn_rank_table: int32


---

[Back to Operator Specifications (Atlas A3 products)](../README.md)
