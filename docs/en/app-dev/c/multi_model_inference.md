# Multi-Model Serial Inference

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:22:09.679Z pushedAt=2026-10-22T06:04:43.394Z nl=2 -->

The basic process of multi-model inference is similar to that of single-model inference. For details, see [Static Shape Model Inference](static_shape_model_inference.md).

The differences between multi-model inference and single-model inference in the use of ACL APIs are as follows:

- For model loading, if multiple models are involved, call the model loading API multiple times. For details about model loading, see [Model Loading](model_load.md).
- For model execution, if multiple models are involved, call the model execution API multiple times. For details about model execution, see [Model Execution](model_execute.md).
