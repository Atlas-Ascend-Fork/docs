# Device Synchronization

Following the API calls, add exception handling branches and specify log printing of error and information levels. The sample code of key steps is as follows, which is for reference only. Do not directly copy and run the code.

```python
import acl
# ......

device_id = 0

# Specify a device.
ret = acl.rt.set_device(device_id)

# Create a stream.
stream, ret = acl.rt.create_stream()

# Blocks app execution until the compute device has completed all preceding requested tasks.
ret = acl.rt.synchronize_device()

# Destroy allocations.
ret = acl.rt.synchronize_stream(stream)
ret = acl.rt.reset_device(device_id)
```
