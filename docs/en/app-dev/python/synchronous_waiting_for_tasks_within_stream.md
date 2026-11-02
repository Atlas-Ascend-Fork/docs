# Intra-Stream Task Synchronization

After APIs are called, add an exception handling branch, and record error logs and warning logs. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......

# Explicitly create a stream.
stream, ret = acl.rt.create_stream()

# Pass the stream argument to the task triggering call.
ret = acl.rt.memcpy_async(dev_ptr, dev_size, host_ptr, host_size, ACL_MEMCPY_HOST_TO_DEVICE, stream)
# Call acl.rt.synchronize_stream to block the app until all tasks in the specified stream are complete.
ret = acl.rt.synchronize_stream(stream)

# Explicitly destroy the stream after using the stream.
ret = acl.rt.destroy_stream(stream)
# ......
```
