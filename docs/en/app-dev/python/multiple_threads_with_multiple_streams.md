# Multithreading, Multistreaming Scenario

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......
def run_thread():
    device_id = 0

    # Specify a compute device.
    ret = acl.rt.set_device(device_id)
    # Explicitly create a stream.
    stream, ret = acl.rt.create_stream()

    # Call the task triggering API.
    # ....

    # Destroy allocations.
    ret = acl.rt.destroy_stream(stream)


# Create two threads. Each thread internally creates a stream.
thread_id1, ret = acl.util.start_thread(run_thread, None)
thread_id2, ret = acl.util.start_thread(run_thread, None)
# Explicitly call the stop_thread function to ensure that the threads are ended.
ret = acl.util.stop_thread(thread_id1)
ret = acl.util.stop_thread(thread_id2)
```
