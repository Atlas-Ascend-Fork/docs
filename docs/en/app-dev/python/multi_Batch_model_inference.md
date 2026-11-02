# Multi-batch Model Inference

A similar workflow, as described in [Model Management](model_management.md), can be followed for inference with larger batch sizes.

However, there are some slight differences worth mentioning in batched inference:

- If the batch size is greater than 1, when building a model, you need to set the batch size by using the `input_shape` parameter of the ATC tool. For details, see [Ascend Tensor Compiler (ATC)](https://hiascend.com/en/document/redirect/cannCommunityATC)..
- Before inference, you need to write a piece of code logic. If the input data meets the requirements of multiple batches (for example, 8 batches), allocate memory on the device to store the data of multiple batches as the input of model inference. The remainder data that is less than the batch size will be directly fed to the model for inference.

Following the API calls, add exception handling branches and specify log printing of error and information levels. In the following example, the batch size is set to `8`. The following is a code snippet of key steps only, which is not ready to use.

```python
batch_size = 8
device_num = 1
device_id = 0

# Obtain the size of the first input of the model.
model_input_size = acl.mdl.get_input_size_by_index(model_desc, 0)
# Obtain the input buffer size per batch.
single_buff_size = model_input_size / batch_size

# Define this variable to check whether the number of the accumulated inputs is greater than 8.
cnt = 0
# Define this variable to describe the offset when each file is loaded to the memory.
pos = 0
infer_file_vec = []

for i in range(len(files_list)):
    # Allocate device memory once for every eight input files (batch size = 8).
    if cnt % batch_size == 0:
        pos = 0
        infer_file_vec.clear()
        # Allocates device memory.
        p_batch_dst, ret = acl.rt.malloc(model_input_size, ACL_MEM_MALLOC_NORMAL_ONLY)

    # TODO: Load a file from a directory and calculate the file size file_size.

    # Allocate memory on the host based on the file size to store file data.
    p_img_buf, ret = acl.rt.malloc_host(file_size)

    # Copy file data from the host to the device.
    ret = acl.rt.memcpy(p_batch_dst + pos, file_size, p_img_buf, file_size, ACL_MEMCPY_HOST_TO_DEVICE)
    pos += file_size
    # Frees host memory.
    acl.rt.free_host(p_img_buf)
    # Save the ith file to the vector and increase the value of cnt by 1.
    infer_file_vec.append(files_list[i])
    cnt += 1
    # Send the data per batch (batch size = 8) for model inference.
    if cnt % batch_size == 0:
        # TODO: Create data of type aclmdlDataset and aclDataBuffer to describe the input and output data of the model.
        # TODO: Call acl.mdl.execute to start model inference.
        # TODO: Call acl.rt.free to free memory on the device after the inference is complete.

# The remainder data that is less than the batch size will be directly fed to the model for inference.
if cnt % batch_size != 0:
    # TODO: Create data of type aclmdlDataset and aclDataBuffer to describe the input and output data of the model.
    # TODO: Call acl.mdl.execute to start model inference.
    # TODO: Call acl.rt.free to free memory on the device after the inference is complete.
# ......
```
