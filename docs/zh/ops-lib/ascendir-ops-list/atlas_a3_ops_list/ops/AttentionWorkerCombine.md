# AttentionWorkerCombine

```c
REG_OP(AttentionWorkerCombine)
		.INPUT(schedule_context, TensorType({DT_INT8}))
		.INPUT(expert_scales, TensorType({DT_FLOAT}))
		.INPUT(layer_id, TensorType({DT_INT32}))
		.OUTPUT(y, TensorType({DT_FLOAT16, DT_BF16}))
		.OUTPUT(next_layer_id, TensorType({DT_INT32}))
		.REQUIRED_ATTR(hidden_size, Int)
		.ATTR(token_dtype, Int, 0)
		.ATTR(need_schedule, Int, 0)
		.OP_END_FACTORY_REG(AttentionWorkerCombine)
```

## Brief

The operator of AttentionWorkerCombine.

## Inputs

- schedule_context: A 1D tensor, represents struct contain token_data. Data type is DT_INT8. Format supports ND.
- expert_scales: A 2D tensor, represents expert scales. Data type is DT_FLOAT32. Shape supports (BS, K). Format supports ND.
- layer_id: A 1D tensor, represents layer id. Data type is DT_INT32. Format supports ND. Shape supports (1,).

## Outputs

- y: A 2D tensor, represents the combine result of token_data and expert scales. Data type is DT_FLOAT16, DT_BF16. Format supports ND. Shape supports (BS, H).
- next_layer_id: A 1D tensor, represents the next layer id. Data type is DT_INT32. Format supports ND. Shape supports (1,).

## Attributes

- hidden_size: Required Int, represents token_data hidden size.
- token_dtype: Int, represents token data type. Value 0 represents token data type is FLOAT16, and value 1 represents BFLOAT16.
- need_schedule: Int, Value 1 represents op waits until tokens are filled.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 schedule_context: int8
- input1 expert_scales: float32
- input2 layer_id: int32
- output0 y: bfloat16,float16
- output1 next_layer_id: int32


---

[Back to Operator Specifications (Atlas A3 products)](../README.md)
