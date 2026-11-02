# Model Loading

Load the model generated according to [Model Building](model_construction.md) and prepare for model execution.

## API Call Sequence

If network-wide model inference is involved during application development, the application must contain the code logic for model loading. For details about the API call sequence for model loading, see [API Calling Process](interface_calling_process.md) and then the process description in this section.

This section describes the API call sequence for **network-wide model loading**. For details about operator model loading and execution, see the description of [Single-Operator Calling](single_operator_invoke.md).

pyACL provides two sets of model loading APIs for you to choose from based on use cases.

- Figure 1: Select different APIs according to different loading modes (such as loading from a file or from the memory). The operation is relatively simple, but you need to remember the loading APIs of various modes.
- Figure 2: You only need to set configuration parameters in APIs for different loading modes (such as loading from a file or from the memory). This has a wider application scope, but multiple APIs need to be used together to create configuration objects, set attribute values in objects, and load models, respectively.

**Figure 1** Model loading workflow (using different model loading APIs)
![](figures/model-loading-workflow-(using-different-model-loading-apis).png)

**Figure 2** Model loading workflow (setting parameters in the model loading API)
![](figures/model-loading-workflow-(setting-parameters-in-the-model-loading-api).png)

The key APIs are described as follows:

- Before model loading, create an offline model (*.om file) adapted to AI Processor. For details about how to create a model, see [Model Building](model_construction.md).
- If the memory is managed by the user, you need to call `acl.mdl.query_size` to query the sizes of the workspace and weight memory required for model execution to avoid memory waste.

    If the shape of the model input data is uncertain, `acl.mdl.query_size` cannot be called to query the memory size. As a result, the memory cannot be managed by the user during model loading. Therefore, you need to select the model loading APIs (such as `acl.mdl.load_from_file` and `acl.mdl.load_from_mem`) whose memory is managed by the system.

- A model can be loaded using the following APIs. A model ID is returned after the model is successfully loaded.
    - When using different model loading APIs, the caller can determine whether to load the model from a file or from memory and whether the memory is managed by the system or the user:
        - `acl.mdl.load_from_file`: loads offline model data from a **file**. The memory for running the model is managed by the system.
        - `acl.mdl.load_from_mem`: loads offline model data from **memory**. The memory for running the model is managed by the system.
        - `acl.mdl.load_from_file_with_mem`: loads offline model data from a **file**. The memory (including the workspace for storing temporary data at model runtime and weight memory for storing the weight data of the model) is **managed by the user**.
        - `acl.mdl.load_from_mem_with_mem`: loads offline model data from the **memory**. The memory (including the workspace and weight memory) is **managed by the user**.

    - When setting parameters in the model loading APIs, such as `acl.mdl.set_config_opt` and `acl.mdl.load_with_config`, the caller determines whether to load the model from a file or from memory and whether the memory is managed by the system or the user by setting the attributes in the configuration object.

## Sample Code

After the model is loaded successfully, the ID of the model is returned and will be used in [Model Execution](model_execute.md).

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
# Initialize variables.
model_path = "./model/resnet50.om"
# ......

# Load the offline model file (adapted to Ascend AI Processor). The memory (including the weight memory and working memory) required for model execution is managed by the system.
# Successful model loading returns a model ID.
model_id, ret = acl.mdl.load_from_file(model_path)

# ......
```
