# Header Files and Library Files

<!-- md-trans-meta sourceCommit=8e249fa8820f9d3024e0508027697e45e0ee0c7d translatedAt=2026-10-23T09:33:22.606Z pushedAt=2026-10-26T01:39:04.047Z nl=2 -->

## Environment Requirements

<!-- npu="950,A3,910b,910,310p,310b" id1 -->
- When calling operators via the aclnn API, install the CANN Toolkit package and the ops operator package in advance. For specific operations, see [CANN Software Installation](https://hiascend.com/document/redirect/CannCommunityInstSoftware).
<!-- end id1 -->
<!-- npu="950,A3,910b" id2 -->
- When calling operators via the PyTorch API, install the CANN Toolkit package, the ops operator package, and the TorchNPU package (note that the TorchNPU package version must match the Toolkit package version) in advance. For specific operations, see [CANN Software Installation](https://hiascend.com/document/redirect/CannCommunityInstSoftware) and [TorchNPU Software Installation](https://www.hiascend.com/document/detail/en/Pytorch/2600/configandinstg/instg/docs/en/installation_guide/installation_description.md).
<!-- end id2 -->
- When calling operators through Ascend IR via GE graph construction, install the CANN Toolkit package and the ops operator package in advance. For specific operations, see [CANN Software Installation](https://hiascend.com/document/redirect/CannCommunityInstSoftware).

## Dependent File List

**Different types of APIs in the operator library are defined in different paths:**

<!-- npu="950,A3,910b,910,310p,310b" id3 -->
- When calling the operator aclnn API, you need to include the dependent header files and library files. The header files are in the `${INSTALL_DIR}/include/` directory by default, and the library files are in the `${INSTALL_DIR}/lib64/` directory by default. For detailed reference paths, see [Table 1](#table1).
<!-- end id3 -->
<!-- npu="950,A3,910b" id4 -->
- When calling the **torch\_extension** API, you need to import the following modules, among which **cann\_ops\_transformer** is defined in the `${INSTALL_DIR}/python/site-packages/cann_ops_transformer` directory.

    ```python
    import torch
    import torch_npu
    import cann_ops_transformer
    ```
<!-- end id4 -->

- When calling Ascend IR operators, the header file path is `${INSTALL_DIR}/opp/built-in/op_graph/inc/ops_proto_*.h`, and the library file path is `${INSTALL_DIR}/opp/built-in/op_graph/lib/libopgraph_*.so`. For detailed reference paths, see [Table 1](#table1).

Replace `${INSTALL_DIR}` with the file storage path after CANN software installation. For example, if you install the software as the **root** user, the default storage path is `/usr/local/Ascend/cann`.

**Table 1**  Dependent file list  <a id="table1"></a>

<!-- npu="950,A3,910b,910,310p,310b" id5 -->
|  API Category  |  Purpose  |  Naming Style  |  Dependent Header File  |  Dependent Library File  |
|----------|--------|-----------|--------------|--------------|
|  [Common APIs](https://gitcode.com/cann/opbase/blob/9.2.0/docs/en/api/nnopbase/aclnn/00_aclnn_api_list.md)   |Common Meta APIs that the aclnn API depends on, such as **aclTensor**, **aclScalar**, and **aclIntArray**.|Prefixed with **acl**, in UpperCamelCase style.|<li>aclnn/acl_meta.h</li><li>aclnn/aclnn_base.h</li>|libnnopbase.so|
|  [Operator APIs (aclnn)](op_interface_aclnn.md)  | Provides a set of C APIs to implement CANN operator call, including Math, NN, CV, Transformer, and other categories of operators. | Uses **aclnn** as prefix and is generally divided into two-stage APIs, where "Xxx" indicates the operator name (requiring the UpperCamelCase style).<li>Stage 1: **aclnnXxxGetWorkspaceSize**</li><li>Stage 2: **aclnnXxx**</li>|<li>Header files that each category of API depends on (recommended): **aclnnop/aclnn_ops_math.h**, **aclnnop/aclnn_ops_nn.h**, **aclnnop/aclnn_ops_cv.h**, **aclnnop/aclnn_ops_transformer.h**</li><li>Header file that each API depends on: **aclnnop/aclnn_*.h** (* indicates the specific operator name)</li>  | <li>Overall library file that the aclnn API depends on: **libopapi.so** (deprecated)</li><li>Library files that each category of API depends on: **libopapi_math.so**, **libopapi_nn.so**, **libopapi_cv.so**, **libopapi_transformer.so**</li> |
|   [Operator APIs (torch_extension)](op_interface_torch.md)  | For common large-model operators that are not native to PyTorch, provides a set of PyTorch-style APIs to implement CANN operator call. | Uses **\$\{op\_name\}** as the API name, requiring lowercase and underscore form, with the call style **cann\_ops\_transformer.\$\{op\_name\}**, generally defined in the `${INSTALL_DIR}/python/site-packages/cann_ops_transformer` directory. | - | - |
|   [Ascend IR Operator Specifications](ascendIR_op_specification.md)  | Provides CANN operator specification information used in GE graph scenarios, including functions, data types, and formats. | IR naming uses the UpperCamelCase style: **XxxYyyZzz**, for example, **AsinGrad**. | <li>ops_proto_math.h</li><li>ops_proto_nn.h</li><li>ops_proto_cv.h</li><li>ops_proto_transformer.h</li><li>ops_proto_legacy.h</li> |  <li>libopgraph_math.so</li><li>libopgraph_nn.so</li><li>libopgraph_cv.so</li><li>libopgraph_transformer.so</li><li>libopgraph_legacy.so</li> |
|   [Appendix > nnopbase APIs > Framework Capability APIs](https://gitcode.com/cann/opbase/blob/9.2.0/docs/zh/api/nnopbase/opdev/opbase_frame_interface.md)   | Provides the common framework capability APIs that the aclnn API depends on for development. | UpperCamelCase style | aclnn/opdev/*.h. For specific file names, see the [nnopbase API list](https://gitcode.com/cann/opbase/blob/9.2.0/docs/zh/api/nnopbase/opdev/0_opdev_api_list.md). | - |
|   [Appendix > nnopbase APIs > Basic Tensor Operation APIs](https://gitcode.com/cann/opbase/blob/9.2.0/docs/zh/api/nnopbase/opdev/L0/basic_l0_Interface.md)  | Provides the Level0 APIs that the aclnn API depends on for development. | UpperCamelCase style | aclnn_kernels/*.h. For specific file names, see the [nnopbase API list](https://gitcode.com/cann/opbase/blob/9.2.0/docs/zh/api/nnopbase/opdev/1_opdev_api_introduction.md). | libopapi_math.so |
|   [Appendix > op_common APIs](https://gitcode.com/cann/opbase/blob/9.2.0/docs/zh/api/op_common/0_op_common_list.md)   | Provides the common capabilities that operators depend on during development and calling, such as log retrieval and Tiling/InferShape development APIs. |UpperCamelCase style  |  <ul><li>op\_common/log/\*.h</li><li>op\_common/op\_host/\*.h</li><li>op\_common/op\_kernel/\*.h</li><li>op\_common/op\_graph/\*.h</li></ul> For specific file names, see the [op_common API list](https://gitcode.com/cann/opbase/blob/9.2.0/docs/zh/api/op_common/op_common_api_introduction.md).  | - |
<!-- end id5 -->

<!-- npu="950,A3,910b,910,310p,310b" id7 -->
>**Note:**
>
> - When calling the operator API (aclnn), note the dependent header files:
>   - After referencing the overall header file of each category, you do not need to reference the header file of a single API.
>   - Starting from CANN 7.0.0, the operator header file path **aclnnop/level2/aclnn\_\*.h** is **deprecated**. Use the new header file path **aclnnop/aclnn\_\*.h** instead.
> - When calling the operator API (aclnn), note the dependent library files:
>   - Starting from CANN 9.0.0, **libopapi.so** is **deprecated.** Use the **libopapi\_\*.so** sub-library files to improve operator compilation efficiency.
>   - Starting from CANN 8.5.0, the **libaclnn\_ops\_infer**, **libaclnn\_ops\_train**, **libaclnn\_math**, **libaclnn\_rand** static libraries (\*.a) and the dynamic library \(\*.so\) are **deprecated**. Use the **libopapi\_\*.so** library files.
<!-- end id7 -->
