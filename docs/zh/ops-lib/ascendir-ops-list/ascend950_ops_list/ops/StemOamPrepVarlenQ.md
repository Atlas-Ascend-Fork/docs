# StemOamPrepVarlenQ

```c
REG_OP(StemOamPrepVarlenQ)
    .INPUT(q, TensorType({DT_FLOAT8_E4M3FN}))
    .INPUT(qSeqLens, TensorType({DT_INT64}))
    .INPUT(cuSeqLensQ, TensorType({DT_INT64}))
    .OPTIONAL_INPUT(qScale, TensorType({DT_FLOAT}))
    .ATTR(stemBlockSize, Int, 128)
    .ATTR(stemStride, Int, 16)
    .OUTPUT(qFlat, TensorType({DT_BF16}))
    .OP_END_FACTORY_REG(StemOamPrepVarlenQ)
```

```c
- q last dim D must equal 128 (hardcoded DIM_QK).
- cuSeqLensQ length must be batch + 1, monotonically increasing, starting at 0.
- When q is FLOAT8_E4M3FN, qScale is mandatory.
- Batch max = 1024.
- Q-side stride dimension uses natural order (g in [0, S-1]), unlike the K-side which flips.
- When qSeqLens[b] == 0, the corresponding qFlat output is zero-filled.
```

## Brief

Stem OAM Q-side preprocessing for block-sparse attention.
Converts a variable-length paged Q tensor into a flattened qFlat output grouped by stem blocks,
for downstream OAM score computation. The pipeline is:
Scale Fusion -> De-page Varlen -> Weighted Group Sum (natural order, no flip) -> Flatten -> Cast to output dtype.

## Inputs

- q: Variable-length Q tensor (all batch tokens concatenated). Shape [total_tokens, H_q, D].
       Last dim D must equal 128.
       Supported data types: DT_FLOAT8_E4M3FN.
- qSeqLens: Per-batch Q sequence lengths. Shape [batch]. Data type: DT_INT64.
              Value depend: tiling reads actual values to compute max_Qb.
- cuSeqLensQ: Cumulative sequence-length offsets for varlen indexing. Shape [batch + 1]. Data type: DT_INT64.
                cuSeqLensQ[0] must be 0; cuSeqLensQ[batch] must equal total_tokens; monotonically increasing.
- qScale: Optional. Per-token scale factor for Q. Shape [total_tokens, H_q]. Data type: DT_FLOAT.
            Required when q is FLOAT8_E4M3FN.

## Outputs

- qFlat: Flattened Q output for OAM score computation. Shape [batch, H_q, max_Qb, kflat_dim].
           Where max_Qb = ceil(max(qSeqLens) / stemBlockSize), kflat_dim = stemStride * D.
           Data type: DT_BF16.

## Attributes

- stemBlockSize: Optional. Stem block size (B).  Must be 128.
- stemStride: Optional. Stem stride (S). Must be 16.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 q: float8_e4m3fn
- input1 qSeqLens: int64
- input2 cuSeqLensQ: int64
- input3 qScale: float32
- output0 qFlat: bfloat16


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
