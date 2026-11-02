# Model Execution

## Basic Principles

If network-wide model inference is involved, ensure that your app contains the code logic for model execution. For details about the API call sequence, see [API Calling Process](interface_calling_process.md).

This section describes the API call sequence for **network-wide model execution**. For details about operator model loading and execution, see the description of [Single-Operator Calling](single_operator_invoke.md).

- **Before executing a model after it is loaded**, prepare the input and output data structures, and upload the input data to the memory corresponding to the model's input data structure.
- **After model execution is complete**, free up memory and destroy allocations (including the input data, `aclmdlDesc` type, `aclmdlDataset` type, and `aclDataBuffer` type) in a timely manner to avoid memory exceptions.

    Data of type `aclDataBuffer` is used to describe the buffer address and buffer size of an input or output. A model may have multiple inputs or outputs. Call `acl.rt.free` to free data in the memory and call `acl.destroy_data_buffer` to destroy the `aclDataBuffer` type.

## API Calling Process

**Figure 1** Typical model inference workflow
![](figures/typical-model-inference-workflow.png)

The key APIs are described as follows:

1. Call `acl.mdl.create_desc` to create data for **describing the model**.
2. Call `acl.mdl.get_desc` to obtain the **model information** based on the model ID returned in [Model Loading](model_load.md).
3. Prepare the input and output data structures for model execution. For details, see [Preparing Input/Output Data Structure for Model Execution](#preparing-inputoutput-data-structure-for-model-execution).

    To configure dynamic batch size, dynamic image size, dynamic AIPP, or dynamic dimensions (ND format only) for your model input, see [Model Inference with Dynamic-Shape Inputs](dynamic_shape_model_inference.md) and [Dynamic AIPP Model Inference](dynamic_AIPP_inference.md).

4. **Run model inference.**

    In static batch size (greater than 1) scenarios, the input data is fed to your model for inference only when the input data reaches the given batch size. If the batch size does not meet the requirement, perform operations as required.

    Currently, synchronous and asynchronous model inference is supported.

    - Call `acl.mdl.execute` for synchronous inference.
    - Call `acl.mdl.execute_async` for asynchronous inference.

        Also call `acl.rt.synchronize_stream` to wait for the stream tasks to complete.

        For details about asynchronous inference, see [Asynchronous Model Inference](model_asynchronous_inference.md).

5. Obtain the results of model inference for subsequent use.

    For synchronous inference, obtain the output data of model inference directly.

    For asynchronous inference, when the callback function is implemented, obtain the model inference result from the callback function for subsequent use.

6. **Free the buffer.**

    Call `acl.rt.free` to deallocate device memory.

7. **Destroy data of specific types.**

    After model inference is complete, call `acl.destroy_data_buffer` and `acl.mdl.destroy_dataset` in sequence to free the input data of the model. **If the model takes multiple inputs or outputs**, a separate `acl.destroy_data_buffer` call is needed for each input or output.

## Preparing Input/Output Data Structure for Model Execution

pyACL provides the following data types to describe a model, model inputs, model outputs, and data buffers, as the input parameters of the model execution call:

- Use data of the `aclmdlDesc` type to describe the basic information of your model (such as the input/output count, and the name, data type, format, and shape of each input/output).

    After a model is successfully loaded, call `acl.mdl.get_desc` to obtain the model description based on the model ID. Then, you can obtain the input/output count, and memory size, shape, format, and data type of each input/output from the model description by using the operation APIs under `aclmdlDesc`.

- Use data of the `aclmdlDataset` type to describe the input/output data of your model. Note that a model might have more than one input and more than one output.

    Call the operation APIs under `aclmdlDataset` to add data of type `aclDataBuffer` and obtain the number of `aclDataBuffer`s.

- Use data of the `aclDataBuffer` type to describe the buffer address and buffer size of each input/output.

    Call the operation APIs under `aclDataBuffer` to obtain the buffer address and buffer size of each input/output.

**Figure 2** Relationship between aclmdlDataset and aclDataBuffer
![](figures/relationship-between-aclmdldataset-and-acldatabuffer.png)

After learning related data types, you can use the operation APIs for these data types to prepare the input and output data structures of the model, as shown in the following figure.

**Figure 3** Input and output data structure preparation workflow
![](figures/input-and-output-data-structure-preparation-workflow.png)

The key points are described as follows:

- If a model has multiple inputs and outputs, you can call the `acl.mdl.get_num_inputs` and `acl.mdl.get_num_outputs` APIs to obtain the number of inputs and outputs.
- You can call the `acl.mdl.get_input_size_by_index` and `acl.mdl.get_output_size_by_index` APIs to obtain the memory size required by each input and output of the model.

    If the model allows dynamic batch size, dynamic image size, and dynamic dimensions (ND format only), the shape of the input tensor data supports multiple profiles and is not determined until the model is executed. Therefore, you are advised to call `acl.mdl.get_input_size_by_index` to obtain the memory size required by the maximum profile to ensure that the memory is sufficient.

- For a model with multiple inputs and outputs, you are advised to call `acl.mdl.get_input_name_by_index` and `acl.mdl.get_output_name_by_index` to obtain the names of the inputs and outputs, and then add `aclDataBuffer` to the `aclmdlDataset` in accordance with the corresponding index sequence.

## Sample Code (Preparing the Input and Output Data Structures of a Model)
<!-- npu="950,A3,910b,910,310p,310b" id1 -->
[Click here](https://gitee.com/ascend/samples/tree/master/python/level2_simple_inference/1_classification/resnet50_imagenet_classification) to view the complete code.
<!-- end id1 -->

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
# Initialize variables.
ACL_MEM_MALLOC_HUGE_FIRST = 0

# 1. Obtain the model description based on the model ID.
# self.model_desc is of type aclmdlDesc.
self.model_desc = acl.mdl.create_desc()
ret = acl.mdl.get_desc(self.model_desc, self.model_id)

# 2. Prepare the input dataset for model inference.
# Create data of the aclmdlDataset type to describe the input for model inference.
self.load_input_dataset = acl.mdl.create_dataset()
# Obtain the number of model inputs.
input_size = acl.mdl.get_num_inputs(self.model_desc)
self.input_data = []
# Allocate buffer for each input and add each input to the data of type aclmdlDataset with a for loop.
for i in range(input_size):
    buffer_size = acl.mdl.get_input_size_by_index(self.model_desc, i)
    # Allocate input buffer.
    buffer, ret = acl.rt.malloc(buffer_size, ACL_MEM_MALLOC_HUGE_FIRST)
    data = acl.create_data_buffer(buffer, buffer_size)
    _, ret = acl.mdl.add_dataset_buffer(self.load_input_dataset, data)
    self.input_data.append({"buffer": buffer, "size": buffer_size})

# 3. Prepare the output dataset for model inference.
# Create data of the aclmdlDataset type to describe the output for model inference.
self.load_output_dataset = acl.mdl.create_dataset()
# Obtain the number of model outputs.
output_size = acl.mdl.get_num_outputs(self.model_desc)
self.output_data = []
# Allocate buffer for each output and add each output to the data of type aclmdlDataset with a for loop.
for i in range(output_size):
    buffer_size = acl.mdl.get_output_size_by_index(self.model_desc, i)
    # Allocate output buffer.
    buffer, ret = acl.rt.malloc(buffer_size, ACL_MEM_MALLOC_HUGE_FIRST)
    data = acl.create_data_buffer(buffer, buffer_size)
    _, ret = acl.mdl.add_dataset_buffer(self.load_output_dataset, data)
    self.output_data.append({"buffer": buffer, "size": buffer_size})

# ......
```

## Sample Code (Executing a Model)
<!-- npu="950,A3,910b,910,310p,310b" id2 -->
[Click here](https://gitee.com/ascend/samples/tree/master/python/level2_simple_inference/1_classification/resnet50_imagenet_classification) to view the complete code.
<!-- end id2 -->
Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
ACL_MEMCPY_HOST_TO_DEVICE = 1
ACL_MEMCPY_DEVICE_TO_HOST = 2
NPY_BYTE = 1
images_list = ["./data/dog1_1024_683.jpg", "./data/dog2_1024_683.jpg"]

for image in images_list:
    # 1. Use the custom function transfer_pic to read the image file using the Python library and perform operations such as resizing and cropping on the image.
    # For details about the implementation of the transfer_pic function, see source code in the sample.
    img = transfer_pic(image)

    # 2. Prepare input data for model inference. The default run mode is ACL_HOST. The model in the current instance code has only one input.
    if "bytes_to_ptr" in dir(acl.util):
        bytes_data = img.tobytes()
        ptr = acl.util.bytes_to_ptr(bytes_data)
    else:
        ptr = acl.util.numpy_to_ptr(img)
    # Transfer image data from the host to the device.
    ret = acl.rt.memcpy(self.input_data[0]["buffer"], self.input_data[0]["size"], ptr,
                         self.input_data[0]["size"], ACL_MEMCPY_HOST_TO_DEVICE)

    # 3. Run model inference.
    # self.model_id indicates the model ID. After a model is successfully loaded, its model ID is returned.
    ret = acl.mdl.execute(self.model_id, self.load_input_dataset, self.load_output_dataset)

# ......
```

## Sample Code (Processing the Inference Result: Directly Processing Data in the Memory)
<!-- npu="950,A3,910b,910,310p,310b" id3 -->
[Click here](https://gitee.com/ascend/samples/tree/master/python/level2_simple_inference/1_classification/resnet50_imagenet_classification) to view the complete code.
<!-- end id3 -->

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

Take the image classification network as an example. After the model execution is complete, you might need to process the inference output of each image to present the class indexes corresponding to the top 5 confidence values.

```python
# Process the model inference output and print the class indexes corresponding to the top 5 confidence values.
inference_result = []
for i, item in enumerate(self.output_data):
    buffer_host, ret = acl.rt.malloc_host(self.output_data[i]["size"])
    # Transfer the inference output data from the device to the host.
    ret = acl.rt.memcpy(buffer_host, self.output_data[i]["size"], self.output_data[i]["buffer"],
                         self.output_data[i]["size"], ACL_MEMCPY_DEVICE_TO_HOST)

    bytes_out = acl.util.ptr_to_bytes(buffer_host, self.output_data[i]["size"])
    data = np.frombuffer(bytes_out, dtype=np.byte)

    inference_result.append(data)
    tuple_st = struct.unpack("1000f", bytearray(inference_result[0]))
    vals = np.array(tuple_st).flatten()
    top_k = vals.argsort()[-1:-6:-1]
    print("======== top5 inference results: =============")
    for j in top_k:
        print("[%d]: %f" % (j, vals[j]))

# ......
```

## Sample Code (Processing the Inference Result Using Single-Operators)
<!-- npu="950,A3,910b,910,310p,310b" id4 -->
[Click here](https://gitee.com/ascend/samples/tree/master/python/level2_simple_inference/1_classification/resnet50_imagenet_classification) to view the complete code for synchronous inference.
<!-- end id4 -->

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

Take the image classification network as an example. After the model execution is complete, you might need to process the inference output of each image to present the class index corresponding to the top confidence value.
<!-- npu="910b,910,310p,310b" id5 -->
[Click here](https://gitee.com/ascend/samples/tree/master/python/level2_simple_inference/1_classification/vpc_resnet50_imagenet_classification) to view the complete code for image decoding, resizing, and synchronous inference.
<!-- end id5 -->

In the current sample, the Cast operator is called to cast the data type of the inference result from float32 to float16, and the ArgMaxD operator is called to identify the class indexes with top confidence values of each image from the inference result. For the single-operator API call sequence, see [API Calling Process](single_operator_interface_calling_process.md).

- The Cast operator has been encapsulated into the pyACL API. You can directly pass the input and output tensor description and the memory of the input and output data of the operator to the `acl.op.cast` call to load and execute the operator.
- The ArgMaxD operator has not been encapsulated into a pyACL API. Therefore, you must construct the operator description information (including the input and output tensor descriptions and operator attributes), allocate the memory for storing the input and output data of the operator, specify the operator type, and call the `acl.op.execute_v2` API to load and execute the operator.

```python
ACL_MEMCPY_DEVICE_TO_HOST = 2

# Compile the .json definition files of the Cast and ArgMaxD operators into an offline model adapted to the Ascend AI Processor (.om file) to verify the operators.
# Set the directory of the single-operator model files and load the single-operator models.
ret = acl.op.set_model_dir("./op_models")
# ......

# Loop over the model inference output of each image:
# 1. Obtain the output of model inference: dataset_ptr.
self.input_buffer = acl.mdl.get_dataset_buffer(dataset_ptr, 0)

# 2. Define the _forward_op_cast function to construct the input and output tensor description of the Cast operator, allocate the buffer dev_buffer_cast for storing the operator output data, and call acl.op.cast to load and execute the operator.
self._forward_op_cast()

# 3. Define the _forward_op_arg_max_d function, construct the input and output tensors, input and output tensor descriptions, and operator attributes of the ArgMaxD operator, allocate the buffer dev_buffer_arg_max_d for storing the operator output data, and call acl.op.execute_v2 to load and execute the operator.
self._forward_op_arg_max_d()

# 4. Transfer the ArgMaxD output back to the host.
# 4.1 Allocate host memory based on the size of the ArgMaxD output.
host_buffer, ret = acl.rt.malloc_host(self.tensor_size_arg_max_d)

# 4.2 Copy the ArgMaxD output from the device to the host.
ret = acl.rt.memcpy(host_buffer,
                     self.tensor_size_arg_max_d,
                     self.dev_buffer_arg_max_d,
                     self.tensor_size_arg_max_d,
                     ACL_MEMCPY_DEVICE_TO_HOST)

# 4.3 Print the class index of the top confidence value.
bytes_out = acl.util.ptr_to_bytes(buffer_host, self.output_shape)
data = np.frombuffer(bytes_out, dtype=np.int32).reshape((self.output_shape,))
print("[SingleOP][ArgMaxOp] label of classification result is:{}"
      .format(data[0]))

# 5 Destroy allocations.
# 5.1 Free host memory.
ret = acl.rt.free_host(host_buffer)

# 5.2 Free device memory that stores the operator outputs.
ret = acl.rt.free(self.dev_buffer_cast)
ret = acl.rt.free(self.dev_buffer_arg_max_d)

# 5.3 Destroy data of type aclDataBuffer (used to describe the operator outputs).
ret = acl.destroy_data_buffer(self.output_buffer_cast)
ret = acl.destroy_data_buffer(self.output_buffer_arg_max_d)

# ......
```

## Sample Code (Destroying the Input and Output Resources of a Model)
<!-- npu="950,A3,910b,910,310p,310b" id6 -->
[Click here](https://gitee.com/ascend/samples/tree/master/python/level2_simple_inference/1_classification/resnet50_imagenet_classification) to view the complete code.
<!-- end id6 -->

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
# Destroy input and output resources for model inference.
# Destroy the input data structure and free input buffer.
while self.input_data:
    item = self.input_data.pop()
    ret = acl.rt.free(item["buffer"])
input_number = acl.mdl.get_dataset_num_buffers(self.load_input_dataset)
for i in range(input_number):
    data_buf = acl.mdl.get_dataset_buffer(self.load_input_dataset, i)
    if data_buf:
        ret = acl.destroy_data_buffer(data_buf)
ret = acl.mdl.destroy_dataset(self.load_input_dataset)

# Destroy the output data structure and free output buffer.
while self.output_data:
    item = self.output_data.pop()
    ret = acl.rt.free(item["buffer"])
output_number = acl.mdl.get_dataset_num_buffers(self.load_output_dataset)
for i in range(output_number):
    data_buf = acl.mdl.get_dataset_buffer(self.load_output_dataset, i)
    if data_buf:
        ret = acl.destroy_data_buffer(data_buf)
ret = acl.mdl.destroy_dataset(self.load_output_dataset)
```
