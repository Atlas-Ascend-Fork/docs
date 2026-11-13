# FusedCausalConv1d

```c
REG_OP(FusedCausalConv1d)
    .INPUT(x, TensorType({DT_BF16, DT_FLOAT16}))
    .INPUT(weight, TensorType({DT_BF16, DT_FLOAT16}))
    .INPUT(conv_states, TensorType({DT_BF16, DT_FLOAT16}))
    .OPTIONAL_INPUT(query_start_loc, TensorType({DT_INT32}))
    .OPTIONAL_INPUT(cache_indices, TensorType({DT_INT32}))
    .OPTIONAL_INPUT(initial_state_mode, TensorType({DT_INT32}))
    .OPTIONAL_INPUT(bias, TensorType({DT_BF16, DT_FLOAT16}))
    .OPTIONAL_INPUT(num_accepted_tokens, TensorType({DT_INT32}))
    .OPTIONAL_INPUT(num_computed_tokens, TensorType({DT_INT32}))
    .OPTIONAL_INPUT(block_idx_first_scheduled_token, TensorType({DT_INT32}))
    .OPTIONAL_INPUT(block_idx_last_scheduled_token, TensorType({DT_INT32}))
    .OPTIONAL_INPUT(initial_state_idx, TensorType({DT_INT32}))
    .ATTR(activation_mode, Int, 0)
    .ATTR(pad_slot_id, Int, -1)
    .ATTR(run_mode, Int, 0)
    .ATTR(max_query_len, Int, -1)
    .ATTR(residual_connection, Int, 1)
    .ATTR(block_size, Int, 128)
    .ATTR(conv_mode, Int, 0)
    .ATTR(max_draft_tokens, Int, 7)
    .OUTPUT(conv_states, TensorType({DT_BF16, DT_FLOAT16}))
    .OUTPUT(y, TensorType({DT_BF16, DT_FLOAT16}))
    .OP_END_FACTORY_REG(FusedCausalConv1d)
```

## Brief

Function FusedCausalConv1d.

## Inputs

- x: Input sequence tensor. shape [cu_seq_len, dim] or [batch, seqlen, dim]. Supports float16, bfloat16.
- weight: Convolution kernel of shape [K, dim], K fixed to 3. Same type as x.
- conv_states: Cache state tensor storing historical tokens per sequence, updated in-place. Same type as x.
- query_start_loc: Optional. Start offset of each sequence in x. shape [batch+1]. int32.
- cache_indices: Optional. Index mapping each sequence to its cache slot. 1D [batch] or 2D [batch, max_num_blocks].
int32.
- initial_state_mode: Optional. Flag indicating whether each sequence uses cached data. shape [batch]. int32.
- bias: Optional. Convolution bias of shape [dim]. Same type as x.
- num_accepted_tokens: Optional. Number of accepted tokens per sequence in speculative decoding. shape [batch].
int32.
- num_computed_tokens: Optional. Total computed tokens per batch for initial state detection. shape [batch]. int32.
- block_idx_first_scheduled_token: Optional. Block index of first scheduled token per batch (APC). shape [batch].
int32.
- block_idx_last_scheduled_token: Optional. Block index of last scheduled token per batch (APC). shape [batch].
int32.
- initial_state_idx: Optional. Initial state block index per batch (APC). shape [batch]. int32.

## Outputs

- conv_states: Updated cache state tensor. Same shape and type as input conv_states.
- y: Output sequence tensor. Same shape and type as x.

## Attributes

- activation_mode: A optional int. Activation function type: 0 (None), 1 (silu), 2 (swish).
- pad_slot_id: A optional int. Slot ID used to skip padding batches.
- run_mode: A optional int. Execution mode (legacy, not supported).
- max_query_len: A optional int. Max sequence length across all batches.
- residual_connection: A optional int. Whether to use residual connection: 0 (no), 1 (yes).
- block_size: A optional int. APC block size, supports 128/256.
- conv_mode: A optional int. Convolution mode: 0 (Qwen3-Next), 1 (Pangu v2).
- max_draft_tokens: A optional int. Maximum speculative tokens, supports 0~16.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x: bfloat16,float16
- input1 weight: bfloat16,float16
- input2 conv_states: bfloat16,float16
- input3 query_start_loc: int32
- input4 cache_indices: int32
- input5 initial_state_mode: int32
- input6 bias: bfloat16,float16
- input7 num_accepted_tokens: int32
- input8 num_computed_tokens: int32
- input9 block_idx_first_scheduled_token: int32
- input10 block_idx_last_scheduled_token: int32
- input11 initial_state_idx: int32
- output0 conv_states: bfloat16,float16
- output1 y: bfloat16,float16


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
