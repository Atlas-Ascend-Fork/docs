# Introduction

<!-- md-trans-meta sourceCommit=8e249fa8820f9d3024e0508027697e45e0ee0c7d translatedAt=2026-10-23T09:33:25.630Z pushedAt=2026-10-26T02:41:28.430Z nl=2 -->

## Document Positioning

This manual is intended for **operator call** scenarios and helps you quickly and correctly call the built-in operators of [Compute Architecture for Neural Networks (CANN)](https://www.hiascend.com/cann). These operators are deeply optimized and have good hardware affinity, accelerating network computation on AI processors.

<!-- npu="950,A3,910b,910,310p,310b" id1 -->
- If you need to **develop or debug custom operators**, see [Ascend C Operator Development Guide](https://hiascend.com/document/redirect/CannCommunityOpdevAscendC).
<!-- end id1 -->
- If you encounter issues when calling operators, see [Troubleshooting](https://hiascend.com/document/redirect/CannCommunitytrouble) to locate and analyze the issue.

<!-- npu="950,A3,910b,910,310p,310b" id2 -->
The source code of CANN built-in operators is open-sourced in the GitCode [CANN>Operator Library](https://gitcode.com/cann) project, where you can learn more about the community ecosystem and the operator development/contribution process.
<!-- end id2 -->

## Operator Library Architecture

The operator library is classified by functional domain. Its position in the CANN architecture and the dependencies between libraries are shown in [Figure 1](#fig1). The operator library is classified as follows:

- **Math library**: a numerical computation operator library that provides numerical processing and computation operators at different dimensions, such as Add and Abs, covering scenarios such as tensor shape transformation, basic mathematical operations, and random number generation.
- **NN library**: a neural network operator library that provides common computation operators in deep-learning models, such as convolution, cube multiplication, activation functions, and normalization.
- **CV library**: a computer vision operator library that provides image processing and object detection operators, such as GridSample.
- **Transformer library**: a large model computation operator library that provides core Transformer operators, such as Attention, LayerNorm, and merged compute and communication (MC2 for short) operators.
- **RAS library**: a reliability, availability, and serviceability operator library that provides reliability, availability, and maintainability capabilities, including security, encryption, and maintenance-related operators.
- **Opbase library**: the base framework library on which all operator libraries depend, providing basic scheduling capabilities (such as aclTensor creation/release and workspace reuse) and common dependency capabilities.

**Figure 1** Operator library architecture <a id="fig1"></a>

![fig1](figures/ops_lib_architecture.png "Operator library architecture")

## What Are Operators and Operator APIs

An operator is a basic functional unit in AI computing, similar to a "mathematical function". For example, the Add operator is used for vector addition, and the Matmul operator is used for cube multiplication. By combining these operators, you can build complex neural network models.

In actual use, you call operators through operator APIs.

- **Operator**: underlying computation logic, such as addition and cube multiplication.
- **Operator API**: programming entry exposed by an operator. When you write code on the host side (CPU side), you actually call these APIs, such as aclnn APIs and PyTorch APIs.

**Each operator may correspond to one or more operator APIs.** Take aclnn APIs as an example:

- The Add operator corresponds to the **aclnnAdd** and **aclnnAdds** APIs.
- The MatMulV3 operator corresponds to the **aclnnMatmul** and **aclnnMatmulWeightNz** APIs.

## Operator Call Methods

CANN operators support the following call methods. Select one based on your actual requirements.

<!-- npu="950,A3,910b,910,310p,310b" id3 -->
- **aclnn API**: Provides standard C APIs for all operators to facilitate calls from the host side. This method is referred to as the single-operator API (also known as the operator host API) call method. The call flow is shown in [Figure 2](#fig2).
<!-- end id3 -->
<!-- npu="950,A3,910b" id4 -->
- **PyTorch API**: For common operators that are not native to PyTorch (for example, neural network and large-model operators), a set of **torch\_extension** APIs compatible with the native PyTorch style is provided. These APIs use the JIT mechanism (**torch.utils.cpp\_extension.load**) to compile the C++ Kernel Wrapper just-in-time on the first call, bridging PyTorch functions to the aclnn API. In addition, they support the TorchAir graph mode through GE Converter.
<!-- end id4 -->
- **Ascend IR** (Intermediate Representation): Implements operator call through graph construction. The Graph Engine (GE) uniformly converts operators from mainstream AI frameworks into Ascend IR definitions, enabling accelerated execution of computation graphs on AI processors. For the principles of graph-mode call, see "Programming Guide" in [Graph Development Guide](https://hiascend.com/document/redirect/CannCommunityGraphguide).

<!-- npu="950,A3,910b,910,310p,310b" id5 -->
**Figure 2**  aclnn API call process <a id="fig2"></a>

![fig2](figures/aclnn_call_flowchart.png "aclnn call process")
<!-- end id5 -->

## Usage Guide

This chapter provides comprehensive guidance for your operator call journey. As a beginner, you are advised to read the documentation in the following order:

- <span style="display:inline-block;width:20px;height:20px;line-height:20px;text-align:center;border-radius:50%;background:#0057D9;color:#FFF;font-size:13px">1</span> **Environment setup**: First refer to [Header Files and Library Files](header_and_library.md) to learn how to install the CANN package and the header or library files required for calling operators.
- <span style="display:inline-block;width:20px;height:20px;line-height:20px;text-align:center;border-radius:50%;background:#0057D9;color:#FFF;font-size:13px">2</span> **Concept understanding**: Learn [Basic Concepts](https://gitcode.com/cann/ops-math/blob/9.2.0/docs/zh/context/basic_concept.md) to become familiar with the basic terms and key features of operators (such as determinism and quantization modes).
- <span style="display:inline-block;width:20px;height:20px;line-height:20px;text-align:center;border-radius:50%;background:#0057D9;color:#FFF;font-size:13px">3</span> **API call**: Select an appropriate operator call method based on your business scenario. Refer to the following table to find operators or operator APIs.

    <!-- npu="950,A3,910b,910,310p,310b" id6 -->
    **Table 1**  Operator list (Ascend AI processors)

    <table><thead>
      <tr>
        <th>API Category</th>
        <th>Operation Guide</th>
        <th>Description</th>
      </tr></thead>
    <tbody>
      <tr>
        <td><b>Common API</b></td>
        <td><a href="https://gitcode.com/cann/opbase/blob/9.2.0/docs/en/api/nnopbase/aclnn/00_aclnn_api_list.md">Common API</a></td>
        <td>Common Meta APIs that the aclnn APIs depend on, such as APIs for creating aclTensor, aclScalar, and aclIntArray.</td>
      </tr>
      <tr>
        <td rowspan="5"><b>Operator API (aclnn)</b></td>
        <td><a href="https://gitcode.com/cann/ops-math/blob/9.2.0/docs/zh/menu_aclnn_api.md">Math API</a></td>
        <td>C APIs corresponding to mathematical computation operators, such as Add and Abs.</td>
      </tr>
      <tr>
        <td><a href="https://gitcode.com/cann/ops-nn/blob/9.2.0/docs/zh/menu_aclnn_api.md">NN API</a></td>
        <td>C APIs corresponding to Neural Network operators, such as Matmul. Currently, this category accounts for the largest proportion of the entire operator library.</td>
      </tr>
      <tr>
        <td><a href="https://gitcode.com/cann/ops-cv/blob/9.2.0/docs/zh/menu_aclnn_api.md">CV API</a></td>
        <td>C APIs corresponding to Computer Vision operators, such as GridSample.</td>
      </tr>
      <tr>
        <td><a href="https://gitcode.com/cann/ops-transformer/blob/9.2.0/docs/zh/menu_aclnn_api.md">Transformer API</a></td>
        <td>C APIs corresponding to large-model computation operators, such as FlashAttention, MC2 (merged computing and communication), and MoE (Mixture of Experts).</td>
      </tr>
      <tr>
        <td><a href="https://gitcode.com/cann/ops-ras/blob/9.2.0/docs/zh/menu_aclnn_api.md">RAS APIs</a></td>
        <td>C APIs corresponding to security and maintainability operators.</td>
      </tr>
      <tr>
        <td rowspan="2"><b>Operator APIs (torch_extension)</b></td>
        <td><a href="https://gitcode.com/cann/ops-nn/blob/9.2.0/docs/zh/menu_torch_api.md">NN APIs</a></td>
        <td>Provides PyTorch APIs for common neural network operators that are not native to PyTorch, such as Matmul.</td>
      </tr>
      <tr>
        <td><a href="https://gitcode.com/cann/ops-transformer/blob/9.2.0/docs/zh/menu_torch_api.md">Transformer APIs</a></td>
        <td>Provides PyTorch APIs for common large-model operators that are not native to PyTorch, such as FlashAttention, MC2 (merged computing and communication), and MoE.</td>
      </tr>
      <tr>
        <td><b>Ascend IR operator prototypes</b></td>
        <td><a href="ascendIR_op_specification.md">Ascend IR Operator Specifications</a></td>
        <td>Lists the operator information defined based on Ascend IR.</td>
      </tr>
    </tbody></table>
    <!-- end id6 -->

- <span style="display:inline-block;width:20px;height:20px;line-height:20px;text-align:center;border-radius:50%;background:#0057D9;color:#FFF;font-size:13px">4</span> **Related resources**:
  - [Appendix](appendix/appendix.md): Obtain answers to common operator call questions (FAQs), performance optimization guides, and advanced API descriptions.
    - Provides the nnopbase APIs required for developing aclnn APIs
    - Provides the op_common public APIs required during operator development/call.
    - Improves operator execution performance through static kernel.
    - Common FAQs and cases during operator call
  - [AI Framework Operator Support List](https://hiascend.com/document/redirect/CannCommunityFwOplist): Obtain native IR operator information of mainstream AI frameworks (such as TensorFlow and Caffe).

## Notes

- **V version evolution**: An operator or operator API may have multiple V versions. **Prioritize the highest V version** (a higher version is backward compatible with lower versions).
- **Unsupported scenarios**: For scenarios **not declared as supported** in this document (such as specific product models, data types, and dimensions), developers are not recommended to use them, and the call effect cannot be guaranteed for the time being.
<!-- npu="910b,910,310p" id8 -->
- **Virtualized instances**: Fusion operators do not support this feature. A fusion operator is a complex operator formed by fusing multiple independent basic "small operators" (such as vector and cube). Its functionality is equivalent to that of multiple small operators, while its performance is usually better, for example, the FlashAttention operator.
<!-- end id8 -->
