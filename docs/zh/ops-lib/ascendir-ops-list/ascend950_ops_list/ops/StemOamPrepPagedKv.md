# StemOamPrepPagedKv

```c
REG_OP(StemOamPrepPagedKv)
    .INPUT(k_cache, TensorType({DT_FLOAT8_E4M3FN}))
    .INPUT(v_cache, TensorType({DT_FLOAT8_E4M3FN}))
    .INPUT(kv_indices, TensorType({DT_INT32}))
    .INPUT(kv_seq_lens, TensorType({DT_INT32}))
    .OPTIONAL_INPUT(k_scale_cache, TensorType({DT_FLOAT}))
    .OPTIONAL_INPUT(v_scale, TensorType({DT_FLOAT}))
    .ATTR(lambda_mag, Float, 0.3)
    .ATTR(kv_layout, String, "BNBD")
    .ATTR(stem_block_size, Int, 128)
    .ATTR(stem_stride, Int, 16)
    .OUTPUT(k_flat, TensorType({DT_BF16}))
    .OUTPUT(v_bias, TensorType({DT_FLOAT}))
    .OP_END_FACTORY_REG(StemOamPrepPagedKv)
```

```c
- H_kv (num_heads) max = 8, batch max = 16.
- When k_cache is FLOAT8_E4M3FN, k_scale_cache and v_scale are mandatory.
- k_scale_cache must be 4D with same front 3 dims as k_cache, last dim = 1.
- stem_block_size must be multiple of 32, <=256, and must be multiple of stem_stride.
- stem_stride must be multiple of 16, <=64, <=stem_block_size.
```

## Brief

Stem OAM K/V-side preprocessing for paged KV cache.
Converts paged KV cache into flattened k_flat and v_bias outputs grouped by stem blocks,
for downstream OAM score computation.

## Inputs

- k_cache: Paged K cache. Shape [total_blocks, H_kv, kv_block_size, 128] (BNBD) or
            [total_blocks, kv_block_size, H_kv, 128] (BBND). Data type: DT_FLOAT8_E4M3FN.
            Must be 4D, supporting front 3 dims non-contiguous, last dim must be contiguous.
            Last dim D must equal 128 (hardcoded DIM_QK).
- v_cache: Paged V cache. Same shape/layout as k_cache. Data type: DT_FLOAT8_E4M3FN.
- kv_indices: Block indices for each batch. Shape [batch, max_kv_blocks]. Data type: DT_INT32.
- kv_seq_lens: Per-batch KV sequence lengths. Shape [batch]. Data type: DT_INT32.
               Value depend: tiling reads actual values to compute max_Kb.
- k_scale_cache: Optional. Per-block scale factor for K. Shape [total_blocks, H_kv, kv_block_size, 1] (BNBD).
                 Data type: DT_FLOAT. Required when k_cache is FLOAT8_E4M3FN.
- v_scale: Optional. Per-head scale factor for V. Shape [H_kv]. Data type: DT_FLOAT.
             Must be 1D [H_kv].

## Outputs

- k_flat: Flattened K output. Shape [batch, H_kv, max_Kb, stem_stride * 128]. Data type: DT_BF16.
- v_bias: V bias output. Shape [batch, H_kv, max_Kb]. Data type: DT_FLOAT.

## Attributes

- lambda_mag: Optional. Lambda magnitude for V bias normalization. Default 0.3. Range: [0, 1].
- kv_layout: Optional. KV cache layout. "BNBD" or "BBND" (currently only "BNBD" supported). Default "BNBD".
- stem_block_size: Optional. Stem block size. Default 128.
- stem_stride: Optional. Stem stride. Default 16.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
