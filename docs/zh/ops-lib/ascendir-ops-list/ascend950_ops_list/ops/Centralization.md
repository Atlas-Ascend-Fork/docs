# Centralization

```c
REG_OP(Centralization)
    .INPUT(x, TensorType({ DT_FLOAT, DT_FLOAT16 }))
    .OUTPUT(y, TensorType({ DT_FLOAT, DT_FLOAT16 }))
    .ATTR(axes, ListInt, {-1})
    .OP_END_FACTORY_REG(Centralization)
```

## Brief

Computes Centralization. result = x - mean(x, axes)

## Inputs

 x: An ND tensor of type float16, float32.

## Outputs

y: A Tensor. Has the same type as "x".

## Attributes

axes: The dimensions to reduce. Must be one of the following types: int, list, tuple, NoneType, default: -1.
Must be in the range [-rank(x), rank(x)).

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x: float16,float32
- output0 y: float16,float32

## Third-party framework compatibility

custom operator


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
