# Unilateral Communication

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:13:38.914Z pushedAt=2026-10-22T03:02:32.490Z nl=2 -->

Huawei Xfer Library (HIXL) is a flexible and efficient Ascend unilateral communication library. It provides simple, reliable, and efficient point-to-point data transfer capabilities for cluster scenarios, and exposes them to users through a simple API, bridging multiple AI applications and multiple transfer links. It can be used to build various service scenarios such as large model prefill-decode (PD) disaggregation, parameter switching in reinforcement learning (RL) post-training, and model parameter caching.

This section provides only a brief introduction to HIXL. For details about how to use HIXL, see the *HIXL Unilateral Communication Library*.

## Core Advantages

- Supports a unilateral zero-copy communication mechanism: the unilateral communication library provides simple and reliable unilateral communication APIs. After local memory data is ready, data can be directly transferred to remote memory through unilateral operations. This mechanism requires no operation on the remote node, providing core technical support for users to build scheduling mechanisms that overlap communication and computation. Meanwhile, the zero-copy capability enables direct data transfer between user memories, avoiding redundant data movement. This not only reduces memory bandwidth usage but also lowers memory capacity consumption.
- Shields hardware differences and supports multiple links for high-speed cross-device interconnection: the unilateral communication library shields the underlying hardware differences of Ascend chips, so users do not need to adapt code for different chip architectures. At the communication link level, this technology natively supports multiple high-speed interconnection protocols such as RDMA and HCCS, with a communication bandwidth of up to 119 GB/s. It enables seamless high-speed interconnection of cross-architecture devices, meeting the requirements of low latency and high throughput.
- Minimal API design with deep adaptation to open-source ecosystem frameworks: the unilateral communication library adopts a minimal API design, reducing the number of APIs to more than ten core calls and lowering the integration threshold for developers, while providing complete C++/Python language API support. It has achieved deep integration with open-source frameworks such as Mooncake and DeepLink. Mainstream inference engines such as vLLM and SGLang can also directly call the unilateral communication library APIs to efficiently transfer KV Cache across devices, reducing memory access latency by 20% during large model inference and improving inference throughput.

## Software Architecture

The unilateral communication library is shown in Figure 1.

**Figure 1** Unilateral communication library software architecture  
![](figures/HIXL_arch.png "Unilateral communication library software architecture")

**Core Components**

- HIXL Engine: As the core transfer engine, it provides basic transfer APIs and supports multiple memory types, such as D2D, D2H, and H2D. It is also compatible with multiple transfer protocols, including HCCS and RDMA, enabling high-speed and reliable data transfer. It natively supports multiple types of data links and is applicable to complex scenarios of homogeneous and heterogeneous clusters. When clusters require dynamic scaling of nodes, it can efficiently complete link adaptation and resource scheduling, building a reliable communication foundation for the overall operation of the cluster.
- LLM-DataDist: Built on HIXL Engine, it provides a set of data transfer APIs with KV Cache semantics. It can quickly and flexibly integrate with inference engines such as vLLM and SGLang.

## Quick Experience

This sample scenario is H2RD (data transfer from the host to the remote device), which describes how the client initiates unilateral data read/write to the server.

1. Bind the Ascend device used by the current process on the client side and the server side respectively, initialize the HIXL object, allocate memory, and register the memory with HIXL.
    - Client side:

        ```cpp
        // Bind the Ascend device used by the current process.
        CHECK_ACL(aclrtSetDevice(device));
        
        // Initialize the HIXL engine with local_engine as the identifier (the client side is generally an IP string without a port).
        Hixl hixl_engine;
        std::map<AscendString, AscendString> options;
        CHECK_HIXL(hixl_engine.Initialize(local_engine, options));
        
        // Allocate the host-side transfer buffer for MEM_HOST registration and the local end of unilateral read/write.
        int32_t *host_buf = nullptr;
        CHECK_ACL(aclrtMallocHost(reinterpret_cast<void **>(&host_buf), sizeof(int32_t)));
        
        // Register the host address with HIXL so that the peer can perform unilateral access over the established link.
        MemDesc reg_desc{};
        reg_desc.addr = reinterpret_cast<uintptr_t>(host_buf);
        reg_desc.len = sizeof(int32_t);
        MemHandle handle = nullptr;
        CHECK_HIXL(hixl_engine.RegisterMem(reg_desc, MEM_HOST, handle));
        ```

    - Server side:

        ```cpp
        // Bind the Ascend device used by the current process.
        CHECK_ACL(aclrtSetDevice(device));
        
        // Initialize HIXL on the local_engine with a port, as the connected end.
        Hixl hixl_engine;
        std::map<AscendString, AscendString> options;
        CHECK_HIXL(hixl_engine.Initialize(local_engine, options));
        
        // Allocate memory on the device and write the initial value 1 through H2D for client READ verification.
        constexpr int32_t kInit = 1;
        int32_t *dev_buf = nullptr;
        CHECK_ACL(aclrtMalloc(reinterpret_cast<void **>(&dev_buf), sizeof(int32_t), ACL_MEM_MALLOC_HUGE_ONLY));
        CHECK_ACL(aclrtMemcpy(dev_buf, sizeof(int32_t), &kInit, sizeof(int32_t), ACL_MEMCPY_HOST_TO_DEVICE));
        
        // Register the device address with HIXL so that the client can perform unilateral read/write on this address range.
        MemDesc reg_desc{};
        reg_desc.addr = reinterpret_cast<uintptr_t>(dev_buf);
        reg_desc.len = sizeof(int32_t);
        MemHandle handle = nullptr;
        CHECK_HIXL(hixl_engine.RegisterMem(reg_desc, MEM_DEVICE, handle));
        ```

2. On the client side, initiate a link to the server side.

    ```cpp
    // Establish a transport link with remote_engine (the server listening address).
    CHECK_HIXL(hixl_engine.Connect(remote_engine));
    ```

3. On the client side, initiate data read/write to the server side. Then check whether the read/write values are correct on both the client side and the server side.
    - Client side:

        ```cpp
        // Unilateral read: read the prewritten value 1 from MEM_DEVICE of the peer server to the local host memory.
        TransferOpDesc xfer{reinterpret_cast<uintptr_t>(&host_buf), dev_buf, sizeof(int32_t)};
        CHECK_HIXL(hixl_engine.TransferSync(remote_engine, READ, {xfer}));
        printf("after READ: %d\n", *host_buf);
        
        // Unilateral write: write the locally preset host memory value 2 to MEM_DEVICE of the peer server.
        *host_buf = 2;
        CHECK_HIXL(hixl_engine.TransferSync(remote_engine, WRITE, {xfer}));
        ```

    - Server side:

        ```cpp
        // After the client completes the unilateral write, read the value on the device back to the host on the server side to verify that it should be 2 after the client WRITE.
        int32_t host_val = 0;
        CHECK_ACL(aclrtMemcpy(&host_val, sizeof(int32_t), dev_buf, sizeof(int32_t), ACL_MEMCPY_DEVICE_TO_HOST));
        printf("after transfer: %d\n", host_val);
        ```

4. Release the link on the client side.

    ```cpp
    CHECK_HIXL(hixl_engine.Disconnect(remote_engine));
    ```

5. Deregister the memory, release the memory, and destroy the HIXL engine on the client side and the server side respectively, and finally unbind from the device.
    - Client side:

        ```cpp
        CHECK_HIXL(hixl_engine.DeregisterMem(handle));
        CHECK_ACL(aclrtFreeHost(host_buf));
        hixl_engine.Finalize();
        CHECK_ACL(aclrtResetDevice(device));
        ```

    - Server side:

        ```cpp
        CHECK_HIXL(hixl_engine.DeregisterMem(handle));
        CHECK_ACL(aclrtFree(dev_buf));
        hixl_engine.Finalize();
        CHECK_ACL(aclrtResetDevice(device));
        ```
