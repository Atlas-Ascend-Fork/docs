<!-- npu="910b,910,310p,310b" id1 -->
# Dynamic AIPP (Multiple Dynamic AIPP Inputs)
<!-- end id1 -->
## API Call Sequence

The inference workflow with multiple dynamic AIPP inputs is similar to that with a single dynamic AIPP input. [Dynamic AIPP (Single Dynamic AIPP Input](single_dynamic_AIPP_input.md) describes the workflow of model inference with a single dynamic AIPP input.

When your model has more than one dynamic AIPP input, the inference workflow shows some slight changes:

- Call `acl.mdl.get_aipp_type` to check whether the specified model input is associated with a dynamic AIPP input. If yes, the call returns the index of the dynamic AIPP input, which can be passed to the `acl.mdl.get_input_name_by_index` call to set the dynamic AIPP attributes.
- To avoid setting dynamic AIPP parameters on a wrong input, you can call `acl.mdl.get_input_name_by_index` to obtain the input name of the specified index and then set dynamic AIPP parameters by input index.

## Sample Code

Add exception handling branches following the API calls. The sample code of key steps is as follows, which is for reference only. Do not directly copy and run the code.

```python
import acl
# ......

ACL_DATA_WITH_DYNAMIC_AIPP = 2
ACL_YUV420SP_U8 = 1

# 1. Load the model and set dynamic AIPP parameters.
# ......

# 2. Prepare the model description model_desc, model inputs input_dataset, and model outputs output_dataset.
# ......

# 3. Customize a function for setting dynamic AIPP parameters.
def model_set_dynamic_aipp():
    # 3.1 Obtain the index of the dynamic AIPP input.
    need_dynamic_aipp = []
    input_num = acl.mdl.get_num_inputs(model_desc)
    for index in range(input_num):
        aipp_type, dynamic_attached_index, ret = acl.mdl.get_aipp_type(model_id, index)
        if aipp_type == ACL_DATA_WITH_DYNAMIC_AIPP:
            need_dynamic_aipp.append(index)

    # 3.2 In this example, two dynamic AIPP inputs are used.
    if len(need_dynamic_aipp) != 2:
        return 1
    # Create the first dynamic AIPP configuration.
    batch_number_first = 1
    aipp_dynamic_set_first = acl.mdl.create_aipp(batch_number_first)
    ret = acl.mdl.set_aipp_src_image_size(aipp_dynamic_set_first, 256, 224)
    ret = acl.mdl.set_aipp_input_format(aipp_dynamic_set_first, ACL_YUV420SP_U8)
    ret = acl.mdl.set_aipp_csc_params(aipp_dynamic_set_first, 1, 256, 443, 0, 256, -86,
                                         -178, 256, 0, 350, 0, 0, 0, 0, 128, 128)
    ret = acl.mdl.set_aipp_rbuv_swap_switch(aipp_dynamic_set_first, 0)
    ret = acl.mdl.set_aipp_dtc_pixel_mean(aipp_dynamic_set_first, 0, 0, 0, 0, 0)
    ret = acl.mdl.set_aipp_dtc_pixel_min(aipp_dynamic_set_first, 0, 0, 0, 0, 0)
    ret = acl.mdl.set_aipp_pixel_var_reci(aipp_dynamic_set_first, 1.0, 1.0, 1.0, 1.0, 0)
    ret = acl.mdl.set_aipp_crop_params(aipp_dynamic_set_first, 1, 2, 2, 224, 224, 0)
    # Set dynamic AIPP parameters.
    ret = acl.mdl.set_aipp_by_input_index(model_id, input_dataset, need_dynamic_aipp[0],
                                              aipp_dynamic_set_first)
    ret = acl.mdl.destroy_aipp(aipp_dynamic_set_first)
    # Create the second dynamic AIPP configuration.
    batch_number_second = 2
    aipp_dynamic_set_second = acl.mdl.create_aipp(batch_number_second)
    ret = acl.mdl.set_aipp_src_image_size(aipp_dynamic_set_second, 224, 224)
    # Call more AIPP configuration setting APIs as needed.
    # Set dynamic AIPP parameters.
    ret = acl.mdl.set_aipp_by_input_index(model_id, input_dataset, need_dynamic_aipp[1],
                                              aipp_dynamic_set_second)
    ret = acl.mdl.destroy_aipp(aipp_dynamic_set_second)
    return ret

# 4. Customize a function and execute the model.
def model_execute(index):
    # 4.1 Call the custom function to set dynamic AIPP parameters.
    ret = model_set_dynamic_aipp()
    # 4.2 Execute the model. modelId_ indicates the ID of a successfully loaded model. input_dataset and output_dataset indicates the inputs and outputs of the model.
    ret = acl.mdl.execute(model_id, input_dataset, output_dataset)
    # ......

# 5. Process the model inference result.
# ......
```
