# SparseFillEmptyRows

```c
REG_OP(SparseFillEmptyRows)
    .INPUT(indices, TensorType({DT_INT64}))
    .INPUT(values, TensorType({DT_FLOAT, DT_FLOAT16, DT_INT8, DT_INT16, \
        DT_UINT16, DT_UINT8, DT_INT32, DT_INT64, DT_BOOL, DT_DOUBLE, \
        DT_COMPLEX64, DT_COMPLEX128, DT_RESOURCE, DT_STRING}))
    .INPUT(dense_shape, TensorType({DT_INT64}))
    .INPUT(default_value, TensorType({DT_FLOAT, DT_FLOAT16, DT_INT8, \
        DT_INT16, DT_UINT16, DT_UINT8, \
        DT_INT32, DT_INT64, DT_BOOL, DT_DOUBLE, \
        DT_COMPLEX64, DT_COMPLEX128, DT_RESOURCE, DT_STRING}))
    .OUTPUT(y_indices, TensorType({DT_INT64}))
    .OUTPUT(y_values, TensorType({DT_FLOAT, DT_FLOAT16, DT_INT8, \
        DT_INT16, DT_UINT16, DT_UINT8, \
        DT_INT32, DT_INT64, DT_BOOL, DT_DOUBLE, \
        DT_COMPLEX64, DT_COMPLEX128, DT_RESOURCE, DT_STRING}))
    .OUTPUT(empty_row_indicator, TensorType({DT_BOOL}))
    .OUTPUT(reverse_index_map, TensorType({DT_INT64}))
    .OP_END_FACTORY_REG(SparseFillEmptyRows)
```

## Brief

Fills empty rows in the input 2-D `SparseTensor` with a default value.

## Inputs

4 inputs,contains:
- indices: A `tensor` of type `int64`.2-D. the indices of the sparse tensor.
- values: A `tensor`. 1-D. the values of the sparse tensor.
- dense_shape: A `tensor` of type `int64`.1-D. the shape of the sparse tensor.
- default_value: `tensor`. Must have the same type as `values`.
0-D. default value to insert into location `[row, 0, ..., 0]`
for rows missing from the input sparse tensor.

## Outputs

- y_indices:A `tensor` of type `int64`.
- y_values:A `tensor`. Has the same type as `values`.
- empty_row_indicator:A `tensor` of type `bool`.
- reverse_index_map:A `tensor` of type `int64`.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI CPU
- input0 indices: int64
- input1 values: bool,complex64,complex128,double,float16,float32,int8,int16,int32,int64,uint8,uint16,uint32,uint64
- input2 dense_shape: int64
- input3 default_value: bool,complex64,complex128,double,float16,float32,int8,int16,int32,int64,uint8,uint16,uint32,uint64
- output0 y_indices: int64
- output1 y_values: bool,complex64,complex128,double,float16,float32,int8,int16,int32,int64,uint8,uint16,uint32,uint64
- output2 empty_row_indicator: bool
- output3 reverse_index_map: int64

## Third-party framework compatibility

Compatible SparseFillEmptyRows operator in Tensorflow.


---

[Back to Operator Specifications (Atlas 200I/500 A2 inference products)](../README.md)
