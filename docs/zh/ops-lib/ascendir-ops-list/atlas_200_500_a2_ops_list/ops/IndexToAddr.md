# IndexToAddr

```c
REG_OP(IndexToAddr)
    .INPUT(base_addr, TensorType({DT_INT64, DT_UINT64}))
    .INPUT(x, TensorType({DT_INT64, DT_UINT64}))
    .OUTPUT(addrs_table, TensorType({DT_INT64, DT_UINT64}))
    .REQUIRED_ATTR(ori_shape, ListInt)
    .REQUIRED_ATTR(block_size, ListInt)
    .ATTR(ori_storage_mode, String, "Matrix")
    .ATTR(block_storage_mode, String, "Matrix")
    .ATTR(rank_id, Int, 0)
    .ATTR(dtype, Type, DT_FLOAT)
    .OP_END_FACTORY_REG(IndexToAddr)
```

## Brief

get block tensor according to base addr tensor, for hccl remote read to use.

## Inputs

- base_addr: A Tensor of type int64/uint64.
- x:A Tensor of type int64/uint64.

## Outputs

- addrs_table: list of [rank id, host addr, device addr, read size].

## Attributes

- ori_shape: An required list int. Shape of base tensor.
- block_size: An required list int. Shape of split block tensor.
- ori_storage_mode: An optional string from: '"Matrix", "UT"'. Defaults to
"Matrix". Currently only support Matrix storage.
- block_storage_mode: An optional string from: '"Matrix", "UT"'. Defaults to
"Matrix". Currently only support Matrix storage.
- rank_id: An optional int of rank id. Defaults is 0.
- dtype: An optional Type of base tensor. Defaults is DT_FLOAT.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI CPU
- input0 base_addr: int64,uint64
- input1 x: int64,uint64
- output0 addrs_table: int64,uint64


---

[Back to Operator Specifications (Atlas 200I/500 A2 inference products)](../README.md)
