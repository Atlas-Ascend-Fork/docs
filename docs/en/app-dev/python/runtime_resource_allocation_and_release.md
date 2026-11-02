# Runtime Resource Allocation and Deallocation

During application development, the application must contain the code logic for resource allocation during running. For details about the API call sequence for resource allocation during running, see [API Calling Process](interface_calling_process.md). Then, see the description of the resource allocation and release processes in this section.

## Basic Principles

Allocate runtime resources including the device and stream **in sequence** to support the execution of computing and management tasks. After all data is processed, deallocate these runtime resources in sequence.

Streams can be created implicitly or explicitly based on the application scenarios.

- **Implicit** stream creation: applies to simple apps with low complicity of interaction logic. However, in multithreaded programming, each thread uses the default stream. The execution sequence of tasks in the default stream depends on the thread scheduling sequence of the operating system.
- **Explicit** stream creation: applies to large apps with complex interaction logic, offering better app readability and maintainability.

Single-process, single-thread, and single-stream scenarios are as follows:

- Single-process: Each app maps to one process.
- Single-thread: Only one thread is available by default unless you create more.
- Single-stream: A single stream is used in the entire development process.

    Asynchronous tasks in the same stream are executed in the sequence of tasks in the app.

- For details about multi-thread and multi-stream scenarios, see [Stream Management](stream_management.md).

## Runtime Resource Allocation

**Figure 1** Runtime resource allocation
![](figures/runtime-resource-allocation.png)

The key APIs are described as follows:

Allocate the devices and streams in sequence.

1. Call `acl.rt.set_device` to specify the compute device. This API also implicitly creates the default context and stream. However, the following constraints must be observed:
    - A device corresponds to a default context, which is destroyed when the `acl.rt.destroy_context` API is called. Therefore, you do not need to destroy the default context by explicit call.
    - A device corresponds to a default stream, which is destroyed when the `acl.rt.destroy_stream` API is called. Therefore, you do not need to destroy the default stream by explicit call.
    - The default context and stream are automatically destroyed with the reset of device using `acl.rt.reset_device`.

2. To use the default stream as the input parameter, pass `0`. Alternatively, you can call `acl.rt.create_stream` to explicitly create a stream instead of using the default stream.
3. (Optional) Call `acl.rt.get_run_mode` to obtain the running mode of the software stack and determine the subsequent memory allocation API calling logic based on the running mode.
    <!-- npu="910b,910,310p,310b" id1 -->
    If the query result is `ACL_HOST`, host memory needs to be allocated for data transfer.
    <!-- end id1 -->
    If the query result is `ACL_DEVICE`, only device memory needs to be allocated for data transfer.

## Runtime Resource Deallocation

**Figure 2** Runtime resource deallocation
![](figures/runtime-resource-deallocation.png)

The key APIs are described as follows:

Deallocate runtime resources in the following sequence: streams and devices.

1. If the `acl.rt.create_stream` API is called to explicitly create a stream, the `acl.rt.destroy_stream` API needs to be called to release the stream. Otherwise, the `acl.rt.destroy_stream` API does not need to be called.
2. Call the `acl.rt.reset_device` API to release the resources on the device. In addition, this API implicitly releases the default context and stream. You do not need to release the default context and stream separately.

## Sample Code

After APIs are called, add an exception handling branch, and record error logs and warning logs. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
#......

# ====== Allocate runtime resources. ======
# 1. Specify a compute device.
ret = acl.rt.set_device(device_id)


# 2. Explicitly create a stream.
#To reserve the execution order of asynchronous tasks.
stream, ret = acl.rt.create_stream()
# ====== Allocate runtime resources. ======

#......

# ====== Deallocate runtime resources. ======
ret = acl.rt.destroy_stream(stream)
ret = acl.rt.reset_device(device_id)
# ====== Deallocate runtime resources. ======

#......
```
