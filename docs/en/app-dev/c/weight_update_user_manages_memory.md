# Weight Update (User-Managed Memory)

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:37:05.001Z pushedAt=2026-10-22T08:58:39.433Z nl=2 -->

## API Call Process

For the weight update scenario, to allow users to dynamically update weights during model execution after compiling the model once, the following APIs can be used together to implement this function:

1. Compile and save the model based on the graph construction APIs. The model contains multiple graphs, such as the inference graph, variable initialization graph, and variable update graph.

    Here, call the **aclgrphBundleBuildModel** API to compile the model and the **aclgrphBundleSaveModel** API to save the model. For details about these APIs, see "API Reference \> C++ Language APIs \> aclgrph APIs \> aclgrphBundleBuildModel" and "API Reference \> C++ Language APIs \> aclgrph APIs \> aclgrphBundleSaveModel" in *Graph Development*.

    Weight initialization is an optional step. Users determine whether to include the weight initialization graph based on the service scenario. If it is not included, the device memory required for model loading can be saved.

2. Call the **aclmdlBundleQueryInfoFromFile** or **aclmdlBundleQueryInfoFromMem** API to obtain the model description information.
3. Call the **aclmdlBundleGetQueryModelNum** API to obtain the total number of graphs in the bundled model.
4. Call the **aclmdlBundleGetVarWeightSize** and **aclmdlBundleGetSize** APIs to obtain the memory information required by the model, including the refreshable weight size, and the working memory size and weight memory size required by each graph.
5. Call the **aclmdlBundleInitFromFile** or **aclmdlBundleInitFromMem** API to initialize the model.
6. Call the **aclmdlBundleLoadModelWithMem** API multiple times based on the index to load graphs. This API supports passing in the allocated working memory and weight memory to obtain the **modelId** of the corresponding graph.
7. Based on the **modelId** of the weight initialization graph, call the model execution API (for example, **aclmdlExecute**) to execute the weight initialization graph.
8. If the weights need to be updated, call **aclmdlSetDatasetTensorDesc** to set the tensor description of the graph before executing the weight update graph.
9. Based on the **modelId** of the weight update graph, call the model execution API (for example, **aclmdlExecute**) to execute the weight update graph.
10. Based on the **modelId** of the inference graph, call the model execution API (for example, **aclmdlExecute**) to execute the inference graph.
11. After inference is complete, call **aclmdlBundleUnloadModel** to unload the graph first, and then call **aclmdlBundleUnload** to unload the model.

## Sample Code

The following sample code shows the key steps of model inference. It cannot be directly copied, compiled, and run, and are for reference only. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

```cpp
// 1. Initialize resources.
aclInit(nullptr);
aclrtSetDevice(0);

// 2. Query the memory information of the model built through the graph construction API. The model contains an inference graph, a weight initialization graph, and a weight update graph. The model file name bundle.om is used as an example.
aclmdlBundleQueryInfo *query_info = aclmdlBundleCreateQueryInfo();
aclmdlBundleQueryInfoFromFile("./bundle.om", query_info);

// 3. Obtain the total number of graphs and memory information in the model based on the queried information.
size_t modelNum = 0;
aclmdlBundleGetQueryModelNum(query_info, &modelNum);
// Obtain the size of the refreshable weights required by the model and allocate memory (optional; if not applied for, the system applies for it internally).
size_t variableWeightSize = 0;
aclmdlBundleGetVarWeightSize(query_info, &variableWeightSize);
void *var_p = nullptr;
aclrtMalloc(&var_p, variableWeightSize, ACL_MEM_MALLOC_NORMAL_ONLY);
// Here, modelNum=3 is used as an example, that is, the aclgrphBundleBuildModel API takes three graphs as input, and the index of each graph is fixed, namely 0, 1, and 2.
// Obtain the working memory and weight memory sizes required by the inference graph with index 0 and allocate them (optional; if not applied for, the system applies for them internally).
size_t inferWorkSize, inferConstWeightSize;
aclmdlBundleGetSize(query_info, 0, &inferWorkSize, &inferConstWeightSize);
void *inferWorkPtr = nullptr;
aclrtMalloc(&inferWorkPtr, inferWorkSize, ACL_MEM_MALLOC_NORMAL_ONLY);
void *inferConstWeightPtr = nullptr;
aclrtMalloc(&inferConstWeightPtr, inferConstWeightSize, ACL_MEM_MALLOC_NORMAL_ONLY);

// 4. Initialize bundle.om.
uint32_t bundle_id = 0;
// If the system allocates them internally, pass nullptr at var_p and 0 at variableWeightSize.
aclmdlBundleInitFromFile("./bundle.om", var_p, variableWeightSize, &bundle_id);

// 5. Load graphs on demand by index.
uint32_t infer_id= 0;
// If the system allocates them internally, use aclmdlBundleLoadModelWithMem(bundle_id, 0, nullptr, 0, nullptr, 0, &init_id);
aclmdlBundleLoadModelWithMem(bundle_id, 0, inferWorkPtr, inferWorkSize,inferConstWeightPtr, inferConstWeightSize, &infer_id);
uint32_t init_id= 0;
aclmdlBundleLoadModelWithMem(bundle_id, 1, nullptr, 0, nullptr, 0, &init_id);
uint32_t update_id= 0;
aclmdlBundleLoadModelWithMem(bundle_id, 2, nullptr, 0, nullptr, 0, &update_id);

// If weight update is not required, execute the weight initialization graph and the inference graph.
// 6. Execute the weight initialization graph. For preparing model inputs and outputs, see the example code in other inference feature sections under Model Inference.
aclmdlExecute(init_id, init_mdl_input, init_mdl_output);

// 7. Execute the inference graph. For preparing model inputs and outputs, see the example code in other inference feature sections under Model Inference.
aclmdlExecute(infer_id, infer_mdl_input, infer_mdl_output);

// If weight update is required, execute the weight update graph first, and then execute the inference graph.
// 8. Execute the weight update graph.
// If a weight does not need to be updated, for example, the 0th one, an empty tensor can be passed for shape, but the device memory must be valid.
size_t no_need_refresh_index = 0;
std::vector<int64_t> dims{0};
// An element value of 0 in the dims array indicates an empty tensor.
auto tensorDesc = aclCreateTensorDesc(ACL_FLOAT, dims.size(), dims.data(), ACL_FORMAT_ND);
aclmdlSetDatasetTensorDesc(update_mdl_input, tensorDesc, no_need_refresh_index);

// 9. If a weight needs to be updated, the following uses updating the 1st weight as an example.
size_t need_refresh_index = 1;
std::vector<int64_t> dims{1, 3, 224, 224};
auto tensorDesc = aclCreateTensorDesc(ACL_FLOAT, dims.size(), dims.data(), ACL_FORMAT_ND);
aclmdlSetDatasetTensorDesc(update_mdl_input, tensorDesc, need_refresh_index);

// 10. Execute the weight update graph. For preparing model inputs and outputs, see the sample code in other inference feature sections under Model Inference.
aclmdlExecute(update_id, update_mdl_input, update_mdl_output);

// 11. Execute the inference graph. For preparing model inputs and outputs, see the sample code in other inference feature sections under Model Inference.
aclmdlExecute(infer_id, infer_mdl_input, infer_mdl_output);

// 12. Unload the model.
aclmdlBundleUnloadModel(bundle_id, infer_id);
aclmdlBundleUnloadModel(bundle_id, init_id);
aclmdlBundleUnloadModel(bundle_id, update_id);
aclmdlBundleUnload(bundle_id);

// 13. Release resources.
aclrtResetDevice(0);
aclFinalize();
```
