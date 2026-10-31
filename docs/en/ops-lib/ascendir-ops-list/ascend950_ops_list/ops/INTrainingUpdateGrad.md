# INTrainingUpdateGrad

```c
REG_OP(INTrainingUpdateGrad)
    .INPUT(dy, TensorType({DT_FLOAT16,DT_FLOAT}))
    .INPUT(x, TensorType({DT_FLOAT16,DT_FLOAT}))
    .INPUT(variance, TensorType({DT_FLOAT}))
    .INPUT(mean, TensorType({DT_FLOAT}))
    .OUTPUT(res_gamma, TensorType({DT_FLOAT}))
    .OUTPUT(res_beta, TensorType({DT_FLOAT}))
    .OP_END_FACTORY_REG(INTrainingUpdateGrad)
```

## Brief

Performs the backpropagation of InstanceNorm.

## Inputs

Four inputs, including:
- dy: A 4D tensor of type float16 or float32, for the gradient, format [NCHW, NHWC].
- x: A 4Dtensor of type float16 or float32, format [NCHW, NHWC].
- variance: A 4D tensor of type float32, for the variance of "x", format [NCHW, NHWC] and HW=1.
- mean: A 4D tensor of type float32, for the mean of "x", format [NCHW, NHWC] and HW=1.

## Outputs

- res_gamma: A 4D tensor of type float32, format [NCHW, NHWC] and HW=1.
- res_beta: A 4D tensor of type float32, format [NCHW, NHWC] and HW=1.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 dy: float16,float32
- input1 x: float16,float32
- input2 variance: float32
- input3 mean: float32
- output0 res_gamma: float32
- output1 res_beta: float32


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
