# Finding Precision Loss Layers in Quantization Scenarios

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:38:24.911Z pushedAt=2026-10-26T03:10:39.436Z nl=2 -->

Currently, **only Caffe** framework models are supported. Use the precision comparison tool to find precision loss layers in quantization scenarios. The comparison mainly involves the following two steps:

1. **Locate the precision issues in the quantization phase.**

    Run the non-quantized original model (GPU/CPU) vs. the quantized original model (GPU/CPU).

2. **Locate the precision issues generated in the model conversion phase**, that is, the precision issues that occur when the quantized offline model runs on the NPU.

    Run the quantized original model (GPU/CPU) vs. the quantized offline model (with fusion rules disabled) (NPU).

**For details, see** "GPU/CPU vs NPU (Caffe Offline Inference)" in [Precision Debugging Tool](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/devaids/ModelAccuracyAnalyzer/atlasaccuracy_16_0001.html).
