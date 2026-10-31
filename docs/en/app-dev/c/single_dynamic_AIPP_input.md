# Dynamic AIPP (Single Dynamic AIPP Input)

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:41:58.015Z pushedAt=2026-10-26T03:10:39.444Z nl=2 -->

This section describes the key APIs and sample code involved in a model with a single dynamic AIPP input during model inference.

## API Call Process

Model inference in the dynamic AIPP scenario is similar to that in [Static Shape Input Model Inference](static_shape_model_inference.md), involving initialization and deinitialization, runtime resource application and release, model building, model loading, model execution, and model unloading.

This section focuses on the differences between model inference in the dynamic AIPP scenario and [Static Shape Input Model Inference](static_shape_model_inference.md):

- **During model building**, configure the parameters related to dynamic AIPP:

    **During model building**, configure the dynamic AIPP mode through the **insert\_op\_conf** parameter of the ATC tool. For details about the ATC tool parameters, see "Command Line Options \> Advanced Options \> Feature Options \> --insert\_op\_conf" in [Ascend Tensor Compiler (ATC)](https://gitcode.com/cann/ge/blob/9.2.0/docs/en/user_guides/atc_tools/README.md).

    **After the model is built**, a new input (hereinafter referred to as the dynamic AIPP input) is added to the generated OM model. During model inference, specific AIPP configuration values are provided through this new input.

    **For example**, if the AIPP configuration of input a is dynamic, the OM model contains an input b corresponding to a to describe the AIPP configuration information of a. During model execution, for the data structure of input a, see [Preparing the Input/Output Data Structure for Model Execution](model_execute.md#section1620016465510). For the data structure of input b and the data of input b, see the following content.

- **Before executing model inference**:
    - Prepare the data structure of the dynamic AIPP input:
        1. Before allocating the memory corresponding to the dynamic AIPP input, call the **aclmdlGetAippDataSize** API to obtain the memory size.

            Meanwhile, the method of calling the **aclmdlGetInputSizeByIndex** API to obtain the memory size in earlier versions is still supported. However, in scenarios where the batch size is not fixed, the memory size obtained by this method may be 0. In this case, you need to estimate the memory size by yourself. If you call the **aclmdlGetInputSizeByIndex** API to obtain the memory size, you also need to call the **aclmdlGetInputIndexByName** API in advance to obtain the index that identifies the input in the model based on the input name (fixed as the **ACL\_DYNAMIC\_AIPP\_NAME** macro, which indicates **ascend\_dynamic\_aipp\_data**).

        2. Call the **aclrtMalloc** API to allocate memory based on the size obtained in the previous step.

            After the memory for the dynamic AIPP input is allocated, you do not need to set the data in the memory (otherwise service exceptions may occur). After you call the API for setting dynamic AIPP parameter values, the system automatically fills data into the memory.

        3. Call the **aclCreateDataBuffer** API to create data of the **aclDataBuffer** type, which is used to store the memory address and memory size of the dynamic AIPP input data.
        4. Call the **aclmdlCreateDataset** API to create data of the **aclmdlDataset** type, and call the **aclmdlAddDatasetBuffer** API to add data of the **aclDataBuffer** type to the data of the **aclmdlDataset** type.

    - Set dynamic AIPP parameter values:

        **Figure 1**  API call process  
        ![](figures/dynamic_AIPP_API_call_process.png "API call process")

        1. Call the **aclmdlGetInputIndexByName** API to obtain the index that identifies the input in the model based on the input name (fixed as **ACL\_DYNAMIC\_AIPP\_NAME**).
        2. Set dynamic AIPP parameter values.
            1. Call the **aclmdlCreateAIPP** API to create the **aclmdlAIPP** type.
            2. Based on actual requirements, call the operation APIs of the **aclmdlAIPP** data type to set the dynamic AIPP parameter values.
            3. In the dynamic AIPP scenario, the **aclmdlSetAIPPSrcImageSize** API (which sets the width and height of the source image) must be called.
            4. Call the **aclmdlSetInputAIPP** API to set the dynamic AIPP data for model inference.
            5. Call the **aclmdlDestroyAIPP** API in a timely manner to destroy the **aclmdlAIPP** data type.

## Sample Code

The following sample code shows the key steps of model inference. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

```cpp
......

// 1. Load the model. After the model is loaded, set the dynamic AIPP parameter values.
// ......

// 2. Prepare the model description modelDesc_, the model input data input_, and the model output data output_.

// 3. Custom function for setting the dynamic AIPP parameter values.
int  ModelSetDynamicAIPP()
{
    // 3.1 Obtain the index that identifies the dynamic AIPP input.
    size_t index;
    // modelDesc_ is the model description created by aclmdlCreateDesc. Obtain the model description based on the ID of the model loaded in step 1.
    aclError ret = aclmdlGetInputIndexByName(modelDesc_, ACL_DYNAMIC_AIPP_NAME, &index);

    // 3.2 Set the dynamic AIPP parameter value.
    uint64_t batchNumber = 1;
    aclmdlAIPP *aippDynamicSet = aclmdlCreateAIPP(batchNumber);
    ret = aclmdlSetAIPPSrcImageSize(aippDynamicSet, 256, 224);
    ret = aclmdlSetAIPPInputFormat(aippDynamicSet, ACL_YUV420SP_U8);
    ret = aclmdlSetAIPPCscParams(aippDynamicSet, 1, 256, 443, 0, 256, -86, -178, 256, 0, 350, 0, 0, 0, 0, 128, 128);
    ret = aclmdlSetAIPPRbuvSwapSwitch(aippDynamicSet, 0);
    ret = aclmdlSetAIPPDtcPixelMean(aippDynamicSet, 0, 0, 0, 0, 0);
    ret = aclmdlSetAIPPDtcPixelMin(aippDynamicSet, 0, 0, 0, 0, 0);
    ret = aclmdlSetAIPPPixelVarReci(aippDynamicSet, 1.0, 1.0, 1.0, 1.0, 0);
    ret = aclmdlSetAIPPCropParams(aippDynamicSet, 1, 2, 2, 224, 224, 0);
    ret = aclmdlSetInputAIPP(modelId_, input_, index, aippDynamicSet);
    ret = aclmdlDestroyAIPP(aippDynamicSet);
        
    // ......
}
// 4. Custom function for executing the model.
int ModelExecute(int index)
{
        aclError ret;
        // 4.1 Call the custom function to set the dynamic AIPP parameter value.
    ret = ModelSetDynamicAIPP();
        // 4.2 Execute the model. modelId_ indicates the ID of the successfully loaded model, and input_ and output_ indicate the model input and output, respectively.
        ret = aclmdlExecute(modelId_, input_, output_);
        // ......
}

// 5. Process the model inference result.
......
```
