# InplaceIndexAddWithSorted

```c
REG_OP(InplaceIndexAddWithSorted)
    .INPUT(var, TensorType({DT_FLOAT16, DT_BF16}))
    .INPUT(value, TensorType({DT_FLOAT16, DT_BF16}))
    .INPUT(sorted_indices, TensorType({DT_INT32}))
    .INPUT(pos, TensorType({DT_INT32}))
    .OPTIONAL_INPUT(alpha, TensorType({DT_FLOAT}))
    .OUTPUT(var, TensorType({DT_FLOAT16, DT_BF16}))
    .REQUIRED_ATTR(axis, Int)
    .OP_END_FACTORY_REG(InplaceIndexAddWithSorted)
```

## Brief

Performs in-place addition on the "var" tensor along axis dim using
 "value" rows selected by "sorted_indices". "pos" gives the run-start offsets
 of equal-value runs inside "sorted_indices" so that multiple indices pointing
 to the same row can be accumulated together. "alpha" is a scalar multiplier
 applied to "value" before accumulation.
 computing process (per index i, with sorted_indices[i] = r):
 @code{.c}
 var[r, :] += alpha * sum(value[j, :] for j in run(pos, i))
 @endcode

## Inputs

- var: A mutable tensor. Type: DT_FLOAT16 / DT_BF16. Format: FORMAT_ND.
    Shape: [M, ...], where M is the size of the indexed dimension (axis, currently only supports 0).
- value: A tensor of updates. Same dtype and rank as "var". Format: FORMAT_ND.
    Shape: [N, ...], where N is the number of update rows and equals the length of "sorted_indices".
- sorted_indices: A 1D int32 tensor of row indices into "var" along axis, sorted in
    non-decreasing order. Format: FORMAT_ND. Shape: [N].
- pos: A 1D int32 tensor of run-start positions matching "sorted_indices".
    Format: FORMAT_ND. Shape: [N].
- alpha: An optional scalar tensor. Type: DT_FLOAT. Format: FORMAT_ND.
    Shape: scalar ([] or [1]). Defaults to 1.0 when absent.

## Outputs

var: A mutable tensor. Same dtype and shape as input "var". Format: FORMAT_ND.

## Attributes

axis: A required int. The dimension along which to index (currently only supports 0).

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 var: bfloat16,float16,float32,int16,int32
- input1 value: bfloat16,float16,float32,int16,int32
- input2 sorted_indices: int32
- input3 pos: int32
- input4 alpha: float32,int16,int32
- output0 var: bfloat16,float16,float32,int16,int32

## Attention Constraints

 - "var" and "value" must have the same dtype and rank.
 - "pos" must have the same length as "sorted_indices".

## Third-party framework compatibility

Compatible with the PyTorch operator index_add_ (sorted-index variant).


---

[Back to Operator Specifications (Atlas A2 products)](../README.md)
