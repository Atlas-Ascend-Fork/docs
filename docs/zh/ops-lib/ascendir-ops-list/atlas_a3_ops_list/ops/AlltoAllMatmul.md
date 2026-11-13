# AlltoAllMatmul

```c
REG_OP(AlltoAllMatmul)
    .INPUT(x1, TensorType({DT_BF16, DT_FLOAT16, DT_FLOAT8_E4M3FN, DT_FLOAT8_E5M2, DT_FLOAT4_E2M1}))
    .INPUT(x2, TensorType({DT_BF16, DT_FLOAT16, DT_FLOAT8_E4M3FN, DT_FLOAT8_E5M2, DT_FLOAT4_E2M1}))
    .OPTIONAL_INPUT(bias, TensorType({DT_BF16, DT_FLOAT16, DT_FLOAT}))
    .OPTIONAL_INPUT(x1_scale, TensorType({DT_FLOAT, DT_FLOAT8_E8M0}))
    .OPTIONAL_INPUT(x2_scale, TensorType({DT_FLOAT, DT_FLOAT8_E8M0}))
    .OPTIONAL_INPUT(comm_scale, TensorType({DT_FLOAT}))
    .OPTIONAL_INPUT(x1_offset, TensorType({DT_FLOAT}))
    .OPTIONAL_INPUT(x2_offset, TensorType({DT_FLOAT}))
    .OUTPUT(y, TensorType({DT_BF16, DT_FLOAT16, DT_FLOAT}))
    .OUTPUT(all2all_out, TensorType({DT_BF16, DT_FLOAT16, DT_FLOAT8_E4M3FN, DT_FLOAT8_E5M2, DT_FLOAT4_E2M1}))
    .REQUIRED_ATTR(group, String)
    .REQUIRED_ATTR(world_size, Int)
    .ATTR(all2all_axes, ListInt, {-2, -1})
    .ATTR(y_dtype, Int, 28)
    .ATTR(x1_quant_mode, Int, 0)
    .ATTR(x2_quant_mode, Int, 0)
    .ATTR(comm_quant_mode, Int, 0)
    .ATTR(x1_quant_dtype, Int, 28)
    .ATTR(comm_quant_dtype, Int, 28)
    .ATTR(transpose_x1, Bool, false)
    .ATTR(transpose_x2, Bool, false)
    .ATTR(group_size, Int, 0)
    .ATTR(comm_mode, String, "ai_cpu")
    .ATTR(alltoall_out_flag, Bool, true)
    .OP_END_FACTORY_REG(AlltoAllMatmul)
```

## Brief

Fusion op of alltoall and matmul.

## Inputs

two inputs, including:
- x1: A matrix Tensor. The type support bfloat16, float16, float8_e4m3fn, float8_e5m2, float4_e2m1. The format
supports ND.
- x2: A matrix Tensor. The type support bfloat16, float16, float8_e4m3fn, float8_e5m2, float4_e2m1. The format
supports ND.
- bias: A matrix Tensor. The type support bfloat16, float16, float. The format supports ND.
- x1_scale: A matrix Tensor. The type support float, float8_e8m0. The format supports ND.
- x2_scale: A matrix Tensor. The type support float, float8_e8m0. The format supports ND.
- comm_scale: A matrix Tensor. The type support float. The format supports ND.
- x1_offset: A matrix Tensor. The type support float. The format supports ND.
- x2_offset: A matrix Tensor. The type support float. The format supports ND.

## Outputs

- y: A matrix Tensor. The type support bfloat16, float16, float. The format supports ND.
- all2all_out: A matrix Tensor. The type support bfloat16, float16, float8_e4m3fn, float8_e5m2, float4_e2m1. The
format supports ND.

## Attributes

- group: A string. Communication domain identifier.
- world_size: An int.
- all2all_axes: An ListInt. Indicate the data direction for All2All communication. Default: {-2, -1}.
- y_dtype: An int. Declare the output dtype. Default: static_cast\<int64_t>(ge::DT_UNDEFINED) 为28.
- x1_quant_mode: An int. Quantization mode of x1, which support 0(non-quant), 7(dynamic-pertoken-quant),
6(mx-quant). Default: 0.
- x2_quant_mode: An int. Quantization mode of x2, which support 0(non-quant), 2(perchannel-quant), 6(mx-quant).
Default: 0.
- comm_quant_mode: An int. Quantitative types for communication. Default: 0.
- x1_quant_dtype: An int. Quantization type of the left matrix input to Matmul after communication. Default:
static_cast\<int64_t>(ge::DT_UNDEFINED) 为28.
- comm_quant_dtype: An int. Quantization type of x1 input before communication. Default:
static_cast\<int64_t>(ge::DT_UNDEFINED) 为28.
- transpose_x1: A bool. Whether x1 is transposed. Default: false.
- transpose_x2: A bool. Whether x2 is transposed. Default: false.
- group_size: An int. Default: 0.
- comm_mode: A string. Communication engine. Default: "default".
- alltoall_out_flag: A bool. Default: true.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x1: bfloat16,float16
- input1 x2: bfloat16,float16
- input2 bias: float16,float32
- input3 x1_scale: float32
- input4 x2_scale: float32
- input5 comm_scale: float32
- input6 x1_offset: float32
- input7 x2_offset: float32
- output0 y: bfloat16,float16
- output1 all2all_out: bfloat16,float16


---

[Back to Operator Specifications (Atlas A3 products)](../README.md)
