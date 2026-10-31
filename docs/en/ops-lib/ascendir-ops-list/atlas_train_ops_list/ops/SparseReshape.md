# SparseReshape

```c
REG_OP(SparseReshape)
    .INPUT(indices, TensorType({DT_INT32, DT_INT64}))
    .INPUT(shape, TensorType({DT_INT32, DT_INT64}))
    .INPUT(new_shape, TensorType({DT_INT32, DT_INT64}))
    .OUTPUT(y_indices, TensorType({DT_INT32, DT_INT64}))
    .OUTPUT(y_shape, TensorType({DT_INT32, DT_INT64}))
    .OP_END_FACTORY_REG(SparseReshape)
```

## Brief

Reshapes a SparseTensor to represent values in a new dense shape.

## Inputs

The input of int32 support only static input
- indices: A matrix tensor of type int64 or type int32. 2D. The indices of the SparseTensor.
- shape: A vector tensor of type int64 or type int32. 1D. The shape of the SparseTensor.
- new_shape: A 1D tensor of type int64 or type int32. The requested new dense shape.

## Outputs

- y_indices: A tensor of type int64 or int32. The indices of the new dense shape.
- y_shape: A tensor of type int64 or int32. The shape of the new dense shape.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 indices: int32
- input1 shape: int32
- input2 new_shape: int32
- output0 y_indices: int32
- output1 y_shape: int32
### AI CPU
- input0 indices: int64
- input1 shape: int64
- input2 new_shape: int64
- output0 y_indices: int64
- output1 y_shape: int64

## Third-party framework compatibility

Compatible with the TensorFlow operator SparseReshape.


---

[Back to Operator Specifications (Atlas training products)](../README.md)
