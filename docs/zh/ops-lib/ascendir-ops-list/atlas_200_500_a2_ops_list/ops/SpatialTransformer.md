# SpatialTransformer

```c
REG_OP(SpatialTransformer)
    .INPUT(x, TensorType({DT_FLOAT, DT_FLOAT16, DT_DOUBLE, DT_UINT8, DT_INT8, DT_UINT16, DT_INT16, DT_INT32, DT_UINT32,
                          DT_UINT64, DT_INT64}))
    .OPTIONAL_INPUT(theta, TensorType({DT_FLOAT, DT_FLOAT16, DT_DOUBLE, DT_UINT8, DT_INT8, DT_UINT16, DT_INT16,
                                       DT_INT32, DT_UINT32, DT_UINT64, DT_INT64}))
    .OUTPUT(y, TensorType({DT_FLOAT, DT_FLOAT16, DT_DOUBLE, DT_UINT8, DT_INT8, DT_UINT16, DT_INT16, DT_INT32, DT_UINT32,
                           DT_UINT64, DT_INT64}))
    .ATTR(output_size, ListInt, {-1, -1})
    .ATTR(default_theta, ListFloat, {})
    .ATTR(align_corners, Bool, false)
    .ATTR(use_default_theta, ListInt, {})
    .OP_END_FACTORY_REG(SpatialTransformer)
```

## Brief

Spatial Transformer Network (STN) operator for affine transformation.

## Inputs

Including:
- x: A Tensor. Must be one of following types: float, float16, double, uint8, int8,
           uint16, int16, int32, uint32, uint64, int64.
           4-D tensor with shape [batch, channels, height, width].
           The format must be NCHW or NC1HWC0.
- theta: A Tensor. Must be one of following types: float, float16, double, uint8, int8,
             uint16, int16, int32, uint32, uint64, int64.
             3-D tensor with shape [batch, 2, 3] or [2, 3] containing
             affine transformation parameters.

## Outputs

- y: A Tensor. Must be one of following types: float, float16, double, uint8, int8,
        uint16, int16, int32, uint32, uint64, int64.
        4-D tensor with shape [batch, channels, height, width].
        The format must be NCHW or NC1HWC0.

## Attributes

- output_size: A list of 2 integers. Defaults to [-1, -1].
             Specifies the output height and width. If -1, uses input size.
- default_theta: A list of 6 floats. Defaults to [].
             Default affine transformation parameters when use_default_theta is true.
- align_corners: A bool. Defaults to false.
             If true, centers of the 4 corner pixels of the input and output
             tensors are aligned, preserving the values at the corner pixels.
- use_default_theta: A list of 6 integers. Defaults to [].
             Specifies which theta parameters to use from default_theta.
             1 means use default, 0 means use input theta.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI CPU
- input0 x: double,float16,float32,int8,int16,int32,int64,uint8,uint16,uint32,uint64
- input1 theta: double,float16,float32,int8,int16,int32,int64,uint8,uint16,uint32,uint64
- output0 y: double,float16,float32,int8,int16,int32,int64,uint8,uint16,uint32,uint64

## Third-party framework compatibility

Compatible with TensorFlow SpatialTransformer operator.


---

[Back to Operator Specifications (Atlas 200I/500 A2 inference products)](../README.md)
