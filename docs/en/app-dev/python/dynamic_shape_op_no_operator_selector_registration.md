# Single-Operator with Dynamic Shape (No Operator Selector Registered)

## Basic Principles

For operators that support dynamic shape:

- If the output shape of an operator is specified, the execution process of this operator is similar to that of the static-shape operator. For details about the API call sequence, see [API Calling Process](single_operator_interface_calling_process.md). For details about the sample code for executing the static-shape operator, see [Single-Operator with Static Shape](fixed_shape_op.md).
- If the output shape of an operator cannot be determined, call `acl.op.infer_shape`, `acl.get_tensor_desc_num_dims`, `acl.get_tensor_desc_dim_v2`, or `acl.get_tensor_desc_dim_range` to infer or estimate the output shape of the operator before calling `acl.op.execute_v2`. The output shape is used as the input of `acl.op.execute_v2`.

## Sample Code

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......

# Determine the allocation of memory for storing the input tensor data of the operator. If the app runs on the host, allocate host memory.
# If the app runs on the device, allocate device memory.
ret = acl.op.infer_shape(op_type, self.in_desc_list, self.in_list, num_outputs, self.out_desc_list, self.attr)

tensor_dims = []
# Perform a for loop for each output to infer or estimate the shape value.
for i in range(len(infer_desc_list)):
    dim_nums = acl.get_tensor_desc_num_dims(infer_desc_list[i])
    dim_size = []
    for j in range(dim_nums):
        dim, ret = acl.get_tensor_desc_dim_v2(infer_desc_list[i], j)
        # The dimension size is dynamic in the dynamic-shape scenario.
        if dim == -1:
            # Obtain the shape range and use the maximum shape value to construct the output tensor_desc, as an argument of the acl.op.execute_v2 call.
            dim_range, ret = acl.get_tensor_desc_dim_range(infer_desc_list[i], j, 2)
            dim = dim_range[1]
        dim_size.append(dim)
    tensor_dims.append(dim_size)

# The preceding provides the operator output shape and the output tensor_desc (that is, the value of self.out_desc_list) is constructed based on dims in tensor_dims, as the input parameters of the acl.op.execute_v2 call.
ret = acl.op.execute_v2(op_type, self.in_desc_list, self.in_list, self.out_desc_list, self.out_list, self.attr, self.stream)

out_tensor_dims = []
# Add the following code lines to obtain the accurate shape after operator execution.
for i in range(len(self.out_desc_list)):
    dim_nums = acl.get_tensor_desc_num_dims(self.out_desc_list[i])
    dim_size = []
    for j in range(dim_nums):
        dim, ret = acl.get_tensor_desc_dim_v2(self.out_desc_list[i], j)
        dim_size.append(dim)
    out_tensor_dims.append(dim_size))

# ......
```
