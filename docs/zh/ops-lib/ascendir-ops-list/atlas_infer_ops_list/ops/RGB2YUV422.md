# RGB2YUV422

```c
REG_OP(RGB2YUV422)
.INPUT(rgb, TensorType({DT_UINT8})).OUTPUT(yuv, TensorType({DT_UINT8})).OP_END_FACTORY_REG(RGB2YUV422)
```

## Brief

Converts RGB images to YUV422 (YUYV packed format) color space.

## Inputs

One input, including:
- x: An ND Tensor of type uint8. Shape [..., H, W, 3].

## Outputs

y: An ND Tensor of type uint8. Shape [..., H, W, 2] (YUYV packed).

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 rgb: uint8
- output0 yuv: uint8


---

[Back to Operator Specifications (Atlas inference products)](../README.md)
