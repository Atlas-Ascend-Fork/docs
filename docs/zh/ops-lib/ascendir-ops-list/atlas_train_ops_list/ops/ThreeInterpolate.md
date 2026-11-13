# ThreeInterpolate

```c
REG_OP(ThreeInterpolate)
    .INPUT(features, TensorType({DT_FLOAT, DT_FLOAT16}))
    .INPUT(idx, TensorType({DT_INT32, DT_INT64}))
    .INPUT(weight, TensorType({DT_FLOAT, DT_FLOAT16}))
    .OUTPUT(y, TensorType({DT_FLOAT, DT_FLOAT16}))
    .OP_END_FACTORY_REG(ThreeInterpolate)
```

## Brief

Performs 3-neighbor weighted feature interpolation.

## Inputs

Three inputs, including:
- features: A 3D Tensor of shape (B, M, C). Must be one of the following types: float32, float16.
- idx: A 3D Tensor of shape (B, N, 3). Must be one of the following types: int32, int64.
- weight: A 3D Tensor of shape (B, N, 3). Must be one of the following types: float32, float16.

## Outputs

y: A 3D Tensor of shape (B, N, C). Must be one of the following types: float32, float16.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 features: float32
- input1 idx: int32,int64
- input2 weight: float32


---

[Back to Operator Specifications (Atlas training products)](../README.md)
