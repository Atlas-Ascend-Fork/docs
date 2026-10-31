# Dynamic Shape Input (Setting the Shape Range)

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:36:03.919Z pushedAt=2026-10-26T03:10:39.433Z nl=2 -->

This section describes how to set the shape range in dynamic shape input scenarios, including the key APIs, the API call process, and sample code.

## API Call Process

If the model input shape is dynamic, call **aclmdlSetDatasetTensorDesc** to set the tensor description information (mainly the shape information) of the input before model execution. After model execution, call **aclmdlGetDatasetTensorDesc** to obtain the tensor description information of the model's dynamic output, and then call the operation APIs under **aclTensorDesc** to obtain the memory size occupied by the output tensor data, the format information of the tensor, and the dimension information of the tensor.

The key principles are described as follows:

1. Build the model.

    In model inference scenarios, for input data with dynamic shape, when converting the model using the ATC tool, set the input shape range through the input\_shape parameter. For details about the parameters, see "Command Line Options \> Basic Options \> Input Options \> --input\_shape”" in [Ascend Tensor Compiler (ATC)](https://gitcode.com/cann/ge/blob/9.2.0/docs/en/user_guides/atc_tools/README.md).

2. Load the model.

    For details about the model loading process, see [Model Loading](model_load.md). After the model is loaded successfully, an ID identifying the model is returned.

3. Create data of the **aclmdlDataset** type to describe the input and output of model execution.

    For details about the call process, see [Preparing the Input/Output Data Structure for Model Execution](model_execute.md#section1620016465510).

    Note the following points:

    - When the size obtained by calling **aclmdlGetInputSizeByIndex** is **0**, the shape of the input is dynamic. You can estimate a larger input memory based on the actual situation.
    - When the size obtained by calling **aclmdlGetOutputSizeByIndex** is **0**, the shape of the output is dynamic. You can estimate a larger output memory based on the actual situation, or let the system internally allocate the output memory of the corresponding index. For details, see the **aclmdlGetOutputSizeByIndex** API.

4. After the model is successfully loaded and before the model is executed, call **aclmdlSetDatasetTensorDesc** to set the tensor description information (mainly the shape information) of the dynamic shape input.

    When calling **aclCreateTensorDesc** to create the tensor description information, set the shape information, including the number of dimensions and the dimension size. The number of dimensions and the dimension size set here must be within the input shape range set during model building. For details about model building, see [Model Building](model_build.md).
<a id="li187839613215"></a>
5. (Optional) Create an allocator descriptor and register the allocator.

    **Note**: Currently, an external allocator can be used to manage memory only in dynamic shape model inference scenarios. The API for registering the allocator must be used together with **aclmdlExecuteAsync**, and must be called before **aclmdlExecuteAsync**.

    1. Call **aclrtAllocatorCreateDesc** to create the allocator descriptor.
    2. Call **aclrtAllocatorSetObjToDesc**, **aclrtAllocatorSetAllocFuncToDesc**, **aclrtAllocatorSetGetAddrFromBlockFuncToDesc**, and **aclrtAllocatorSetFreeFuncToDesc** to set the allocator object and callback functions.
    3. Call **aclrtAllocatorRegister** to register the allocator and bind the allocator to a stream. The same stream must be used during model execution.
    4. After the allocator is registered, call **aclrtAllocatorDestroyDesc** to destroy the allocator descriptor.

6. Execute the model.
    - The synchronous inference scenario is supported, for example, by calling the **aclmdlExecute** API.
    - The asynchronous inference scenario is also supported, for example, by calling the **aclmdlExecuteAsync** API. However, in the asynchronous scenario, you need to call a stream synchronization API (for example, **aclrtSynchronizeStream**) to confirm that the asynchronous task is complete.

        In the asynchronous inference scenario, only the **aclmdlExecuteAsync** API currently supports the use of the user-registered allocator, that is, the allocator registered in step [5](#li187839613215).

7. Obtain the result data of model execution.

    Call the **aclmdlGetDatasetTensorDesc** API to obtain the tensor description information of the dynamic shape output, and then use the operation APIs of the **aclTensorDesc** data type to obtain the attributes of the tensor description information. Here, **size** (indicating the space occupied by the tensor data) is used as an example, and then the data of the corresponding size is read from the memory.

8. (Optional) If an allocator is registered in [5](#li187839613215), unregister and destroy the registered allocator here.

    The user-registered allocator is bound to a stream. To proactively release and destroy the allocator, call **aclrtAllocatorUnregister** to unregister it before releasing the stream, and then release the stream resources and destroy the user's allocator.

## Synchronous Inference Sample Code

The following sample code shows the key steps of model inference. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

```cpp
......

// In this example, assume that the first input of the model is a dynamic input with index 0, and the first output of the model is a dynamic output with index 0.

// 1. Load the model. After the model is loaded, set the tensor description information of the dynamic input, mainly the shape information of the dynamic input.
......

// 2. Prepare the model description information modelDesc_, the model input data input_, and the model output data output_.
// Note the following:
// If the size obtained by aclmdlGetInputSizeByIndex is 0, the shape of the input is dynamic. You can estimate a larger input memory based on the actual situation.
// If the size obtained by aclmdlGetOutputSizeByIndex is 0, the shape of the output is dynamic. You can estimate a larger output memory based on the actual situation.
// ......

// 3. Custom function: set the tensor description information of the dynamic input.
void SetTensorDesc()
{
        // ......
        // Create the tensor description information.
        // The shape must be consistent with the shape of the given input data.
    int64_t shapes[4] = {1, 3, 224, 224};
    aclTensorDesc *inputDesc = aclCreateTensorDesc(ACL_FLOAT, 4, shapes, ACL_FORMAT_NCHW);
    // Set the tensor description information of the dynamic input with index 0.
    aclError ret = aclmdlSetDatasetTensorDesc(input_, inputDesc, 0);
        // ......
}
// 4. Custom function: execute the model and obtain the tensor description information of the dynamic output.
void ModelExecute()
{
    aclError ret;
    // Call the custom API to set the tensor description information of the dynamic input.
    SetTensorDesc();
        // Execute the model.
    ret = aclmdlExecute(modelId, input_, output_);
    // Obtain the tensor description information of the dynamic output with index 0.
        aclTensorDesc *outputDesc = aclmdlGetDatasetTensorDesc(output_, 0);
    // Use the operation APIs of the aclTensorDesc data type to obtain the attributes of outputDesc. Here, obtain size (the space occupied by the tensor data), and then read the data of the corresponding size from the memory
    string outputFileName = ss.str();
        FILE *outputFile = fopen(outputFileName.c_str(), "wb");
    size_t outputDesc_size = aclGetTensorDescSize(outputDesc);
        aclDataBuffer *dataBuffer = aclmdlGetDatasetBuffer(output_, 0);
        void *data = aclGetDataBufferAddr(dataBuffer);
    void *outHostData = nullptr;
        // Call aclrtGetRunMode to obtain the running mode of the software stack, and determine whether to transfer data based on the running mode.
        aclrtRunMode runMode;
        ret = aclrtGetRunMode(&runMode);
        if (runMode == ACL_HOST) {
            ret = aclrtMallocHost(&outHostData, outputDesc_size);
       // Because the memory allocated for the dynamic shape is relatively large while the actual data size is outputDesc_size, use the actual data size to copy the memory here.
        ret = aclrtMemcpy(outHostData, outputDesc_size, data, outputDesc_size, ACL_MEMCPY_DEVICE_TO_HOST);
        fwrite(outHostData, outputDesc_size, sizeof(char), outputFile);
            ret = aclrtFreeHost(outHostData);
    } else {
        // if app is running in host, write model output data into result file
                fwrite(data, outputDesc_size, sizeof(char), outputFile);
    }
    fclose(outputFile);
        // ......
}

// 5. Process the model inference result.
......
```

## Asynchronous Inference Sample Code

The example in this section focuses on the code logic of model inference. In the example scenario, the user registers an allocator and calls the asynchronous API **aclmdlExecuteAsync** to perform inference.

After the API is called, exception handling branches must be added, and error logs and prompt logs must be recorded. These are not listed one by one here. The following is sample code of the key steps. It cannot be directly copied, compiled, and run, and is for reference only.

```cpp
......

// The sample code is for process reference only. In actual application scenarios, check the return values.
// In this example, assume that the first input of the model is a dynamic input with index 0, and the first output of the model is a dynamic output with index 0.

// 1. Load the model. After the model is loaded, set the tensor description information of the dynamic input, mainly the shape information of the dynamic input.
......

// 2. Prepare the model description information modelDesc_, the model input data input_, and the model output data output_.
// Note the following:
// If the size obtained by aclmdlGetInputSizeByIndex is 0, the shape of the input is dynamic. You can estimate a larger input memory based on the actual situation.
// If the size obtained by aclmdlGetOutputSizeByIndex is 0, the shape of the output is dynamic. You can estimate a larger output memory based on the actual situation.
// ......

// 3. Custom function to set the tensor description information of the dynamic input.
void SetTensorDesc()
{
        // ......
        // Create the tensor description information.
        // The shape must be consistent with the shape of the given input data.
    int64_t shapes = {1, 3, 224, 224};
    aclTensorDesc *inputDesc = aclCreateTensorDesc(ACL_FLOAT, 4, shapes, ACL_FORMAT_NCHW);
    // Set the tensor description information of the dynamic input with index 0.
    aclError ret = aclmdlSetDatasetTensorDesc(input_, inputDesc, 0);
        // ......
}

// 4. Create the allocator descriptor and register the allocator.
// Assume that allocator is the Allocator object that the user wants to register.
void RegisterCustomAllocator(aclrtAllocator allocator, aclrtStream stream) {
    // 6.1 Create AllocatorDesc.
    aclrtAllocatorDesc allocatorDesc = aclrtAllocatorCreateDesc();
    // 6.2 Initialize AllocatorDesc and set the callback functions for allocator memory allocation and release. CustomMallocFunc, CustomFreeFunc, CustomMallocAdviseFunc, and CustomGetBlockAddrFunc are callback functions defined in the "C" style and are passed to AllocatorDesc as function pointers.
    aclrtAllocatorSetObjToDesc(allocatorDesc, allocator);
    aclrtAllocatorSetAllocFuncToDesc(allocatorDesc, CustomMallocFunc);
    aclrtAllocatorSetFreeFuncToDesc(allocatorDesc, CustomFreeFunc);
    aclrtAllocatorSetAllocAdviseFuncToDesc(allocatorDesc, CustomMallocAdviseFunc);
    aclrtAllocatorSetGetAddrFromBlockFuncToDesc(allocatorDesc, CustomGetBlockAddrFunc);
    // Register the allocator and bind it to the stream. The API creates the allocator based on AllocatorDesc.
    aclrtAllocatorRegister(stream, allocatorDesc);
    // After the allocator descriptor is used, it can be destroyed directly.
    aclrtAllocatorDestroyDesc(allocatorDesc);
}


// 5. Custom function: execute the model and obtain the tensor description information of the dynamic output.
void ModelExecute(aclrtStream stream)
{
    aclError ret;
    // Call the custom API to set the tensor description information of the dynamic input.
    SetTensorDesc();
       // Execute the model. Only the asynchronous API supports using the user-registered allocator, and the execution stream must be the same as the stream bound to the registered allocator.
    ret = aclmdlExecuteAsync(modelId, input_, output_, stream);
       // A successful call to the asynchronous API only indicates that the task has been delivered. Before obtaining the result, call the synchronization wait API to ensure that the task has been executed.
        aclrtSynchronizeStream(stream);
       // Obtain the tensor description information of the dynamic output with index 0.
        aclTensorDesc *outputDesc = aclmdlGetDatasetTensorDesc(output_, 0);
       // Use the operation API of the aclTensorDesc data type to obtain the attributes of outputDesc. Here, obtain size (the space occupied by the tensor data), and then read data of the corresponding size from the memory.
    string outputFileName = ss.str();
        FILE *outputFile = fopen(outputFileName.c_str(), "wb");
    size_t outputDesc_size = aclGetTensorDescSize(outputDesc);
        aclDataBuffer *dataBuffer = aclmdlGetDatasetBuffer(output_, 0);
        void *data = aclGetDataBufferAddr(dataBuffer);
    void *outHostData = nullptr;
       // Call aclrtGetRunMode to obtain the running mode of the software stack, and determine whether to transfer data based on the running mode.
        aclrtRunMode runMode;
        ret = aclrtGetRunMode(&runMode);
        if (runMode == ACL_HOST) {
            ret = aclrtMallocHost(&outHostData, outputDesc_size);
           // Because the memory allocated for the dynamic shape is relatively large while the actual data size is outputDesc_size, use the actual data size to copy the memory.
        ret = aclrtMemcpy(outHostData, outputDesc_size, data, outputDesc_size, ACL_MEMCPY_DEVICE_TO_HOST);
        fwrite(outHostData, outputDesc_size, sizeof(char), outputFile);
            ret = aclrtFreeHost(outHostData);
        } else {
        // if app is running in host, write model output data into result file
                fwrite(data, outputDesc_size, sizeof(char), outputFile);
        }
    fclose(outputFile);
        // ......
}

// 6. Process the model inference result.
......

// 7. Unregister and destroy the registered allocator.
void UnregisterCustomAllocator(aclrtStream stream) {
     aclrtAllocatorUnregister(stream);
     // Destroy the custom allocator by the user.
}

......
```
