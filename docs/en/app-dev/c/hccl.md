# Collective Communication

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:38:14.384Z pushedAt=2026-10-26T03:10:39.436Z nl=2 -->

Huawei Collective Communication Library (HCCL) is a high-performance collective communication library built on Ascend hardware, providing high-performance and highly reliable communication solutions for computing clusters.

>**Note:** 
>This section only provides a brief introduction to HCCL. For details about how to use HCCL, see the *HCCL Collective Communication Library*.

## Core Functions

- Provides high-performance collective communication and point-to-point communication in single-node and multi-node environments.
- Supports collective communication primitives such as AllReduce, Broadcast, AllGather, ReduceScatter, AlltoAll, Send, and Receive.
- Supports communication algorithms such as Ring, Mesh, and Recursive Halving-Doubling (RHD).
- Supports high-speed communication links such as HCCS, RoCE, PCIe, and Unified Bus (UB).
- Supports two execution modes: single-operator mode and graph mode.
- Supports custom development of communication operators.

## Software Architecture

HCCL is a core component of CANN, providing high-performance and highly reliable communication solutions for NPU clusters. HCCL supports multiple AI frameworks at the upper layer and enables efficient interconnection between various Ascend AI processors at the lower layer. Its architecture is shown in the following figure.

**Figure 1** Software architecture of the collective communication library  
![](figures/HCCL_arch.png "Software architecture of the collective communication library")

HCCL consists of the HCCL collective communication library and the Huawei Communication (HCOMM) basics library:

- **HCCL**: Contains built-in communication operators and extended communication operators, and provides external communication operator APIs.
    - Built-in communication operators: basic communication operators provided by HCCL, including collective communication operators and point-to-point communication operators.
    - Extended communication operators: Users can use the APIs provided by the HCOMM basics library to customize extended communication operators.

- **HCOMM basics library**: adopts a layered and decoupled design approach, dividing communication capabilities into a control plane and a data plane.

    - Control plane: provides topology information query and communication resource management functions.
    - Data plane: provides data movement and compute functions such as local operations, inter-operator synchronization, and communication operations.

    The control plane provides communication resources, and the data plane provides operation resources. The related APIs allow communication operator developers to focus on service innovation without concerning themselves with the complex implementation details at the chip level.

## Quick Experience

The following uses the AllReduce operator as an example to describe how to use it in single-operator execution mode, helping you quickly experience the collective communication function.

- AllReduce operator description

    The AllReduce operation performs a reduction operation (supporting sum, prod, max, and min) on the input data of all nodes in the communicator, and then sends the result to the output buffer of all nodes.

    ![](figures/allreduce.png)

    Note: Each rank can have only one input.

- Sample introduction

    You can click [here](https://gitcode.com/cann/hcomm/tree/9.2.0/examples/01_communicators/03_one_device_per_pthread) to obtain the complete sample code. The sample creates a communicator based on root node information and manages one AI server in one process, where each NPU device is managed by one thread. It mainly includes the following functions:

    1. Device detection: queries the number of available devices by calling the **aclrtGetDeviceCount\(\)** API.
    2. Uses rank 0 as the root node and generates the **rootInfo** identifier of the root node by calling the **HcclGetRootInfo\(\)** API.
    3. Based on **rootInfo**, initializes the communicator in each thread by calling the **HcclCommInitRootInfo\(\)** API.
    4. Call the **HcclAllReduce\(\)** API to add the input data of all ranks in the communicator, send the result to all nodes, and print the result.

- Compilation and running

    Run the following command in the sample code directory:

    ```bash
    make
    make test
    ```

- Result analysis

    The data of each rank is initialized to 0-7. After the AllReduce operation, the result of each rank is the sum of the data at the corresponding positions of all ranks (the sum of the data of eight ranks).

    ```bash
    Found 8 NPU device(s) available
    rankId: 0, output: [ 0 8 16 24 32 40 48 56 ]
    rankId: 1, output: [ 0 8 16 24 32 40 48 56 ]
    rankId: 2, output: [ 0 8 16 24 32 40 48 56 ]
    rankId: 3, output: [ 0 8 16 24 32 40 48 56 ]
    rankId: 4, output: [ 0 8 16 24 32 40 48 56 ]
    rankId: 5, output: [ 0 8 16 24 32 40 48 56 ]
    rankId: 6, output: [ 0 8 16 24 32 40 48 56 ]
    rankId: 7, output: [ 0 8 16 24 32 40 48 56 ]
    ```
