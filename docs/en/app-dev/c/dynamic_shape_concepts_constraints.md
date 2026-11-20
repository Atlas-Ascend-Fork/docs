# Concepts and Constraints

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:05:29.867Z pushedAt=2026-10-22T01:20:50.959Z nl=2 -->

## Related Concepts

**Table 1** Concept introduction

| Concept | Description |
| --- | --- |
| Dynamic batch/dynamic resolution | In some scenarios, the batch size or resolution of each model input is not fixed. For example, after a target is detected, a target recognition network is executed. Because the number of targets is not fixed, the batch size of the target recognition network input is not fixed.<br><br>  - Dynamic batch: When a user performs inference, the batch size is dynamically variable.<br>  - Dynamic resolution: When a user performs inference, the resolution H*W of each image is dynamically variable. |
| Dynamic dimension (ND format) | To support scenarios where the input format dimensions of networks such as Transformer are uncertain, dynamic setting of any dimension in ND format must be supported. |

## Constraints

| Usage Scenario | Constraint |
| --- | --- |
| When performing inference on the same model | AIPP (including static AIPP and dynamic AIPP) cannot be used together with dynamic dimension (ND format). |
| When performing inference on the same model | Only one of the following methods can be selected:<br>  - Call the **aclmdlSetDatasetTensorDesc** API to set the shape range.<br>  - Call the **aclmdlSetDynamicBatchSize** API to set the dynamic batch.<br>  - Call the **aclmdlSetDynamicHWSize** API to set the dynamic resolution.<br>  - Call the **aclmdlSetInputDynamicDims** API to set the dimension values of the dynamic dimension. |
| When allocating output memory for model inference | You can allocate memory based on the actual size of each level, or call the **aclmdlGetOutputSizeByIndex** API to obtain the memory size and then allocate memory (this method is recommended to ensure sufficient memory). |
| When static AIPP and dynamic resolution are used together | Because the width and height of the input image are uncertain in the dynamic resolution scenario, when the **insert_op_conf** parameter of the ATC tool is used to pass in the AIPP configuration file, the cropping and padding functions cannot be enabled in the AIPP configuration file, and **src_image_size_w** and **src_image_size_h** in the configuration file must be set to **0**. |
| When dynamic AIPP and dynamic batch are used together | - When calling the **aclmdlCreateAIPP** API to set **batchSize**, **batchSize** must be set to the maximum batch size.<br>  - For the data node in the model that requires dynamic AIPP processing, the corresponding input memory size must be allocated based on the maximum batch. |
| When dynamic AIPP and dynamic resolution are used together | - If the cropping, resizing, or padding function is enabled when setting dynamic AIPP parameters, dynamic AIPP cannot be used together with dynamic resolution.<br>  - If the cropping, resizing, or padding function is not enabled when setting dynamic AIPP parameters, when dynamic AIPP is used together with dynamic resolution, ensure that the width and height set through the **aclmdlSetAIPPSrcImageSize** API are equal to the width and height set through the **aclmdlSetDynamicHWSize** API, and both must be set to the width and height of the maximum dynamic resolution level during model conversion.<br>  - For the data node in the model that requires dynamic AIPP processing, the corresponding input memory size must be allocated based on the maximum resolution (width and height). |
| When dynamic AIPP and dynamic shape input (setting the shape range) are used together | The width and height of the dynamic AIPP output image must be within the set shape range. |
