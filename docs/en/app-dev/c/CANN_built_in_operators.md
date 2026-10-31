# CANN Built-in Operator Call

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:26:59.970Z pushedAt=2026-10-26T03:10:39.414Z nl=2 -->

## Overview

The CANN operator library provides an extensive set of deeply optimized, hardware-friendly, high-performance built-in operators that can be directly applied to AI service. An operator consists of a device-side kernel implementation and a host-side call. For ease of call, each operator provides a corresponding C language API for users to call on the host side, hereinafter referred to as the single-operator API (or operator host API).

This chapter mainly describes the call of single-operator APIs, which adopt the "two-stage API" form, use **aclnn** as the API prefix, and follow the camelCase naming style. The specific format is as follows:

```text
aclnnStatus aclnnXxxGetWorkspaceSize(const aclTensor *src, ..., aclTensor *out, ..., uint64_t *workspaceSize, aclOpExecutor **executor)
aclnnStatus aclnnXxx(void *workspace, uint64_t workspaceSize, aclOpExecutor *executor, aclrtStream stream)
```

Here, **_Xxx_** indicates the corresponding operator type, such as the Add operator. The specific functions of the two-stage API are as follows:

- First-stage API **aclnn_Xxx_GetWorkspaceSize**: completes tasks such as input parameter verification, output shape inference in dynamic shape scenarios, data tiling, and calculation of the workspace memory size required by the operator during execution.
- Second-stage API **aclnn_Xxx_**: The executor performs the computation, and the framework automatically calls DFX (for example, Dump and overflow detection) and the **LaunchKernel** API provided by Runtime.

## Operator Classification

CANN operators are mainly classified into the following categories:

- **Math operators**: numerical computation operators that provide numerical processing and computation at different dimensions, such as Add and Abs, covering scenarios such as tensor shape transformation, basic mathematical operations, and random number generation.
- **NN operators**: neural network operators that provide common computation operators in deep learning models, such as convolution, matrix multiplication, activation functions, and normalization.
- **CV operators**: computer vision operators that provide image processing and object detection operators, such as GridSample.
- **Transformer operators**: large model computation operators that provide core Transformer operators, such as Attention, LayerNorm, and merged compute and communication (MC2 for short) operators.

    Operators that fuse and parallelize collective communication and MatMul computation are collectively referred to as merged compute and communication operators (MC2 operators for short), such as AllGatherMatmul, AlltoAllAllGatherBatchMatMul, BatchMatMulReduceScatterAlltoAll, MatMulAllReduce, MatMulAllReduceAddRmsNorm, and MatMulReduceScatter.

For details about the operator Intermediate Representation (IR) specifications, see "Ascend IR Operator Specifications" in [Operator Library](https://gitcode.com/cann/docs/blob/9.2.0/docs/zh/ops-lib/0_README.md). For details about the API documentation corresponding to operators, see "Operator APIs (aclnn)" in [Operator Library](https://gitcode.com/cann/docs/blob/9.2.0/docs/zh/ops-lib/0_README.md).

When calling operator APIs, include the required header files and library files. Replace **$\{INSTALL\_DIR\}** with the file storage path after CANN software installation. For example, when it is installed by the **root** user, the default file storage path is **/usr/local/Ascend/cann**.

- Header file path: **$\{INSTALL\_DIR\}/include/** by default. You can reference the general header files of all operator categories (**aclnnop/aclnn\_ops\_math.h**, **aclnnop/aclnn\_ops\_nn.h**, **aclnnop/aclnn\_ops\_cv.h**, and **aclnnop/aclnn\_ops\_transformer.h**) or reference the header file of a single operator.

    **aclnnop/aclnn\_\*.h** (\* indicates the specific operator name).

- Library file path: **$\{INSTALL\_DIR\}/lib64/** by default. You can reference the general library files of all operator categories: **libopapi\_math.so**, **libopapi\_nn.so**, **libopapi\_cv.so**, and **libopapi\_transformer.so**. Note that starting from CANN 8.5.0, the general library file **libopapi.so** for all operators is deprecated. Do not use it.

To learn more about the implementation of the CANN operator library, visit the [CANN open-source project](https://gitcode.com/cann).

## Single-Operator API Call Process

**Figure 1** Single-operator API call process
![](figures/aclnn_API_call_process.png "Single-operator API call process")

The key APIs are described as follows. For details about the **acl**-prefixed APIs used in the process, see the *Runtime API*.

1. **Perform initialization:** Call **aclInit** to perform initialization.

2. **Allocate runtime resources:** Call APIs such as **aclrtSetDevice** and **aclrtCreateStream** to allocate runtime resources (device, context, and stream) in sequence.

3. **Allocate data memory and transfer data.**

    1. Call **aclrtMalloc** to allocate memory on the device to store the input and output data of the operator to be executed.
    2. Call **aclCreateTensor**, **aclCreateIntArray**, and other APIs to construct the input and output parameters of the operator. For details about the related APIs, see "Common APIs" in [Operator Library](https://gitcode.com/cann/docs/blob/9.2.0/docs/zh/ops-lib/0_README.md).

    If data on the host needs to be transferred to the device, call **aclrtMemcpy** (synchronous API) or **aclrtMemcpyAsync** (asynchronous API) to transfer data through memory copy.

4. **Calculate the workspace and execute the operator.**
    1. Call the **acl_xx__Xxx_GetWorkspaceSize** API to obtain the operator input parameters and calculate the workspace size required for executing the operator.
    2. Call the **aclrtMalloc** API to allocate memory on the device side based on the workspace size.
    3. Call the **acl_xx__Xxx_** API to execute the computation and obtain the result.

5. Call the **aclrtSynchronizeStream** API to **block the application** until all tasks in the specified stream are complete.
6. Call the **aclrtFree** API to **release the memory**.

    If the operator execution result data on the device needs to be transferred to the host, call the **aclrtMemcpy** API (synchronous API) or the **aclrtMemcpyAsync** API (asynchronous API) to transfer the data through memory copy, and then release the memory.

7. **Release runtime resources**.
    1. Call **aclDestroyTensor**, **aclDestroyIntArray**, and other APIs to release the input and output parameters of the operator. For details about the related APIs, see "Common APIs" in [Operator Library](https://gitcode.com/cann/docs/blob/9.2.0/docs/zh/ops-lib/0_README.md).
    2. After all data is released, call APIs such as **aclrtDestroyStream** and **aclrtResetDevice** to release the runtime resources (stream, context, and device) in sequence.

8. **Perform deinitialization:** Call the **aclFinalize** API to implement deinitialization.

<a id="section9465185611515"></a>

## Sample Code

Using the **Add operator API call** as an example, this section describes the basic logic of the operator's two-stage API call. The call process of other operators is similar. Modify it as needed based on the actual situation.

The Add operator implements tensor addition, and its calculation formula is y=x<sub>1</sub>+αxx<sub>2</sub>. You can obtain the following sample code and name the file **test\_add.cpp**. The code is as follows:

```cpp
#include <iostream>
#include <vector>
#include "acl/acl.h"
#include "aclnnop/aclnn_add.h"

#define CHECK_RET(cond, return_expr) \
  do {                               \
    if (!(cond)) {                   \
      return_expr;                   \
    }                                \
  } while (0)

#define LOG_PRINT(message, ...)     \
  do {                              \
    printf(message, ##__VA_ARGS__); \
  } while (0)

int64_t GetShapeSize(const std::vector<int64_t>& shape) {
  int64_t shape_size = 1;
  for (auto i : shape) {
    shape_size *= i;
  }
  return shape_size;
}

int Init(int32_t deviceId, aclrtStream* stream) {
  // Fixed format. Initialization.
  auto ret = aclInit(nullptr);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclInit failed. ERROR: %d\n", ret); return ret);
  ret = aclrtSetDevice(deviceId);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtSetDevice failed. ERROR: %d\n", ret); return ret);
  ret = aclrtCreateStream(stream);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtCreateStream failed. ERROR: %d\n", ret); return ret);
  return 0;
}

template <typename T>
int CreateAclTensor(const std::vector<T>& hostData, const std::vector<int64_t>& shape, void** deviceAddr,
                    aclDataType dataType, aclTensor** tensor) {
  auto size = GetShapeSize(shape) * sizeof(T);
  // Call aclrtMalloc to allocate device-side memory.
  auto ret = aclrtMalloc(deviceAddr, size, ACL_MEM_MALLOC_HUGE_FIRST);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtMalloc failed. ERROR: %d\n", ret); return ret);
  // Call aclrtMemcpy to copy host-side data to the device-side memory.
  ret = aclrtMemcpy(*deviceAddr, size, hostData.data(), size, ACL_MEMCPY_HOST_TO_DEVICE);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtMemcpy failed. ERROR: %d\n", ret); return ret);
  // Calculate the strides of consecutive tensors.
  std::vector<int64_t> strides(shape.size(), 1);
  for (int64_t i = shape.size() - 2; i >= 0; i--) {
    strides[i] = shape[i + 1] * strides[i + 1];
  }
  // Call aclCreateTensor to create an aclTensor.
  *tensor = aclCreateTensor(shape.data(), shape.size(), dataType, strides.data(), 0, aclFormat::ACL_FORMAT_ND,
                            shape.data(), shape.size(), *deviceAddr);
  return 0;
}

int main() {
  // 1. (Fixed format) Initialize the device/stream.
  // Set deviceId based on your actual device.
  int32_t deviceId = 0;
  aclrtStream stream;
  auto ret = Init(deviceId, &stream);
  // check as needed.
  CHECK_RET(ret == 0, LOG_PRINT("Init acl failed. ERROR: %d\n", ret); return ret);

  // 2. Construct the input and output. Customize the construction based on the API.
  std::vector<int64_t> selfShape = {4, 2};
  std::vector<int64_t> otherShape = {4, 2};
  std::vector<int64_t> outShape = {4, 2};
  void* selfDeviceAddr = nullptr;
  void* otherDeviceAddr = nullptr;
  void* outDeviceAddr = nullptr;
  aclTensor* self = nullptr;
  aclTensor* other = nullptr;
  aclScalar* alpha = nullptr;
  aclTensor* out = nullptr;
  std::vector<float> selfHostData = {0, 1, 2, 3, 4, 5, 6, 7};
  std::vector<float> otherHostData = {1, 1, 1, 2, 2, 2, 3, 3};
  std::vector<float> outHostData = {0, 0, 0, 0, 0, 0, 0, 0};
  float alphaValue = 1.2f;
  // Create the self aclTensor.
  ret = CreateAclTensor(selfHostData, selfShape, &selfDeviceAddr, aclDataType::ACL_FLOAT, &self);
  CHECK_RET(ret == ACL_SUCCESS, return ret);
  // Create the other aclTensor.
  ret = CreateAclTensor(otherHostData, otherShape, &otherDeviceAddr, aclDataType::ACL_FLOAT, &other);
  CHECK_RET(ret == ACL_SUCCESS, return ret);
  // Create the alpha aclScalar.
  alpha = aclCreateScalar(&alphaValue, aclDataType::ACL_FLOAT);
  CHECK_RET(alpha != nullptr, return ret);
  // Create the out aclTensor.
  ret = CreateAclTensor(outHostData, outShape, &outDeviceAddr, aclDataType::ACL_FLOAT, &out);
  CHECK_RET(ret == ACL_SUCCESS, return ret);

  // 3. Call the CANN operator library API. Change it to the specific operator API.
  uint64_t workspaceSize = 0;
  aclOpExecutor* executor;
  // Call the first-stage API of aclnnAdd.
  ret = aclnnAddGetWorkspaceSize(self, other, alpha, out, &workspaceSize, &executor);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclnnAddGetWorkspaceSize failed. ERROR: %d\n", ret); return ret);
  // Allocate device memory based on the workspaceSize calculated by the first-stage API.
  void* workspaceAddr = nullptr;
  if (workspaceSize > 0) {
    ret = aclrtMalloc(&workspaceAddr, workspaceSize, ACL_MEM_MALLOC_HUGE_FIRST);
    CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("allocate workspace failed. ERROR: %d\n", ret); return ret);
  }
  // Call the second-stage API of aclnnAdd.
  ret = aclnnAdd(workspaceAddr, workspaceSize, executor, stream);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclnnAdd failed. ERROR: %d\n", ret); return ret);

  // 4. (Fixed format) Synchronously wait for the task execution to complete.
  ret = aclrtSynchronizeStream(stream);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtSynchronizeStream failed. ERROR: %d\n", ret); return ret);

  // 5. Obtain the output value and copy the result from the device memory to the host memory. Modify this step based on the specific API definition.
  auto size = GetShapeSize(outShape);
  std::vector<float> resultData(size, 0);
  ret = aclrtMemcpy(resultData.data(), resultData.size() * sizeof(resultData[0]), outDeviceAddr, size * sizeof(float),
                    ACL_MEMCPY_DEVICE_TO_HOST);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("copy result from device to host failed. ERROR: %d\n", ret); return ret);
  for (int64_t i = 0; i < size; i++) {
    LOG_PRINT("result[%ld] is: %f\n", i, resultData[i]);
  }

  // 6. Release aclTensor and aclScalar. Modify this step based on the specific API definition.
  aclDestroyTensor(self);
  aclDestroyTensor(other);
  aclDestroyScalar(alpha);
  aclDestroyTensor(out);

  // 7. Release device resources. Modify this step based on the specific API definition.
  aclrtFree(selfDeviceAddr);
  aclrtFree(otherDeviceAddr);
  aclrtFree(outDeviceAddr);
  if (workspaceSize > 0) {
    aclrtFree(workspaceAddr);
  }
  aclrtDestroyStream(stream);
  aclrtResetDevice(deviceId);
  aclFinalize();
  return 0;
}
```

<a id="section1930615371323"></a>

## CMakeLists File

The following uses the compilation of the **Add operator** as an example. The CMake file is defined as follows. Modify it based on the actual situation.

```cmake
# CMake lowest version requirement
cmake_minimum_required(VERSION 3.14)

# Set the project name.
project(ACLNN_EXAMPLE)

# Compile options
add_compile_options(-std=c++11)

# Set the compilation options.
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY  "./bin")
set(CMAKE_CXX_FLAGS_DEBUG "-fPIC -O0 -g -Wall")
set(CMAKE_CXX_FLAGS_RELEASE "-fPIC -O2 -Wall")

# Set the executable file name (for example, opapi_test) and specify the directory where the operator file *.cpp to be run is located.
add_executable(opapi_test
               test_add.cpp)

# Set ASCEND_PATH (the CANN software package directory; modify it based on the actual path) and INCLUDE_BASE_DIR (the header file directory).
if(NOT "$ENV{ASCEND_CUSTOM_PATH}" STREQUAL "")
    set(ASCEND_PATH $ENV{ASCEND_CUSTOM_PATH})
else()
    set(ASCEND_PATH "/usr/local/Ascend/cann")
endif()
set(INCLUDE_BASE_DIR "${ASCEND_PATH}/include")
include_directories(
    ${INCLUDE_BASE_DIR}
    ${INCLUDE_BASE_DIR}/aclnn
)

# Set the library file path to be linked.
target_link_libraries(opapi_test PRIVATE
                      ${ASCEND_PATH}/lib64/libascendcl.so
                      ${ASCEND_PATH}/lib64/libnnopbase.so
                      ${ASCEND_PATH}/lib64/libopapi_${ops_project}.so)

# The executable file is located in the bin directory under the directory where the CMakeLists file resides.
install(TARGETS opapi_test DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
```

Here, **$\{ops\_project\}** indicates different types of operator libraries. Reference them as required:

- Math operators: reference the corresponding **libopapi\_math.so**.
- NN operators: reference **libopapi\_math.so** and **libopapi\_nn.so**.
- CV operators: reference **libopapi\_math.so** and **libopapi\_cv.so**.
- Transformer operators: reference **libopapi\_math.so** and **libopapi\_transformer.so**.

When calling MC2 operator APIs, multithreading and Huawei Collective Communication Library (HCCL) are generally involved. Therefore, the CMake file needs to additionally import the following content; otherwise, compilation will fail.

```cmake
# Set the library file path for linking.
find_package(Threads REQUIRED)
target_link_libraries(opapi_test PRIVATE
                      ${ASCEND_PATH}/lib64/libascendcl.so
                      ${ASCEND_PATH}/lib64/libnnopbase.so
                      ${ASCEND_PATH}/lib64/libopapi_${ops_project}.so
                      ${ASCEND_PATH}/lib64/libhccl.so      # Collective communication library file
                      ${CMAKE_THREAD_LIBS_INIT})            # Library file that multithreading depends on
```

**find\_package\(Threads REQUIRED\)** is a CMake command used to find the thread library. It can automatically link the header files that the thread library depends on and other indirectly dependent library files.

## Compilation and Running

This section uses the **combined development and runtime environment scenario** as an example, where the machine with the AI processor serves as both the development environment and the runtime environment. In this scenario, code development and code execution are performed on the same machine.

1. Based on the [sample code](#section9465185611515) and [CMakeLists file](#section1930615371323) provided earlier, prepare the operator call code (\*.cpp) and the compilation script (**CMakeLists.txt**) in advance.
2. Configure the environment variables.

    After CANN is installed, log in to the environment as the CANN running user and run the following command to make the environment variables take effect.

    ```bash
    source /usr/local/Ascend/cann/set_env.sh
    ```

3. Compile and run.
    1. Go to the directory where **CMakeLists.txt** is located and run the following command to create a **build** directory for storing the generated compilation files.

        ```bash
        mkdir -p build
        ```

    2. Go to the **build** directory, run the **cmake** command to compile, and then run the **make** command to generate the executable file.

        ```bash
        cd build
        cmake ../ -DCMAKE_CXX_COMPILER=g++ -DCMAKE_SKIP_RPATH=TRUE
        make
        ```

        After the compilation succeeds, the **opapi\_test** executable file is generated in the **bin** folder of the **build** directory.

    3. Go to the **bin** directory and run the executable file **opapi\_test**.

        ```bash
        cd bin
        ./opapi_test
        ```

        The following uses the running result of the Add operator as an example. The result after running is as follows:

        ![](figures/add_operator_execution_result.png)
