# InplacePartialRotaryMulGrad

```c
REG_OP(InplacePartialRotaryMulGrad)
    .INPUT(dy, TensorType({DT_FLOAT16, DT_FLOAT, DT_BFLOAT16}))
    .INPUT(cos, TensorType({DT_FLOAT16, DT_FLOAT, DT_BFLOAT16}))
    .INPUT(sin, TensorType({DT_FLOAT16, DT_FLOAT, DT_BFLOAT16}))
    .OUTPUT(dy, TensorType({DT_FLOAT16, DT_FLOAT, DT_BFLOAT16}))
    .ATTR(rotary_mode, Int, 0)
    .ATTR(partial_slice, ListInt, {0, 0})
    .OP_END_FACTORY_REG(InplacePartialRotaryMulGrad)
```

## Brief

Backwards calculation of InplacePartialRotaryMul.

## Inputs

- dy: A 4D tensor which represents the gradient of output "y" in InplacePartialRotaryMul, updated
in-place to be the grad of input "x" in InplacePartialRotaryMul. Format supports ND, and data type must be float16,
float32 or bfloat16.
- cos: A 4D tensor which is input "cos" in InplacePartialRotaryMul, format supports ND, data type must be
float16, float32 or bfloat16 and must be the same as "sin", and shape must be the same as "sin". The D of "cos"
must be equal to the slice length ("partial_slice"'s end - start).
- sin: A 4D tensor which is input "sin" in InplacePartialRotaryMul, format supports ND, data type must be
float16, float32 or bfloat16 and must be the same as "cos", and shape must be the same as "cos". The D of "sin"
must be equal to the slice length ("partial_slice"'s end - start).

## Outputs

- dy: A 4D Tensor, in-place updated from input "dy", which is the grad of input "x" in
InplacePartialRotaryMul. Format supports ND, data type and shape must be the same as input "dy".

## Attributes

- rotary_mode: An optional attribute of type int, specifying the mode of rotary position embedding, must be
0-"half", 1-"interleave", 2-"quarter" or 3-"interleave-half". Defaults to 0.
- partial_slice: An optional attribute of type list int, specifying the slice range of the partial rotary position
embedding. The value is a list of two integers. Defaults to {0, 0}.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 dy: bfloat16,float16,float32
- input1 cos: bfloat16,float16,float32
- input2 sin: bfloat16,float16,float32
- output0 dy: bfloat16,float16,float32

## Attention Constraints

- This operator is only supported on Ascend 950PR&950DT products.
- Currently only interleave mode (rotary_mode=1) is supported. Other modes (half=0, quarter=2,
interleave-half=3) are not implemented yet.
Let (B, S, N, D) represents the shape of the input "dy". Under this
representation, the shape constraints of each parameter can be described as follows:
- The D of "dy" must be equal and less or equal to 1024. When the slice length is greater than 0, the D of
"cos", "sin" must be equal to the slice length ("partial_slice"'s end - start).
- B, S, N of "cos", "sin" must broadcast to match the B, S, N of "dy". When the slice length is greater than 0,
the D of these tensors equals ("partial_slice"'s end - start). Specifically, B, S, N must meet one of the following
four conditions:
 - B, S, N are 1, means the shape is (1, 1, 1, end-start).
 - B, S, N are the same as that of "dy", means the shape is (B, S, N, end-start).
 - One of S and N is 1, the remaining one dimension and B are the same as that of "dy", means the shape is (B, 1, N,
end-start) or (B, S, 1, end-start).
 - Two of B, S and N are 1, the remaining one dimension is the same as that of "dy", means the shape is (1, 1, N,
end-start), (1, S, 1, end-start) or (B, 1, 1, end-start).
- Let the value of "partial_slice" be [start, end]. "start" must be in range [0, D], "end" must be in range
["start", D]. When the slice length is greater than 0: in half, interleave and interleave-half mode,
("end" - "start") must be a multiple of 2; in quarter mode, ("end" - "start") must be a multiple of 4.
- Empty-input support: when the slice length is 0 ("partial_slice"'s start equals end, e.g. [0, 0]), or any of
"dy"/"cos"/"sin" is an empty tensor (some dim is 0), the operator performs a no-op: no rotary grad is computed and
the output equals the input (in-place).


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
