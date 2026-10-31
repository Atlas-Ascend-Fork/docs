# MhcPostBackward

```c
REG_OP(MhcPostBackward)
    .INPUT(grad_y, TensorType({DT_FLOAT16, DT_BF16}))
    .INPUT(x, TensorType({DT_FLOAT16, DT_BF16}))
    .INPUT(h_res, TensorType({DT_FLOAT}))
    .INPUT(h_out, TensorType({DT_FLOAT16, DT_BF16}))
    .INPUT(h_post, TensorType({DT_FLOAT}))
    .OUTPUT(grad_x, TensorType({DT_FLOAT16, DT_BF16}))
    .OUTPUT(grad_h_res, TensorType({DT_FLOAT}))
    .OUTPUT(grad_h_out, TensorType({DT_FLOAT16, DT_BF16}))
    .OUTPUT(grad_h_post, TensorType({DT_FLOAT}))
    .OP_END_FACTORY_REG(MhcPostBackward)
```

## Brief

Backward operator for mhc_post. Computes gradients of grad_output w.r.t.
x, h_res, h_out and h_post.

## Inputs

- grad_y: A Tensor. Gradient of output. Type is: BFloat16 or Float16.
Dataformat:ND. Supports 3D (Shape:[T, n, D]) or 4D (Shape:[B, S, n, D]) tensors.
- x: A Tensor. Input data in the mHC layer. Type is: BFloat16 or Float16.
Dataformat:ND. Supports 3D (Shape:[T, n, D]) or 4D (Shape:[B, S, n, D]) tensors.
- h_res: A Tensor. The h_res transformation matrix. Type is: Float32.
Dataformat:ND. Supports 3D (Shape:[T, n, n]) or 4D (Shape:[B, S, n, n]) tensors.
- h_out: A Tensor. Output of the Atten/MLP layer. Type is: BFloat16 or Float16.
Dataformat:ND. Supports 2D (Shape:[T, D]) or 3D (Shape:[B, S, D]) tensors.
- h_post: A Tensor. The h_post gating vector. Type is: Float32.
Dataformat:ND. Supports 2D (Shape:[T, n]) or 3D (Shape:[B, S, n]) tensors.

## Outputs

- grad_x: A Tensor. Gradient of x. Type is: BFloat16 or Float16.
Dataformat:ND. Supports 3D (Shape:[T, n, D]) or 4D (Shape:[B, S, n, D]) tensors.
- grad_h_res: A Tensor. Gradient of h_res. Type is: Float32.
Dataformat:ND. Supports 3D (Shape:[T, n, n]) or 4D (Shape:[B, S, n, n]) tensors.
- grad_h_out: A Tensor. Gradient of h_out. Type is: BFloat16 or Float16.
Dataformat:ND. Supports 2D (Shape:[T, D]) or 3D (Shape:[B, S, D]) tensors.
- grad_h_post: A Tensor. Gradient of h_post. Type is: Float32.
Dataformat:ND. Supports 2D (Shape:[T, n]) or 3D (Shape:[B, S, n]) tensors.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 grad_y: bfloat16,float16
- input1 x: bfloat16,float16
- input2 h_res: float32
- input3 h_out: bfloat16,float16
- input4 h_post: float32
- output0 grad_x: bfloat16,float16
- output1 grad_h_res: float32
- output2 grad_h_out: bfloat16,float16
- output3 grad_h_post: float32


---

[Back to Operator Specifications (Atlas A3 products)](../README.md)
