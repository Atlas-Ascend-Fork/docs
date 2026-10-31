# UnsortedSegmentProd

```c
REG_OP(UnsortedSegmentProd)
    .INPUT(x, TensorType::NumberType())
    .INPUT(segment_ids, TensorType::IndexNumberType())
    .INPUT(num_segments, TensorType::IndexNumberType())
    .OUTPUT(y, TensorType::NumberType())
    .OP_END_FACTORY_REG(UnsortedSegmentProd)
```

## Brief

Computes the product along segments of a tensor.
Computes a tensor such that (output[i] = mul_{j...} x[j...].
the value of segment_ids must be  in [0, num_segments - 1].
for example:x = [[0,1,2],[3,4,5],[6,7,8]], segment_ids = [0,0,1] num_segments = 5
output[0] = [0, 4, 10]
output[1] = [6, 7, 8]
output[2] = [1, 1, 1]
output[3] = [1, 1, 1]
output[4] = [1, 1, 1]

## Inputs

Three inputs, including:
- x: A Tensor of type NumberType(), format is ND. bank of shape must greater zero.
- segment_ids: A 1D Tensor of type IndexNumberType, whose shape is a prefix of "x.shape".
A Tensor of type int32, int64, whose shape is a prefix, format is ND,
bank of shape is small than x rank, or equal of x shape rank.
- num_segments: A Tensor of type int32, int64, format is ND.
Indicates the output segment.

## Outputs

y: A Tensor type and format is the same as x type.

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 x: bfloat16,float16,float32,int32,int64,uint32,uint64
- input1 segment_ids: int32,int64
- input2 num_segments: int32,int64
- output0 y: bfloat16,float16,float32,int32,int64,uint32,uint64
### AI CPU
- input0 x: complex64,complex128,double,float16,float32,int8,int16,int32,int64,qint8,qint32,quint8,uint8,uint16,uint32,uint64
- input1 segment_ids: int32,int64
- input2 num_segments: int32,int64
- output0 y: complex64,complex128,double,float16,float32,int8,int16,int32,int64,qint8,qint32,quint8,uint8,uint16,uint32,uint64

## Third-party framework compatibility

Compatible with the TensorFlow operator UnsortedSegmentProd.


---

[Back to Operator Specifications (Ascend 950PR&950DT Products)](../README.md)
