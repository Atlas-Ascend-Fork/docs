# AlltoAllvQuantGroupedMatMul

```c
REG_OP(AlltoAllvQuantGroupedMatMul)
    .INPUT(gmm_x, TensorType({DT_HIFLOAT8, DT_FLOAT8_E4M3FN, DT_FLOAT8_E5M2, DT_FLOAT4_E2M1}))
    .INPUT(gmm_weight, TensorType({DT_HIFLOAT8, DT_FLOAT8_E4M3FN, DT_FLOAT8_E5M2, DT_FLOAT4_E2M1}))
    .INPUT(gmm_x_scale, TensorType({DT_FLOAT, DT_FLOAT8_E8M0}))
    .INPUT(gmm_weight_scale, TensorType({DT_FLOAT, DT_FLOAT8_E8M0}))
    .OPTIONAL_INPUT(send_counts_tensor, TensorType({DT_INT64}))
    .OPTIONAL_INPUT(recv_counts_tensor, TensorType({DT_INT64}))
    .OPTIONAL_INPUT(mm_x, TensorType({DT_HIFLOAT8, DT_FLOAT8_E4M3FN, DT_FLOAT8_E5M2, DT_FLOAT4_E2M1}))
    .OPTIONAL_INPUT(mm_weight, TensorType({DT_HIFLOAT8, DT_FLOAT8_E4M3FN, DT_FLOAT8_E5M2, DT_FLOAT4_E2M1}))
    .OPTIONAL_INPUT(mm_x_scale, TensorType({DT_FLOAT, DT_FLOAT8_E8M0}))
    .OPTIONAL_INPUT(mm_weight_scale, TensorType({DT_FLOAT, DT_FLOAT8_E8M0}))
    .OUTPUT(gmm_y, TensorType({DT_FLOAT16, DT_BF16}))
    .OUTPUT(mm_y, TensorType({DT_FLOAT16, DT_BF16}))
    .OUTPUT(permute_out, TensorType({DT_HIFLOAT8, DT_FLOAT8_E4M3FN, DT_FLOAT8_E5M2, DT_FLOAT4_E2M1}))
    .REQUIRED_ATTR(group, String)
    .REQUIRED_ATTR(ep_world_size, Int)
    .REQUIRED_ATTR(send_counts, ListInt)
    .REQUIRED_ATTR(recv_counts, ListInt)
    .REQUIRED_ATTR(gmm_x_quant_mode, Int)
    .REQUIRED_ATTR(gmm_weight_quant_mode, Int)
    .ATTR(trans_gmm_weight, Bool, false)
    .ATTR(trans_mm_weight, Bool, false)
    .ATTR(permute_out_flag, Bool, false)
    .ATTR(mm_x_quant_mode, Int, 0)
    .ATTR(mm_weight_quant_mode, Int, 0)
    .ATTR(group_size, Int, 0)
    .ATTR(y_dtype, Int, 28)
    .ATTR(mm_dtype, Int, 28)
    .ATTR(comm_mode, String, "ai_cpu")
    .OP_END_FACTORY_REG(AlltoAllvQuantGroupedMatMul)
```

## Brief

Fusion of alltoallv and grouped matmul.

## Inputs

- gmm_x: A matrix Tensor of shape [BSK, H1]. The data type of elements supports hifloat8, float8_e4m3fn,
float8_e5m2, float4_e2m1; the format supports ND.
- gmm_weight: A matrix Tensor of shape [e, H1, N1]. The data type of elements supports hifloat8, float8_e4m3fn,
float8_e5m2, float4_e2m1; the format supports ND.
- gmm_x_scale: A matrix Tensor. The type support float32 or float8_e8m0. The format supports ND.
- gmm_weight_scale: A matrix Tensor. The type support float32 or float8_e8m0. The format supports ND.
- send_counts_tensor: A Tensor of shape [e * ep]. The data type of elements supports int64; the format supports ND.
- recv_counts_tensor: A Tensor of shape [e * ep]. The data type of elements supports int64; the format supports ND.
- mm_x: A matrix Tensor of shape [BS, H1]. The data type of elements supports hifloat8, float8_e4m3fn,
float8_e5m2, float4_e2m1 and should match that of gmm_x; the format supports ND.
- mm_weight: A matrix Tensor of shape [H2, N2]. The data type of elements supports hifloat8, float8_e4m3fn,
float8_e5m2, float4_e2m1 and should match that of gmm_weight; the format supports ND.
- mm_x_scale: A matrix Tensor. The type support float32 or float8_e8m0. The format supports ND.
- mm_weight_scale: A matrix Tensor. The type support float32 or float8_e8m0. The format supports ND.

## Outputs

- gmm_y: A matrix tensor of shape [A, N1] containing result of grouped matmul. The data type of elements supports
float16 or bfloat16; the format supports ND.
- mm_y: A matrix tensor of shape [BS, N2] containing result of matmul. The data type of elements supports float16 or
bfloat16; the format supports ND.
- permute_out: A matrix tensor of shape [BSK, H1] containing result of permutation if permute_out_flag == true.
The data type of elements supports hifloat8, float8_e4m3fn, float8_e5m2, float4_e2m1; the format supports ND.

## Attributes

- group: A required String identifying the expert group of ranks.
- ep_world_size: A required int identifying the number of expert parallel group rank num.
- send_counts: An int list. A list containing amount of data to be sent.
- recv_counts: An int list. A list containing amount of data to be received.
- gmm_x_quant_mode: An int. Quantization mode of gmm_x. Default: 0.
       - 0：No Quantization
       - 1：PerTensor Quantization
       - 2：PerChannel Quantization
       - 3：PerToken Quantization
       - 4：PerGroup Quantization
       - 5：PerBlock Quantization
       - 6：Mx Quant Quantization
- gmm_weight_quant_mode: An int. Quantization mode of gmm_weight. Default: 0.
- trans_gmm_weight: A boolean value. Whether gmm_weight is transposed. True indicates transposition. Default: false.
- trans_mm_weight: A boolean value. Whether mm_weight is transposed. True indicates transposition. Default: false.
- permute_out_flag: A boolean value. Whether to output permute_out. True indicates that output permute_out is
required. Default: false.
- mm_x_quant_mode: An int. Quantization mode of mm_x and should be same as gmm_x_quant_mode. Default: 0.
- mm_weight_quant_mode: An int. Quantization mode of mm_weight and should be same as gmm_weight_quant_mode. Default:
0.
- group_size: An int. Default: 0.
- y_dtype: An int. Declare the gmm_y dtype. Default: static_cast\<int64_t>(ge::DT_UNDEFINED) is 28.
- mm_dtype: An int. Declare the mm_y dtype and should be same as y_dtype. Default:
static_cast\<int64_t>(ge::DT_UNDEFINED) is 28.
- comm_mode: A String value. Indicating communication type. Default: ai_cpu.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 gmm_x: float4_e2m1,float8_e4m3fn,float8_e5m2,hifloat8
- input1 gmm_weight: float4_e2m1,float8_e4m3fn,float8_e5m2,hifloat8
- input2 gmm_x_scale: float8_e8m0,float32
- input3 gmm_weight_scale: float8_e8m0,float32
- input4 send_counts_tensor: int64
- input5 recv_counts_tensor: int64
- input6 mm_x: float4_e2m1,float8_e4m3fn,float8_e5m2,hifloat8
- input7 mm_weight: float4_e2m1,float8_e4m3fn,float8_e5m2,hifloat8
- input8 mm_x_scale: float8_e8m0,float32
- input9 mm_weight_scale: float8_e8m0,float32
- output0 gmm_y: bfloat16,float16
- output1 mm_y: bfloat16,float16
- output2 permute_out: float4_e2m1,float8_e4m3fn,float8_e5m2,hifloat8


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
