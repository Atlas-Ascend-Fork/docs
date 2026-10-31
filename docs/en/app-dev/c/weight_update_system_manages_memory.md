# Weight Update (System-Managed Memory)

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:42:26.906Z pushedAt=2026-10-26T03:10:39.444Z nl=2 -->

## API Call Process

For the weight update scenario, to allow users to dynamically update weights during model execution after compiling the model once, the following APIs can be used together to implement this function:

1. Compile and save the model based on the graph construction APIs. The model contains multiple graphs, such as the inference graph, variable initialization graph, and variable update graph.

    Here, call the **aclgrphBundleBuildModel** API to compile the model and the **aclgrphBundleSaveModel** API to save the model. For details about the APIs, see "API Reference \> C++ APIs \> aclgrph APIs \> aclgrphBundleBuildModel" and "API Reference \> C++ APIs \> aclgrph APIs \> aclgrphBundleSaveModel" in [Graph Development](https://gitcode.com/cann/ge/blob/9.2.0/docs/en/user_guides/graph_dev/README.md).

    Weight initialization is an optional step. Users determine whether to include the weight initialization graph based on the service scenario. If it is not included, the device memory required for model loading can be saved.

2. Call the **aclmdlBundleLoadFromFile** or **aclmdlBundleLoadFromMem** API to load the model.
3. Call the **aclmdlBundleGetModelId** API to obtain the graph ID.
4. Based on the weight initialization graph ID, call the model execution API (for example, **aclmdlExecute**) to execute the weight initialization graph.
5. If the weights need to be updated, call the **aclmdlSetDatasetTensorDesc** API to set the tensor description of the graph before executing the weight update graph.
6. Based on the weight update graph ID, call the model execution API (for example, **aclmdlExecute**) to execute the weight update graph.
7. Based on the inference graph ID, call a model execution API (for example, **aclmdlExecute**) to execute the inference graph.
8. After inference is complete, call the **aclmdlBundleUnload** API to unload the model.

## Sample Code

The following sample code show the key steps of model inference. They are for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

```cpp
// 1. Initialize resources.
aclInit(nullptr);
aclrtSetDevice(0);

// 2. Load the model built by the graph construction API. The model contains an inference graph, a weight initialization graph, and a weight update graph. The model file name is bundle.om as an example.
uint32_t bundle_id = 0;
aclmdlBundleLoadFromFile("./bundle.om", &bundle_id);

// 3. Obtain the number of executable graphs based on bundleId.
size_t modelNum = 0;
aclmdlBundleGetModelNum(bundle_id, &modelNum);

// Here, modelNum=3 is used as an example, that is, the aclgrphBundleBuildModel API takes three graphs as input, and the index of each graph is fixed, namely 0, 1, and 2.
uint32_t infer_id= 0;
aclmdlBundleGetModelId(bundle_id, 0, &infer_id);
uint32_t init_id= 0;
aclmdlBundleGetModelId(bundle_id, 1, &init_id);
uint32_t update_id= 0;
aclmdlBundleGetModelId(bundle_id, 2, &update_id);

// If weight update is not required, execute the weight initialization graph and the inference graph.
// 4. Execute the weight initialization graph. For preparing model inputs and outputs, see the example code in other inference feature sections under Model Inference.
aclmdlExecute(init_id, init_mdl_input, init_mdl_output);

// 5. Execute the inference graph. For preparing model inputs and outputs, see the example code in other inference feature sections under Model Inference.
aclmdlExecute(infer_id, infer_mdl_input, infer_mdl_output);

// If weights need to be updated, execute the weight update graph before the inference graph.
// 6. Execute the weight update graph.
// If a weight does not need to be updated, for example, the 0th one, an empty tensor can be passed for shape, but the device memory must be valid.
size_t no_need_refresh_index = 0;
std::vector<int64_t> dims{0};
// An element value of 0 in the dims array indicates an empty tensor.
auto tensorDesc = aclCreateTensorDesc(ACL_FLOAT, dims.size(), dims.data(), ACL_FORMAT_ND);
aclmdlSetDatasetTensorDesc(update_mdl_input, tensorDesc, no_need_refresh_index);

// 7. If a weight needs to be updated, the following uses updating the 1st weight as an example.
size_t need_refresh_index = 1;
std::vector<int64_t> dims{1, 3, 224, 224};
auto tensorDesc = aclCreateTensorDesc(ACL_FLOAT, dims.size(), dims.data(), ACL_FORMAT_ND);
aclmdlSetDatasetTensorDesc(update_mdl_input, tensorDesc, need_refresh_index);

// 8. Execute the weight update graph. For details about preparing model inputs and outputs, see the example code in other inference feature sections under Model Inference.
aclmdlExecute(update_id, update_mdl_input, update_mdl_output);

// 9. Execute the inference graph. For details about preparing model inputs and outputs, see the example code in other inference feature sections under Model Inference.
aclmdlExecute(infer_id, infer_mdl_input, infer_mdl_output);

// 10. Unload the bundled model.
aclmdlBundleUnload(bundle_id);

// 11. Release resources.
aclrtResetDevice(0);
aclFinalize();
```
