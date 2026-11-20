# Queue-Based Model Inference

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:30:38.151Z pushedAt=2026-10-22T07:25:13.624Z nl=2 -->

This section describes how to load a model, prepare model input data, and obtain model inference output data based on queues.

Queue-based model inference uses queues to decouple inference tasks from data production and consumption and to implement asynchronous scheduling. For example, data preprocessing and model inference are executed asynchronously in parallel through asynchronous queues.

## Basic Principles

- Call **aclmdlLoadFromFileWithQ** or **aclmdlLoadFromMemWithQ** to load a model in queue mode.
- Call **acltdtEnqueueData** to pass the model input data to the queue. The API internally performs model inference based on the input data in the queue, so you do not need to call the model execution API.
- Call **acltdtDequeueData** to wait until model inference is complete, and then obtain the result data from the output memory.

>**Note:** 
>In a multi-thread scenario, if a model has multiple inputs, the enqueue tasks of the multiple input data (that is, calls to **acltdtEnqueueData**) must be performed in the same thread. If a model has multiple outputs, the dequeue tasks of the multiple output data (that is, calls to **acltdtDequeueData**) must be performed in the same thread.

## Sample Code

The following sample code shows the key steps of model inference in queue mode. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

```cpp
#include "acl/acl.h"
......

// Obtain the running mode of the current AI software stack. The subsequent API call methods for memory allocation and memory copy vary depending on the running mode.
extern bool g_isDevice;
aclrtRunMode runMode;
aclError ret = aclrtGetRunMode(&runMode);
g_isDevice = (runMode == ACL_DEVICE);

// 1. Load and execute the model.
// Here, .. indicates a relative path, which is relative to the directory where the executable file is located.
// For example, if the compiled executable file is stored in the out directory, .. here indicates the parent directory of the out directory.
const char* omModelPath = "../model/resnet50.om";

// 1.1 Create an input queue for the model. If the model has multiple inputs, create multiple input queues. Here, one input is used as an example.
acltdtQueueAttr *attr = acltdtCreateQueueAttr();
uint32_t *inputQueueList = new (nothrow) uint32_t[num];
int32_t inputNum = 1;

for (int n = 0; n < inputNum; n++) {
        uint32_t inputQid;
        ret = acltdtCreateQueue(attr, &inputQid);
        inputQueueList[n] = inputQid;
    }

// 1.2 Create an output queue for the model. If the model has multiple outputs, create multiple output queues. Here, one output is used as an example.
uint32_t *outputQueueList = new (nothrow) uint32_t[num];
int32_t outputNum = 1;

for (int n = 0; n < outputNum; n++) {
        uint32_t outputQid;
        ret = acltdtCreateQueue(attr, &outputQid);
        outputQueueList[n] = outputQid;
    }

// 1.3 Load the model.
uint32_t modelId;
ret= aclmdlLoadFromFileWithQ(omModelPath, &modelId, 
                             inputQueueList, inputNum, outputQueueList, outputNum);

// 1.4 Obtain the description of the model based on the model ID.
aclmdlDesc *modelDesc = aclmdlCreateDesc();
ret = aclmdlGetDesc(modelDesc, modelId);

// 1.5 Obtain the input memory size of the model. If the model has multiple inputs, obtain the memory size of each input. Here, one input is used as an example.
size_t inputSize = aclmdlGetInputSizeByIndex(modelDesc, 0);

// 1.6 Load the test image data, perform model inference, and post-process the inference result data.
string testFile[] = {
        "../data/dog1_1024_683.bin",
        "../data/dog2_1024_683.bin"
};

for (size_t index = 0; index < sizeof(testFile) / sizeof(testFile[0]); ++index) {
        uint32_t devBufferSize;
        void *picDevBuffer = nullptr;
        // Custom function ReadBinFile: allocate the corresponding memory based on the running mode of the AI software stack, and then call the functions in the C++ standard library to read the image data into the memory.
        ret = Utils::ReadBinFile(testFile[index], picDevBuffer, devBufferSize);

        // Pass the model input data to the queue and perform model inference. -1 indicates that the program is blocked until the input data is enqueued.
        ret = acltdtEnqueueData(inputQid, picDevBuffer, devBufferSize, nullptr, 0, -1, 0);
        // Obtain the size of each output.
    size_t dataSize = aclmdlGetOutputSizeByIndex(modelDesc, 0);
    void *data = nullptr;
        size_t retDataSize = 0;
        // Allocate memory for the model output data.
    if (!g_isDevice) {
            aclError aclRet = aclrtMallocHost(&data, dataSize);
     } else {
        aclError aclRet = aclrtMalloc(&data, dataSize, ACL_MEM_MALLOC_HUGE_FIRST);
     }
         // Wait for the model inference to complete, and obtain the result data from the output memory. -1 indicates that the program is blocked until the inference output data is enqueued.
         ret = acltdtDequeueData(outputQid, data, dataSize, &retDataSize, nullptr, 0, -1);
         // Convert the data in the output memory to the float type.
         float *outData = NULL;
         outData = reinterpret_cast<float*>(data);
        
         // Display the category IDs of the top 5 confidence levels of each image.
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
         if (!g_isDevice) {
            aclError aclRet = aclrtFreeHost(picDevBuffer);
            aclrtFreeHost(data);
     } else {
        aclError aclRet = aclrtFree(picDevBuffer);
            aclrtFree(data); 
     }
}

// 2. Unload the model and release the resources related to model inference.
aclmdlUnload(modelId);
aclmdlDestroyDesc(modelDesc);
acltdtDestroyQueue(inputQid);
acltdtDestroyQueue(outputQid);
acltdtDestroyQueueAttr(attr);

......
```
