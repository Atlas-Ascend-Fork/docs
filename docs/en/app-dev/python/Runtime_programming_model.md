# Programming Model

## Host and Device Programming Model

**Host**: A host is an x86 or Arm server CPU that connects to one or more devices through a bus. The host utilizes the compute capabilities (for example, Neural-Network [NN]) provided by the device to implement services.

**Device** **(NPU)**: A device refers to the hardware equipped with AI processors. It connects to the host through a bus (such as PCIe and HCCS), providing compute capabilities (for example, NN). HCCS stands for Huawei Cache Coherence System.

The following figure shows the relationship between the host and the device.

![](figures/logic_structure_image.png)

The summary is as follows:

1. **The host and device each possess independent memory spaces.** Runtime provides memory allocation APIs for both the host and device, along with memory copy APIs to transfer data between them. During programming, you must distinguish between host and device memory allocations and explicitly call the memory copy APIs to transfer data from the host to the device. This ensures that the device hardware accelerator achieves optimal performance when accessing its local memory.
2. **The host and device use the asynchronous parallel execution mode.**

    After the host delivers a task to the device, the host **does not wait for the task to complete on the device** and immediately returns. The device then starts scheduling and executing the delivered task. The CPU on the host can work in parallel with the accelerator on the device. Asynchronous task submission APIs typically include a stream parameter, indicating that the task is dispatched into the specified stream for execution.

    When the host needs to obtain the compute result from the device, it must explicitly call a synchronous API. The synchronous API blocks the host CPU until the task on the device is complete.

    This asynchronous parallel execution mechanism effectively hides the host processing time or the data transfer latency between the host and the device, improving throughput and shortening the end-to-end execution time.

3. **The asynchronous task is dispatched to the stream for execution.**

    Tasks in a stream are executed in order, and tasks in different streams are executed in parallel. For example, in the following figure, the host starts the Kernel 1, Kernel 2, and Kernel 3 tasks in sequence. The execution sequence is as follows:

    - Kernel 1 and Kernel 3 are in the same stream. Therefore, Kernel 3 is started only after Kernel 1 is completed.
    - Kernel 2 is not in the same stream as Kernel 1 and Kernel 3. Therefore, Kernel 2 can be executed in parallel with Kernel 1 and Kernel 3.

    ![](figures/relationship_among_Device-Context-Stream_0.png)

## Main Programming Concepts of Runtime

- A **host** is the abstraction of Runtime on the host.
- A **device** represents the abstraction of the hardware device where the AI processor is installed. Typically, one host maps to *N* devices. The user application can call ACL APIs such as `aclrtSetDevice` to specify the compute device.
- A **context** is the logical operating environment of a device. The relationship between contexts and devices is *N*:1, meaning that each context must belong to a unique device. A context manages the lifetime of its runtime resource objects (including streams, events, and Notifys, but excluding memory). Each unique context has isolated objects, and they cannot be synchronized with one another. Runtime errors are also isolated at the context level.
- A **stream** is a logical task execution queue provided by a device. Tasks can be asynchronously added to a stream, and tasks in the same stream are strictly executed in FIFO mode. The relationship between streams and contexts is *N*:1. A stream must belong to a unique context.
- A **task** is an execution task that can be added to a stream. Tasks can be classified into compute tasks, memory copy tasks, and event synchronization tasks. The relationship between tasks and streams is *N*:1. A task will be added to a unique stream.

The following figure shows the relationship between the device, context, and stream.

![](figures/relationship_among_Device-Context-Stream.png)

## Thread-Context Association

Most Runtime APIs do not have the device ID parameter because the device on which these APIs operate is obtained from the context associated with the calling thread. Therefore, when a host thread calls a Runtime API, the following requirements must be met:

- A thread (CPU thread on the host) can correctly call Runtime APIs only after being associated with a context.
- A thread can be associated with only one context at a time.
- Applications can explicitly create contexts to meet the requirements of runtime resource isolation. In this case, the context is visible to all threads in the same process, and the threads can switch the context by calling `aclrtGetCurrentContext` and `aclrtSetCurrentContext`.

The following code example describes the association and switching process between a thread and a context when the thread calls context-related APIs. The example is for reference only. Do not copy and run it.

```Python
# Initially, the thread is not associated with any context.
acl.init()
acl.rt.set_device(0)  # acl.rt.set_device creates a default context and associates the thread with the default context.
# Context associated with the thread: default context

ctx1, _ = acl.rt.create_context(0)  # Device 0 explicitly creates ctx1 and associates the thread with ctx1.
# Context associated with the thread: ctx1
current_ctx, _ = acl.rt.get_context()  # Obtain the context associated with the current thread. In this case, the returned current_ctx is ctx1.
# Context associated with the thread: ctx1

ctx2, _ = acl.rt.create_context(0)  # Device 0 explicitly creates ctx2 and associates the thread with ctx2.
# Context associated with the thread: ctx2

acl.rt.set_context(current_ctx)  # Switch the context. Because current_ctx is ctx1, the thread is associated with ctx1.
# Context associated with the thread: ctx1

acl.rt.set_context(current_ctx)  # Switch the context.
# Context associated with the thread: ctx2
.....

acl.rt.destroy_context(ctx2)  # The current thread is associated with ctx2. When ctx2 is destroyed, the thread is also disassociated from ctx2.
# Context associated with the thread: NA

# ctx2 has been destroyed. You should switch to another context (for example, ctx1).
acl.rt.set_context(ctx1)
# Context associated with the thread: ctx1
.....

acl.rt.destroy_context(ctx1);  # The current thread is associated with ctx1. When ctx1 is destroyed, the thread is also disassociated from ctx1.
# Context associated with the thread: NA
acl.rt.reset_device_force(0)
acl.finalize()
```

## Use Cases of Default Context and Default Stream

- A context and a stream must exist before operations for execution are dispatched on a device, and these can be created either explicitly or implicitly. The **implicitly** created context and stream are the default context and stream.

    To pass the default stream to any API call, pass **0** directly.

- The **default context** does not allow `acl.rt.get_context`, `acl.rt.set_context`, or `acl.rt.destroy_context` operations.
- An implicitly created context or stream is applicable to simple apps where only one compute device is needed. For multi-thread apps, you are advised to use the explicitly created contexts and streams.

The following is a code example for reference only. Do not copy and run it.

```python
# ...
ret = acl.init(config_path)
ret = acl.rt.set_device(device_id)

# In the default context, a default stream is created, and the stream is available in the current thread.
# ...
ret = acl.op.execute_v2(op1, input_desc, inputs, output_desc, outputs, attr, 0)  # 0 indicates that op1 is executed in the default stream.
ret = acl.op.execute_v2(op2, input_desc, inputs, output_desc, outputs, attr, 0)  # 0 indicates that op2 is executed in the default stream.
ret = acl.rt.synchronize_stream(0)

# Output the result as required when all computing tasks (op1 and op2 execution tasks) are complete.
# ...
ret = acl.rt.reset_device(device_id)  # Reset device 0. The lifetime of the corresponding default context and default stream end.
```
