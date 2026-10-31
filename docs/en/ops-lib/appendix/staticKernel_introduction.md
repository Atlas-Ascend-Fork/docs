# Introduction

<!-- md-trans-meta sourceCommit=ed69a6e4ddc089b45629fd67e49093ec3f403d7e translatedAt=2026-10-20T07:17:17.620Z pushedAt=2026-10-21T02:33:30.168Z nl=2 -->

## Before You Start

**Usage Scenarios**

For networks with only static shapes or dynamic-shape networks with infrequent shape changes, if you want to quickly improve network execution performance, you can use the operator compilation tool (op\_compiler) to build a static kernel package during network deployment to improve operator call performance.

**Tuning Principles**

Static kernel compilation means that the operator shape size is specified at compilation time, and the shape size does not need to be specified at runtime. The operator compilation tool obtains the determined shape information based on the input operator information statistics file, and compiles an operator binary for each shape, thereby improving operator execution efficiency and performance.

The advantages of static kernel compilation are as follows:

- The sizes of all tensors are known at compilation time, resulting in high storage space utilization.
- Targeted optimization can be performed for the actual shape size at compilation time.
- AI processors are good at executing parallel instructions but not at logical computation. Too many scalar operations may interrupt the execution of parallel instructions, leading to performance degradation. Static compilation can complete scalar computation at compilation time, improving performance to a certain extent.
- The compilation tool knows the exact operation data size at compilation time, so it does not insert additional synchronization, and does not cause parallel execution of multiple instructions to become serial execution, improving performance to a certain extent.

**Constraints**

The static compilation mode supports the following product models:
<!-- npu="310p" id1 -->
- <term>Atlas inference products</term>
<!-- end id1 -->
<!-- npu="910" id2 -->
- <term>Atlas training products</term>
<!-- end id2 -->
<!-- npu="910b" id3 -->
- <term>Atlas A2 products</term>
<!-- end id3 -->
<!-- npu="950" id4 -->
- <term>Ascend 950PR & 950DT products</term>
<!-- end id4 -->

## Overall Process

**Figure 1** Schematic diagram of using static kernels to improve performance

![fig1](../figures/staticKernel_flowchart.png "Schematic diagram of using static kernels to improve performance")

The basic process of improving operator execution performance in a network model by compiling static kernels is shown in the preceding figure. The overall tuning steps are as follows:

1. Dump operator information.

    Before tuning operators, obtain the operator information in the network model.

    - **Method 1**: If you use the Python APIs of PyTorch for programming, dump the operator JSON file through the Ascend PyTorch Profiler APIs.
    - **Method 2**: If you use the ACL APIs, directly call the **aclopStartDumpArgs** and **aclopStopDumpArgs** APIs to dump the operator JSON file.

2. Compile the static kernel package.

    Use the **operator compilation tool** to compile the dumped operator information statistics file (\*.json) and generate a kernel package.

    > **Note:** The operator compilation tool (op\_compiler) is a command-line tool provided by CANN for compiling operators and generating operator binary files. When the operator shape is fixed or changes infrequently, you can use this tool to compile and install a static kernel package to improve operator call performance. For details about this tool, see [Operator Compilation Tool](https://hiascend.com/document/redirect/CannCommunityopcompiler).

3. Install the static kernel package.

    Upload the static kernel package to the server where the target network model runs, and directly run the RUN package to complete the installation.

4. Verify the model execution effect.

    After installing the static kernel package, rerun the target network model, and compare the overall network running performance and the single-operator running time between the cases with and without the static kernel package installed.
