# ForeachNeg

```c
REG_OP(ForeachNeg)
    .DYNAMIC_INPUT(x, TensorType({DT_FLOAT, DT_FLOAT16, DT_INT32, DT_BF16, DT_INT16, DT_INT8, DT_UINT8}))
    .DYNAMIC_OUTPUT(y, TensorType({DT_FLOAT, DT_FLOAT16, DT_INT32, DT_BF16, DT_INT16, DT_INT8, DT_UINT8}))
    .OP_END_FACTORY_REG(ForeachNeg)
```

## Brief

Apply neg operation for each tensor in a tensor list in manner of element-wise

## Inputs

One inputs:
- x: A tensor list containing multiple tensors

## Outputs

- y: A tensor list which store the tensors whose value are the neg value of the x

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x: bfloat16,float16,float32,int8,int16,int32,uint8
- output0 y: bfloat16,float16,float32,int8,int16,int32,uint8


---

[Back to Operator Specifications (Atlas A2 products)](../README.md)
