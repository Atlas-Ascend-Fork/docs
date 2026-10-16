# ScatterPaKvCacheWithKScale

```c
REG_OP(ScatterPaKvCacheWithKScale)
    .INPUT(key, "T")
    .INPUT(value, "T")
    .INPUT(key_cache, "T")
    .INPUT(value_cache, "T")
    .INPUT(slot_mapping, TensorType::IndexNumberType())
    .INPUT(key_scale, TensorType({DT_FLOAT}))
    .INPUT(key_scale_cache, TensorType({DT_FLOAT}))
    .OUTPUT(key_cache, "T")
    .OUTPUT(value_cache, "T")
    .OUTPUT(key_scale_cache, TensorType({DT_FLOAT}))
    .ATTR(cache_layout, String, "BNBD")
    .DATATYPE(T, TensorType({DT_FLOAT8_E5M2, DT_FLOAT8_E4M3FN}))
    .OP_END_FACTORY_REG(ScatterPaKvCacheWithKScale)
```

```c
- key, value, key_cache, and value_cache must have the same data type.
- key_scale and key_scale_cache must be of float32 type.
- slot_mapping must be of DT_INT32 or DT_INT64 type.
- Values in slot_mapping must be in the range [0, num_blocks * block_size - 1].
- num_tokens <= num_blocks * block_size.
```

## Brief

Scatter KV cache with key scale. Updates key, value, and key_scale into corresponding caches.

## Inputs

7 input tensors:
- key: Key values to be updated, FP8 format. Shape is [num_tokens, num_head, k_head_size].
         Supported data types: DT_FLOAT8_E5M2 or DT_FLOAT8_E4M3FN.
- value: Value values to be updated, FP8 format. Shape is [num_tokens, num_head, v_head_size].
           Supported data types: DT_FLOAT8_E5M2 or DT_FLOAT8_E4M3FN.
- key_cache: Cache to be updated by key, FP8 format. Shape is [num_blocks, num_head, block_size, k_head_size].
               Supported data types: DT_FLOAT8_E5M2 or DT_FLOAT8_E4M3FN.
- value_cache: Cache to be updated by value, FP8 format. Shape is [num_blocks, num_head, block_size, v_head_size].
                 Supported data types: DT_FLOAT8_E5M2 or DT_FLOAT8_E4M3FN.
- slot_mapping: Offset of each token in the cache. Shape is [num_tokens].
                  Supported data types: DT_INT32 or DT_INT64.
- key_scale: Key scaling factor to be updated, FP32 format. Shape is [num_tokens, num_head].
               Supported data types: float32.
- key_scale_cache: Cache to be updated by key_scale, FP32 format.
                     Shape is [num_blocks, num_head, block_size, 1].
                     Supported data types: float32.

## Outputs

3 output tensors (inplace update):
- key_cache: Updated key_cache, same shape and data type as input key_cache.
- value_cache: Updated value_cache, same shape and data type as input value_cache.
- key_scale_cache: Updated key_scale_cache, same shape and data type as input key_scale_cache.

## Attributes

- cache_layout: Optional attribute, describes the cache layout format. Default value is "BNBD".
                  Current version only supports "BNBD" layout.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 key: float8_e4m3fn,float8_e5m2
- input1 value: float8_e4m3fn,float8_e5m2
- input2 key_cache: float8_e4m3fn,float8_e5m2
- input3 value_cache: float8_e4m3fn,float8_e5m2
- input4 slot_mapping: int32,int64
- input5 key_scale: float32
- input6 key_scale_cache: float32
- output0 key_cache: float8_e4m3fn,float8_e5m2
- output1 value_cache: float8_e4m3fn,float8_e5m2
- output2 key_scale_cache: float32


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
