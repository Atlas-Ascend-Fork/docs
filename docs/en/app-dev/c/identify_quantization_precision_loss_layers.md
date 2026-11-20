# Finding Precision Loss Layers in Quantization Scenarios

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:13:56.669Z pushedAt=2026-10-22T03:23:28.540Z nl=2 -->

Currently, **only Caffe** framework models are supported. Use the precision comparison tool to find precision loss layers in quantization scenarios. The comparison mainly involves the following two steps:

1. **Locate the precision issues in the quantization phase.**

    Run the non-quantized original model (GPU/CPU) vs. the quantized original model (GPU/CPU).

2. **Locate the precision issues generated in the model conversion phase**, that is, the precision issues that occur when the quantized offline model runs on the NPU.

    Run the quantized original model (GPU/CPU) vs. the quantized offline model (with fusion rules disabled) (NPU).

**For detailed operations, see** "GPU/CPU vs NPU (Caffe Offline Inference)" in [Precision Debugging Tool](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/devaids/ModelAccuracyAnalyzer/atlasaccuracy_16_0001.html).
