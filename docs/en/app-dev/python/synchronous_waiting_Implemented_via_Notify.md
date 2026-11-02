# Synchronous Wait of Tasks Between Streams (Implemented Using Notify)

The synchronization of tasks between multiple streams can be implemented by using Notify. For example, if the task of stream2 depends on the task of stream1, to ensure that the task in stream1 is completed first, you can create a Notify and call the `acl.rt.record_notify` API to insert the Notify into stream1 (usually called the Record Notify task). Call the `acl.rt.wait_and_reset_notify` API to insert a task (usually called Wait Notify task) to stream2.

**Figure 1** Synchronization between streams
![](figures/synchronization-between-streams-1.png)

For details about the model loading and execution process in the preceding figure, see [Model Management](model_management.md). For details about the operator loading and execution process, see [Single-Operator Calling](single_operator_invoke.md).

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to be built or run.

```python
import acl
# ......
# Create a Notify object.
notify, ret = acl.rt.create_notify(0)

# Create stream_1 and stream_2.
stream_1, ret = acl.rt.create_stream()
stream_2, ret = acl.rt.create_stream()

# Append the Notify object to stream_1.
ret = acl.rt.record_notify(notify, stream_1)

# Block stream_2 until the specified Notify occurs, which means stream_1 is executed.
# Wake up stream_2 for execution after stream_1 is complete.
ret = acl.rt.wait_and_reset_notify(notify, stream_2, 0)

ret = acl.rt.synchronize_stream(stream_1)
ret = acl.rt.synchronize_stream(stream_2)

# Explicitly destroy allocations.
ret = acl.rt.destroy_stream(stream_2)
ret = acl.rt.destroy_stream(stream_1)
ret = acl.rt.destroy_notify(notify)
# ......
```
