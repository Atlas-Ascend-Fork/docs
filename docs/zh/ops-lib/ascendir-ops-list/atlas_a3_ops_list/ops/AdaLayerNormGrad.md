# AdaLayerNormGrad

```c
REG_OP(AdaLayerNormGrad)
    .INPUT(dy, TensorType({DT_FLOAT, DT_FLOAT16, DT_BF16}))
    .INPUT(x, TensorType({DT_FLOAT, DT_FLOAT16, DT_BF16}))
    .INPUT(rstd, TensorType({DT_FLOAT}))
    .INPUT(mean, TensorType({DT_FLOAT}))
    .INPUT(scale, TensorType({DT_FLOAT, DT_FLOAT16, DT_BF16}))
    .INPUT(gamma, TensorType({DT_FLOAT, DT_FLOAT16, DT_BF16}))
    .INPUT(beta, TensorType({DT_FLOAT, DT_FLOAT16, DT_BF16}))
    .OUTPUT(pd_x, TensorType({DT_FLOAT, DT_FLOAT16, DT_BF16}))
    .OUTPUT(pd_scale, TensorType({DT_FLOAT, DT_FLOAT16, DT_BF16}))
    .OUTPUT(pd_shift, TensorType({DT_FLOAT, DT_FLOAT16, DT_BF16}))
    .OUTPUT(pd_gamma, TensorType({DT_FLOAT, DT_FLOAT16, DT_BF16}))
    .OUTPUT(pd_beta, TensorType({DT_FLOAT, DT_FLOAT16, DT_BF16}))
    .OP_END_FACTORY_REG(AdaLayerNormGrad)
```

```c
 Forward: out = LayerNorm(x) * (1 + scale) + shift \n
 Backward calculations: \n
 z = (x - mean) * rstd \n
 dy_g = dy * gamma * (1 + scale) \n
 temp_1 = 1/N * ∑(dy * gamma * (1 + scale)) \n
 temp_2 = 1/N * (x - mean) * rstd * ∑(dy * gamma * (1 + scale) * (x - mean) * rstd) \n
 pd_x = (dy * gamma * (1 + scale) - (temp_1 + temp_2)) * rstd \n
 pd_scale = ∑(dy * ((x - mean) * rstd * gamma + beta)) \n
 pd_shift = ∑dy \n
 pd_gamma = ∑dy * (1 + scale) * (x - mean) * rstd \n
 pd_beta = ∑dy * (1 + scale)
```

## Brief

AdaLayerNormGrad operator interface implementation

## Inputs

Seven inputs, including:
- dy: A tensor. The gradient tensor that represents the reverse calculation.
Must be one of the following types: float16, float32, bfloat16. The format must be ND.
The shape is [B, S, H], where B supports 0-6 dimensions.
- x: A tensor. First input of forward propagation.
Must be one of the following types: float16, float32, bfloat16.
The shape is the same as dy, which is [B, S, H], where B supports 0-6 dimensions.
- rstd: A tensor. Third output of forward propagation, indicates the reciprocal of the standard deviation of x.
Must be one of the following types: float32. The format must be ND.
Has the shape [B, S, 1], where the last dimension is fixed to 1.
- mean: A tensor. Second output of forward propagation, indicates the mean value of x.
Must be one of the following types: float32. The format must be ND.
Has the shape [B, S, 1], where the last dimension is fixed to 1.
- scale: A tensor. Indicates the adaptive scale parameter.
Must be one of the following types: float16, float32, bfloat16. The format must be ND.
The shape is [B, H] or [B, 1, H].
- gamma: A tensor. Indicates the normalization weight parameter.
Must be one of the following types: float16, float32, bfloat16. The format must be ND.
The shape is [H].
- beta: A tensor. Indicates the normalization bias parameter.
Must be one of the following types: float16, float32, bfloat16. The format must be ND.
The shape is [H].

## Outputs

Five outputs, including:
- pd_x: A tensor. Indicates the gradient of input x.
Must be one of the following types: float16, float32, bfloat16. The format must be ND.
Has the same type, shape and format as x.
- pd_scale: A tensor. Indicates the gradient of scale.
Must be one of the following types: float16, float32, bfloat16. The format must be ND.
Has the same type, shape and format as scale.
- pd_shift: A tensor. Indicates the gradient of adaptive offset parameter.
Must be one of the following types: float16, float32, bfloat16. The format must be ND.
Has the same type and format as scale. The shape is [B, H] or [B, 1, H], where B supports 0-6 dimensions.
- pd_gamma: A tensor. Indicates the gradient of gamma.
Must be one of the following types: float16, float32, bfloat16. The format must be ND.
Has the same type, shape and format as gamma.
- pd_beta: A tensor. Indicates the gradient of beta.
Must be one of the following types: float16, float32, bfloat16. The format must be ND.
Has the same type, shape and format as beta.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 dy: bfloat16,float16,float32
- input1 x: bfloat16,float16,float32
- input2 rstd: float32
- input3 mean: float32
- input4 scale: bfloat16,float16,float32
- input5 gamma: bfloat16,float16,float32
- input6 beta: bfloat16,float16,float32
- output0 pd_x: bfloat16,float16,float32
- output1 pd_scale: bfloat16,float16,float32
- output2 pd_shift: bfloat16,float16,float32
- output3 pd_gamma: bfloat16,float16,float32
- output4 pd_beta: bfloat16,float16,float32


---

[Back to Operator Specifications (Atlas A3 products)](../README.md)
