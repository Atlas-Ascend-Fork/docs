# BallQuery

```c
REG_OP(BallQuery)
    .INPUT(xyz, TensorType({DT_FLOAT16, DT_FLOAT}))
    .INPUT(center_xyz, TensorType({DT_FLOAT16, DT_FLOAT}))
    .OUTPUT(idx, TensorType({DT_INT32}))
    .REQUIRED_ATTR(min_radius, Float)
    .REQUIRED_ATTR(max_radius, Float)
    .REQUIRED_ATTR(sample_num, Int)
    .OP_END_FACTORY_REG(BallQuery)
```

## Brief

Ball query: for each query center point center_xyz[m, b],
      search the point set xyz[b] (coordinates stored in the middle
      dimension) and collect the indices of points whose squared
      distance d2 to the center satisfies d2 == 0 ||
      (min_radius^2 <= d2 < max_radius^2). Up to sample_num points
      are kept in order; when fewer points are found, the remaining
      slots are filled with the index of the first selected point.

## Inputs

Two inputs, including:
- xyz: A ND Tensor of shape (B, 3, N) where coordinates lie in the
        middle dimension. Must be one of: float16, float32.
- center_xyz: A ND Tensor of shape (M, B, 3) holding the query
               center coordinates. Must be same dtype as xyz.

## Outputs

idx: A ND Tensor of shape (M, B, sample_num) holding the selected
    point indices. Type int32.

## Attributes

- min_radius: Float, inner radius of the query ball, must be >= 0.
- max_radius: Float, outer radius of the query ball, must be > 0.
- sample_num: Int, max number of sampled points per ball, must be >= 1.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 xyz: float16,float32
- input1 center_xyz: float16,float32
- output0 idx: int32


---

[Back to Operator Specifications (Atlas training products)](../README.md)
