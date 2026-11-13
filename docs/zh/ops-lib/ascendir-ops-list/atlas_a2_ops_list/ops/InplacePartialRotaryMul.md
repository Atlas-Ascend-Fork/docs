# InplacePartialRotaryMul

```c
REG_OP(InplacePartialRotaryMul)
    .INPUT(x, TensorType({DT_FLOAT16, DT_FLOAT, DT_BFLOAT16}))
    .INPUT(cos, TensorType({DT_FLOAT16, DT_FLOAT, DT_BFLOAT16}))
    .INPUT(sin, TensorType({DT_FLOAT16, DT_FLOAT, DT_BFLOAT16}))
    .OUTPUT(x, TensorType({DT_FLOAT16, DT_FLOAT, DT_BFLOAT16}))
    .ATTR(rotary_mode, Int, 0)
    .ATTR(partial_slice, ListInt, {0, 0})
    .OP_END_FACTORY_REG(InplacePartialRotaryMul)
```

## Brief

Apply inplace partial rotary position embedding for a single tensor.

## Inputs

- x: A tensor which rotary position embedding is applied inplace, format supports ND, and data type must be
float16, float or bfloat16.
- cos: A tensor which is "cos" in rotary position embedding, format supports ND, data type must be the same as
"x", and shape must be the same as "sin".
- sin: A tensor which is "sin" in rotary position embedding, format supports ND, data type must be the same as
"x", and shape must be the same as "cos".

## Outputs

x: A tensor which is the result of inplace rotary position embedding, format supports ND, data type must be
the same as input "x", and shape must be the same as input "x".

## Attributes

rotary_mode: An optional attribute of type int, specifying the mode of rotary position embedding. Currently only
supports interleave mode (rotary_mode=1). Defaults to 0.
partial_slice: An optional attribute of type list int, specifying the slice range [start, end) for partial rotary.
Defaults to [0, 0]. When sliceEnd equals sliceStart, no rotary position embedding is performed.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x: bfloat16,float16,float32
- input1 cos: bfloat16,float16,float32
- input2 sin: bfloat16,float16,float32
- output0 x: bfloat16,float16,float32

## Attention Constraints

Let (B, S, N, D) represents the shape of the input "x". Under this representation, the shape constraints of each
parameter can be described as follows:
- Non-contiguous tensors are not supported.
- The D of "x" must not exceed 1024.
- In interleave mode (rotary_mode=1), D of "x" must be a multiple of 2.
- The last dimension sizes of "cos" and "sin" must be equal, and must equal the partialSlice length
(partialSlice[1] - partialSlice[0]).
- partialSlice constraints: sliceStart >= 0, sliceEnd >= 0, sliceEnd <= D of "x",
sliceLength = sliceEnd - sliceStart >= 0.
- Only interleave mode (rotary_mode=1) is supported.
- Inplace execution: input "x" and output "x" share the same tensor, results are written back to input "x".
- cos/sin shapes must satisfy broadcast relationship with "x".
- On Ascend 950PR&950DT products: input "x" supports only BSND, B1ND, B11D, 111D layouts.
- On Atlas A3 products and Atlas A2 products: input "x" supports only BS1D, B11D layouts.


---

[Back to Operator Specifications (Atlas A2 products)](../README.md)
