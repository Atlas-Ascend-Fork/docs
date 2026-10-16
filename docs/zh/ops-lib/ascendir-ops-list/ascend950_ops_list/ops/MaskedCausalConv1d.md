# MaskedCausalConv1d

```c
REG_OP(MaskedCausalConv1d)
    .INPUT(x, TensorType({DT_BF16, DT_FLOAT16}))
    .INPUT(weight, TensorType({DT_BF16, DT_FLOAT16}))
    .OPTIONAL_INPUT(mask, TensorType({DT_BOOL}))
    .OUTPUT(y, TensorType({DT_BF16, DT_FLOAT16}))
    .OP_END_FACTORY_REG(MaskedCausalConv1d)
```

## Brief

Applies masked causal 1D convolution on input sequences.

## Inputs

- x: Input sequence tensor of shape [S, B, H]. Supports float16, bfloat16.
- weight: Convolution kernel of shape [W, H], W fixed to 3. Same dtype as x.
- mask: Optional. Boolean mask tensor of shape [B, S]. Positions marked as False in the mask
    will be zeroed out in the output. Tensor data type: bool.

## Outputs

- y: Output sequence tensor. Same shape and dtype as x.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x: bfloat16,float16
- input1 weight: bfloat16,float16
- input2 mask: bool
- output0 y: bfloat16,float16


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
