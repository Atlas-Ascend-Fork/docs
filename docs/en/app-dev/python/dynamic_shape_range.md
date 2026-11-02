<!-- npu="950,A3,910b,910,310p,310b" id1 -->
# Dynamic Shape Input (Setting the Shape Range)
<!-- end id1 -->
## API Call Sequence

If the input shape of the model is dynamic, call `acl.mdl.set_dataset_tensor_desc` to set the tensor description (mainly the shape information) before the model is executed. After the model is executed, call `acl.mdl.get_dataset_tensor_desc` to obtain the tensor description information dynamically output by the model, and then call the operation APIs of the `aclTensorDesc` type to obtain the memory size occupied by the output tensor data, tensor format, and tensor dimensions.

The procedure is described as follows:

1. Build a model.

    In the model inference scenario, when the ATC tool is used to convert the dynamic-shape input, the `input_shape` parameter is used to set the input shape range.

    For details about ATC parameters, see [Ascend Tensor Compiler (ATC)](https://hiascend.com/en/document/redirect/cannCommunityATC).

2. Load the model.

    For details about the model loading workflow, see [Model Loading](model_load.md). After the model is successfully loaded, the model ID is returned.

3. Create data of the `aclmdlDataset` type to describe the input and output of model execution.

    For details about the call sequence, see [Preparing Input/Output Data Structure for Model Execution](model_execute.md).

    Notes:

    - If the size obtained by calling `acl.mdl.get_input_size_by_index` is `0`, the `input` shape is dynamic. A larger `input` buffer can be estimated based on the actual situation.
    - If the size obtained by calling `acl.mdl.get_output_size_by_index` is `0`, the output shape is dynamic. You can estimate a large output buffer as required, or let the system allocate the output buffer of the corresponding index. For details, see the `acl.mdl.get_output_size_by_index` API.

4. After a model is successfully loaded and before it is executed, call `acl.mdl.set_dataset_tensor_desc` to set the tensor description (mainly the shape information) of the dynamic shape input.

    When calling `acl.create_tensor_desc` to create a tensor description, set the shape information, including the number of dimensions and the number of elements in each dimension, which must be within the range of the input shape set during model building. For details about model building, see [Model Building](model_construction.md).

5. (Optional) Create an Allocator descriptor and register an Allocator.

    **Note**: External Allocators manages memory only for dynamic-shape model inference. The Allocator registration API must be used together with `acl.mdl.execute_async` and called before `acl.mdl.execute_async`.

    1. Call `acl.rt.allocator_create_desc` to create an Allocator descriptor.
    2. Call `acl.rt.allocator_set_obj_to_desc`, `acl.rt.allocator_set_alloc_func_to_desc`, `acl.rt.allocator_set_get_addr_from_block_func_to_desc` and `acl.rt.allocator_set_free_func_to_desc` to set the Allocator object and callback function.
    3. Call `acl.rt.allocator_register` to register the Allocator and bind the Allocator to the stream. The same stream must be used during model execution.
    4. After the Allocator is registered, call `acl.rt.allocator_destroy_desc` to destroy the Allocator descriptor.

6. Execute the model.
    - Call `acl.mdl.execute` for synchronous inference.
    - For asynchronous inference, call `acl.mdl.execute_async`, but also call the stream synchronization API (for example, `acl.rt.synchronize_stream`) to ensure that an asynchronous task completes.
        <!-- npu="910b,910,310p,310b" id3 -->
        For asynchronous inference, only `acl.mdl.execute_async` supports user-registered Allocators, that is, the Allocator registered in step 5.
        <!-- end id3 -->
7. Obtain the model execution result.

    Call `acl.mdl.get_dataset_tensor_desc` to obtain the tensor description of the dynamic shape output, and then call the API of the aclTensorDesc data type to obtain the tensor description attributes. The following describes how to obtain `size` (size of the space occupied by the tensor data) and read the data of the corresponding `size` from the memory.

8. (Optional) If an Allocator is registered in step 5, deregister and destroy registered Allocator.

    The user-registered Allocator is bound to the stream. If the Allocator needs to be released or destroyed, call `acl.rt.allocator_unregister` to cancel the registration before releasing the stream, and then release the stream resources and destroy the Allocator.

## Sample Code for Synchronous Inference

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following code snippet demonstrates key steps for reference only. Do not copy, build, or run it.

```python
# In this sample, assume that the first input of the model is dynamic with an index of 0, and the first output of the model is dynamic with also an index of 0.
# 1. Load the model. After the model is successfully loaded, set the tensor description for dynamic input, mainly the shape information.
# ......

# 2. Prepare the model description modelDesc_, and the model inputs input_ and model outputs output_.
# Pay attention to the following:
# If the size obtained by using acl.mdl.get_input_size_by_index is 0, the input shape is dynamic. A larger input buffer can be estimated based on the actual situation.
# If the size obtained by using acl.mdl.get_output_size_by_index is 0, the output shape is dynamic. A larger output buffer can be estimated based on the actual situation.
# ......

# 3. Customize a function to set the description of the dynamic input tensor.
def set_tensor_desc():
    # ......
    # Create a tensor description. You do not need to set the data type and format. It directly obtains them from the model. The default values are used here.
    # The shape must be the same as that of the specified input data.
    shapes = [1, 3, 224, 224]
    inputDesc = acl.create_tensor_desc(0, shapes, 0)

    # Set the description of the dynamic input tensor whose index is 0.
    dataset, ret = acl.mdl.set_dataset_tensor_desc(input_, inputDesc, 0)
    # ......

# 4. Customize a function, execute the model, and obtain the description of the dynamic output tensor.
def model_execute():
    # ......
    # Call a custom API to set the description of the dynamic input tensor.
    set_tensor_desc()

    # Execute the model.
    ret = acl.mdl.execute(modelId, input_, output_)

    # Obtain the description of the dynamic output tensor whose index is 0.
    outputDesc = acl.mdl.get_dataset_tensor_desc(output_, 0)

    # Use the operation API of the aclTensorDesc type to obtain the outputDesc attribute. You need to obtain size (size occupied by tensor data) as an example: Then, read the data of the corresponding size from the memory.
    outputFileName = "./output"
    outputDesc_size = acl.get_tensor_desc_size(outputDesc)
    dataBuffer = acl.mdl.get_dataset_buffer(output_, 0)
    data = acl.get_data_buffer_addr(dataBuffer)
    outHostData = None

    # Call acl.rt.get_run_mode to obtain the run mode of the software stack and determine whether to transfer data, based on the run mode.
    runMode, ret = acl.rt.get_run_mode()
    if runMode == ACL_HOST:
        ret = acl.rt.malloc_host(outHostData, outputDesc_size)

        # Since the memory allocated for the dynamic shape is large, the actual data size outputDesc_size is used to copy the memory.
        ret = acl.rt.memcpy(outHostData, outputDesc_size, data, outputDesc_size, ACL_MEMCPY_DEVICE_TO_HOST)
        with open(outputFileName, "wb") as f:
            f.write(outHostData)
        ret = acl.rt.free_host(outHostData)
    else:
        with open(outputFileName, "wb") as f:
            f.write(data)
    # ......

# 5. Process the model inference result.
# TODO
```

## Sample Code for Asynchronous Inference Scenarios

In this example, the user registers an Allocator and calls the asynchronous API `acl.mdl.execute_async` to perform inference.

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following code snippet demonstrates key steps for reference only. Do not copy, build, or run it.

```python
# In this sample, assume that the first input of the model is dynamic with an index of 0, and the first output of the model is dynamic with also an index of 0.
# 1. Load the model. After the model is successfully loaded, set the tensor description for dynamic input, mainly the shape information.
# ......

# 2. Prepare the model description modelDesc_, and the model inputs input_ and model outputs output_.
# Pay attention to the following:
# If the size obtained by using acl.mdl.get_input_size_by_index is 0, the input shape is dynamic. A larger input buffer can be estimated based on the actual situation.
# If the size obtained by using acl.mdl.get_output_size_by_index is 0, the output shape is dynamic. A larger output buffer can be estimated based on the actual situation.
# ......

# 3. Customize a function to set the description of the dynamic input tensor.
def set_tensor_desc():
    # ......
    # Create a tensor description. You do not need to set the data type and format. It directly obtains them from the model. The default values are used here.
    # The shape must be the same as that of the specified input data.
    shapes = [1, 3, 224, 224]
    inputDesc = acl.create_tensor_desc(0, shapes, 0)

    # Set the description of the dynamic input tensor whose index is 0.
    ret = acl.mdl.set_dataset_tensor_desc(input_, inputDesc, 0)
    # ......

# 4. Create an Allocator descriptor and register an Allocator.
# Assume that the allocator is the Allocator object that the user wants to register.
def register_custom_allocator(allocator, stream):
    # 4.1 Create AllocatorDesc.
    allocatorDesc = acl.rt.allocator_create_desc()
    # 4.2 Initialize AllocatorDesc and set callback functions related to allocator memory allocation and deallocation.
    acl.rt.allocator_set_obj_to_desc(allocatorDesc, allocator)
    acl.rt.allocator_set_alloc_func_to_desc(allocatorDesc, CustomMallocFunc)
    acl.rt.allocator_set_free_func_to_desc(allocatorDesc, CustomFreeFunc)
    acl.rt.allocator_set_alloc_advise_func_to_desc(allocatorDesc, CustomMallocAdviseFunc)
    acl.rt.allocator_set_get_addr_from_block_func_to_desc(allocatorDesc, CustomGetBlockAddrFunc)
    # Register the Allocator and bind it to the stream. The API is created based on AllocatorDesc.
    acl.rt.allocator_register(stream, allocatorDesc)
    # After the allocator descriptor is used, it can be destroyed.
    acl.rt.allocator_destroy_desc(allocatorDesc)

def model_execute():
    # ......
    # Call a custom API to set the description of the dynamic input tensor.
    set_tensor_desc()

    # Execute the model.
    ret = acl.mdl.execute_async(modelId, input_, output_, stream)

    # Obtain the description of the dynamic output tensor whose index is 0.
    outputDesc = acl.mdl.get_dataset_tensor_desc(output_, 0)

    # Use the operation API of the aclTensorDesc type to obtain the outputDesc attribute. You need to obtain size (size occupied by tensor data) as an example: Then, read the data of the corresponding size from the memory.
    outputFileName = "./output"
    outputDesc_size = acl.get_tensor_desc_size(outputDesc)
    dataBuffer = acl.mdl.get_dataset_buffer(output_, 0)
    data = acl.get_data_buffer_addr(dataBuffer)
    outHostData = None

    # Call acl.rt.get_run_mode to obtain the run mode of the software stack and determine whether to transfer data, based on the run mode.
    runMode, ret = acl.rt.get_run_mode()
    if runMode == ACL_HOST:
        ret = acl.rt.malloc_host(outHostData, outputDesc_size)

        # Since the memory allocated for the dynamic shape is large, the actual data size outputDesc_size is used to copy the memory.
        ret = acl.rt.memcpy(outHostData, outputDesc_size, data, outputDesc_size, ACL_MEMCPY_DEVICE_TO_HOST)
        with open(outputFileName, "wb") as f:
            f.write(outHostData)
        ret = acl.rt.free_host(outHostData)
    else:
        with open(outputFileName, "wb") as f:
            f.write(data)
    # ......

# 5. Process the model inference result.
# TODO
# 6. Deregister and destroy the registered Allocator.
def unregister_custom_allocator(stream):
   acl.rt.allocator_unregister(stream)# Destroy the customized Allocator.
```
