# CBLAS API Calling

## Basic Principles

The GEMM operator (used for matrix-vector multiplication and matrix-matrix multiplication) and the Cast operator (used for data type conversion) have been encapsulated into pyACL APIs. For details, see CBLAS APIs in the *Runtime APIs*. pyACL supports the following execution modes:

- Non-handle mode: Call APIs whose names do not contain keyword "handle", for example, `acl.blas.gemm_ex` (with the GEMM operator encapsulated) and `acl.op.cast` (with the Cast operator encapsulated).
- Handle mode: Call APIs whose names contain keyword "handle", for example, `acl.blas.create_handle_for_gemm_ex` and `acl.op.create_handle_for_cast`, to create a handle, and then call `acl.op.execute_with_handle`.

>[!NOTE]
>
>- If an operator is executed in non-handle mode, the system matches the model in the memory based on the operator description in every execution.
>- If an operator is executed in handle mode, the system matches the model in the memory based on the operator description, and caches it in the handle. The handle mode boosts the efficiency in scenarios where the same operator is executed for multiples times. Call `acl.op.destroy_handle` to destroy the handle when it is no longer needed.

## Sample code

This section uses the `acl.blas.gemm_ex` API as an example. In this example, the matrix multiplication calculation formula is C = αAB + βC, indicating that matrix C is obtained after matrix A and matrix B are multiplied. α and β indicate the coefficient of the product.

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......

ACL_MEM_MALLOC_HUGE_FIRST = 2
ACL_TRANS_N = 0
ACL_COMPUTE_HIGH_PRECISION = 0
ACL_MEMCPY_HOST_TO_DEVICE = 1
ACL_MEMCPY_DEVICE_TO_HOST = 2

# 1. Perform initialization.
ret = acl.init("test_data/config/acl.json")

# 2. Set the directory of the single-operator model file.
ret = acl.op.set_model_dir("op_models")

# 3. Specify a compute device.
device_id = 0
ret = acl.rt.set_device(device_id)

# 4. Allocate memory.
# 4.1 Allocate device memory to store the operator inputs.
# In this matrix-matrix multiplication sample, size_a indicates the size of matrix A, size_b the size of matrix B, and size_c the size of matrix C.
in_dtype, out_dtype = 1, 1
size_a = m * k * acl.data_type_size(acl_dtype)
size_b = k * n * acl.data_type_size(acl_dtype)
size_c = m * n * acl.data_type_size(acl_dtype)
dev_matrix_a, ret = acl.rt.malloc(size_a, ACL_MEM_MALLOC_HUGE_FIRST)
dev_matrix_b, ret = acl.rt.malloc(size_b, ACL_MEM_MALLOC_HUGE_FIRST)
dev_matrix_c, ret = acl.rt.malloc(size_c, ACL_MEM_MALLOC_HUGE_FIRST)
# 4.2 Allocate host memory.
# In this matrix-matrix multiplication sample, m indicates the number of rows of matrix A and matrix C and n indicates the number of columns of matrix B and matrix C.
# k indicates the number of columns of matrix A and the number of rows of matrix B.
host_matrix_a, ret = acl.rt.malloc_host(size_a)
host_matrix_b, ret = acl.rt.malloc_host(size_b)
host_matrix_c, ret = acl.rt.malloc_host(size_c)

# 5. Prepare input data.
# Read data from the file to host_matrix_a and host_matrix_b.
# For this matrix-matrix multiplication sample, copy the data of matrix A and matrix B from the host to the device.
ret = acl.rt.memcpy(dev_matrix_a, size_a, host_matrix_a, size_a, ACL_MEMCPY_HOST_TO_DEVICE)
ret = acl.rt.memcpy(dev_matrix_b, size_b, host_matrix_b, size_b, ACL_MEMCPY_HOST_TO_DEVICE)

# 6. Execute the single-operator.
stream, ret = acl.rt.create_stream()
# In this example, acl.blas.gemm_ex (asynchronous mode) is called to implement matrix-matrix multiplication.
ret = acl.blas.gemm_ex(ACL_TRANS_N, ACL_TRANS_N, ACL_TRANS_N, m, n, k, dev_alpha, dev_matrix_a, k, input_type, dev_matrix_b, n, input_type, dev_beta, dev_matrix_c, n, output_type, ACL_COMPUTE_HIGH_PRECISION, stream)
# Call acl.rt.synchronize_stream to block the host until all tasks in the specified stream are complete.
ret = acl.rt.synchronize_stream(stream)

# 7. Copy the output data of the operator from the device to the host.
ret = acl.rt.memcpy(host_matrix_c, size_c, dev_matrix_c, size_c, ACL_MEMCPY_DEVICE_TO_HOST)

# 8. Deallocate runtime resources.
ret = acl.rt.destroy_stream(stream)
ret = acl.rt.reset_device(device_id)
ret = acl.finalize()
# ......
```
