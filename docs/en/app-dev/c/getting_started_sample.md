# Getting Started Sample

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:37:53.251Z pushedAt=2026-10-26T03:10:39.435Z nl=2 -->

## Sample Function

This sample demonstrates how to use the CANN Runtime API and the Add operator in the operator library to implement vector addition: out = self + alpha × other.

```bash
Input vectors:
  self:   [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
  other:  [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
  alpha:  1.0

Vector addition result:
  out:   [1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5, 12.0]
```

## Compiling and Running the Application

You can click [here](https://gitcode.com/cann/runtime/tree/9.2.0/example/0_quickstart/0_hello_cann) to obtain the complete sample code. The **README.md** file of this sample also provides instructions for compiling and running the sample.

## Understanding the Key Code Logic

This section describes the sample code logic in the order of application development: **resource initialization → stream creation → input preparation → Add operator call → result output → resource release → resource deinitialization**. This section also helps you understand the functions of key APIs in CANN application development. The names of these key APIs are prefixed with **acl**, and are hereinafter referred to as acl APIs.

1. **Initialize resources**.

    ```cpp
    // Initialize the system. nullptr indicates that the system is initialized with the default configuration. Before calling other acl APIs, you must initialize the system first. Otherwise, subsequent internal resource initialization may fail, causing other service exceptions.
    aclInit(nullptr); 
    
    // Specify the compute device.
    int32_t deviceId = 0;
    aclrtSetDevice(deviceId);
    ```

2. **Create a stream**.

    ```cpp
    // A stream is equivalent to a task queue. Tasks are executed in the order in which they enter the queue.
    aclrtStream stream = nullptr;
    aclrtCreateStream(&stream);
    ```

3. **Prepare the input.**

    According to the formula of the Add operator (out = self + alpha × other), **self** and **other** are the two input vectors to be added, **alpha** is the coefficient, and **out** is the result vector after addition. Therefore, when preparing the input, you need to create two input tensors, a scalar representing the coefficient, and an output tensor. When creating the input and output tensors, you need to allocate device memory to store the input or output data.

    1. **Define a general API for creating tensors.**

        ```cpp
        template <typename T>
        int CreateAclTensor(const std::vector<T>& hostData, const std::vector<int64_t>& shape, void** deviceAddr, aclDataType dataType, aclTensor** tensor)
        {
            auto size = GetShapeSize(shape) * sizeof(T);
            // Allocate device memory.
            aclrtMalloc(deviceAddr, size, ACL_MEM_MALLOC_HUGE_FIRST);
            // Copy input data from the host to the device synchronously.
            aclrtMemcpy(*deviceAddr, size, hostData.data(), size, ACL_MEMCPY_HOST_TO_DEVICE);
            // Calculate strides.
            std::vector<int64_t> strides(shape.size(), 1);
            for (int64_t i = shape.size() - 2; i >= 0; i--) {
                strides[i] = shape[i + 1] * strides[i + 1];
            }
            // Create a tensor.
            *tensor = aclCreateTensor(shape.data(), shape.size(), dataType, strides.data(), 0, aclFormat::ACL_FORMAT_ND, shape.data(), shape.size(), *deviceAddr);
            return 0;
        }
        ```

    2. **Create the input and output tensors and a coefficient scalar.**

        ```cpp
        std::vector<int64_t> shape{8}; // The vector length is 8.
        void* selfDeviceAddr = nullptr;
        void* otherDeviceAddr = nullptr;
        void* outDeviceAddr = nullptr;
        aclDataBuffer* outDataBuffer = nullptr;
        aclTensor* self = nullptr;
        aclTensor* other = nullptr;
        aclTensor* out = nullptr;
        aclScalar* alpha = nullptr;
        std::vector<float> selfHostData = {1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f, 7.0f, 8.0f};    // Input data of the self vector
        std::vector<float> otherHostData = {0.5f, 1.0f, 1.5f, 2.0f, 2.5f, 3.0f, 3.5f, 4.0f};   // Input data of the other vector
        std::vector<float> outHostData(8, 0.0f);   
        float alphaValue = 1.0f;       // Coefficient value
        
        // Create the input tensor
        CreateAclTensor(selfHostData, shape, &selfDeviceAddr, aclDataType::ACL_FLOAT, &self);
        CreateAclTensor(otherHostData, shape, &otherDeviceAddr, aclDataType::ACL_FLOAT, &other);
        // Create the alpha scalar
        alpha = aclCreateScalar(&alphaValue, aclDataType::ACL_FLOAT);
        // Create the output tensor
        CreateAclTensor(outHostData, shape, &outDeviceAddr, aclDataType::ACL_FLOAT, &out);
        ```

4. **Call the Add operator**.

    ```cpp
    // Call the built-in CANN operator, which typically uses two-stage APIs.
    
    // The first-stage API aclnnAddGetWorkspaceSize performs input parameter verification, infers the output shape in dynamic shape scenarios, performs data tiling, and calculates the workspace memory size required for operator execution.
    uint64_t workspaceSize = 0;
    aclOpExecutor* executor = nullptr;
    ret = aclnnAddGetWorkspaceSize(self, other, alpha, out, &workspaceSize, &executor);
    
    // The second-stage API aclnnAdd executes the operator computation, which internally involves DFX (such as dump and overflow detection) and calls the LaunchKernel API provided by Runtime.
    // workspaceAddr indicates the workspace memory address allocated on the device side.
    ret = aclnnAdd(workspaceAddr, workspaceSize, executor, stream);
    
    // Synchronously wait for the task to complete.
    aclrtSynchronizeStream(stream);
    ```

5. **Output the result.**

    Copy the result data from the device side back to the host.

    ```cpp
    // outBufferAddr indicates the memory address for storing the result data on the device.
    // resultData.data() indicates the memory address for storing the data on the host.
    aclrtMemcpy(resultData.data(), resultData.size() * sizeof(float), outBufferAddr, size * sizeof(float), ACL_MEMCPY_DEVICE_TO_HOST);
    ```

6. **Release resources.**

    ```cpp
    // Destroy the tensor and scalar.
    aclDestroyTensor(self);
    aclDestroyTensor(other);
    aclDestroyScalar(alpha);
    aclDestroyTensor(out);
     
    // Release the device memory.
    aclrtFree(selfDeviceAddr);
    aclrtFree(otherDeviceAddr);
    aclrtFree(outDeviceAddr);
    aclrtFree(workspaceAddr);
    
    // Destroy the stream.
    aclrtDestroyStream(stream);
    ```

7. **Deinitialize resources.**

    ```cpp
    // Reset the device.
    aclrtResetDeviceForce(deviceId);
    // Deinitialize.
    aclFinalize();
    ```
