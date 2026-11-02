# Single-Threading, Multistreaming Scenario

After APIs are called, add an exception handling branch, and record error logs and warning logs. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......

device_id = 0
model_id_1 = 0
model_id_2 = 1

stream1, ret = acl.rt.create_stream()
# Call the task execution API. For example, the asynchronous model inference job is delivered to stream1.
ret = acl.mdl.execute_async(model_id_1, dataset_in_1, dataset_out_1, stream1)

stream2, ret = acl.rt.create_stream()
# Call the task execution API. For example, the asynchronous model inference job is delivered to stream2.
ret = acl.mdl.execute_async(model_id_2, dataset_in_2, dataset_out_2, stream2)

# Synchronize streams.
ret = acl.rt.synchronize_stream(stream1)
ret = acl.rt.synchronize_stream(stream2)

# Destroy allocations.
ret = acl.rt.destroy_stream(stream2)
ret = acl.rt.destroy_stream(stream1)

# ....
```
