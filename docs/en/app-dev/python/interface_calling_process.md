# API Calling Process

By calling pyacl APIs, you can develop apps that provide functions such as model inference, media data processing, and single-operator execution. These functions can exist independently or in combinations. The following figure shows the overall sequence of calling pyacl APIs to develop AI apps.

<!-- npu="910b,910,310p,310b" id1 -->
**Figure 1** API call sequence
![](figures/api-call-sequence.png)
<!-- end id1 -->

In the preceding figure, the main API call sequence is abstracted based on the typical functions involved in app development. The specific scenarios are as follows:

- If the size of the input image does not meet the model requirements, media data processing is required.
- To implement model inference, the model needs to be loaded first. On the completion of model inference, the model needs to be unloaded.
- After model inference, the inference result needs to be postprocessed for looking up the class indexes with the top confidence values.

The API calling process is as follows:

1. Performs initialization.

    Call `acl.init`.

2. Allocate runtime resources.

    For details, see [Runtime Resource Allocation](runtime_resource_allocation_and_release.md#runtime-resource-allocation).

3. Model inference, media data processing, and single-operator execution
    - **Model inference**
        1. Load a model. Before inference, load the model to the system. Use an offline model adapted to Ascend AI Processor. If you need to build a model, see [Model Building](model_construction.md).

            For the interface calling process and examples, see [Migration Loading](model_load.md).

        2. (Optional) **Process media data**, including JPEG image and video decoding, image cropping, resizing, format conversion, and JPEG image encoding.

            For the interface calling process and examples, see [Media Data Processing (DVPP)](DVPP.md).

        3. Run model inference to implement functions such as image classification and target recognition.

            For the API call sequence, see [Model Execution](model_execute.md).

        4. (Optional) Data postprocessing: Postprocess the model inference result as required. For example, you can export the inference result to a file, and look up in the inference result for the class with the highest confidence score using single-operators.
        5. Call `acl.mdl.unload` to unload the model.

    - **Operator execution**

        If your AI app involves not only model inference but also mathematical operations such as Basic Linear Algebra Subprogram (BLAS) and data type conversion, use single-operator calling when using pyACL APIs. In this way, you can avoid additional model building and training. In addition, you can verify the functions of a custom operator via single-operator calling. For the API call sequence, see [API Calling Process](single_operator_interface_calling_process.md).

4. Deallocate runtime resources.

    For details, see [Runtime Resource Deallocation](runtime_resource_allocation_and_release.md#runtime-resource-deallocation).

5. Perform deinitialization.

    Call `acl.finalize` to deinitialize the configuration.

>[!NOTE]NOTE
>Memory allocation and deallocation, data transfer (by memory copy), and data type creation and destruction are the most frequently-used calls in each phase of the app development, and therefore are not thoroughly illustrated in the flowchart. For details, see *Runtime APIs*.
