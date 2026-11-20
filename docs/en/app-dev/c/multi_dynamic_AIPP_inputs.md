# Dynamic AIPP (Multiple Dynamic AIPP Inputs)

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:21:42.932Z pushedAt=2026-10-22T06:03:13.930Z nl=2 -->

This section describes the key APIs and sample code involved in a model with multiple dynamic AIPP inputs during model inference.

## API Call Process

The basic inference process for a model with multiple dynamic AIPP inputs is similar to that for a single dynamic AIPP input. For details, see [Dynamic AIPP (Single Dynamic AIPP Input)](single_dynamic_AIPP_input.md).

The differences between multiple dynamic AIPP inputs and a single dynamic AIPP input are as follows:

- Call **aclmdlGetAippType** to query whether a specified input of a specified model has an associated dynamic AIPP input. If yes, the API outputs the index that identifies the dynamic AIPP input. This value can be used as an input parameter of **aclmdlSetAIPPByInputIndex** to set the dynamic AIPP parameter values on the corresponding input.
- To avoid setting dynamic AIPP parameters on an incorrect input, call **aclmdlGetInputNameByIndex** to obtain the input name of a specified input index, and set the dynamic AIPP parameters based on the index corresponding to the input name.

## Sample Code

The following sample code shows the key steps. It cannot be directly copied, compiled, and run, and are for reference only. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

```cpp
// 1. Load the model. After the model is loaded, set the dynamic AIPP parameter values.
// ......

// 2. Prepare the model description modelDesc_, the model input data input_, and the model output data output_.
// ......

// 3. Custom function for setting the dynamic AIPP parameter values.
int  ModelSetDynamicAIPP()
{
    // 3.1 Obtain the index that identifies the dynamic AIPP input.
    std::vector<size_t> dataNeedDynamicAipp;
    for (size_t index = 0; index < aclmdlGetNumInputs(modelDesc_); ++index) {
        aclmdlInputAippType aippType;
        size_t dynamicAttachedDataIndex;
        aclError ret = aclmdlGetAippType(modelId_, index, &aippType, &dynamicAttachedDataIndex);
        if (aippType == ACL_DATA_WITH_DYNAMIC_AIPP) {
            dataNeedDynamicAipp.push_back(index);
        }
    }

    // 3.2 In this example, two dynamic AIPP inputs are used. You can modify the number based on the actual situation.
    if (dataNeedDynamicAipp.size() != 2) {
        return -1;
    }
    // Create the first dynamic AIPP configuration parameters.
    uint64_t batchNumber1 = 1;
    aclmdlAIPP *aippDynamicSet1 = aclmdlCreateAIPP(batchNumber1);
    ret = aclmdlSetAIPPSrcImageSize(aippDynamicSet1, 256, 224);
    ret = aclmdlSetAIPPInputFormat(aippDynamicSet1, ACL_YUV420SP_U8);
    ret = aclmdlSetAIPPCscParams(aippDynamicSet1, 1, 256, 443, 0, 256, -86, -178, 256, 0, 350, 0, 0, 0, 0, 128, 128);
    ret = aclmdlSetAIPPRbuvSwapSwitch(aippDynamicSet1, 0);
    ret = aclmdlSetAIPPDtcPixelMean(aippDynamicSet1, 0, 0, 0, 0, 0);
    ret = aclmdlSetAIPPDtcPixelMin(aippDynamicSet1, 0, 0, 0, 0, 0);
    ret = aclmdlSetAIPPPixelVarReci(aippDynamicSet1, 1.0, 1.0, 1.0, 1.0, 0);
    ret = aclmdlSetAIPPCropParams(aippDynamicSet1, 1, 2, 2, 224, 224, 0);
    // Set the dynamic AIPP parameter values for model inference.
    ret = aclmdlSetAIPPByInputIndex(modelId_, input_, dataNeedDynamicAipp[0], aippDynamicSet1);
    ret = aclmdlDestroyAIPP(aippDynamicSet1);

    // Create the second dynamic AIPP configuration parameters.
    uint64_t batchNumber2 = 1;
    aclmdlAIPP *aippDynamicSet2 = aclmdlCreateAIPP(batchNumber2);
    ret = aclmdlSetAIPPSrcImageSize(aippDynamicSet2, 224, 224);
    // You can continue to call other AIPP parameter setting APIs here.
    // Set the dynamic AIPP parameter values for model inference.
    ret = aclmdlSetAIPPByInputIndex(modelId_, input_, dataNeedDynamicAipp[1], aippDynamicSet2);
    ret = aclmdlDestroyAIPP(aippDynamicSet2);
}

// 4. Custom function for executing the model.
int ModelExecute(int index)
{
        aclError ret;
        // 4.1 Call the custom function to set the dynamic AIPP parameter values.
    ret = ModelSetDynamicAIPP();
        // 4.2 Execute the model. modelId_ indicates the ID of the successfully loaded model, and input_ and output_ indicate the model input and output respectively.
        ret = aclmdlExecute(modelId_, input_, output_);
        // ......
}

// 5. Process the model inference result.
// TODO
```
