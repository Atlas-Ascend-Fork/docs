# Feature Vector Search (FV)

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:09:24.396Z pushedAt=2026-10-22T02:06:49.647Z nl=2 -->

## Basic Principles

This section mainly verifies the feature search bfunction. It generates a random base library and randomly generates feature data for feature search (currently two search modes are supported: 1:N and M:N; the sample code below uses the 1:N mode as an example). The process can be roughly divided into the following main steps: initialization, adding features to the base library, base library search, precise modification or deletion of base library features, and deinitialization. The specific API call methods are as follows:

- **Initialization**: Call the **aclInit** API for initialization, and call the **aclfvCreateInitPara** API to create data of the **aclfvInitPara** type to specify the initialization parameters for feature vector search.
- **Adding features to the base library**: Mainly call the **aclfvCreateFeatureInfo** API to create data of the **aclfvFeatureInfo** type to represent the description information of the feature to be created, and then call **aclfvRepoAdd** to add it to the base library.
- **Repository search**: Call the **aclfvSearch** API to implement search.
- **Precise modification or deletion of base library features**: Call the **aclfvDel** and **aclfvModify** APIs to delete or modify a feature in the base library. The code below uses deleting a base library feature as an example.
- **Deinitialization**: Mainly includes releasing runtime resources, calling the **aclfvDestroyInitPara** API to destroy data of the **aclfvInitPara** type, and calling the **aclfvRelease** API to deinitialize the feature search module and release memory space.

## Sample Code

The examples in this section focus on the code logic of feature vector search. They cannot be directly copied, compiled, and run, and are for reference only. For the complete sample code, click [here](https://gitee.com/ascend/samples/tree/master/cplusplus/level1_single_api/9_feature_retrieval/feature_retrieval).

After calling the APIs, you need to add branches for exception handling and record error logs and prompt logs, which are not listed one by one here.

```cpp
// Set the default running mode to HOST.
aclrtRunMode runMode = ACL_HOST;

// 1. Initialize
// 1.1 Initialize the feature search module. Here, the number of features in the base library is 100000.
size_t fsNum = 100000;
fvInitPara = aclfvCreateInitPara(fsNum);

// 1.2 Specify the initialization parameters for feature vector search.
ret = aclfvInit(fvInitPara);

// 2. Add the base library and feature vectors.
// 2.1 Add the first feature. When creating the feature description, set the offset parameter to 0.
uint32_t offset = 0;
uint32_t featureCount = 1000;
uint32_t featureLen = 36;

// The custom function BaseShortFeaAlloc is used to generate random feature data and is implemented by the user.
void *featureData = BaseShortFeaAlloc(1000, static_cast<size_t>(featureCount), 0);
std::shared_ptr<void> feaBufPtr(featureData, [](void *p){(void)aclrtFreeHost(p);});
void *inputData = featureData;
std::shared_ptr<void> inputDataPtr = nullptr;

// If the running mode is ACL_HOST, allocate memory and then use aclrtMemcpy to transfer the random feature data from the host to the device. Otherwise, directly read the random feature data into the device memory.
if (aclrtGetRunMode(&runMode) == ACL_HOST) {
      // Allocate memory for inputData.
      ret = aclrtMalloc(&inputData, featureLen * featureCount, 
                        ACL_MEM_MALLOC_HUGE_FIRST);
      // Read the random feature data into the device memory.
      inputDataPtr.reset(inputData, [](void *p) {(void)aclrtFree(p);});
      // Copy featureData from the host to the device.      
      ret = aclrtMemcpy(inputData,
                        featureLen * featureCount,
                        featureData,
                        featureLen * featureCount,
                        ACL_MEMCPY_HOST_TO_DEVICE);
}

// Create the feature description. inputData indicates the random feature data generated in the previous step.
auto featureInfo = aclfvCreateFeatureInfo(id0, id1, offset, featureLen, featureCount, 
                        reinterpret_cast<uint8_t *>(inputData), featureLen * featureCount);

// Add a base library and add features to it. featureInfo indicates the feature description generated in the previous step.
aclError ret = aclfvRepoAdd(SEARCH_1_N, featureInfo);

// Destroy the aclfvFeatureInfo feature description.
aclfvDestroyFeatureInfo(featureInfo);

// 2.2 Add the second feature. When creating the feature description, set offset to the number of features already added to the library, and precisely delete or modify a feature in the base library.
offset += featureCount;

// For the steps of adding features to the base library, see the code in 2.1.
// ....

uint8_t featureData[36];
for (size_t i = 0; i < 36; i++) {
        featureData[i] = static_cast<uint8_t>(i);
}

// Create memory and transfer the feature data.
void *inputData = nullptr;
aclrtMalloc(&inputData, 36, ACL_MEM_MALLOC_HUGE_FIRST);
std::shared_ptr<void> inputDataPtr(inputData, [](void *p){(void)aclrtFree(p);});
aclrtMemcpyKind kind = ACL_MEMCPY_DEVICE_TO_DEVICE;

// If the running mode is ACL_HOST, copy the feature data to the device side. Otherwise, no copy is required. dataLen indicates the memory length requested by the featureData pointer.
if (aclrtGetRunMode(&runMode) == ACL_HOST) {
        kind = ACL_MEMCPY_HOST_TO_DEVICE;
}
aclrtMemcpy(inputData, 36, featureData, dataLen, kind);

// Create the feature description.
uint32_t id0 = 0;
uint32_t id1 = 0;
auto featureInfo1 = aclfvCreateFeatureInfo(id0, id1, offset, 36, 1,
                                          reinterpret_cast<uint8_t *>(inputData), 36);
std::shared_ptr<aclfvFeatureInfo> featureInfoPtr(featureInfo1,
                                          [](aclfvFeatureInfo *p){(void)aclfvDestroyFeatureInfo(p);});

// Delete one feature.
aclfvDel(featureInfo1);

// 2.3 Add features to other base libraries, where the first-level base library is 1 and the second-level base library is 1.
id0 = 1;
id1 = 1;
offset = 0; 

// Add features to the base library. For details, see the code in section 2.1.
// ....

// 3 Search the base library (using 1:N search as an example). This mainly includes three parts: feature search preprocessing, feature 1:N search, and feature search result processing.
// 3.1 Feature search preprocessing. For 1:N search, queryCnt must be 1.
uint32_t queryCnt = 1;
uint32_t topK = 5;
uint32_t dataLen = queryCnt * topK * sizeof(uint32_t);
uint32_t resultNumDataLen = queryCnt * sizeof(uint32_t);
const uint32_t tableLen = 32 * 1024; 
uint32_t tableDataLen = queryCnt * tableLen;

// Generate a data table. Users perform search and comparison through the data table. The custom function AdcTabInit here is used to initialize the Adc table for feature search input and is implemented by the user.
uint8_t *tableDataTmp = (uint8_t *)AdcTabInit(1000, queryCnt * 1024);
std::shared_ptr<void> tableDataTmpPtr(tableDataTmp,[](void *p){(void)aclrtFreeHost(p);});

// Allocate memory for the data table. tableDataDev is used to create the search input table information.
void *devPtr = nullptr;
aclrtMalloc(&devPtr, tableDataLen, ACL_MEM_MALLOC_HUGE_FIRST);
tableDataDev.reset(devPtr, [](void *p) {(void)aclrtFree(p);});

// Copy the table data to the device side.
uint8_t *devPtrTmp = reinterpret_cast<uint8_t *>(devPtr);
for (uint32_t i = 0; i < queryCnt; ++i) {
     for (uint32_t j = 0; j < 32; ++j) {
          uint8_t *dst = devPtrTmp + i * 32 * 1024 + j * 1024;
          uint8_t *src = tableDataTmp + i * 1024;
          aclrtMemcpy(dst, 1024, src, 1024, ACL_MEMCPY_HOST_TO_DEVICE);
     }
}

// Allocate memory for the search results. resultNumDev, id0Dev, id1Dev, resultOffsetDev, and resultDistanceDev.
aclrtMalloc(&devPtr, resultNumDataLen, ACL_MEM_MALLOC_HUGE_FIRST);
resultNumDev.reset(devPtr, [](void *p) {(void)aclrtFree(p);});
aclrtMalloc(&devPtr, dataLen, ACL_MEM_MALLOC_HUGE_FIRST);
id0Dev.reset(devPtr, [](void *p) {(void)aclrtFree(p);});
aclrtMalloc(&devPtr, dataLen, ACL_MEM_MALLOC_HUGE_FIRST);
id1Dev.reset(devPtr, [](void *p) {(void)aclrtFree(p);});
aclrtMalloc(&devPtr, dataLen, ACL_MEM_MALLOC_HUGE_FIRST);              
resultOffsetDev.reset(devPtr, [](void *p) {(void)aclrtFree(p);});
aclrtMalloc(&devPtr, dataLen, ACL_MEM_MALLOC_HUGE_FIRST);
resultDistanceDev.reset(devPtr, [](void *p) {(void)aclrtFree(p);}); 
 
// Create the search input table information. The result is used to create the search task input information.
aclfvQueryTable *searchQueryTable = aclfvCreateQueryTable(queryCnt, tableLen, reinterpret_cast<uint8_t *>
                                   (tableDataDev.get()), tableDataLen);
searchQueryTable.reset(searchQueryTable, [](aclfvQueryTable *p){(void)aclfvDestroyQueryTable(p);});

// Create the feature library range parameters. The result is used to create the search task input information.
aclfvRepoRange *searchRange = aclfvCreateRepoRange(0, 1023, 0, 1023); 
searchRange.reset(searchRange, [](aclfvRepoRange *p){(void)aclfvDestroyRepoRange(p);});

// Create the search task input information. The result is used for feature 1:N search.
aclfvSearchInput *searchInput = aclfvCreateSearchInput(searchQueryTable, searchRange, topK);
searchInput.reset(searchInput, [](aclfvSearchInput *p){(void)aclfvDestroySearchInput(p);});

// Create the search result information, which is used for 1:N feature search.
aclfvSearchResult *searchResult = aclfvCreateSearchResult(queryCnt,
                                   reinterpret_cast<uint32_t *>(resultNumDev.get()),
                                   resultNumDataLen,
                                   reinterpret_cast<uint32_t *>(id0Dev.get()),
                                   reinterpret_cast<uint32_t *>(id1Dev.get()),
                                   reinterpret_cast<uint32_t *>(resultOffsetDev.get()),
                                   reinterpret_cast<float *>(resultDistanceDev.get()),
                                   dataLen);
searchResult.reset(searchResult, [](aclfvSearchResult *p){(void)aclfvDestroySearchResult(p);});

// 3.2 1:N feature search
aclfvSearch(SEARCH_1_N, searchInput.get(), searchResult.get());

// 3.3 Process the feature search result.
// Obtain the search result.
uint32_t dataLen = queryCnt * topK * sizeof(uint32_t);
uint32_t *id0 = (uint32_t *)id0Dev.get();
uint32_t *id1 = (uint32_t *)id1Dev.get();
uint32_t *resultOffset= (uint32_t *)resultOffsetDev.get();
float *resultDistance = (float *)resultDistanceDev.get();

// If the running mode is ACL_HOST, call aclrtMemcpy to copy the search result from the device to the host. Otherwise, no copy is required.
if (aclrtGetRunMode(&runMode) == ACL_HOST) {
        // Copy data from the device to the host.
        id0 = (uint32_t *)malloc(dataLen);
        id0Ptr.reset(id0);
        id1 = (uint32_t *)malloc(dataLen);
        id1Ptr.reset(id1);
        resultOffset = (uint32_t *)malloc(dataLen);
        resultOffsetPtr.reset(resultOffset);
        resultDistance = (float *)malloc(dataLen);
        resultDistancePtr.reset(resultDistance);
        aclrtMemcpy(id0, dataLen, id0Dev.get(), dataLen, ACL_MEMCPY_DEVICE_TO_HOST);
        aclrtMemcpy(id1, dataLen, id0Dev.get(), dataLen, ACL_MEMCPY_DEVICE_TO_HOST);
        aclrtMemcpy(resultOffset, dataLen, resultOffsetDev.get(), dataLen, ACL_MEMCPY_DEVICE_TO_HOST);
        aclrtMemcpy(resultDistance, dataLen, resultDistanceDev.get(), dataLen, ACL_MEMCPY_DEVICE_TO_HOST);
}

// Display the data in the base library.
for (uint32_t i = 0; i < queryCnt; i++) {
     for (uint32_t j = 0; j < topK; ++j) {
          uint32_t i0 = id0[i * topK + j];
          uint32_t i1 = id1[i * topK + j];
          uint32_t offset = resultOffset[i * topK + j];
          float distance = resultDistance[i * topK + j];
    }
}

// 4. Delete the base library and data.
// Create a feature library range and delete the base library within the specified range.
uint32_t id0Min = 0;
uint32_t id0Max = 1023;
uint32_t id1Min = 0;
uint32_t id1Max = 1023;
aclfvRepoRange *repoRange = aclfvCreateRepoRange(id0Min, id0Max, id1Min, id1Max);
aclfvRepoDel(SEARCH_1_N, repoRange);
// Destroy the data of the aclfvInitPara type.
aclfvDestroyInitPara(fvInitPara);

......
```
