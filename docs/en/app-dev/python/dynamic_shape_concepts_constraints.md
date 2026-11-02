<!-- npu="950,A3,910b,910,310p,310b" id1 -->
# Concepts and Restrictions
<!-- end id1 -->
## Concepts

**Table 1** Concepts

| Concept| Description|
| --- | --- |
| Dynamic batch/image size| The batch size or image size is not fixed in certain scenarios. For example, if you execute a target recognition network after detecting the targets, the input batch size for object recognition is dynamic because the number of targets detected can vary.<br>Dynamic batch: The batch size is not determinable until inference time.<br>Dynamic image size: The image size (H x W) of each image is dynamically variable during inference.|
| Dynamic dimensions (ND format only)| To support the scenarios where the input dimension sizes are uncertain, such as the Transformer network, the dynamic dimensions feature for the ND format is supported.<br>ND indicates any format with up to four dimensions.|

## Usage Restrictions

- For a single model, AIPP (static or dynamic) and dynamic dimensions (ND format) are mutually exclusive.
- For the same model, you can select **only one of the following methods**:
  - Call `acl.mdl.set_dataset_tensor_desc` to set the shape.
  - Call `acl.mdl.set_dynamic_batch_size` to set the dynamic batch size.
  - Call `acl.mdl.set_dynamic_hw_size` to set the dynamic image size.
  - Call `acl.mdl.set_input_dynamic_dims` to set the dynamic dimensions.

- When allocating output buffers for model inference, you can allocate memory based on the actual size for each profile. Alternatively, call `acl.mdl.get_output_size_by_index` to query the exact required size prior to allocation (recommended to ensure sufficient memory).

- If dynamic AIPP and dynamic batch size are both enabled:
  - The `batchSize` parameter passed to the `acl.mdl.create_aipp` call must be set to the allowed maximum value.
  - For data nodes that require dynamic AIPP, the corresponding input buffer must be allocated based on the allowed maximum batch size.

- If the dynamic AIPP and dynamic image size are both enabled:
  - If the image cropping, resizing, or padding function is **enabled** in setting the dynamic AIPP parameters, the dynamic image size becomes unavailable.
  - If the image cropping, resizing, or padding function is **not enabled** in setting the dynamic AIPP parameters, the dynamic AIPP and dynamic image size are both available. However, ensure that the width and height configured by calling `acl.mdl.set_aipp_src_image_size` are consistent with those configured by calling `acl.mdl.set_dynamic_hw_size`.
  - For data nodes that require dynamic AIPP processing, allocating the input buffer must be based on the maximum allowed image size.

- When dynamic AIPP and dynamic shape input (setting the shape range) are used at the same time, the width and height of the output image of dynamic AIPP must be within the configured shape range.

- **If static AIPP and dynamic image size are both enabled**, because the width and height of the input image are uncertain in the dynamic image size scenario, when the `insert_op_conf` parameter of the ATC tool is used to transfer the AIPP configuration file, the crop, resize, and padding functions cannot be enabled in the AIPP configuration file. Additionally, the `src_image_size_w` and `src_image_size_h` values in the configuration file need to be set to `0`.
