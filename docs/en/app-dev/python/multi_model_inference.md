# Multi-model Cascading Inference

The basic procedure of multi-model inference is similar to that of single-model inference. For details, see [Model Management](model_management.md).

The differences are as follows:

- If you need to load more models, call the model loading API separately for each model. For details about model loading, see [Model Loading](model_load.md).
- If you need to run more models, call the model execution API separately for each model. For details about model execution, see [Model Execution](model_execute.md).

    For example, call `acl.mdl.execute` to run synchronous model inference.
