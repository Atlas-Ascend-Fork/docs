# IndexerQuantCache

```c
REG_OP(IndexerQuantCache)
    .INPUT(cache, "T1")
    .INPUT(cache_scale, "T2")
    .INPUT(x, "T0")
    .INPUT(slot_mapping, TensorType::IndexNumberType())
    .OUTPUT(cache, "T1")
    .OUTPUT(cache_scale, "T2")
    .ATTR(quant_mode, Int, 1)
    .ATTR(round_scale, Bool, true)
    .ATTR(x_scale, Float, 1.0)
    .DATATYPE(T0, TensorType({DT_FLOAT16, DT_BF16}))
    .DATATYPE(T1, TensorType({DT_FLOAT8_E4M3FN, DT_FLOAT8_E5M2, DT_UINT8, DT_FLOAT4_E2M1, DT_FLOAT4_E1M2}))
    .DATATYPE(T2, TensorType({DT_FLOAT, DT_FLOAT8_E8M0}))
    .OP_END_FACTORY_REG(IndexerQuantCache)
```

```c
 - cache and cache_scale are both input and output (in-place update).
 - slot_mapping dimensions should equal x dimensions minus 1.
 - The last dimension (d) of x is quantized per 128 elements per block;
   MX-FP4 (quant_mode=3) quantizes per 32 elements (standard MX block).
 - Ascend 950PR&950DT products.
```

## Brief

Compresses cached key/value data in the Indexer attention epilog stage
       by applying block-wise dynamic quantization (FP8/INT8/MX-FP4) with scale factors.
       Supports per-block quantization on the last dimension with optional MX-FP8/MX-FP4 scale format.

## Inputs

Inputs including:
- cache: The existing key/value cache tensor to be updated in-place.
  - Data types: float8_e4m3fn, float8_e5m2, uint8, float4_e2m1, float4_e1m2.
  - format: ND
- cache_scale: Scale factors for per-block quantization.
  - Data types: float32, float8_e8m0.
  - format: ND
- x: Input activation tensor to be quantized and written into the cache.
  - Data types: float16, bfloat16.
  - format: ND
- slot_mapping: Token index mapping indicating which cache slot each token maps to.
  - Data types: int32.
  - format: ND

## Outputs

- cache: Updated key/value cache after in-place compression.
- cache_scale: Updated scale factors after in-place compression.

## Attributes

- quant_mode: An optional int attribute. Quantization mode.
  - 0: MX-FP8 quantization (scale stored as float8_e8m0)
  - 1: Normal block-wise quantization (default, scale stored as float32)
  - 2: HiFloat8 quantization (scale attribute applied)
  - 3: MX-FP4 quantization (cache packed as uint8, scale stored as float8_e8m0)
- round_scale: An optional bool attribute. Whether to round the MX-FP8 scale value. Defaults to true.
- x_scale: An optional float attribute. Global scale multiplier for HiFloat8 mode. Defaults to 1.0.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 cache: float4_e1m2,float4_e2m1,float8_e4m3fn,float8_e5m2,uint8
- input1 cache_scale: float8_e8m0,float32
- input2 x: bfloat16,float16
- input3 slot_mapping: int32
- output0 cache: float4_e1m2,float4_e2m1,float8_e4m3fn,float8_e5m2,uint8
- output1 cache_scale: float8_e8m0,float32


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
