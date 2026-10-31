# Specification Introduction

<!-- md-trans-meta sourceCommit=ed69a6e4ddc089b45629fd67e49093ec3f403d7e translatedAt=2026-10-20T07:04:55.031Z pushedAt=2026-10-21T02:33:30.158Z nl=2 -->

This section describes the operator information defined based on Ascend IR. The path of the header file where the operators are located is **\$\{INSTALL\_DIR\}/opp/built-in/op\_graph/inc**.

Replace **\$\{INSTALL\_DIR\}** with the file storage path after CANN software installation. For example, if you install the software as the **root** user, the default storage path is **/usr/local/Ascend/cann**.

Before using the operators, read the following descriptions listed in this chapter:

| Basic Knowledge | Description |
| --- | --- |
| [Format](#format) | Describes the format information listed in the operator specifications. |
| [TensorType](#tensortype) | Describes the TensorType types listed in the operator specifications in detail. |
| [Type Promotion](#type-promotion) | When the input tensor data types of some operators (such as Add and Mul) are inconsistent, the data type is automatically promoted during internal computation. This part provides the rules for data type promotion. |
| [Deterministic Computing](#deterministic-computing) | Lists the operators involved in and supported by the deterministic computing feature. |

## Format

- ND: indicates that any format is supported. Use this format with caution for operators except for single-input operators that process the input itself, such as Square and Tanh.
- NC1HWC0: a self-developed 5D data format. C0 is strongly related to the microarchitecture and equals the size of the cube unit, for example, 16. C1 is obtained by splitting the C dimension by C0: C1 = C/C0. If the result is not divisible, the last data block must be padded to C0.
- FRACTAL\_Z: format of convolution weights.

## TensorType

>**Note:**
> For the DT\_COMPLEX32 data types in **OrdinaryType**, **BasicType**, **NumberType**, **ComplexDataType**, and **UnaryDataType**, only the StridedSlice, StridedSliceGrad, and AsStrided operators are currently supported.

```cpp
struct TensorType {
  explicit TensorType(DataType dt);

  TensorType(const std::initializer_list<DataType> &initial_types);

  static TensorType ALL() {
    return TensorType{DT_BOOL,   DT_COMPLEX128, DT_COMPLEX64, DT_DOUBLE, DT_FLOAT,  DT_FLOAT16, DT_INT16,
                      DT_INT32,  DT_INT64,      DT_INT8,      DT_QINT16, DT_QINT32, DT_QINT8,   DT_QUINT16,
                      DT_QUINT8, DT_RESOURCE,   DT_STRING,    DT_UINT16, DT_UINT32, DT_UINT64,  DT_UINT8,
                      DT_BF16, DT_COMPLEX32};
  }

  static TensorType QuantifiedType() { return TensorType{DT_QINT16, DT_QINT32, DT_QINT8, DT_QUINT16, DT_QUINT8}; }

  static TensorType OrdinaryType() {
    return TensorType{DT_BOOL,  DT_COMPLEX128, DT_COMPLEX64, DT_DOUBLE, DT_FLOAT,  DT_FLOAT16, DT_INT16,
                      DT_INT32, DT_INT64,      DT_INT8,      DT_UINT16, DT_UINT32, DT_UINT64,  DT_UINT8,
                      DT_BF16, DT_COMPLEX32};
  }

  static TensorType BasicType() {
    return TensorType{DT_COMPLEX128, DT_COMPLEX64, DT_DOUBLE, DT_FLOAT,  DT_FLOAT16, DT_INT16,
                      DT_INT32,      DT_INT64,     DT_INT8,   DT_QINT16, DT_QINT32,  DT_QINT8,
                      DT_QUINT16,    DT_QUINT8,    DT_UINT16, DT_UINT32, DT_UINT64,  DT_UINT8,
                      DT_BF16, DT_COMPLEX32};
  }

  static TensorType NumberType() {
    return TensorType{DT_COMPLEX128, DT_COMPLEX64, DT_DOUBLE, DT_FLOAT,  DT_FLOAT16, DT_INT16,  DT_INT32,  DT_INT64,
                      DT_INT8,       DT_QINT32,    DT_QINT8,  DT_QUINT8, DT_UINT16,  DT_UINT32, DT_UINT64, DT_UINT8,
                      DT_BF16, DT_COMPLEX32};
  }

  static TensorType RealNumberType() {
    return TensorType{DT_DOUBLE, DT_FLOAT,  DT_FLOAT16, DT_INT16,  DT_INT32, DT_INT64,
                      DT_INT8,   DT_UINT16, DT_UINT32,  DT_UINT64, DT_UINT8, DT_BF16};
  }

  static TensorType ComplexDataType() { return TensorType{DT_COMPLEX128, DT_COMPLEX64, DT_COMPLEX32}; }

  static TensorType IntegerDataType() {
    return TensorType{DT_INT16, DT_INT32, DT_INT64, DT_INT8, DT_UINT16, DT_UINT32, DT_UINT64, DT_UINT8};
  }

  static TensorType SignedDataType() { return TensorType{DT_INT16, DT_INT32, DT_INT64, DT_INT8}; }

  static TensorType UnsignedDataType() { return TensorType{DT_UINT16, DT_UINT32, DT_UINT64, DT_UINT8}; }

  static TensorType FloatingDataType() { return TensorType{DT_DOUBLE, DT_FLOAT, DT_FLOAT16}; }

  static TensorType IndexNumberType() { return TensorType{DT_INT32, DT_INT64}; }

  static TensorType UnaryDataType() {
    return TensorType{DT_COMPLEX128, DT_COMPLEX64, DT_DOUBLE, DT_FLOAT, DT_FLOAT16, DT_BF16, DT_COMPLEX32};
  }

  static TensorType FLOAT() { return TensorType{DT_FLOAT, DT_FLOAT16, DT_BF16}; }

  std::shared_ptr<TensorTypeImpl> tensor_type_impl_;
};

```

## Type Promotion

When the tensor data types of the inputs to some operators (such as Add and Mul) are inconsistent, the operator automatically promotes the data types during internal computation. The rules for data type promotion are as follows:

| Data Type | f32 | f16 | bf16 | s8 | u8 | s16 | u16 | s32 | u32 | s64 | u64 | bool | c32 | c64 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| f32 | f32 | f32 | f32 | f32 | f32 | f32 | × | f32 | × | f32 | × | f32 | c64 | c64 |
| f16 | f32 | f16 | f32 | f16 | f16 | f16 | × | f16 | × | f16 | × | f16 | c32 | c64 |
| bf16 | f32 | f32 | bf16 | bf16 | bf16 | bf16 | × | bf16 | × | bf16 | × | bf16 | c32 | c64 |
| s8 | f32 | f16 | bf16 | s8 | s16 | s16 | × | s32 | × | s64 | × | s8 | c32 | c64 |
| u8 | f32 | f16 | bf16 | s16 | u8 | s16 | × | s32 | × | s64 | × | u8 | c32 | c64 |
| s16 | f32 | f16 | bf16 | s16 | s16 | s16 | × | s32 | × | s64 | × | s16 | c32 | c64 |
| u16 | × | × | × | × | × | × | u16 | × | × | × | × | × | × | × |
| s32 | f32 | f16 | bf16 | s32 | s32 | s32 | × | s32 | × | s64 | × | s32 | c32 | c64 |
| u32 | × | × | × | × | × | × | × | × | u32 | × | × | × | × | × |
| s64 | f32 | f16 | bf16 | s64 | s64 | s64 | × | s64 | × | s64 | × | s64 | c32 | c64 |
| u64 | × | × | × | × | × | × | × | × | × | × | u64 | × | × | × |
| bool | f32 | f16 | bf16 | s8 | u8 | s16 | × | s32 | × | s64 | × | bool | c32 | c64 |
| c32 | c64 | c32 | c32 | c32 | c32 | c32 | × | c32 | × | c32 | × | c32 | c32 | c64 |
| c64 | c64 | c64 | c64 | c64 | c64 | c64 | × | c64 | × | c64 | × | c64 | c64 | c64 |

> **Note:**
>
>- For ease of description, the data types used in the table are abbreviated. Their meanings are as follows: DT\_FLOAT\(f32\), DT\_FLOAT16\(f16\), DT\_BF16\(bf16\), DT\_INT8\(s8\), DT\_UINT8\(u8\), DT\_INT16\(s16\), DT\_UINT16\(u16\), DT\_INT32\(s32\), DT\_UINT32\(u32\), DT\_INT64\(s64\), DT\_UINT64\(u64\), DT\_BOOL\(bool\), DT\_COMPLEX32\(c32\), DT\_COMPLEX64\(c64\).
>- The operator precision promotion on the current AI Core engine does not support the DT\_DOUBLE type and the DT\_COMPLEX128 type. Example: When the data types of the input parameters of the Mul operator are \(float32, double\) respectively, the inputs that cannot be promoted to double run on the AI Core engine and are assigned to the AI CPU engine.
>- In the table, the header row and the leftmost column represent the two input data types to be inferred, and the corresponding cell represents the inferred data type.
>- × indicates that the two data types cannot be used for inference computation.

## Deterministic Computing

In operator implementation, asynchronous multi-thread execution causes the order of floating-point accumulation to change. As a result, an operator may produce different results across multiple executions on the same hardware and with the same input. When deterministic computing is enabled, the operator produces the same output across multiple executions on the same hardware and with the same input.

The following operators are related to the deterministic computing feature. If an operator is not listed in the corresponding specification list, the current chip version does not support that operator.

- The following operators are involved but do not support deterministic computing:
  - resizegradD
  - WeightQuantBatchMatmulV2

- The following operators are involved and support deterministic computing:
  - AvgPool3DGrad
  - BatchMatMul
  - BatchMatMulV2
  - BiasAddGrad
  - BinaryCrossEntropy
  - BN3DTrainingReduce
  - BN3DTrainingUpdateGrad
  - BNTrainingReduce
  - BNTrainingUpdateGrad
    <!-- npu="A3,910b,910" id1 -->
  - Conv2DBackpropFilter: This operator is supported only on <term>Atlas training products</term>, <term>Atlas A2 products</term>, and <term>Atlas A3 products</term>.
    <!-- end id1 -->
    <!-- npu="A3,910b,910" id2 -->
  - Conv3DBackpropFilter: This operator is supported only on <term>Atlas training products</term>, <term>Atlas A2 products</term>, and <term>Atlas A3 products</term>.
    <!-- end id2 -->
  - EmbeddingDenseGrad
  - FullyConnection
  - GroupNormGrad
  - Histogram
  - InplaceIndexAdd
  - KLDiv
  - LpNormReduceV2
  - LpNormV2
  - MseLoss
  - MatMul
  - MatMulV2
  - NLLLoss
  - ReduceMean
  - ReduceSum
  - ScatterAdd
  - ScatterElements
  - ScatterNd
  - ScatterNdAdd
  - UnsortedSegmentSum
