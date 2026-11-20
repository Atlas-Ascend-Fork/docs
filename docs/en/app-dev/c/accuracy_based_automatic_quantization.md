# Accuracy-Based Automatic Quantization

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T02:29:48.696Z pushedAt=2026-10-21T02:59:41.667Z nl=2 -->

Accuracy-based automatic quantization is a feature provided for users who have certain requirements on quantization accuracy. It is implemented through the Python APIs provided by the AMCT tool. While ensuring the model accuracy required by users, this method automatically searches for the quantization configuration of the model and executes the **post-training quantization** process, ultimately generating a quantized model that meets the accuracy requirements.

**Currently, accuracy-based automatic quantization is supported only by the PyTorch, TensorFlow, and Caffe frameworks. For detailed usage guides, see [Ascend Model Compression Toolkit (AMCT)](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/devaids/amct/atlasamct_16_0001.html)**.
