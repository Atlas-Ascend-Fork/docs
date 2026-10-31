# CumulativeLogsumexp

```c
REG_OP(CumulativeLogsumexp)
    .INPUT(x, TensorType({DT_DOUBLE, DT_FLOAT, DT_FLOAT16}))
    .INPUT(axis, TensorType({DT_INT32, DT_INT16}))
    .OUTPUT(y, TensorType({DT_DOUBLE, DT_FLOAT, DT_FLOAT16}))
    .ATTR(exclusive, Bool, false)
    .ATTR(reverse, Bool, false)
    .OP_END_FACTORY_REG(CumulativeLogsumexp)
```

## Brief

Computes the cumulative log sum exp of the tensor "x" along "axis" .

## Inputs

Two inputs, including:
- x: A Tensor. Must be one of the following types: float32, float16.
- axis A Tensor of type int32 or int16. Defaults to "0".

## Outputs

y: A Tensor. Has the same type as "x".

## Attributes

- exclusive: If "False", performs inclusive CumulativeLogsumexp,
which means that the first element of the input is identical to the first element of the output.
If "True", performs exclusive CumulativeLogsumexp.
- reverse: A bool. Defaults to "False".

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x: float16,float32
- input1 axis: int16,int32,int64
- output0 y: float16,float32

## Third-party framework compatibility

Compatible with the TensorFlow operator Cumsum.


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
