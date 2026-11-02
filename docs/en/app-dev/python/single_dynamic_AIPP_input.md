<!-- npu="950,A3,910b,910,310p,310b" id1 -->
# Dynamic AIPP (Single Dynamic AIPP Input)
<!-- end id1 -->
## API Call Sequence

For dynamic AIPP, the model inference process is similar to [Model Management](model_management.md), including initialization and deinitialization, runtime resource allocation and release, model building, model loading, model execution, and model unloading.

This section focuses on the differences between the two scenarios.

- **During model building**: You need to set the parameters related to dynamic AIPP.

    When building a model, you need to call the API provided by pyACL to set the AIPP configuration required for model inference. The AIPP mode supported by the model has been configured during model building (using the `insert_op_conf` parameter of the ATC tool). For details about ATC parameters, see [Ascend Tensor Compiler (ATC)](https://hiascend.com/en/document/redirect/cannCommunityATC).

    **After model building**, the AIPP inputs are added to the generated OM model. During model inference, the AIPP input values are provided.

    Assume that the AIPP configuration of input `a` is dynamic. In the generated .om model, input `b` is added to describe the AIPP configuration of input `a`. For details about how to prepare the data structure of input `a` for model execution, see [Preparing Input/Output Data Structure for Model Execution](model_execute.md). For details about how to prepare the data structure of input `b` and set the data of input `b`, see the following description.

- **Before model inference**:
    - Prepare the data structure of the dynamic AIPP inputs.
        1. Before allocating memory for the dynamic AIPP input, call `acl.mdl.get_input_index_by_name` to obtain the index that identifies the input in the model based on the input name (fixed at `ascend_dynamic_aipp_data`).
        2. Call `acl.mdl.get_input_size_by_index` to obtain the input buffer size based on the index.
        3. Pass the size obtained in the previous step to the `acl.rt.malloc` call to allocate memory.

            Do not initialize the buffer manually; otherwise, the service will be unavailable. After the API calls described in the previous step, the system automatically initializes the buffer.

        4. Call `acl.create_data_buffer` to create data of type `aclDataBuffer` to describe the buffer address and buffer size of the dynamic AIPP input.
        5. Call `acl.mdl.create_dataset` to create data of type `aclmdlDataset`, and call acl.mdl.add_dataset_buffer to add data of type `aclDataBuffer` to data of type `aclmdlDataset`.

    - Set dynamic AIPP parameters.

        **Figure 1** API call sequence
        ![](figures/api-call-sequence-3.png)

        1. Call `acl.mdl.get_input_index_by_name` to obtain the index of an input using the input name (fixed to `ascend_dynamic_aipp_data`).
        2. Set dynamic AIPP parameters.
            1. Call `acl.mdl.create_aipp` to create data of the `aclmdlAIPP` type.
            2. Call the APIs of the `aclmdlAIPP` data type to set dynamic AIPP attributes as required.
            3. For dynamic AIPP, `acl.mdl.set_aipp_src_image_size` must be called to set the source image size.
            4. Call `acl.mdl.set_input_aipp` to set the dynamic AIPP data for model inference.
            5. Call `acl.mdl.destroy_aipp` to destroy data of type `aclmdlAIPP` in a timely manner.

## Sample Code

After APIs are called, add an exception handling branch, and record error logs and warning logs. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......

ACL_YUV420SP_U8 = 1

# 1. Load the model and set dynamic AIPP parameters.
# ......

# 2. Create data of type aclmdlDataset to describe the input data input_dataset and output data output_dataset of the model.
# ......

# 3. Customize a function for setting dynamic AIPP parameters.
def model_set_dynamic_aipp():
    # 3.1 Obtain the index of the dynamic AIPP input.
    index, ret = acl.mdl.get_input_index_by_name(model_desc, "ascend_dynamic_aipp_data")

    # 3.2 Set dynamic AIPP parameters.
    batch_number = 1
    aipp_dynamic_set = acl.mdl.create_aipp(batch_number)
    ret = acl.mdl.set_aipp_src_image_size(aipp_dynamic_set, 256, 224)
    ret = acl.mdl.set_aipp_input_format(aipp_dynamic_set, ACL_YUV420SP_U8)
    ret = acl.mdl.set_aipp_csc_params(aipp_dynamic_set, 1, 256, 443, 0, 256, -86, -178, 256, 0, 350, 0, 0, 0, 0, 128, 128)
    ret = acl.mdl.set_aipp_rbuv_swap_switch(aipp_dynamic_set, 0)
    ret = acl.mdl.set_aipp_dtc_pixel_mean(aipp_dynamic_set, 0, 0, 0, 0, 0)
    ret = acl.mdl.set_aipp_dtc_pixel_min(aipp_dynamic_set, 0, 0, 0, 0, 0)
    ret = acl.mdl.set_aipp_pixel_var_reci(aipp_dynamic_set, 1, 1, 1, 1, 0)
    ret = acl.mdl.set_aipp_crop_params(aipp_dynamic_set, 1, 0, 0, 224, 224, 0)
    ret = acl.mdl.set_input_aipp(model_id, input_dataset, index, aipp_dynamic_set)
    ret = acl.mdl.destroy_aipp(aipp_dynamic_set)
    # ......

# 4. Customize a function and execute the model.
def model_execute(index):
    # 4.1 Call the custom function to set dynamic AIPP parameters.
    ret = model_set_dynamic_aipp()
    # 4.2 Execute the model. model_id indicates the ID of a successfully loaded model. input_ and output_ indicate the input and output of the model.
    ret = acl.mdl.execute(model_id, input_dataset, output_dataset)
    # ......

# 5. Process the model inference result.
# ......
```
