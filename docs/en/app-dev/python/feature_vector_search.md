<!-- npu="310p" id1 -->
# Feature Vector Search

## Basic Principles

Feature vector search is used to verify the feature search function. To do so, you need to generate a random repository in which random features can be searched for. (Currently, the `1:N` and `M:N` search modes are supported. The following sample code uses the `1:N` mode as an example.) The process can be broken into the following steps: initialization, adding features to the repository, repository search, precise modification or deletion of the features in the repository, and deinitialization. The API calls are described as follows:

- Initialization: Call `acl.init` to perform initialization and allocate runtime resources, and call `acl.fv.create_init_para` to create data of the aclfvInitPara type to specify the initialization parameters for feature vector search.
- Adding features to the repository: Call `acl.fv.create_feature_info` to create data of the aclfvFeatureInfo type as the feature description, and call `acl.fv.repo_add` to add a repository.
- Repository search: Call `acl.fv.search` to search.
- Precise modification or deletion of features in the repository: Call `acl.fv.delete` and `acl.fv.modify` to delete or modify a feature in the repository. The following code uses feature deletion as an example.
- Deinitialization: Release runtime resources, call `acl.fv.destroy_init_para` to destroy data of the aclfvInitPara type, and call `acl.fv.release` to deinitialize the feature search module and free the memory.

## Sample code

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to be built or run.

```python
# 1. Perform initialization.

# 2. Allocate runtime resources.

# 3. Initialization
# 3.1 Initialize the feature search module. The following uses the repository with 100,000 features as an example.
fs_num = 100000
fv_init_para = acl.fv.create_init_para(fs_num)

# 3.2 Specify the initialization parameter for feature vector search.
ret = acl.fv.init(fv_init_para)

# 4. Add the repository and feature vectors.
# 4.1 Add the first feature. When creating the feature description, set the offset parameter to 0.
offset = 0
feature_count = 1000
feature_len = 36
base_data_len = feature_count * feature_len

# Create memory.
feature_info_device, ret = acl.rt.malloc(base_data_len, ACL_MEM_MALLOC_NORMAL_ONLY)

# The user-defined function base_short_feature_alloc is used to generate random feature data.
feature_type = SEARCH_1_N
feature_info_buffer = base_short_feature_alloc(feature_count, feature_type)

# Convert the random feature data into an array.
feature_info_list_arr = numpy.array(feature_info_buffer, dtype=numpy.uint8)
# Convert the random feature data into a bytes object and obtain the pointer address of the bytes object through acl.util.bytes_to_ptr.
bytes_data = feature_info_list_arr.tobytes()
feature_info_ptr = acl.util.bytes_to_ptr(bytes_data)
# Copy the random feature data from the host to the device.
ret = acl.rt.memcpy(feature_info_device, feature_count * feature_len, feature_info_ptr, feature_count * feature_len, ACL_MEMCPY_HOST_TO_DEVICE)


# Create feature description information. inputData indicates the random feature data generated in the previous step.
feature_info = acl.fv.create_feature_info(id0, id1, offset, feature_len, feature_count, feature_info_device, feature_len * feature_count)

# Add a repository and add features to the repository. featureInfo indicates the feature description generated in the previous step.
ret = acl.fv.repo_add(SEARCH_1_N, feature_info)

# Destroy the aclfvFeatureInfo data.
ret = acl.fv.destroy_feature_info(feature_info)

# 4.2 Add the second feature and precisely delete or modify a feature in the repository. When creating the feature description information, ensure that the offset value is the same as the number of features added to the repository.
offset += feature_count

# For details about how to add a feature to the repository, see step 4.1.
# ....

feature_data_list = []
for i in range(36):
    feature_data_list.append(i)
# Convert the random feature data into an array.
feature_info_list_arr = numpy.array(feature_data_list, dtype=numpy.uint8)
# Convert the random feature data into a bytes object and obtain the pointer address of the bytes object through acl.util.bytes_to_ptr.
bytes_data = feature_info_list_arr.tobytes()
feature_info_ptr = acl.util.bytes_to_ptr(bytes_data)
# Create memory and transfer the feature data.
feature_info_device, ret = acl.rt.malloc(36, ACL_MEM_MALLOC_NORMAL_ONLY)
kind = ACL_MEMCPY_DEVICE_TO_DEVICE

# If the run mode is ACL_HOST, copy the feature data to the device. feature_len indicates the length of the memory allocated using the feature_data_list dataset.
ret = acl.rt.memcpy(feature_info_device, feature_count * feature_len, feature_info_ptr, feature_count * feature_len, ACL_MEMCPY_HOST_TO_DEVICE)

# Create feature description information.
id0 = 0
id1 = 0
feature_info = acl.fv.create_feature_info(id0, id1, offset, 36, 1, feature_info_buffer, 36)

#  Delete a feature.
acl.fv.destroy_feature_info(feature_info)

# 4.3 Add features to other repositories. The value for the level-1 and level-2 repositories are both 1.
id0 = 1
id1 = 1
offset = 0

# For details about how to add a feature to the repository, see step 4.1.
# ....

# 5. Repository search (in 1:N mode for example), including feature search preprocessing, 1:N feature search, and feature search result processing.
# 5.1 Feature search preprocessing. In 1:N mode, the value of queryCnt must be 1.
query_cnt = 1
table_len = 32 * 1024
topK = 5
type_size = 4
table_data_len = query_cnt * table_len

# Generate a data table for search and comparison. The user-defined function adc_table_init is used to initialize the input ADC table for feature search.
table_data_tmp = adc_table_init(1000, query_cnt * 1024)

# Allocate memory to the data table. table_data_dev is used to create and search for the input table information.
table_data,ret = acl.rt.malloc(table_data_len, ACL_MEM_MALLOC_NORMAL_ONLY)

# Allocate memory for the search result resultNumDev, id0Dev, id1Dev, resultOffsetDev, and resultDistanceDev.
data_len = query_cnt * topK * type_size
result_num_data_len = query_cnt * type_size
result_num, ret = acl.rt.malloc(result_num_data_len, ACL_MEM_MALLOC_NORMAL_ONLY)
id_0, ret = acl.rt.malloc(data_len, ACL_MEM_MALLOC_NORMAL_ONLY)
id_1, ret = acl.rt.malloc(data_len, ACL_MEM_MALLOC_NORMAL_ONLY)
result_offset, ret = acl.rt.malloc(data_len, ACL_MEM_MALLOC_NORMAL_ONLY)
result_distance, ret = acl.rt.malloc(data_len, ACL_MEM_MALLOC_NORMAL_ONLY)

# Create a search input table. The result is used as the input information for creating a search task.
query_table = acl.fv.create_query_table(query_cnt, table_len, table_data, table_data_len)

# Create a feature repository range parameter. The result is used as the input information for creating a search task.
repo_range = acl.fv.create_repo_range(0, 1023, 0, 1023)
# Create the input information of a search task. The result is used for feature search in 1:N mode.
search_input = acl.fv.create_search_input(query_table, repo_range, topK)

# Create the search result information. The result is used for feature search in 1:N mode.
search_result = acl.fv.create_search_result(query_cnt, result_num, result_num_data_len, id_0, id_1, result_offert, result_distance, data_len)

# 5.2 Feature search in 1:N mode
ret = acl.fv.search(SEARCH_1_N, search_input, search_result)

# 6. Delete the repository and data.
# Create a feature repository range and delete the repository in the specified range.
id0Min = 0
id0Max = 1023
id1Min = 0
id1Max = 1023
repo_range = acl.fv.create_repo_range(id0Min, id0Max, id1Min, id1Max)
ret = acl.fv.repo_del(SEARCH_1_N, repo_range)

#  Destroy data of the aclfvInitPara type.
ret = acl.fv.destroy_init_para(fv_init_para)

# 7. Deallocate runtime resources.

# 8. Perform deinitialization.
# ......
```
<!-- end id1 -->
