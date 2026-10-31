# ScatterNonAliasingAdd

```c
REG_OP(ScatterNonAliasingAdd)
    .INPUT(x, TensorType({DT_FLOAT, DT_FLOAT16, DT_INT32}))
    .INPUT(indices, TensorType::IndexNumberType())
    .INPUT(updates, TensorType({DT_FLOAT, DT_FLOAT16, DT_INT32}))
    .OUTPUT(y, TensorType({DT_FLOAT, DT_FLOAT16, DT_INT32}))
    .OP_END_FACTORY_REG(ScatterNonAliasingAdd)
```

## Brief

Applies sparse addition to input "x" using individual values or slices
from "updates" according to "indices". The updates are non-aliasing: "x" is
only modified in-place if no other operations will use it. Otherwise, a copy
of "x" is made. This operation has a gradient with respect to both "x" and
"updates" .

## Inputs

Three inputs, including:
- x: A Tensor. Must be one of the following types: float32, float16, int32. A batch_size x classes tensor.
- indices: A Tensor of type IndexNumberType. Specifies the indices into "x".
- updates: A Tensor. Must have the same type as "x".
Specifies the updated values to add to "x" .

## Outputs

y: A Tensor with the same shape as "x", containing values of "x" updated with
"updates" .
@see ScatterNd(),ScatterNdAdd()

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x: float16,float32,int32
- input1 indices: int32,int64
- input2 updates: float16,float32,int32
- output0 y: float16,float32,int32

## Third-party framework compatibility

- Compatible with the TensorFlow operator ScatterNDNonAliasingAdd.


---

[Back to Operator Specifications (Atlas inference products)](../README.md)
