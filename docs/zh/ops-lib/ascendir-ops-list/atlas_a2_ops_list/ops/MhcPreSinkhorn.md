# MhcPreSinkhorn

```c
REG_OP(MhcPreSinkhorn)
    .INPUT(x, "T1")
    .INPUT(phi, "T2")
    .INPUT(alpha, "T2")
    .INPUT(bias, "T2")
    .OUTPUT(hin, "T1")
    .OUTPUT(hPost, "T2")
    .OUTPUT(hRes, "T2")
    .OUTPUT(hPre, "T2")
    .OUTPUT(hcBeforeNorm, "T2")
    .OUTPUT(invRms, "T2")
    .OUTPUT(sumOut, "T2")
    .OUTPUT(normOut, "T2")
    .DATATYPE(T1, TensorType({DT_BF16, DT_FLOAT16}))
    .DATATYPE(T2, TensorType({DT_FLOAT}))
    .ATTR(hc_mult, Int, 4)
    .ATTR(num_iters, Int, 20)
    .ATTR(hc_eps, Float, 1e-6f)
    .ATTR(norm_eps, Float, 1e-6f)
    .ATTR(need_backward, Bool, true)
    .OP_END_FACTORY_REG(MhcPreSinkhorn)
```

## Brief

MhcPreSinkhorn operator performs Sinkhorn normalization with hierarchical combination

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x: bfloat16,float16
- input1 phi: float32
- input2 alpha: float32
- input3 bias: float32
- output0 hin: bfloat16,float16
- output1 hPost: float32
- output2 hRes: float32
- output3 hPre: float32
- output4 hcBeforeNorm: float32
- output5 invRms: float32
- output6 sumOut: float32
- output7 normOut: float32


---

[Back to Operator Specifications (Atlas A2 products)](../README.md)
