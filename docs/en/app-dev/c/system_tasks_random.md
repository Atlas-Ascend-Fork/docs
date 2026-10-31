# Random Number Generation

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:34:06.903Z pushedAt=2026-10-22T07:50:53.016Z nl=2 -->

In addition to dispatching kernel tasks, Runtime also supports dispatching built-in system tasks for random number generation. Unlike kernel tasks, system tasks do not require you to provide execution code. A system task can be dispatched to a stream for asynchronous execution, and it also follows the rule of ordered execution of tasks on the same stream.

The following is an example of calling **aclrtRandomNumAsync** to execute a random number generation task:

```c
aclError NormalFloatAsync(
    float mean, float stddev, uint64_t seed, uint64_t num, void *counterDevAddr, void *devOutput, aclrtStream stream)
{
    aclrtRandomNumTaskInfo taskInfo = {};
    taskInfo.dataType = ACL_FLOAT;
    taskInfo.randomNumFuncParaInfo.funcType = ACL_RT_RANDOM_NUM_FUNC_TYPE_NORMAL_DIS;
    taskInfo.randomParaAddr = NULL;
    taskInfo.randomCounterAddr = counterDevAddr;
    taskInfo.randomResultAddr = devOutput;
    memcpy(taskInfo.randomNumFuncParaInfo.paramInfo.normalDisInfo.mean.valueOrAddr, &mean, sizeof(float));
    taskInfo.randomNumFuncParaInfo.paramInfo.normalDisInfo.mean.size = sizeof(float);
    taskInfo.randomNumFuncParaInfo.paramInfo.normalDisInfo.mean.isAddr = 0;
    memcpy(taskInfo.randomNumFuncParaInfo.paramInfo.normalDisInfo.stddev.valueOrAddr, &stddev, sizeof(float));
    taskInfo.randomNumFuncParaInfo.paramInfo.normalDisInfo.stddev.size = sizeof(float);
    taskInfo.randomNumFuncParaInfo.paramInfo.normalDisInfo.stddev.isAddr = 0;
    memcpy(taskInfo.randomSeed.valueOrAddr, &seed, sizeof(uint64_t));
    taskInfo.randomSeed.size = sizeof(uint64_t);
    taskInfo.randomSeed.isAddr = 0;
    memcpy(taskInfo.randomNum.valueOrAddr, &num, sizeof(uint64_t));
    taskInfo.randomNum.size = sizeof(uint64_t);
    taskInfo.randomNum.isAddr = 0;
    return aclrtRandomNumAsync(&taskInfo, stream, NULL);
}
int main()
{
    aclError ret;
    // Initialize ACL.
    ret = aclInit(NULL);
    ret = aclrtSetDevice(0);
    aclrtStream stream;
    ret = aclrtCreateStream(&stream);
    uint64_t num = 128;
    size_t size = num * sizeof(uint64_t);  // Allocate a sufficiently large memory block.
    // Allocate device memory.
    void *devOutput = NULL;
    ret = aclrtMalloc(&devOutput, size, ACL_MEM_MALLOC_NORMAL_ONLY);
    // Prepare host data.
    void *hostOutput = malloc(size);
    // Allocate 16-byte device memory for storing the random number state counter.
    void *counterAddr = NULL;
    ret = aclrtMalloc((void **)&counterAddr, 16, ACL_MEM_MALLOC_NORMAL_ONLY);
    
    float mean = 3.0;
    float stddev = 2.0;    
    ret = NormalFloatAsync(mean, stddev, 0, num, counterAddr, devOutput, stream);
    // Synchronize the stream.
    aclrtSynchronizeStream(stream);
    // Copy the result back.
    aclrtMemcpy(hostOutput, size, devOutput, size, ACL_MEMCPY_DEVICE_TO_HOST);
    
    // Release resources.
    free(hostOutput);
    aclrtFree(devOutput);
    aclrtFree(counterAddr);
    aclrtDestroyStream(stream);
    aclrtResetDeviceForce(0);
    aclFinalize();
    return 0;
}
```
