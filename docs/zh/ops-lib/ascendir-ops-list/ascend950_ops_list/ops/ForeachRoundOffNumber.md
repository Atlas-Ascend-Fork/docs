# ForeachRoundOffNumber

```c
REG_OP(ForeachRoundOffNumber)
    .DYNAMIC_INPUT(x, TensorType({DT_FLOAT16, DT_FLOAT, DT_BF16, DT_INT16}))
    .INPUT(roundMode, TensorType({DT_INT8}))
    .DYNAMIC_OUTPUT(y, TensorType({DT_FLOAT, DT_FLOAT16, DT_BF16, DT_INT16}))
    .OP_END_FACTORY_REG(ForeachRoundOffNumber)
```

## Brief

round off number foreach element in each tensor in tesnorlist, this is an in-place operation.

## Inputs

Two inputs
- x: A tensor list containing multiple tensors, can be float16, float, bfloat16 or int16.
- roundMode: mode of round off.

## Outputs

- y: A tensor list which store the tensors whose value are produced by round off

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x: bfloat16,float16,float32,int16
- input1 roundMode: int8
- output0 y: bfloat16,float16,float32,int16


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
