# Model Execution

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:39:10.162Z pushedAt=2026-10-26T03:10:39.438Z nl=2 -->

This section describes the API call process for **whole-network model execution**. Combined with the API call process and sample code, this section describes the data to be prepared before model execution, the model execution APIs, and the resources to be released after model execution.

## Basic Principles

**After the model is loaded and before model execution**, you need to prepare the input and output data structures and transfer the input data to the corresponding memory of the model input data structure.

**After model execution is complete**, if the input data and related resources such as the **aclmdlDesc** type, **aclmdlDataset** type, and **aclDataBuffer** type are no longer needed, release the memory and destroy the corresponding data types in a timely manner to prevent memory exceptions. A model may have multiple inputs and multiple outputs. The memory address and memory size of each input/output are described by data of the **aclDataBuffer** type. For each input/output, call the **aclrtFree** API to release the data in the memory, and then call the **aclDestroyDataBuffer** API to destroy the corresponding **aclDataBuffer** type.

## Model Execution Process

**Figure 1**  Basic model inference process  
![](figures/basic_model_inference_process.png "Basic model inference process")

The key APIs are described as follows:

1. Call the **aclmdlCreateDesc** API to **create the data type that describes the basic model information**.
2. Call the **aclmdlGetDesc** API to **obtain the basic model information** based on the model ID returned in [Model Loading](model_load.md).
3. **Prepare the input and output data structures for model execution**. For details about the process, see [Preparing Input/Output Data Structures for Model Execution](#section1620016465510).

    <!-- npu="950,A3,910b,910,310p,310b" id1 -->
    If the model input involves features such as dynamic batch, dynamic resolution, dynamic AIPP, and dynamic dimensions (ND format), see [Model Inference with Dynamic Shape Input](static_shape_model_inference.md) and [Model Inference with Dynamic AIPP](dynamic_AIPP_inference.md).
    <!-- end id1 -->

4. **Execute model inference**.

    For fixed multi-batch scenarios, the input data can be sent to the model for inference only after the batch size is satisfied. If the batch size is not satisfied, you need to handle it based on your actual scenario.

    The current system supports both synchronous inference and asynchronous inference of models:

    - Synchronous inference

        <!-- npu="950,A3,910b,910,310p,310b" id2 -->
        Call the **aclmdlExecute** API to perform synchronous inference.
        <!-- end id2 -->

        <!-- npu="IPV350" id3 -->
        Call the **aclmdlExecuteV2** API to perform synchronous inference.
        <!-- end id3 -->

    - Asynchronous inference

        <!-- npu="950,A3,910b,910,310p,310b" id4 -->
        Call the **aclmdlExecuteAsync** API to perform asynchronous inference.
        <!-- end id4 -->

        <!-- npu="IPV350" id5 -->
        Call the **aclmdlExecuteAsyncV2** API to perform asynchronous inference.
        <!-- end id5 -->

        However, for asynchronous APIs, you also need to call the **aclrtSynchronizeStream** API to block the application until all tasks in the specified stream are complete.

        <!-- npu="950,A3,910b,910,310p,310b" id6 -->
        For details about asynchronous inference, see [Asynchronous Model Inference](async_model_inference.md).
        <!-- end id6 -->

5. **Obtain the model inference result** for subsequent processing.
    - For synchronous inference, directly obtain the output data of model inference.
    - For asynchronous inference, when implementing the callback function, obtain the model inference result in the callback function for subsequent use.

6. **Release memory.**

    Call the **aclrtFree** API to release the memory on the device.

7. **Release the data of the related data types.**

    After model inference is complete, call the **aclDestroyDataBuffer** API and the **aclmdlDestroyDataset** API in sequence to release the data that describes the model input and output data types in a timely manner. If there are multiple inputs and outputs, call the **aclDestroyDataBuffer** API multiple times.

<a id="section1620016465510"></a>

## Preparing Input/Output Data Structures for Model Execution

The following data types are used to describe a model, describe its inputs and outputs, and store data in memory. Before model execution, you need to construct these data types as the input for model execution:

- Use data of the **aclmdlDesc** type to describe the basic information of a model (for example, the number, names, data types, Format, and dimension information of inputs/outputs).

    After a model is loaded successfully, you can call the **aclmdlGetDesc** API based on the model ID to obtain the description information of the model, and then obtain the number of model inputs/outputs, memory size, dimension information, format, data type, and other information from the model description. For details, see the operation APIs under the **aclmdlDesc** type.

- Use data of the **aclmdlDataset** type to describe the input/output data of a model. A model may have multiple inputs and multiple outputs.

    Call the operation APIs under the **aclmdlDataset** type to add data of the **aclDataBuffer** type and obtain the number of **aclDataBuffer** objects.

- The memory address and memory size of each input/output are described by data of the **aclDataBuffer** type.

    Call the operation APIs under the **aclDataBuffer** type to obtain information such as the memory address and memory size.

    **Figure 2** Relationship between the aclmdlDataset type and the aclDataBuffer type  
    ![](figures/relationship_between_aclmdlDataset_and_aclDataBuffer.png "Relationship between the aclmdlDataset type and the aclDataBuffer type")

After understanding the related data types, you can use the operation APIs of these data types to prepare the input and output data structures of a model, as shown in the following figure.

**Figure 3** Preparation process of the input/output data structure for model execution  
![](figures/prepare_model_input_output.png "Preparation process of the input-output data structure for model execution")

Key notes are as follows:

- When a model has multiple inputs and outputs, you can call **aclmdlGetNumInputs** and **aclmdlGetNumOutputs** to obtain the number of inputs and outputs.
- You can call **aclmdlGetInputSizeByIndex** and **aclmdlGetOutputSizeByIndex** to obtain the memory size required by each input and output of the model.
- When a model has multiple inputs and outputs, to avoid adding **aclDataBuffer** to **aclmdlDataset** in the wrong order, you can first call **aclmdlGetInputNameByIndex** and **aclmdlGetOutputNameByIndex** to obtain the names of the inputs and outputs, and then add them in the order of the indexes corresponding to the input and output names.

## Sample Code

The sample code here processes the output result of an image classification model and displays the top-5 confidence category IDs of each image on the screen. You can implement the processing logic for the model inference output data based on your actual requirements.

The following sample code shows the key steps. It cannot be directly copied, compiled, and run, and are for reference only. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

<!-- npu="950,A3,910b,910,310p,310b" id7 -->
You can click [resnet50\_imagenet\_classification](https://gitcode.com/cann/ge/tree/9.2.0/examples/acl/1_sample_resnet50_imagenet_classification) to obtain the sample code.
<!-- end id7 -->

```cpp
// 1. Obtain the description of the model based on the model ID.
// modelDesc_ is of the aclmdlDesc type.
modelDesc_ = aclmdlCreateDesc();
aclError ret = aclmdlGetDesc(modelDesc_, modelId_);

// 2. Prepare the input data structure for model inference.
// (1) Allocate input memory.
size_t modelInputSize;
void *modelInputBuffer = nullptr;
// The model in this example has only one input, so index is 0. If the model has multiple inputs, call aclmdlGetNumInputs first to obtain the number of model inputs.
modelInputSize = aclmdlGetInputSizeByIndex(modelDesc_, 0);
ret = aclrtMalloc(&modelInputBuffer, modelInputSize, ACL_MEM_MALLOC_HUGE_FIRST);

// (2) Prepare the input data structure of the model
// Create data of the aclmdlDataset type to describe the input of model inference. input_ is of the aclmdlDataset type.
input_ = aclmdlCreateDataset();
aclDataBuffer *inputData = aclCreateDataBuffer(modelInputBuffer, modelInputSize);
ret = aclmdlAddDatasetBuffer(input_, inputData);

// 3. Prepare the output data structure for model inference
// (1) Create data of the aclmdlDataset type to describe the output of model inference. output_ is of the aclmdlDataset type.
output_ = aclmdlCreateDataset();

// (2) Obtain the number of model outputs.
size_t outputSize = aclmdlGetNumOutputs(modelDesc_);

// (3) Allocate memory for each output in a loop, and add each output to the data of the aclmdlDataset type.
for (size_t i = 0; i < outputSize; ++i) {
    size_t buffer_size = aclmdlGetOutputSizeByIndex(modelDesc_, i);
    void *outputBuffer = nullptr;
    ret = aclrtMalloc(&outputBuffer, buffer_size, ACL_MEM_MALLOC_HUGE_FIRST);
    aclDataBuffer* outputData = aclCreateDataBuffer(outputBuffer, buffer_size);   
    ret = aclmdlAddDatasetBuffer(output_, outputData);
    }

// 4. Execute the model.
string testFile[] = {
        "../data/dog1_1024_683.bin",
        "../data/dog2_1024_683.bin"
    };

for (size_t index = 0; index < sizeof(testFile) / sizeof(testFile[0]); ++index) {
    // 4.1 Custom function ReadBinFile: call the functions in the C++ standard library std::ifstream to read the image file, and output the memory size inputBuffSize occupied by the image file and the address inputBuff where the image file is stored in memory.
    void *inputBuff = nullptr;
    uint32_t inputBuffSize = 0;
    auto ret1 = Utils::ReadBinFile(fileName, inputBuff, inputBuffSize);
    
    // 4.2 Prepare the input data for model inference.
    // Call aclrtGetRunMode to obtain the run mode of the software stack when allocating for runtime resources.
    // If the run mode is ACL_DEVICE, the value of g_isDevice is true, indicating that the software stack runs on the device side and no image data transfer or intra-device data transfer is required; otherwise, call the memory copy API to transfer the data to the device.
    if (!g_isDevice) {
        // if app is running in host, need copy data from host to device
        // modelInputBuffer and modelInputSize indicate the memory address and memory size of the model inference input data, respectively. This memory is allocated when preparing the input/output data structures.
        ret = aclrtMemcpy(modelInputBuffer, modelInputSize, inputBuff, inputBuffSize, ACL_MEMCPY_HOST_TO_DEVICE);
        (void)aclrtFreeHost(inputBuff);
    } else { // app is running in device
        ret = aclrtMemcpy(modelInputBuffer, modelInputSize, inputBuff, inputBuffSize, ACL_MEMCPY_DEVICE_TO_DEVICE);
        (void)aclrtFree(inputBuff);
    }

    // 4.3 Execute model inference.
    // modelId_ indicates the model ID, which is returned after the model is loaded successfully.
    // input_ and output_ indicate the input and output data of model inference, respectively. They are defined when preparing the input and output data structures for model inference.
    ret = aclmdlExecute(modelId_, input_, output_);
        

    // Process the output data of model inference and output the category numbers of the top 5 confidence levels. 
    // output_ indicates the output of model execution.
    for (size_t i = 0; i < aclmdlGetDatasetNumBuffers(output_); ++i) {
    // Obtain the memory address and memory size of each output.
        aclDataBuffer* dataBuffer = aclmdlGetDatasetBuffer(output_, i);
        void* data = aclGetDataBufferAddr(dataBuffer);

        size_t len = aclGetDataBufferSizeV2(dataBuffer);

        // Convert the data in the memory to the float type.
        float *outData = NULL;
        outData = reinterpret_cast<float*>(data);
        
        // Display the class IDs of the top 5 confidence values of each image.
        map<float, int, greater<float> > resultMap;
        for (int j = 0; j < len / sizeof(float); ++j) {
            resultMap[*outData] = j;
            outData++;
        }
        int cnt = 0;
        for (auto it = resultMap.begin(); it != resultMap.end(); ++it) {
            // print top 5
            if (++cnt > 5) {
                break;
            }

            INFO_LOG("top %d: index[%d] value[%lf]", cnt, it->second, it->first);
        }
    }
}

// 5. Release the input and output resources of model inference.
// Release the input resources, including the data structure and memory.
for (size_t i = 0; i < aclmdlGetDatasetNumBuffers(input_); ++i) {
        aclDataBuffer *dataBuffer = aclmdlGetDatasetBuffer(input_, i);
        (void)aclDestroyDataBuffer(dataBuffer);
}
(void)aclmdlDestroyDataset(input_);
input_ = nullptr;
aclrtFree(modelInputBuffer);

// Release the output resources, including the data structure and memory.
for (size_t i = 0; i < aclmdlGetDatasetNumBuffers(output_); ++i) {
    aclDataBuffer* dataBuffer = aclmdlGetDatasetBuffer(output_, i);
    void* data = aclGetDataBufferAddr(dataBuffer);
    (void)aclrtFree(data);
    (void)aclDestroyDataBuffer(dataBuffer);
}

(void)aclmdlDestroyDataset(output_);
output_ = nullptr;
```

When building a model, if **batchSize** is greater than or equal to 2 (set through the **input\_shape** parameter of the ATC tool), you need to write a piece of code before inference to implement the following logic: wait until the input data meets the **batchSize** requirement (for example, **batchSize = 8**), allocate memory on the device to store the data of **batchSize = 8**, and use it as the input of model inference. If the **batchSize** requirement is still not met after all input data has been traversed in the final loop, directly use the remaining data as the input of model inference.

The following sample code uses **batchSize = 8**:

```cpp
uint32_t batchSize = 8;
uint32_t deviceNum = 1;
uint32_t deviceId = 0;

// Obtain the size of the first input of the model.
uint32_t modelInputSize = aclmdlGetInputSizeByIndex(modelDesc, 0);
// Obtain the size of the input data of each batch.
uint32_t singleBuffSize = modelInputSize / batchSize;

// Define this variable to accumulate whether the batch size reaches 8 batches.
uint32_t cnt = 0;
// Define this variable to describe the position offset when each file is read into memory.
uint32_t pos = 0;

void* p_batchDst = NULL;
std::vector<std::string>inferFile_vec;

for (int i = 0; i < files.size(); ++i) 
        {
            // Allocate memory on the device once for every 8 files to store the input data of 8 batches. 
            if (cnt % batchSize == 0)
            {
                pos = 0;
                inferFile_vec.clear();
                // Allocate memory on the device.
                aclrtMalloc(&p_batchDst, modelInputSize, ACL_MEM_MALLOC_HUGE_FIRST);
            }

            // TODO: Read files from a directory and calculate the file size fileSize.
            
            // Allocate memory based on the file size to store the file data.
            aclrtMallocHost(&p_imgBuf, fileSize);

            // Transfer the data to the device memory.
            aclrtMemcpy((uint8_t *)p_batchDst + pos, fileSize, p_imgBuf, fileSize, ACL_MEMCPY_HOST_TO_DEVICE);
            pos += fileSize;
            // Release unused memory in a timely manner.
            aclrtFreeHost(p_imgBuf);

            // Store the i-th file in the vector and increment cnt by 1.
            inferFile_vec.push_back(files[i]);
            cnt++;

            // Send the input data of every 8 batches to the model for inference.
            if (cnt % batchSize == 0)
            {
                // TODO: Create data of the aclmdlDataset and aclDataBuffer types to describe the input and output data of the model.
                // TODO: Call the aclmdlExecute API to perform model inference.
                // TODO: After inference is complete, call the aclrtFree API to release the memory on the device.
            }
        }

// If the multiple-batch requirement is still not met after all input data has been traversed, directly use the remaining data as the input for model inference.
if (cnt % batchSize != 0)
    {
            // TODO: Create data of the aclmdlDataset and aclDataBuffer types to describe the input and output data of the model.
            // TODO: Call the aclmdlExecute API to perform model inference.
            // TODO: After inference is complete, call the aclrtFree API to release the memory on the device.
    }
```
