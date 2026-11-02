# Synchronous Wait of Tasks Between Streams (Implemented Using Events)

The synchronization of tasks between multiple streams can be implemented by using events. The `acl.rt.stream_wait_event` API is called to block the running of a specified stream until the specified event is complete. Call `acl.rt.record_event` before the `acl.rt.stream_wait_event` call.

For details about the model loading and execution process, see [Model Management](model_management.md).

For details about the operator loading and execution process, see [Single-Operator Calling](single_operator_invoke.md).

**Figure 1** Synchronization between streams
![](figures/synchronization-between-streams.png)

After APIs are called, add an exception handling branch, and record error logs and warning logs. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......
# Creates an event.
event, ret = acl.rt.create_event()

# Create two streams.
s1, ret = acl.rt.create_stream()
s2, ret = acl.rt.create_stream()

# Append an event to s1.
ret = acl.rt.record_event(event, s1)

# Block s2 until the event is complete, that is, the completion of s1.
# Wake up s2 for execution after s1 is complete.
ret = acl.rt.stream_wait_event(s2, event)

ret = acl.rt.synchronize_stream(s1)
ret = acl.rt.synchronize_stream(s2)

# Explicitly destroy resources.
ret = acl.rt.destroy_stream(s2)
ret = acl.rt.destroy_stream(s1)
ret = acl.rt.destroy_event(event)
# ......
```
