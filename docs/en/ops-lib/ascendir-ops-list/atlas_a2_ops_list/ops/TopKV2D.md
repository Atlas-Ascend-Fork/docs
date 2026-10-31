# TopKV2D

```c
REG_OP(TopKV2D)
    .INPUT(x, TensorType::RealNumberType())
    .INPUT(k, TensorType({DT_INT32}))
    .INPUT(assist_seq, TensorType({DT_FLOAT16}))
    .OUTPUT(values, TensorType::RealNumberType())
    .OUTPUT(indices, TensorType({DT_INT32}))
    .ATTR(sorted, Bool, true)
    .ATTR(dim, Int, -1)
    .ATTR(largest, Bool, true)
    .OP_END_FACTORY_REG(TopKV2D)
```

## Brief

Finds values and indices of the "k" largest elements for the last
dimension .

## Inputs

Two inputs, including:
- x: A 1D-8D tensor, with the last dimension at least "k".
Supported type: float16, float32, bfloat16. Supported format: ND.
- k: A 0D Tensor of type int32. Supported format: ND.
Number of top elements to look for along the last dimension (along each row
for matrices) .
- assist_seq: A 1D tensor of type float16. Supported format: ND.
with size of 2N, which "N" is the last dimension.
The first N numbers is indices, and the next N numbers is deviation of casting
int32 to float16.

## Outputs

- values: A Tensor, specifying the sorted data. Has the same type and format as
"input". Supported format: ND.
- indices: A Tensor of type int32, specifying the indices of sorted data. Supported format: ND .
@see TopK()

## Attributes

- sorted: An optional bool. Defaults to "True".
If "True", the returned "k" elements are themselves sorted.
If "False", the returned "k" elements are not sorted.
- dim: An optional int. Defaults to -1. For reserved use.
- largest: An optional bool, controls whether to return largest or smallest elements. Defaults to true.
If "True", the "k" largest elements are returned in descending order.
If "False", the "k" smallest elements are returned in ascending order.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI CPU
- input0 x: float16
- input1 k: int32
- input2 assist_seq: float16
- output0 values: float16
- output1 indices: int32

## Third-party framework compatibility

- Compatible with the TensorFlow operator TopKV2.


---

[Back to Operator Specifications (Atlas A2 products)](../README.md)
