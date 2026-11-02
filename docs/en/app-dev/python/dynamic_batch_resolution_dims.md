<!-- npu="950,A3,910b,910,310p,310b" id1 -->
# Dynamic Batch/Dynamic Image Size/Dynamic Dimension (Setting Multi-Dimension Profiles)
<!-- end id1 -->
## API Call Sequence

The model inference process with dynamic-shape inputs is similar to that in [Model Management](model_management.md). Both of them involve initialization and deinitialization, runtime resource allocation and release, model building, model loading, model execution, and model unloading.

This section focuses on the differences between the two scenarios.

1. **During model building**: You need to set the dynamic batch size, dynamic image size, and dynamic dimensions (ND format).

    **If the dynamic batch size feature is involved during model inference**, call the pyACL API to set the batch size. The batch size supported by the model has been configured during model building (by using the `dynamic_batch_size` parameter of ATC).

    **If the dynamic image size feature is involved during model inference**, call the pyACL API to set the image size. The image size supported by the model has been configured during model building (by using the `dynamic_image_size` parameter of ATC).

    **If the ****dynamic dimensions (ND format)**** feature is involved during model inference**, call the pyACL API to set the dimensions. The dimensions supported by the model have been configured during model building (by using the `dynamic_dims` parameter of ATC).

    After model building, the inputs of dynamic batch size, dynamic image size, and dynamic dimensions are added to the generated OM model. During model inference, the input values are provided.

    Assume that the batch size of input `a` is dynamic. In the generated OM model, input `b` is added to describe the batch size of input `a`.

    - For details about how to prepare the data structure of input `a` for model execution, see [Preparing Input/Output Data Structure for Model Execution](model_execute.md).

        The shape of the input tensor supports multiple profiles and can be determined only before model execution. Therefore, you are advised to call `acl.mdl.get_input_size_by_index` and `acl.mdl.get_output_size_by_index` to obtain the memory size required by the inputs and outputs. The APIs obtain the memory of the maximum profile to ensure sufficient memory. After the model is executed, you can call `acl.mdl.get_output_dims` to obtain the actual dimensions of the output tensor.

    - For details about how to prepare the data structure and set the data of input `b`, see step 2.

    For details about ATC parameters, see [Ascend Tensor Compiler (ATC)](https://hiascend.com/en/document/redirect/cannCommunityATC).

2. **Before model inference**:
    - Prepare the data structures of the inputs of dynamic batch size, dynamic image size, and dynamic dimensions.
        1. Before allocating memory for the inputs of dynamic batch size, dynamic image size, and dynamic dimensions, call `acl.mdl.get_input_index_by_name` to obtain the indexes of the inputs in the model based on the input name (the input name is fixed to `ascend_mbatch_shape_data`).
        2. Call `acl.mdl.get_input_size_by_index` to obtain the input buffer size based on the index.
        3. Pass the size obtained in the previous step to the `acl.rt.malloc` call to allocate memory.

            Do not initialize the buffer manually; otherwise, the service will be unavailable. After the API calls described in the previous step, the system automatically initializes the buffer.

        4. Call `acl.create_data_buffer` to create data of the `aclDataBuffer` type to store the memory address and memory size of the inputs of dynamic batch size, image size, and dimensions.
        5. Call `acl.mdl.create_dataset` to create data of type `aclmdlDataset`, and call `acl.mdl.add_dataset_buffer` to add data of type `aclDataBuffer` to data of type `aclmdlDataset`.

    - Set the dynamic batch size, dynamic image size, and dynamic dimensions.

        **Figure 1** API call sequence
        ![](figures/api-call-sequence-4.png)

        1. Call `acl.mdl.get_input_index_by_name` to obtain the index of an input using the input name (fixed to `ascend_mbatch_shape_data`).
        2. Set the dynamic batch size, dynamic image size, and dynamic dimensions.
            - Call `acl.mdl.set_dynamic_batch_size` to set the dynamic batch size.

                The configured `batch size` must be among the batch size profiles set during model building.

                You can call `acl.mdl.get_dynamic_batch` to obtain the batch size profiles supported by the model.

            - Call `acl.mdl.set_dynamic_hw_size` to set the dynamic image size.

                The configured image size must be among the image size profiles set during model building.

                You can also call `acl.mdl.get_dynamic_hw` to obtain the number of image size choices as well as the image size of each choice supported by the model.

            - Call `acl.mdl.set_input_dynamic_dims` to set the dynamic dimensions.

                The configured dimensions must be among the dimension profiles set during model building.

                You can also call `acl.mdl.get_input_dynamic_dims` to obtain the dimension profiles supported by the model.

## Sample Code for Dynamic Batch

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
# 1. Load the model and set dynamic batch size profiles.
# ......

# 2. Create data of type aclmdlDataset to describe the inputs and outputs of the model.
# ......

# 3. Customize a function for setting dynamic batch size profiles.
def model_set_dynamic_info():
    # 3.1 Obtain the indexes of the input with dynamic batch size. The input name is fixed to ascend_mbatch_shape_data.
    index, ret = acl.mdl.get_input_index_by_name(model_desc, "ascend_mbatch_shape_data")
    # 3.2 Set the batch size. model_id indicates the ID of a successfully loaded model, input indicates data of type aclmdlDataset, and index indicates the index of the input with dynamic batch size.
    batch_size = 8
    ret = acl.mdl.set_dynamic_batch_size(model_id, input, index, batch_size)
    # ......

# 4. Customize a function and execute the model.
def model_execute(index):
    # 4.1 Call the customized function to set dynamic batch size profiles.
    ret = model_set_dynamic_info()
    # 4.2 Execute the model. model_id indicates the ID of a successfully loaded model. input and output indicate the inputs and outputs of the model.
    ret = acl.mdl.execute(model_id, input, output)
    # ......

# 5. Process the model inference result.
# ......
```

## Sample Code for Dynamic Image Size

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
# 1. Load the model and set dynamic image size profiles.
# ......

# 2. Create data of type aclmdlDataset to describe the inputs and outputs of the model.
# ......

# 3. Customize a function for setting dynamic image size profiles.
def model_set_dynamic_info():
    # 3.1 Obtain the indexes of the inputs with dynamic image size. The input name is fixed to ascend_mbatch_shape_data.
    index, ret = acl.mdl.get_input_index_by_name(model_desc, "ascend_mbatch_shape_data")
    # 3.2 Set the image size. model_id indicates the ID of a successfully loaded model, input indicates data of type aclmdlDataset, and index indicates the index of the input with dynamic image size.
    height = 224
    width = 224
    ret = acl.mdl.set_dynamic_hw_size(model_id, input, index, height, width)
    # ......

# 4. Customize a function and execute the model.
def model_execute(index):
    # 4.1 Call the customized function to set dynamic image size profiles.
    ret = model_set_dynamic_info()
    # 4.2 Execute the model. model_id indicates the ID of a successfully loaded model. input and output indicate the inputs and outputs of the model.
    ret = acl.mdl.execute(model_id, input, output)
    # ......

# 5. Process the model inference result.
# ......
```

## Sample Code for Dynamic Dimensions (ND Format)

Add an exception handling branch following the API calls. The sample code of key steps is as follows, which is for reference only. Do not directly copy and run the code.

```python
import acl
# ......

# 1. Load the model and set dynamic dimension profiles.
# ......

# 2. Prepare the model description model_desc, model inputs, and model outputs.
# ......

# 3. Define a function for setting dynamic dimension profiles.
def model_set_dynamic_info():
    # 3.1 Obtain the indexes of the inputs with dynamic dimensions. The input name is fixed to ascend_mbatch_shape_data.
    index, ret = acl.mdl.get_input_index_by_name(model_desc, "ascend_mbatch_shape_data")
    # 3.2 Set the runtime dimensions, including the dimension count (dimCount) and the size of each dimension. model_id indicates the ID of a successfully loaded model, input indicates data of type aclmdlDataset, and index indicates the index of the dynamic dimension input.
    current_dims = {'name': '', 'dimCount': 4, 'dims': [8, 3, 224, 224]}
    ret = acl.mdl.set_input_dynamic_dims(model_id, input, index, current_dims)
    # ......

# 4. Customize a function and execute the model.
def model_execute(index):
    # 4.1 Call the customized function to set dynamic dimension profiles.
    ret = model_set_dynamic_info()
    # 4.2 Execute the model. model_id indicates the ID of a successfully loaded model. input and output indicate the inputs and outputs of the model.
    ret = acl.mdl.execute(model_id, input, output)
    # ......

# 5. Process the model inference result.
# ......
```
