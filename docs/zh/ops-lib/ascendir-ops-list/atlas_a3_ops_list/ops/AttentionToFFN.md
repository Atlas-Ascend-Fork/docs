# AttentionToFFN

```c
REG_OP(AttentionToFFN)
    .INPUT(x, TensorType({DT_FLOAT16, DT_BF16}))
    .INPUT(session_id, TensorType({DT_INT32}))
    .INPUT(micro_batch_id, TensorType({DT_INT32}))
    .INPUT(layer_id, TensorType({DT_INT32}))
    .INPUT(expert_ids, TensorType({DT_INT32}))
    .INPUT(expert_rank_table, TensorType({DT_INT32}))
    .OPTIONAL_INPUT(scales, TensorType({DT_FLOAT32}))
    .OPTIONAL_INPUT(active_mask, TensorType({DT_BOOL}))
    .REQUIRED_ATTR(group, String)
    .REQUIRED_ATTR(world_size, Int)
    .REQUIRED_ATTR(ffn_token_info_table_shape, ListInt)
    .REQUIRED_ATTR(ffn_token_data_shape, ListInt)
    .REQUIRED_ATTR(attn_token_info_table_shape, ListInt)
    .REQUIRED_ATTR(moe_expert_num, Int)
    .ATTR(quant_mode, Int, 0)
    .ATTR(sync_flag, Int, 0)
    .ATTR(ffn_start_rank_id, Int, 0)
    .OP_END_FACTORY_REG(AttentionToFFN)
```

## Brief

Fusion op AttentionToFFN.

## Inputs

- x:
- session_id:
- micro_batch_id:
- layer_id:
- expert_ids:
- expert_rank_table:
- scales:
- active_mask:

## Attributes

- group:
- world_size:
- quant_mode:
- expert_tokens_cnt_flag_len:

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x: bfloat16,float16
- input1 session_id: int32
- input2 micro_batch_id: int32
- input3 layer_id: int32
- input4 expert_ids: int32
- input5 expert_rank_table: int32
- input6 scales: float32
- input7 active_mask: bool


---

[Back to Operator Specifications (Atlas A3 products)](../README.md)
