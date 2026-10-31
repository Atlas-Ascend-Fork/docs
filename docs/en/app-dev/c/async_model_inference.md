# Asynchronous Model Inference

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T02:34:51.973Z pushedAt=2026-10-21T03:25:03.467Z nl=2 -->

This section describes how asynchronous inference APIs work with callback functions to deliver a callback task at regular intervals and obtain the asynchronous inference results generated in the preceding interval.

## API Call Process

When developing an application, if synchronous waiting is involved in an asynchronous scenario, the application must include the relevant code logic. For the API call process in this scenario, see the following figure.

**Figure 1** Synchronous waiting process in the callback scenario  
![](figures/asynchronous_model_inference_process.png "Synchronous waiting process in the callback scenario")

The key APIs are described as follows:

1. The callback function must be created by the user in advance to obtain and process the results of model inference or operator execution.
2. The thread must be created by the user in advance, and a custom thread function must be defined. In the thread function, call **aclrtProcessReport** to set the timeout period and wait for the callback task delivered by **aclrtLaunchCallback** to be executed.
3. Call **aclrtSubscribeReport** to specify the thread that processes the callback function on the stream. The thread must be the same as the one created in step 2.
4. Call **aclmdlExecuteAsync** for asynchronous inference.

    For asynchronous APIs, also call **aclrtSynchronizeStream** to block the application until all tasks in the specified stream are complete.

    You can obtain the asynchronous inference results of all images at once after **aclrtSynchronizeStream**. However, if the amount of image data is large, the waiting time is long. In this case, you can use the callback function to deliver a callback task at intervals and obtain the asynchronous inference results generated in the preceding interval.

5. Call **aclrtLaunchCallback** to enqueue a callback task in the task queue of the stream. When the system executes this callback task, it runs the callback function in the thread registered on the stream (the thread registered through **aclrtSubscribeReport**). The callback function is the same as that in step 1.

    Each call to **aclrtLaunchCallback** triggers one execution of the callback function.

6. Call **aclrtUnSubscribeReport** to cancel the thread registration (the callback function on the stream is no longer processed by the specified thread).

## Sample Code

The following sample code shows the key steps of the asynchronous model inference function. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

You can click [resnet50\_async\_imagenet\_classification](https://gitee.com/ascend/samples/tree/master/cplusplus/level2_simple_inference/1_classification/resnet50_async_imagenet_classification) to obtain the sample code.

```cpp
#include "acl/acl.h"
......

// Obtain the current running mode of the AI software stack. Based on the running mode, the subsequent APIs for memory allocation and memory copy are called differently.
aclrtRunMode runMode;
extern bool g_isDevice;
aclrtGetRunMode(&runMode);
g_isDevice = (runMode == ACL_DEVICE);

// 1. Allocate model inference resources.

// Here, .. indicates a relative path, which is relative to the directory where the executable file is located.
// For example, if the compiled executable file is stored in the out directory, .. indicates the parent directory of the out directory.
const char* omModelPath = "../model/resnet50.om";

// 1.1 Load the model.
// Obtain the weight memory size and workspace memory size required for model execution based on the model file, and allocate the weight memory and workspace memory.
aclmdlQuerySize(omModelPath, &modelMemSize_, &modelWeightSize_);
aclrtMalloc(&modelMemPtr_, modelMemSize_, ACL_MEM_MALLOC_HUGE_FIRST);
aclrtMalloc(&modelWeightPtr_, modelWeightSize_, ACL_MEM_MALLOC_HUGE_FIRST);

// Load the offline model file. If the model is loaded successfully, the ID of the model is returned.
aclmdlLoadFromFileWithMem(modelPath, &modelId_, modelMemPtr_,
        modelMemSize_, modelWeightPtr_, modelWeightSize_);

// 1.2 Obtain the description of the model based on the model ID.
modelDesc_ = aclmdlCreateDesc();
aclmdlGetDesc(modelDesc_, modelId_);

// 1.3 Call the custom function InitMemPool to initialize the memory pool for storing the input and output data of model inference.
// -----Key implementation of the custom function InitMemPool-----
string testFile[] = {
        "../data/dog1_1024_683.bin",
        "../data/dog2_1024_683.bin"
    };
size_t fileNum = sizeof(testFile) / sizeof(testFile[0]);
// g_memoryPoolSize indicates the number of memory blocks in the memory pool. The default value is 100.
for (size_t i = 0; i < g_memoryPoolSize; ++i) {
        size_t index = i % (sizeof(testFile) / sizeof(testFile[0]));
        // model process
        uint32_t devBufferSize;
        // The custom function GetDeviceBufferOfFile performs the following operations:
        // Obtain the memory and memory size for storing the input image data, and transfer the image data to the device.
        void *picDevBuffer = Utils::GetDeviceBufferOfFile(testFile[index], devBufferSize);
        aclmdlDataset *input = nullptr;
        // Call the custom function CreateInput to create the aclmdlDataset data input for storing the input data of model inference.
        Result ret = CreateInput(picDevBuffer, devBufferSize, input);
        aclmdlDataset *output = nullptr;
        // Call the custom function CreateOutput to create the aclmdlDataset data output for storing the output data of model inference. modelDesc indicates the description of the model.
        CreateOutput(output, modelDesc);
        {
            std::lock_guard<std::recursive_mutex> lk(freePoolMutex_);
            freeMemoryPool_[input] = output;
        }
}
// -----Key implementation of the custom function InitMemPool-----

// 2 Model inference
// 2.1 Create thread tid and specify it as the thread for processing callback functions on the stream.
// ProcessCallback is the thread function. In this function, call aclrtProcessReport to trigger callback function processing after waiting for a specified period of time.
pthread_t tid;
(void)pthread_create(&tid, nullptr, ProcessCallback, &s_isExit);

// 2.2 Specify the thread for processing callback functions on the stream.
aclrtSubscribeReport(tid, stream_);

// 2.3 Create a callback function for processing model inference results. The callback function is user-defined.
void ModelProcess::CallBackFunc(void *arg)
{
    std::map<aclmdlDataset *, aclmdlDataset *> *dataMap =
        (std::map<aclmdlDataset *, aclmdlDataset *> *)arg;

    aclmdlDataset *input = nullptr;
    aclmdlDataset *output = nullptr;
    MemoryPool *memPool = MemoryPool::Instance();

    for (auto& data : *dataMap) {
        ModelProcess::OutputModelResult(data.second);
        memPool->FreeMemory(data.first, data.second);
    }

    delete dataMap;
}

// 2.4 Custom function ExecuteAsync, which executes model inference
// -----Key implementation of the custom function ExecuteAsync starts-----
// g_callbackInterval indicates the callback interval. The default value is 1, which means a callback task is delivered after one asynchronous inference.
bool isCallback = (g_callbackInterval != 0);
size_t callbackCnt = 0;
std::map<aclmdlDataset *, aclmdlDataset *> *dataMap = nullptr;
aclmdlDataset *input = nullptr;
aclmdlDataset *output = nullptr;
MemoryPool *memPool = MemoryPool::Instance();
// g_executeTimes indicates the number of times asynchronous model inference is executed. The default value is 100.
for (uint32_t cnt = 0; cnt < g_executeTimes; ++cnt) {
    if (memPool->mallocMemory(input, output) != SUCCESS) {
        ERROR_LOG("get free memory failed");
        return FAILED;
    }
    // Perform asynchronous inference.
    aclError ret = aclmdlExecuteAsync(modelId_, input, output, stream_);

    if (isCallback) {
        if (dataMap == nullptr) {
            dataMap = new std::map<aclmdlDataset *, aclmdlDataset *>;
            if (dataMap == nullptr) {
                ERROR_LOG("malloc list failed, modelId is %u", modelId_);
                memPool->FreeMemory(input, output);
                return FAILED;
            }
        }
        (*dataMap)[input] = output;
        callbackCnt++;
        if ((callbackCnt % g_callbackInterval) == 0) {
            // Add a callback function to be executed to the task queue of the stream.
            ret = aclrtLaunchCallback(CallBackFunc, (void *)dataMap, ACL_CALLBACK_BLOCK, stream_);
            if (ret != ACL_SUCCESS) {
                ERROR_LOG("launch callback failed, index=%zu", callbackCnt);
                memPool->FreeMemory(input, output);
                delete dataMap;
                return FAILED;
            }
            dataMap = nullptr;
        }

    }
}
// -----End of the key implementation inside the custom function ExecuteAsync-----

// 2.5 For asynchronous inference, block the application until all tasks in the specified stream are complete
aclrtSynchronizeStream(stream_);

// 2.6 Deregister the thread so that callback functions on the stream are no longer processed by the specified thread. 
aclrtUnSubscribeReport(static_cast<uint64_t>(tid), stream_);
s_isExit = true;
(void)pthread_join(tid, nullptr);

......
```
