# ForeachBinaryOp

```c
REG_OP(ForeachBinaryOp)
    .DYNAMIC_INPUT(x1, TensorType({DT_FLOAT, DT_FLOAT16, DT_INT32, DT_BF16}))
    .DYNAMIC_INPUT(x2, TensorType({DT_FLOAT, DT_FLOAT16, DT_INT32, DT_BF16}))
    .DYNAMIC_OUTPUT(y, TensorType({DT_FLOAT, DT_FLOAT16, DT_INT32, DT_BF16}))
    .REQUIRED_ATTR(op_code, Int)
    .OP_END_FACTORY_REG(ForeachBinaryOp)
```

## Brief

Apply an element-wise binary operation for each tensor pair (x1[i], x2[i]).
The operation is selected by attribute op_code: 0=add, 1=sub, 2=mul, 3=div.

## Inputs

Two inputs:
- x1: A tensor list containing multiple tensors
- x2: Another tensor list containing multiple tensors

## Outputs

- y: A tensor list storing y[i] = x1[i] \<op> x2[i]

## Attributes

- op_code: Required Int. Selects the binary op (0=add, 1=sub, 2=mul, 3=div)

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x1: float16,float32
- input1 x2: float16,float32,int32
- output0 y: float16,float32,int32


---

[Back to Operator Specifications (Atlas A2 products)](../README.md)
