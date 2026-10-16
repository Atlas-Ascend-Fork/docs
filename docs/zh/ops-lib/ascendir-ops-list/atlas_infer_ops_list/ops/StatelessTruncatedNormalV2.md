# StatelessTruncatedNormalV2

```c
REG_OP(StatelessTruncatedNormalV2)
    .INPUT(shape, TensorType({ DT_INT32, DT_INT64 }))
    .INPUT(key, TensorType({ DT_UINT64 }))
    .INPUT(counter, TensorType({ DT_UINT64 }))
    .INPUT(alg, TensorType({ DT_INT32 }))
    .OUTPUT(y, TensorType({ DT_FLOAT16, DT_BF16, DT_FLOAT, DT_DOUBLE }))
    .ATTR(dtype, Type, DT_FLOAT)
    .OP_END_FACTORY_REG(StatelessTruncatedNormalV2)
```

## Brief

Outputs random values from a truncated normal distribution.

## Inputs

Inputs include:
- shape: A Tensor. Must be one of the following types: int32, int64.
- key: Key of RNG algorithm. Shape[1].
- counter: Counter of RNG algorithm. Shape[2] for philox, shape[1] for threefry.
- alg: RNG algorithm. 1:philox, 2:threefry.

## Outputs

y: A Tensor of types: float16, bfloat16, float32, double. A tensor of the specified shape
filled with random truncated normal values.

## Attributes

- dtype: dtype: A optional attr, specifying the output data type. Defaults to "DT_FLOAT".

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI CPU
- input0 shape: int32,int64
- input1 key: uint64
- input3 alg: int32
- output0 y: bfloat16,double,float16,float32

## Attention Constraints

The implementation for StatelessTruncatedNormalV2 on Ascend uses AICPU, with bad performance.

## Third-party framework compatibility

- compatible with tensorflow StatelessTruncatedNormalV2 operator.


---

[Back to Operator Specifications (Atlas inference products)](../README.md)
