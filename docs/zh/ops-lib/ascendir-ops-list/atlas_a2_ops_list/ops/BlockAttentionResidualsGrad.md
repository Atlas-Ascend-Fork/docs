# BlockAttentionResidualsGrad

```c
REG_OP(BlockAttentionResidualsGrad)
    .INPUT(partial_block, TensorType({DT_FLOAT16, DT_BF16, DT_FLOAT}))
    .INPUT(block_res, TensorType({DT_FLOAT16, DT_BF16, DT_FLOAT}))
    .INPUT(proj_weight, TensorType({DT_FLOAT16, DT_BF16, DT_FLOAT}))
    .INPUT(norm_weight, TensorType({DT_FLOAT16, DT_BF16, DT_FLOAT}))
    .INPUT(grad_hidden_states, TensorType({DT_FLOAT16, DT_BF16, DT_FLOAT}))
    .INPUT(inv_norm, TensorType({DT_FLOAT}))
    .INPUT(probs, TensorType({DT_FLOAT}))
    .OUTPUT(grad_partial_block, TensorType({DT_FLOAT16, DT_BF16, DT_FLOAT}))
    .OUTPUT(grad_block_res, TensorType({DT_FLOAT16, DT_BF16, DT_FLOAT}))
    .OUTPUT(grad_proj_weight, TensorType({DT_FLOAT16, DT_BF16, DT_FLOAT}))
    .OUTPUT(grad_norm_weight, TensorType({DT_FLOAT16, DT_BF16, DT_FLOAT}))
    .ATTR(valid_block_num, Int, -1)
    .OP_END_FACTORY_REG(BlockAttentionResidualsGrad)
```

## Brief

Computes gradients for the BlockAttentionResiduals forward operator.
The operator fuses the backward of softmax, RMS normalization and attention
weighted-sum to produce gradients of partial_block, block_res, proj_weight
and norm_weight.

## Inputs

- partial_block: A 2D tensor of shape [B, H]. Type supports FLOAT16,
    BFLOAT16 and FLOAT32. Dataformat: ND.
- block_res: A 3D tensor of shape [B, N, H]. Type supports FLOAT16,
    BFLOAT16 and FLOAT32. Dataformat: ND.
- proj_weight: A 2D tensor of shape [1, H]. Type supports FLOAT16,
    BFLOAT16 and FLOAT32. Dataformat: ND.
- norm_weight: A 1D tensor of shape [H]. Type supports FLOAT16,
    BFLOAT16 and FLOAT32. Dataformat: ND.
- grad_hidden_states: A 2D tensor of shape [B, H]. Type supports FLOAT16,
    BFLOAT16 and FLOAT32. Dataformat: ND.
- inv_norm: A 2D tensor of shape [B, N + 1]. Type supports FLOAT32.
    Dataformat: ND.
- probs: A 2D tensor of shape [B, N + 1]. Type supports FLOAT32.
    Dataformat: ND.

## Outputs

- grad_partial_block: A 2D tensor of shape [B, H], gradient of
    partial_block.
- grad_block_res: A 3D tensor of shape [B, N, H], gradient of block_res.
- grad_proj_weight: A 2D tensor of shape [1, H], gradient of proj_weight.
- grad_norm_weight: A 1D tensor of shape [H], gradient of norm_weight.
    Output dtype is the same as the corresponding input.

## Attributes

- valid_block_num: An optional int attribute. Defaults to -1 (all N blocks).
    Only -1 or N (block_res.shape[1]) is supported.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 partial_block: bfloat16,float16,float32
- input1 block_res: bfloat16,float16,float32
- input2 proj_weight: bfloat16,float16,float32
- input3 norm_weight: bfloat16,float16,float32
- input4 grad_hidden_states: bfloat16,float16,float32
- input5 inv_norm: float32
- input6 probs: float32
- output0 grad_partial_block: bfloat16,float16,float32
- output1 grad_block_res: bfloat16,float16,float32
- output2 grad_proj_weight: bfloat16,float16,float32
- output3 grad_norm_weight: bfloat16,float16,float32


---

[Back to Operator Specifications (Atlas A2 products)](../README.md)
