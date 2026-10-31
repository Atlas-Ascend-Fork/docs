# Model Loading

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:39:44.462Z pushedAt=2026-10-26T03:10:39.439Z nl=2 -->

This section describes the API call process of **full-network model loading**.

## API Call Process

Currently, there are **two sets of ACL APIs for model loading**. You can select the appropriate model loading API based on your programming habits and usage scenarios:

- As shown in Figure 1, for different loading methods (such as load from files and load from memory), you only need to **set the configuration parameters in the API**. This applies to various loading methods, but requires **multiple APIs to work together**, which are used to create a configuration object, set the attribute values in the object, and load the model.
- As shown in Figure 2, you need to **select different APIs** based on the loading method (such as load from files and load from memory). The operation is relatively simple, but you need to **remember the loading APIs for each method**.

    **Figure 1**  Model loading process (loading methods distinguished by configuration parameters in the API)  
    ![](figures/model_load_set_param.png "Model loading process (loading methods distinguished by configuration parameters in the API)")

    **Figure 2**  Model loading process (loading methods distinguished by different APIs)  
    ![](figures/model_load_different_APIs.png "Model loading process (loading methods distinguished by different APIs)")

The key APIs are described as follows:

- **Before model loading**, you need to first **build** an offline model (**\*.om file**) that is adapted to the AI processor. For details about how to build the model, see [Model Building](model_build.md).
- When memory is managed by the user, to avoid wasting memory, you need to call the **aclmdlQuerySize** API to **query** the sizes of the **working memory** and **weight memory** required for model running before allocating the working memory and weight memory.

    If the shape of the model input data is uncertain, you cannot call the **aclmdlQuerySize** API to query the memory size. In this case, the memory cannot be managed by the user when loading the model, so you need to select a model loading API in which memory is managed by the system (for example, **aclmdlLoadFromFile**).

    If you build your own network by calling the graph construction API when building the model, and no offline OM model file is generated but the model data is stored in memory, you cannot query the memory size by calling the **aclmdlQuerySize** API. For details about the graph construction API, see [Graph Development](https://gitcode.com/cann/ge/blob/9.2.0/docs/en/user_guides/graph_dev/README.md).

- The following methods are supported for **model loading**. After the model is loaded successfully, a model ID that identifies the model is returned:
    - When **aclmdlSetConfigOpt** and **aclmdlLoadWithConfig** are used, the attributes in the configuration object are used to distinguish whether the model is loaded from a file or from memory, and whether the memory is managed internally by the system or by the user.
    - When the following APIs are used, the API used determines whether the model is loaded from a file or from memory, and whether the memory is managed internally by the system or by the user.
        - **aclmdlLoadFromFile**: loads offline model data from a file, with the memory managed internally by the system.
        - **aclmdlLoadFromMem**: loads offline model data from memory, with the memory for model running managed internally by the system.
        - **aclmdlLoadFromFileWithMem**: loads offline model data from a file, with the memory for model running managed by the user (including working memory and weight memory; the working memory is used for temporary data during model execution, and the weight memory is used to store weight data).
        - **aclmdlLoadFromMemWithMem**: loads offline model data from memory, with the memory for model running managed by the user (including working memory and weight memory).

## Sample Code

The following uses loading a model from a file with the memory managed by the user as an example. After the model is loaded successfully, an ID that identifies the model is returned. This ID is required during [model execution](model_execute.md).

The following sample code shows the key steps. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

<!-- npu="950,A3,910b,910,310p,310b" id1 -->
You can click [resnet50\_imagenet\_classification](https://gitcode.com/cann/ge/tree/9.2.0/examples/acl/1_sample_resnet50_imagenet_classification) to obtain the sample code.
<!-- end id1 -->

```cpp
// 1. Initialize variables.
// Here, .. indicates a relative path, relative to the directory where the executable file resides.
// For example, if the compiled executable file is stored in the out directory, .. here indicates the parent directory of the out directory.
const char* omModelPath = "../model/resnet50.om";
// ......

// 2. Obtain the weight memory size and working memory size required for model execution based on the model file.
aclError ret = aclmdlQuerySize(omModelPath, &modelMemSize_, &modelWeightSize_);

// 3. Allocate the working memory on the device for model execution based on the working memory size.
ret = aclrtMalloc(&modelMemPtr_, modelMemSize_, ACL_MEM_MALLOC_HUGE_FIRST);

// 4. Allocate the weight memory on the device for model execution based on the weight memory size.
ret = aclrtMalloc(&modelWeightPtr_, modelWeightSize_, ACL_MEM_MALLOC_HUGE_FIRST);

// 5. Load the offline model file. The memory (including weight memory and working memory) used for model running is managed by the user.
// The model is loaded successfully, and the ID identifying the model is returned.
ret = aclmdlLoadFromFileWithMem(omModelPath, &modelId_, modelMemPtr_, modelMemSize_, modelWeightPtr_, modelWeightSize_);

// ......
```
