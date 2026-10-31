# Accuracy-Based Automatic Quantization

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:26:02.018Z pushedAt=2026-10-26T03:10:39.412Z nl=2 -->

Accuracy-based automatic quantization is a feature provided for users who have certain requirements on quantization accuracy. It is implemented through the Python APIs provided by the AMCT tool. While ensuring the model accuracy required by users, this method automatically searches for the quantization configuration of the model and executes the **post-training quantization** process, ultimately generating a quantized model that meets the accuracy requirements.

**Currently, only the PyTorch, TensorFlow, and Caffe frameworks support accuracy-based automatic quantization. For detailed usage instructions, see [Ascend Model Compression Toolkit (AMCT)](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/devaids/amct/atlasamct_16_0001.html)**.
