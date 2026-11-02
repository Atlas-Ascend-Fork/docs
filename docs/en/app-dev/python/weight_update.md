<!-- npu="950,A3,910b,910,310p,310b" id1 -->
# Weight Update

## API Call Sequence

In the weight update scenario, you can call the following APIs to dynamically update the weight during model execution after the model is built:

1. Build and save the model in graph mode. The model contains the inference graph, weight initialization graph, and weight update graph.

    Call the `aclgrphBundleBuildModel` API (see "API Reference > C++ APIs > aclgrph APIs > aclgrphBundleBuildModel") to build the model and call the `aclgrphBundleSaveModel` API (see "API Reference > C++ APIs > aclgrph APIs > aclgrphBundleSaveModel") to save the model. For details about the APIs, see *Graph Development*.

    Weight initialization is optional. You can determine whether to include the weight initialization graph based on the service scenario. If the weight initialization graph is not included, the device memory required for model loading can be saved.

2. Call `acl.mdl.bundle_load_from_file` or `acl.mdl.load_from_mem` to load the model.
3. Call `acl.mdl.bundle_get_model_id` to obtain the IDs of three graphs.
4. Call the model execution API (for example, `acl.mdl.execute`) to execute the weight initialization graph based on the graph ID.
5. To update the weight, call `acl.mdl.set_dataset_tensor_desc` to set the tensor description of the graph before updating the weight.
6. Update the graph based on the weight update graph ID and call the model execution API (for example, `acl.mdl.execute`) to update the weight graph.
7. Call the model execution API (for example, `acl.mdl.execute`) to execute the inference graph based on the inference graph ID.
8. After the inference is complete, call `acl.mdl.bundle_unload` to unload the model.

## Sample Code

This section focuses on the code logic of model inference. For details about how to perform initialization and deinitialization, see [Initialization and Deinitialization](initialization_and_deinitialization.md). For details about how to allocate and deallocate runtime resources, see [Runtime Resource Allocation and Deallocation](runtime_resource_allocation_and_release.md).

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to be built or run.

```python
# 1. Initialize resources.
ret = acl.init(config_path)
ret = acl.rt.set_device(device_id)

# 2. Load the model built in graph mode. The model contains the inference graph, weight initialization graph, and weight update graph. The model file bundle.om is used as an example.
bundle_id, ret = acl.mdl.bundle_load_from_file("./bundle.om")

# 3. Obtain the ID of each graph in the model.
model_num, ret = acl.mdl.bundle_get_model_num(bundle_id)

# The input parameters of aclgrphBundleBuildModel are three images with fixed IDs.
infer_id, ret = acl.mdl.bundle_get_model_id(bundle_id, 0)
init_id, ret = acl.mdl.bundle_get_model_id(bundle_id, 1)
update_id, ret = acl.mdl.bundle_get_model_id(bundle_id, 2)

# If the weight does not need to be updated, execute the weight initialization graph and inference graph.
# 4. Execute the weight initialization graph. For details about how to prepare the model input and output, see the sample code in other sections about inference features under "Model Inference".
ret = acl.mdl.execute(init_id, init_mdl_input, init_mdl_output)

# 5. Execute the inference graph. For details about how to prepare the model input and output, see the sample code in other sections about inference features under "Model Inference".
ret = acl.mdl.execute(infer_id, infer_mdl_input, infer_mdl_output)

# If a weight needs to be updated, update the weight before executing the inference graph.
# 6. Execute the weight update graph.
# If a weight does not need to be updated, for example, the 0th weight, the shape can be passed as an empty tensor, but the device memory must be valid.
no_need_refresh_index = 0
dims = [0]
# If the elements in the dims array are 0, the tensor is empty.
tensor_desc = acl.create_tensor_desc(data_type, dims, format)
update_mdl_input, ret = acl.mdl.set_dataset_tensor_desc(update_mdl_input, tensor_desc, no_need_refresh_index)

# The following is an example of updating the first weight.
need_refresh_index = 1
dims = [1, 3, 224, 224]
tensor_desc = acl.create_tensor_desc(data_type, dims, format)
update_mdl_input, ret = acl.mdl.set_dataset_tensor_desc(update_mdl_input, tensor_desc, need_refresh_index)

# 7. Execute the weight update graph. For details about how to prepare the model input and output, see the sample code in other sections about inference features under "Model Inference".
ret = acl.mdl.execute(update_id, update_mdl_input, update_mdl_output)

# 8. Execute the inference graph. For details about how to prepare the model input and output, see the sample code in other sections about inference features under "Model Inference".
ret = acl.mdl.execute(infer_id, infer_mdl_input, infer_mdl_output)

# 9. Unload the bundle model.
ret = acl.mdl.unload(bundle_id)

# 10. Destroy allocations.
ret = acl.rt.reset_device(0)
ret = acl.finalize()
```
<!-- end id1 -->
