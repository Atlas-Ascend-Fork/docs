# Event-based Synchronization

After APIs are called, add an exception handling branch, and record error logs and warning logs. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......
# Creates an event.
event, ret = acl.rt.create_event()

# Creates a stream.
stream, ret = acl.rt.create_stream()

# Append an event to a stream.
ret = acl.rt.record_event(event, stream)

# Block the application execution and wait until the event is complete, that is, the completion of the stream.
# The stream completion event wakes up the control flow, starting the application execution.
ret = acl.rt.synchronize_event(event)

# Explicitly destroy resources.
ret = acl.rt.destroy_stream(stream)
ret = acl.rt.destroy_event(event)
# ......
```
