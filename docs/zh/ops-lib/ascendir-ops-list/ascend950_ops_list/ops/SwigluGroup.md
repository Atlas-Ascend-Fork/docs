# SwigluGroup

```c
REG_OP(SwigluGroup)
    .INPUT(x, TensorType({DT_FLOAT16, DT_BF16, DT_FLOAT}))
    .OPTIONAL_INPUT(weight, TensorType({DT_FLOAT}))
    .OPTIONAL_INPUT(group_index, TensorType({DT_INT64}))
    .OUTPUT(y, TensorType({DT_FLOAT16, DT_BF16, DT_FLOAT}))
    .ATTR(clamp_limit, Float, -1.0f)
    .OP_END_FACTORY_REG(SwigluGroup)
```

## Brief

Performs SwiGLU activation.

## Inputs

- x: Required tensor of type float16, bfloat16 or float32. The rank must be in [1, 8], empty tensors
are supported, and the last dimension is split into two equal parts for SwiGLU and must be divisible by 2.
- weight: Optional float32 tensor. Per-token weight multiplied into the SwiGLU result. The rank must be
in [1, 8], empty tensors are supported, and the element count must equal the product of all x dims
except the last one.
- group_index: Optional int64 tensor. Count-mode group token numbers. It must be 1D, its element values
must be greater than or equal to 0, the sum of all its elements must be greater than 0, and it does not support
being an empty tensor on its own.

## Outputs

- y: SwiGLU result tensor with the same dtype and rank as x, the same dims as x except that the last
dimension is halved.

## Attributes

- clamp_limit: Optional float. Defaults to -1.0, which disables clamp. If set to a positive value,
clamps SwiGLU inputs before activation.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x: bfloat16,float16,float32
- input1 weight: float32
- input2 group_index: int64
- output0 y: bfloat16,float16,float32

## Third-party framework compatibility

It is a custom operator. It has no corresponding operator in Caffe, ONNX, TensorFlow, or PyTorch.


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
