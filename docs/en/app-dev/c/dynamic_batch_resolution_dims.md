# Dynamic Batch/Dynamic Resolution/Dynamic Dimension (Setting Multiple Dimension Values)

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:35:42.798Z pushedAt=2026-10-26T03:10:39.431Z nl=2 -->

This section describes the key APIs, API call process, and sample code involved in the dynamic batch, dynamic resolution, and dynamic dimension features.

## API Call Process

Model inference in the dynamic shape input scenario is similar to [static shape input model inference](static_shape_model_inference.md), both involving initialization and deinitialization, runtime resource allocation and release, model building, model loading, model execution, and model unloading.

This section focuses on the differences between model inference in the dynamic shape input scenario and [static shape input model inference](static_shape_model_inference.md):

1. **When building a model**, configure the information related to dynamic batch, dynamic resolution, and dynamic dimension (ND format):

    **If the model inference involves the dynamic batch feature**, during model inference, call the ACL API to set the batch size to be used for model inference. The batch sizes supported by the model are configured in advance when building the model. For example, when building the model, use the **dynamic\_batch\_size** parameter of the ATC tool. For details about the parameters, see "Command Line Options \> Basic Options \> Input Options \> --dynamic\_batch\_size" in [Ascend Tensor Compiler (ATC)](https://gitcode.com/cann/ge/blob/9.2.0/docs/en/user_guides/atc_tools/README.md).

    **If the model inference involves the dynamic resolution feature**, during model inference, call the ACL API to set the resolution to be used for model inference. The resolutions supported by the model are configured in advance when building the model. For example, when building the model, use the **dynamic\_image\_size** parameter of the ATC tool. For details about the parameters, see "Command Line Options \> Basic Options \> Input Options \> --dynamic\_image\_size" in [Ascend Tensor Compiler (ATC)](https://gitcode.com/cann/ge/blob/9.2.0/docs/en/user_guides/atc_tools/README.md).

    **If the model inference involves the dynamic dimension (ND format) feature**, during model inference, call the ACL API to set the dimension values to be used for model inference. The dimension values supported by the model are configured in advance when building the model. For example, when building the model, use the **dynamic\_dims parameter** of the ATC tool. For details about the parameters, see "Command Line Options \> Basic Options \> Input Options \> --dynamic\_dims”" in [Ascend Tensor Compiler (ATC)](https://gitcode.com/cann/ge/blob/9.2.0/docs/en/user_guides/atc_tools/README.md).

    After the model is built successfully, a corresponding input (hereinafter referred to as dynamic batch input/dynamic resolution input/dynamic dimension input) is added to the generated OM model. During model inference, the specific batch value/resolution/dimension value is provided through this newly added input.

    **For example**, if the batch size of input a is dynamic, an input b corresponding to a is added to the OM model to describe the batch information of a.

    - During model execution, for preparing the data structure of input a, see [Preparing the Input/Output Data Structure for Model Execution](model_execute.md#section1620016465510).

        Because the shape of the input tensor data supports multiple levels and can be determined only before model execution, it is recommended that you call the **aclmdlGetInputSizeByIndex** and **aclmdlGetOutputSizeByIndex** APIs to obtain the memory size required for the input and output. These APIs obtain the memory size of the maximum level to ensure that the memory is sufficient. After model execution is complete, you can call the **aclmdlGetCurOutputDims** API to obtain the actual dimension information of the model output tensor.

    - For the data structure of input b and the data setting of input b, see step 2.

2. **Before model inference:**
    - Prepare the data structure of the dynamic batch/dynamic resolution/dynamic dimension input:
        1. Before allocating memory for the dynamic batch/dynamic resolution/dynamic dimension input, call the **aclmdlGetInputIndexByName** API to obtain the index that identifies the input in the model based on the input name (fixed as **ACL\_DYNAMIC\_TENSOR\_NAME**).

            >**Note:** 
            >**ACL\_DYNAMIC\_TENSOR\_NAME** is a macro, which is defined as follows:
>
            >```
            >#define ACL_DYNAMIC_TENSOR_NAME "ascend_mbatch_shape_data"
            >```

        2. Call **aclmdlGetInputSizeByIndex** to obtain the input memory size based on the index.
        3. Call the **aclrtMalloc** API to allocate memory based on the size obtained in the previous step.

            After the memory for the dynamic batch/dynamic resolution/dynamic AIPP/dynamic dimension input is allocated, you do not need to set the data in the memory (otherwise service exceptions may occur). After you call the API in [2.b](#li1767343825610), the system automatically fills data into the memory.

        4. Call the **aclCreateDataBuffer** API to create data of the **aclDataBuffer** type, which is used to store the memory address and memory size of the dynamic batch/dynamic resolution/dynamic dimension input data.
        5. Call **aclmdlCreateDataset** to create data of the **aclmdlDataset** type, and call **aclmdlAddDatasetBuffer** to add data of the **aclDataBuffer** type to the **aclmdlDataset** data.

    - Dynamic batch/dynamic resolution/dynamic dimension parameter values need to be set:

        **Figure 1**  API call process  
        ![](figures/dynamic_shape_API_call_process.png "API call process")

        1. Call **aclmdlGetInputIndexByName** to obtain the index that identifies the input in the model based on the input name (fixed as **ACL\_DYNAMIC\_TENSOR\_NAME**).
        2. Set the dynamic batch/dynamic resolution/dynamic dimension parameter values.
            - Call **aclmdlSetDynamicBatchSize** to set the dynamic batch.

                The batch size set here can only be one of the batch levels set when building the model.

                You can also call **aclmdlGetDynamicBatch** to obtain the number of batch levels supported by the specified model and the batch size in each level.

            - Call **aclmdlSetDynamicHWSize** to set the dynamic resolution.

                The resolution set here can only be one of the resolution levels set when building the model.

                Alternatively, call the **aclmdlGetDynamicHW** API to obtain the number of resolution levels supported by a specified model and the width and height in each level.

            - Call the **aclmdlSetInputDynamicDims** API to set the dimension values of the dynamic dimension.

                The dynamic dimension values set here can only be one of the levels configured when building the model.

                Alternatively, call the **aclmdlGetInputDynamicDims** API to obtain the number of dynamic dimension levels supported by a specified model and the values in each level.

## Dynamic Batch Sample Code

The following sample code shows the key steps of model inference. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

<!-- npu="910,310p,310b" id1 -->
You can click [YOLOV3\_dynamic\_batch\_detection\_picture](https://gitee.com/ascend/samples/tree/master/cplusplus/level2_simple_inference/2_object_detection/YOLOV3_dynamic_batch_detection_picture) to obtain the sample code.
<!-- end id1 -->

```cpp
......

// 1. Load the model. After the model is loaded, set the dynamic batch.
......

// 2. Prepare the model description modelDesc_, the model input data input_, and the model output data output_.
// ......

// 3. Customize the function for setting the dynamic batch.
int  ModelSetDynamicInfo()
{
        size_t index;
        // 3.1 Obtain the index of the dynamic batch input. The input name identifying the dynamic batch input is fixed to ACL_DYNAMIC_TENSOR_NAME.
        aclError ret = aclmdlGetInputIndexByName(modelDesc_, ACL_DYNAMIC_TENSOR_NAME, &index);
        // 3.2 Set the batch.
        // modelId_ indicates the ID of the loaded model, input_ indicates the data of the aclmdlDataset type, index indicates the input index identifying the dynamic batch input, and batchSize indicates the batch size (8 is used as an example here).
        uint64_t batchSize = 8;
        ret = aclmdlSetDynamicBatchSize(modelId_, input_, index, batchSize);
        // ......
}

// 4. Customize the function for executing the model.
int ModelExecute(int index)
{
        aclError ret;
        // 4.1 Call the custom function to set the dynamic batch.
    ret = ModelSetDynamicInfo();
        // 4.2 Execute the model. modelId_ indicates the ID of the successfully loaded model, and input_ and output_ indicate the model input and output respectively.
        ret = aclmdlExecute(modelId_, input_, output_);
        // ......
}
// 5. Process the model inference result.
......
```

## Dynamic Resolution Sample Code

The following sample code shows the key steps of model inference. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

<!-- npu="910,310p,310b" id2 -->
You can click [YOLOV3\_dynamic\_batch\_detection\_picture](https://gitee.com/ascend/samples/tree/master/cplusplus/level2_simple_inference/2_object_detection/YOLOV3_dynamic_batch_detection_picture) to obtain the sample code.
<!-- end id2 -->

```cpp
......

// 1. Load the model. After the model is loaded successfully, set the dynamic resolution.
......

// 2. Prepare the model description information modelDesc_, the model input data input_, and the model output data output_.
......

// 3. Custom function: set the dynamic resolution.
int  ModelSetDynamicInfo()
{
        size_t index;
                // 3.1 Obtain the index of the dynamic resolution input. The input name identifying the dynamic resolution input is fixed to ACL_DYNAMIC_TENSOR_NAME.
        aclError ret = aclmdlGetInputIndexByName(modelDesc_, ACL_DYNAMIC_TENSOR_NAME, &index);
                // 3.2 Set the input image resolution. modelId_ indicates the ID of the successfully loaded model, input_ indicates the data of the aclmdlDataset type, and index indicates the input index identifying the dynamic resolution input.
                uint64_t height = 224;
        uint64_t width = 224;
        ret = aclmdlSetDynamicHWSize(modelId_, input_, index, height, width);
                // ......
}

// 4. Custom function: execute the model.
int ModelExecute(int index)
{
        aclError ret;
        // 4.1 Call the custom function to set the dynamic resolution.
    ret = ModelSetDynamicInfo();
        // 4.2 Execute the model. modelId_ indicates the ID of the successfully loaded model, and input_ and output_ indicate the input and output of the model, respectively.
        ret = aclmdlExecute(modelId_, input_, output_);
        // ......
}

// 5. Process the model inference result.
......
```

## ND Format, Dynamic Dimension Sample Code

The following sample code shows the key steps of model inference. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

```cpp
......

// 1. Load the model. After the model is loaded, set the dynamic dimension.
......

// 2. Prepare the model description modelDesc_, the model input data input_, and the model output data output_.
......

// 3. Customize the function for setting the dynamic dimension.
int  ModelSetDynamicInfo()
{
        size_t index;
        // 3.1 Obtain the index of the dynamic dimension input. The input name of the dynamic dimension input is fixed to ACL_DYNAMIC_TENSOR_NAME.
        aclError ret = aclmdlGetInputIndexByName(modelDesc_, ACL_DYNAMIC_TENSOR_NAME, &index);
        // 3.2 Set the specific level information, including the dimension count dimCount and the value of each dimension. modelId_ indicates the ID of the successfully loaded model, input_ indicates the data of the aclmdlDataset type, and index indicates the input index that identifies the dynamic dimension input.
        aclmdlIODims currentDims;
        currentDims.dimCount = 4;
        currentDims.dims[0] = 8;
        currentDims.dims[1] = 3;
        currentDims.dims[2] = 224;
        currentDims.dims[3] = 224;
        ret = aclmdlSetInputDynamicDims(modelId_, input_, index, &currentDims);
        // ......
}

// 4. Customize the function for executing the model.
int ModelExecute(int index)
{
        aclError ret;
        // 4.1 Call the custom function to set the dynamic dimension.
    ret = ModelSetDynamicInfo();
        // 4.2 Execute the model. modelId_ indicates the ID of the successfully loaded model, and input_ and output_ indicate the model input and output, respectively.
        ret = aclmdlExecute(modelId_, input_, output_);
        // ......
}
// 5. Process the model inference result.
......
```
