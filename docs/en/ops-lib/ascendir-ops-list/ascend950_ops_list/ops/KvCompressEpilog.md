# KvCompressEpilog

```c
REG_OP(KvCompressEpilog)
    .INPUT(cache, TensorType({DT_UINT8}))
    .INPUT(x, TensorType({DT_BF16}))
    .INPUT(slot_mapping, TensorType::IndexNumberType())
    .OUTPUT(cache, TensorType({DT_UINT8}))
    .ATTR(quant_group_size, Int, 64)
    .ATTR(quant_mode, Int, 1)
    .ATTR(round_scale, Bool, true)
    .ATTR(x_scale, Float, 1.0)
    .OP_END_FACTORY_REG(KvCompressEpilog)
```

```c
 - cache is both input and output (in-place update).
 - slot_mapping dimensions should equal x dimensions minus 1.
 - The last dimension (d) of x must be 64-aligned (d % 64 == 0) and greater than 64.
 - For quant_mode==2, quant_group_size must be 16/32/64 and (d-64) divisible by it.
 - Ascend 950PR&950DT products.
```

## Brief

Compresses cached key/value data in the KV-cache epilog stage by applying
       group-wise dynamic quantization (FP8 group / E8M0) with scale factors.
       The quantized rows are scattered into cache for each valid slot.

## Inputs

Inputs including:
- cache: The existing key/value cache tensor to be updated in-place.
  - Data types: uint8.
  - format: ND
- x: Input activation tensor to be quantized and written into the cache.
  - Data types: bfloat16.
  - format: ND
- slot_mapping: Token index mapping indicating which cache slot each token maps to.
  - Data types: int32, int64.
  - format: ND

## Outputs

- cache: Updated key/value cache after in-place compression.

## Attributes

- quant_group_size: An optional int attribute. Quant group size. Defaults to 64.
  For quant_mode 2 only 16/32/64 are supported and (d-64) must be divisible by it.
- quant_mode: An optional int attribute. Quantization mode.
  - 0: nope per-group(64) FP8(E4M3) dynamic quant, scale stored as bfloat16, rope kept as bf16
  - 1: same as 0 but scale stored as float8_e8m0 (default)
  - 2: rope static hifloat8 quant (scaled by x_scale), nope per-group FLOAT4_E2M1 dynamic quant
       (scale = group amax / 6, stored as bfloat16). Row layout (bytes):
       [rope hifloat8 64B][nope fp4 (d-64)/2 B][nope bf16 scale nGroup*2 B][pad to 128]
- round_scale: An optional bool attribute. Whether to round the group scale value for
  quant_mode 0/1. Defaults to true. Ignored when quant_mode==2.
- x_scale: An optional float attribute. For quant_mode 2 it is the rope hifloat8 static
  quant scale; reserved/unused for quant_mode 0/1. Defaults to 1.0.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 cache: uint8
- input1 x: bfloat16
- input2 slot_mapping: int32,int64
- output0 cache: uint8


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
