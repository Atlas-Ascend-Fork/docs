# Introduction

<!-- md-trans-meta sourceCommit=ed69a6e4ddc089b45629fd67e49093ec3f403d7e translatedAt=2026-10-20T07:09:06.511Z pushedAt=2026-10-21T02:33:30.162Z nl=2 -->

## Document Purpose

This document is intended for **operator call** scenarios and helps you quickly and correctly call the built-in operators of [CANN](https://www.hiascend.com/cann) (Compute Architecture for Neural Networks). These operators are deeply optimized and have good hardware affinity, which accelerates network computation on AI processors.

<!-- npu="950,A3,910b,910,310p,310b" id1 -->
- If you need to **develop or debug custom operators**, see [Ascend C Operator Development Guide](https://hiascend.com/document/redirect/CannCommunityOpdevAscendC).
<!-- end id1 -->
- If you encounter issues when calling operators, see [Troubleshooting](https://hiascend.com/document/redirect/CannCommunitytrouble) to locate and analyze the issues.

<!-- npu="950,A3,910b,910,310p,310b" id2 -->
The source code of CANN built-in operators is open-sourced in the GitCode [CANN > Operator Library](https://gitcode.com/cann) project, where you can learn more about the community ecosystem and the operator development/contribution process.
<!-- end id2 -->

## Operator Library Architecture

The operator library is classified by functional domain. Its position in the CANN architecture and the dependencies between libraries are shown in [Figure 1](#fig1). The operator library is classified as follows:

- **Math library**: a numerical computation operator library that provides numerical processing and computation operators of different dimensions, such as Add and Abs, covering scenarios such as tensor shape transformation, basic mathematical operations, and random number generation.
- **NN library**: a neural network operator library that provides common computation operators in deep learning models, such as convolution, matrix multiplication, activation functions, and normalization.
- **CV library**: a computer vision operator library that provides image processing and object detection operators, such as GridSample.
- **Transformer library**: a large model computation operator library that provides core Transformer operators, such as Attention, LayerNorm, and merged compute and communication (MC2 for short) operators.
- **RAS library**: a security maintenance and testing operator library (reliability, availability and serviceability) that provides reliability, availability, and maintainability capabilities, including operators related to security, encryption, and maintenance and testing.
- **Opbase library**: the basic framework library on which all operator libraries depend. It provides basic scheduling capabilities (such as aclTensor creation/release and workspace reuse) and common dependency capabilities.

**Figure 1** Operator library architecture diagram <a id="fig1"></a>

![fig1](figures/ops_lib_architecture.png "Operator library architecture diagram")

## What Are Operators and Operator APIs

An operator is a basic functional unit in AI computation, similar to a "mathematical function". For example, the Add operator is used for vector addition, and the Matmul operator is used for matrix multiplication. By combining these operators, you can build complex neural network models.

In actual use, operators are called through operator APIs.

- **Operator**: underlying computation logic, such as addition and matrix multiplication.
- **Operator API**: programming entry exposed by an operator. When you write code on the host side (CPU side), what you actually call are these APIs, such as aclnn APIs and PyTorch APIs.

**Each operator may correspond to one or more operator APIs**. Take aclnn APIs as an example:

- The Add operator corresponds to the **aclnnAdd** and **aclnnAdds** APIs.
- The MatMulV3 operator corresponds to the **aclnnMatmul** and **aclnnMatmulWeightNz** APIs.

## Operator Call Methods

CANN operators support the following call methods. Select one based on your actual situation.

- **aclnn API**: Provides standard C APIs for all operators to facilitate call on the host side, that is, the single-operator API (also called operator host API) call method. The call flow is shown in [Figure 2](#fig2).
- **PyTorch API**: For non-native but common PyTorch operators (such as neural network and large model operators), provides a set of **torch\_extension** APIs compatible with the native PyTorch style. This API uses the JIT mechanism (**torch.utils.cpp\_extension.load**) to compile the C++ Kernel Wrapper just-in-time on the first call, bridging PyTorch functions to the aclnn API. In addition, it supports the TorchAir graph mode through the GE Converter.
- **Ascend IR** (Intermediate Representation): Implements operator call through graph construction. The Graph Engine (GE) uniformly converts mainstream AI framework operators into Ascend IR definitions, enabling accelerated execution of computation graphs on AI processors. For the graph mode call principle, see "Programming Guide" in [Graph Development Guide](https://hiascend.com/document/redirect/CannCommunityGraphguide).

**Figure 2**  aclnn API call flow <a id="fig2"></a>

![fig2](figures/aclnn_call_flowchart.png "aclnn call flow")

## Product Support

Different products support different operator invocation methods. Please refer to the "Product Support" section in the actual API documentation for details.

## Usage Guide

This chapter provides comprehensive guidance for your operator call journey. As a beginner, you are advised to read the following sections in order:

- <span style="display:inline-block;width:20px;height:20px;line-height:20px;text-align:center;border-radius:50%;background:#0057D9;color:#FFF;font-size:13px">1</span> **Environment Setup**: First read [Header Files and Library Files](header_and_library.md) to learn how to install the CANN package and the header or library files that operator call depends on.
- <span style="display:inline-block;width:20px;height:20px;line-height:20px;text-align:center;border-radius:50%;background:#0057D9;color:#FFF;font-size:13px">2</span> **Concept Understanding**: Learn [Basic Concepts](https://gitcode.com/cann/ops-math/blob/master/docs/en/context/basic_concept.md) to become familiar with the basic terms and key features of operators (such as determinism and quantization modes).
- <span style="display:inline-block;width:20px;height:20px;line-height:20px;text-align:center;border-radius:50%;background:#0057D9;color:#FFF;font-size:13px">3</span> **API Call**: Select an appropriate operator call method based on your service scenario. Refer to the following table to find the operator or operator API.

    **Table 1**  Operator list

    <table><thead>
      <tr>
        <th>API Category</th>
        <th>Operation Guide</th>
        <th>Description</th>
      </tr></thead>
    <tbody>
      <tr>
        <td><b>Common APIs</b></td>
        <td><a href="https://gitcode.com/cann/opbase/blob/master/docs/en/api/nnopbase/aclnn/00_aclnn_api_list.md">Common APIs</a></td>
        <td>Common Meta APIs that aclnn API calls depend on, such as creating **aclTensor**, **aclScalar**, and **aclIntArray**.</td>
      </tr>
      <tr>
        <td rowspan="5"><b>Operator API (aclnn)</b></td>
        <td><a href="https://gitcode.com/cann/ops-math/blob/master/docs/zh/menu_aclnn_api.md">Math APIs</a></td>
        <td>C APIs corresponding to mathematical computation operators, such as Add and Abs.</td>
      </tr>
      <tr>
        <td><a href="https://gitcode.com/cann/ops-nn/blob/master/docs/en/menu_aclnn_api.md">NN APIs</a></td>
        <td>C APIs corresponding to Neural Network (NN) operators, such as Matmul. Currently, NN operators account for the largest proportion of the entire operator library.</td>
      </tr>
      <tr>
        <td><a href="https://gitcode.com/cann/ops-cv/blob/master/docs/zh/menu_aclnn_api.md">CV APIs</a></td>
        <td>C APIs corresponding to Computer Vision (CV) operators, such as GridSample.</td>
      </tr>
      <tr>
        <td><a href="https://gitcode.com/cann/ops-transformer/blob/master/docs/en/menu_aclnn_api.md">Transformer APIs</a></td>
        <td>C APIs corresponding to large model computation operators, such as FlashAttention, MC2 (merged compute and communication), and MoE (Mixture of Experts).</td>
      </tr>
      <tr>
        <td><a href="https://gitcode.com/cann/ops-ras/blob/master/docs/en/menu_aclnn_api.md">RAS APIs</a></td>
        <td>C APIs corresponding to security maintenance and testing operators.</td>
      </tr>
      <tr>
        <td rowspan="2"><b>Operator APIs (torch_extension)</b></td>
        <td><a href="https://gitcode.com/cann/ops-nn/blob/master/docs/zh/menu_torch_api.md">NN APIs</a></td>
        <td>PyTorch APIs for common neural network operators that are not native to PyTorch, such as Matmul.</td>
      </tr>
      <tr>
        <td><a href="https://gitcode.com/cann/ops-transformer/blob/master/docs/en/menu_torch_api.md">Transformer APIs</a></td>
        <td>PyTorch APIs for common large model operators that are not native to PyTorch, such as FlashAttention, MC2 (merged compute and communication), and MoE.</td>
      </tr>
      <tr>
        <td><b>Ascend IR operator prototype</b></td>
        <td><a href="ascendIR_op_specification.md">Ascend IR Operator Specifications</a></td>
        <td>Lists the operator information defined based on Ascend IR.</td>
      </tr>
    </tbody></table>

- <span style="display:inline-block;width:20px;height:20px;line-height:20px;text-align:center;border-radius:50%;background:#0057D9;color:#FFF;font-size:13px">4</span> **Related Resources**:
  - [Appendix](appendix/appendix.md): Obtains common operator call FAQs, performance optimization guides, and advanced API descriptions.
    - Provides the nnopbase APIs required for developing aclnn APIs.
    - Provides the op_common APIs required during operator development/call.
    - Improves operator execution performance through static kernels.
    - Provides common FAQs and cases during operator call.
  - [AI Framework Operator Support List](https://hiascend.com/document/redirect/CannCommunityFwOplist): Obtains native IR operator information of mainstream AI frameworks (such as TensorFlow and Caffe).

## Precautions

- **V version evolution**: An operator or operator API may have multiple V versions. **Select the highest V version first** (a higher version is compatible with lower versions).
- **Unsupported scenarios**: For scenarios that are **not declared as supported** in the documentation (such as specific product models, data types, and dimensions), developers are advised not to use them, and the call effect cannot be guaranteed for the time being.
<!-- npu="910b,910,310p" id8 -->
- **Virtualized instances**: Fusion operators do not support this feature yet. A fusion-type operator is a complex operator formed by fusing multiple independent basic "small operators" (such as vector and cube operators). Its functionality is equivalent to that of multiple small operators, while its performance is usually better, for example, the FlashAttention operator.
<!-- end id8 -->
