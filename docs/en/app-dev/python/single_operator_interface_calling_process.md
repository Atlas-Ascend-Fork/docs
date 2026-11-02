# API Calling Process

If single-operator execution is involved during app development, ensure that your app contains the code logic for executing the single-operator. For details about the API call sequence, see [API Calling Process](interface_calling_process.md).

For details about the operators supported by the system, see *Operator Library*.

For operators that are not supported by the system, you need to develop custom operators by referring to [Ascend C Operator Development Guide](https://hiascend.com/en/document/redirect/CannCommunityOpdevAscendC).

**Figure 1** Operator calling workflow
![](figures/operator-calling-workflow.png)

The key APIs are described as follows:

1. Load the operator model file.

    You can use either of the following methods:

    - Call `acl.op.set_model_dir` to set the directory for loading the model file. The single-operator model file (\*.om file) is stored in the directory.
    - Call `acl.op.load` to load the single-operator model data from the memory. The memory is managed by the user. Single-operator model data refers to the data that is loaded to the memory from the \*.om file. The .om file is compiled from a single-operator.

2. Call the `acl.rt.malloc` API to allocate device memory to store the input and output data of the operator.

    To transfer data from the host to the device, call the `acl.rt.memcpy` (synchronous) or `acl.rt.memcpy_async` (asynchronous) API to implement data transfer in memory copy mode.

3. In the dynamic-shape scenario, if the output shape of an operator cannot be determined, you need to infer or estimate the output shape of the operator before executing the operator.

    You need to call the `acl.op.infer_shape`, `acl.get_tensor_desc_num_dims`, `acl.get_tensor_desc_dim_v2`, and `acl.get_tensor_desc_dim_range` APIs to deduce or estimate the output shape of the operator as the input of the operator execution API `acl.op.execute_v2`.

4. Execute the operator.

    - Operators encapsulated as acl APIs (for details, see [CBLAS API Calling](calling_cblas_interface.md)), including the GEMM operator and Cast operator, can be executed in either of the following ways:
        - Non-handle mode: Call APIs whose names do not contain keyword "Handle", for example, `acl.blas.gemm_ex` (with the GEMM operator encapsulated) and `acl.op.cast` (with the Cast operator encapsulated).
        - Handle mode: Call APIs whose names contain keyword "Handle", for example, `acl.blas.create_handle_for_gemm_ex` and `acl.op.create_handle_for_cast`, to create a handle, and then call `acl.op.execute_with_handle`.

    - Operators that are not encapsulated as pyACL APIs can be executed in either of the following ways:
        - Non-handle mode: Call `acl.op.execute_v2`.
        - Handle mode: Call `acl.op.create_handle` to create a handle, and then call `acl.op.execute_with_handle`.

    >[!NOTE]
    >- If an operator is executed in non-handle mode, the system matches the model in the memory based on the operator description in every execution.
    >- If an operator is executed in handle mode, the system matches the model in the memory based on the operator description, and caches it in the handle. The handle mode boosts the efficiency in scenarios where the same operator is executed for multiples times. Call `acl.op.destroy_handle` to destroy the handle when it is no longer needed.

5. Call `acl.rt.synchronize_stream` to block the app until all tasks in the specified stream are complete.
6. Call `acl.rt.free` to free the memory.

    To transfer the operator execution result from the device to the host, call `acl.rt.memcpy` (synchronous) or `acl.rt.memcpy_async` (asynchronous) to implement data transfer through memory copy, and then free the memory.
