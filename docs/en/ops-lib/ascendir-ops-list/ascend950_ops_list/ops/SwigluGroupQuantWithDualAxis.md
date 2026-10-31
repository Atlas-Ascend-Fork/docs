# SwigluGroupQuantWithDualAxis

```c
REG_OP(SwigluGroupQuantWithDualAxis)
    .INPUT(x, TensorType({DT_FLOAT16, DT_BF16}))
    .OPTIONAL_INPUT(weight, TensorType({DT_FLOAT16, DT_BF16, DT_FLOAT}))
    .OPTIONAL_INPUT(group_index, TensorType({DT_INT64}))
    .OUTPUT(y1, TensorType({DT_FLOAT8_E4M3FN, DT_FLOAT8_E5M2}))
    .OUTPUT(mxscale1, TensorType({DT_FLOAT8_E8M0}))
    .OUTPUT(y2, TensorType({DT_FLOAT8_E4M3FN, DT_FLOAT8_E5M2}))
    .OUTPUT(mxscale2, TensorType({DT_FLOAT8_E8M0}))
    .OUTPUT(y_origin, TensorType({DT_FLOAT16, DT_BF16}))
    .ATTR(dst_type, Int, DT_FLOAT8_E4M3FN)
    .ATTR(quant_mode, Int, 1)
    .ATTR(clamp_limit, Float, -1.0f)
    .ATTR(output_origin, Bool, false)
    .ATTR(alpha, Float, 1.0f)
    .ATTR(bias, Float, 0.0f)
    .OP_END_FACTORY_REG(SwigluGroupQuantWithDualAxis)
```

## Brief

Fuses clipped SwiGLU with ordinary and grouped MX quantization.
x must be a two-dimensional [T, 2H] tensor.
group_index is an optional one-dimensional INT64 cumsum vector. It only
defines route-2 group boundaries; SwiGLU and route 1 always process all rows.
When present, endpoints are non-negative and non-decreasing, and the final
endpoint is T. Repeated endpoints represent empty groups.
y_origin contains the clipped SwiGLU activation before applying weight and
has shape [T, H] when output_origin is true; otherwise it is a [0] placeholder.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x: bfloat16,float16
- input1 weight: bfloat16,float16,float32
- input2 group_index: int64
- output0 y1: float8_e4m3fn,float8_e5m2
- output1 mxscale1: float8_e8m0
- output2 y2: float8_e4m3fn,float8_e5m2
- output3 mxscale2: float8_e8m0
- output4 y_origin: bfloat16,float16


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
