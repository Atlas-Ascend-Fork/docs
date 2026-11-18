# What's New

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T10:02:43.418Z pushedAt=2026-11-16T03:10:48.324Z nl=2 -->

This section describes the latest changes to the CANN documentation.

## 9.2.0

<table>
  <colgroup>
    <col style="width: 6%">
    <col style="width: 18%">
    <col style="width: 52%">
    <col style="width: 24%">
  </colgroup>
  <thead>
    <tr>
      <th>No.</th>
      <th>Update</th>
      <th>Description</th>
      <th>Document</th>
    </tr>
  </thead>
  <tbody style="font-size:14px">
    <tr>
      <td style="font-size:14px">1</td>
      <td style="font-size:14px">Ascend product form descriptions</td>
      <td style="font-size:14px">Optimized the product portfolio, and added NPU_ARCH, soc_series, and soc_version parameter descriptions.</td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/Glossary/productform/hardwaredesc_0001.html">Ascend Product Overview</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">2</td>
      <td style="font-size:14px">Ascend C Operator Development</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">Added L2 cache partitioning optimization notes.</li><li style="font-size:14px">Added usage guides for new features of NPU architecture version 3510.</li><li style="font-size:14px">Optimized and adjusted the "Aclnn Operator Engineering Development" section by adding recommended readings, quick start guide, and other content.</li><li style="font-size:14px">Added the "Advanced Programming > Memory Model" chapter, which introduces the concepts, principles, common issues, and solutions of cache coherence and memory consistency.</li><li style="font-size:14px">Added the "Tensor-based C++ Programming" chapter.</li><li style="font-size:14px">Added the "Atomic Operation Instruction Optimization" chapter.</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/920/programug/Ascendcopdevg/asc-devkit/docs/en/guide/getting_started/ascend_c_overview_and_learning_path.md">Ascend C Operator Development</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">3</td>
      <td style="font-size:14px">PyPTO Pro Programming Model</td>
      <td style="font-size:14px">Added support for the PyPTO Pro development mode and the tile programming model for tile operations.</td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/920/programug/pyptoopdevg/docs/en/guide/introduction.md">PyPTO Operator Development</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">4</td>
      <td style="font-size:14px">Custom Operator Graph Integration and AutoFuse chapters</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">Adjusted the features and directory structure of the "Custom Operator Graph Integration" chapter.</li><li style="font-size:14px">Optimized the "AutoFuse" chapter:<ul><li style="font-size:14px">Adjusted the directory structure, added the "Quick Start" and "Enabling AutoFuse" chapters, and moved the detailed environment variable descriptions to the "Appendix" chapter.</li><li style="font-size:14px">The "Enabling AutoFuse" chapter introduces the two paths to enable AutoFuse, and adds the fusion enabling method under the Inductor path.</li></ul></li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/920/programug/graphdevg/docs/en/user_guides/graph_dev/overview/GE_definition.md">Graph Development</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">5</td>
      <td style="font-size:14px">New documentation</td>
      <td style="font-size:14px">Added the *PTOAS* document.</td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/920/compiler/ptoas/overview/what_is_ptoas.md">PTOAS</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">6</td>
      <td style="font-size:14px">HCCL fault troubleshooting cases</td>
      <td style="font-size:14px">Optimized three fault cases: the "Link Setup Timeout", "notify_wait Timeout", and "Communicator Initialization Topology Detection Timeout" sections.</td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/920/commlib/hcclug/docs/en/user_guide/hccl_intro.md">Huawei Collective Communication Library (HCCL)</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">7</td>
      <td style="font-size:14px">Ascend C API documentation</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">Restructured the Ascend 950PR&950DT products documentation in the "C API" chapter, refined the directory structure and optimized the internal structure, and improved the API function descriptions, call examples, and constraints.</li><li style="font-size:14px">Improved the cube_compute_load/store, layout_structure, data_move, tensor_structure, and other documentation in the "Tensor API" chapter.</li><li style="font-size:14px">Optimized the "SIMT API" chapter:<ul><li style="font-size:14px">Supplemented the UB reuse layout rule description.</li><li style="font-size:14px">Updated the precision description of the math library APIs.</li><li style="font-size:14px">Added grid_group and thread_group descriptions to the cooperative groups.</li><li style="font-size:14px">Added the "SIMT Instruction Theoretical Performance Summary" chapter.</li><li style="font-size:14px">Added integer conversion functions.</li><li style="font-size:14px">Added the build options used in SIMT programming.</li></ul></li><li style="font-size:14px">Added the "CheckOpResSufficient" chapter.</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/920/API/ascendcopapi/docs/en/api/api_list.md">Ascend C APIs</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">8</td>
      <td style="font-size:14px">New chapter</td>
      <td style="font-size:14px">Added the PyPTO Pro API chapter.</td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/920/API/pyptoapi/docs/en/api/tensor_api/tensor/pypto-Tensor_introduction.md">PyPTO API</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">9</td>
      <td style="font-size:14px">Operator Library</td>
      <td style="font-size:14px">Added the "NN APIs" chapter under "Operator APIs (torch_extension)".</td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/920/API/aolapi/docs/en/ops-lib/introduction.md">Operator Library</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">10</td>
      <td style="font-size:14px">Performance Tuning Tool documentation</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">Adjusted the directory structure to flatten the documentation by profiling tool.</li><li style="font-size:14px">Moved the chapters about Ascend PyTorch Profiler, MindSpore Profiler, "Using TensorFlow APIs for Data Profiling", and "Using acl Python APIs for Data Profiling" to their respective source documents. Their redirection links remain in the Overview section in *Performance Tuning Tool*.</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/920/devaids/Profiling/docs/en/profiling/overview.md">Performance Tuning Tool</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">11</td>
      <td style="font-size:14px">Content about enhanced memory analysis</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">Added a device memory OOM analysis item to dump the latest and largest memory block information when OOM occurs.</li><li style="font-size:14px">Supported collecting process device memory curves and whole-device memory curves.</li><li style="font-size:14px">Added documentation for the host memory leak detection feature.</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/920/devaids/msMemScope/docs/en/quick_start/quick_start.md">msMemScope</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">12</td>
      <td style="font-size:14px">Content about AMCT quantization</td>
      <td style="font-size:14px">Added the quantization features and API description for AMCT (acl) use cases.</td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/920/devaids/amct/atlasamct_16_0001.html">Ascend Model Compression Toolkit (AMCT)</a></td>
    </tr>
  </tbody>
</table>

## 9.1.0

<table>
  <colgroup>
    <col style="width: 6%">
    <col style="width: 18%">
    <col style="width: 52%">
    <col style="width: 24%">
  </colgroup>
  <thead>
    <tr>
      <th>Np.</th>
      <th>Update</th>
      <th>Description</th>
      <th>Document</th>
    </tr>
  </thead>
  <tbody style="font-size:14px">
    <tr>
      <td style="font-size:14px">1</td>
      <td style="font-size:14px">Unified documentation</td>
      <td style="font-size:14px">Removed the two separate document sets of "CANN Community Edition" and "CANN Commercial Edition". Consolidated all materials into one unified documentation portal "CANN".</td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/index/index.html">CANN documentation</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">2</td>
      <td style="font-size:14px">Ascend C Operator Development</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">Optimized the "Getting Started" section:<ul><li style="font-size:14px">Updated the Ascend C learning path.</li><li style="font-size:14px">Added a general description of heterogeneous systems and the programming model.</li></ul></li><li style="font-size:14px">Optimized and adjusted the SIMD-related sections in the "Programming Guide", categorizing them by the C API at the language extension layer, tensor-based C++ programming, and Tpipe/TQue-based programming.</li><li style="font-size:14px">Added "Advanced Programming > SuperKernel" and "Advanced Programming > SIMT Cooperative Groups" sections to the "Programming Guide".</li><li style="font-size:14px">Extensively restructured the Ascend C API sections:<ul><li style="font-size:14px">Adjusted the directory structure of data movement APIs and matrix computation APIs: Related APIs are placed adjacent to each other, for example, matrix-computation-related movement APIs are placed under the matrix computation directory.</li><li style="font-size:14px">Organized the API directory structure by use case: for example, matrix computation is divided into matrix computation data move-in, Mmad computation, and matrix computation data move-out.</li><li style="font-size:14px">Added necessary background knowledge, concept and mechanism introductions, general constraints, and key feature descriptions for each API category.</li><li style="font-size:14px">Added constraint descriptions and special parameter value descriptions for each API.</li><li style="font-size:14px">Added an API appendix that summarizes API pipeline types, theoretical performance, and API boundary values.</li></ul></li><li style="font-size:14px">Added tensor API reference. Tensor APIs are experimental and may be adjusted or improved in future releases without guaranteed backward compatibility. You should pay attention to later version updates during use.</li><li style="font-size:14px">Added documentation on the matrix computation overview and computation fractal introduction.</li><li style="font-size:14px">Optimized the vector computation API documentation and supplemented instruction constraints.</li><li style="font-size:14px">Added an overview of performance optimization for SIMD and SIMT hybrid programming.</li><li style="font-size:14px">Built a VitePress documentation site to provide Ascend C documentation preview.</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/programug/Ascendcopdevg/docs/guide/getting_started/Ascend-C_overview_and_learning_path.md">Ascend C Operator Development</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">3</td>
      <td style="font-size:14px">CCU communication operator development section</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">Added the "Programming Model and Concepts > CCU Programming Models and Concepts" section.</li><li style="font-size:14px">Added the "Communication Operator Development > CCU Operator Development" section.</li><li style="font-size:14px">Added the following APIs to the communication operator development APIs:<ul><li style="font-size:14px">"Control Plane APIs" > "CCU Kernel Lifecycle and Memory Token Management"</li><li style="font-size:14px">"Data Plane APIs" > "CCU APIs"</li></ul></li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/commlib/commopdev/docs/en/comm_op_dev_guide/intro.md">Communication Operator Development</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">4</td>
      <td style="font-size:14px">Content about graph development pass and SuperKernel</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">Added "Custom Pass Development" > "Modifying a Graph Using a Custom Pass" > "Implementing Pass Based on Pattern Matching (Python)".</li><li style="font-size:14px">Added "Programming Guide" > "SuperKernel Fusion Scope Marking".</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/programug/graphdevg/atlasag_25_0081.html">Graph Development</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">5</td>
      <td style="font-size:14px">Content about ATC command-line tool</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">"Python APIs" > "Pyatc APIs": Added the ATC command-line tool for Python use cases.</li><li style="font-size:14px">"Basic Data Structures and APIs of Graphs" > "Options" > "ge.tiling_schedule_optimize": Changed the parameter level from "global session" to "all".</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/API/ascendgraphapi/atlasgeapi_07_1058.html">GE APIs</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">6</td>
      <td style="font-size:14px">Operator library documentation</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">Separated the "Operator Library > AI Framework Operator Support List" section from previous versions and added the *AI Framework Operator Support List* manual in the current version.</li><li style="font-size:14px">Added the "Operator Library > Operator API (torch_extension)" section.</li><li style="font-size:14px">Added the "RAS APIs" section to "Operator API (aclnn)".</li><li style="font-size:14px">Added a multi-platform operator migration guide to the ops-cv library to help developers migrate operators from Atlas A2 products to Ascend 950PR&950DT products.</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/API/aolapi/operatorlist_00001.html">Operator Library</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">7</td>
      <td style="font-size:14px">Communication operator support list</td>
      <td style="font-size:14px">"References" > "Communication Operator Support List": Added the "Ascend 950PR/Ascend 950DT" support list.</td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/commlib/hcclug/docs/en/user_guide/hccl_intro.md">Huawei Collective Communication Library (HCCL)</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">8</td>
      <td style="font-size:14px">ATB build and test instructions</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">Added a test framework guide and supplemented the dependency instructions for building and running the test framework.</li><li style="font-size:14px">Supplemented the method for determining the cxx_abi version.</li><li style="font-size:14px">Updated the documentation links to CANN 9.1.0 and PyTorch 26.0.0.</li><li style="font-size:14px">Corrected the ATB_BUILD_DEPENDENCY_PATH and ABI determination instructions, covering README/FAQ/test framework guide.</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/acce/ascendtb/ascendtb_0001.html">ATB Acceleration Library</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">9</td>
      <td style="font-size:14px">ATC framework parameter description</td>
      <td style="font-size:14px">"Parameters" > "framework": Added a note that the Caffe framework is no longer evolving in the current form and model conversion availability is not guaranteed.</td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/devaids/atctool/atlasatc_16_0001.html">Ascend Tensor Compiler (ATC)</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">10</td>
      <td style="font-size:14px">New chapter</td>
      <td style="font-size:14px">Added the "LLM-based Quantization" chapter.</td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/devaids/amct/atlasamct_16_0001.html">Ascend Model Compression Toolkit (AMCT)</a></td>
    </tr>
  </tbody>
</table>

## 9.0.0

<table>
  <colgroup>
    <col style="width: 6%">
    <col style="width: 18%">
    <col style="width: 52%">
    <col style="width: 24%">
  </colgroup>
  <thead>
    <tr>
      <th>No.</th>
      <th>Update</th>
      <th>Description</th>
      <th>Document</th>
    </tr>
  </thead>
  <tbody style="font-size:14px">
    <tr>
      <td style="font-size:14px">1</td>
      <td style="font-size:14px">Quick installation guide</td>
      <td style="font-size:14px">Moved *CANN Quick Start* to "Environment Preparation" and renamed it to *CANN Installation*.</td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/en-sg/cann/download?versionId=731&ids=d806%2Ch0502%2Ch0601%2Ch0702">CANN Installation</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">2</td>
      <td style="font-size:14px">Content about Ascend C SIMT and Reg programming</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">Added SIMD and SIMT introduction, and a quick start chapter based on SIMT programming in "Quick Start".</li><li style="font-size:14px">In "Programming Guide" > "Programming Model", added "AI Core SIMT Programming" and "SIMD and SIMT Hybrid Programming" chapters.</li><li style="font-size:14px">In "Programming Guide" > "Programming Model", added the "AI Core SIMT Programming" chapter.</li><li style="font-size:14px">In "Programming Guide" > "Language Extension Layer", added "SIMT BuiltIn Keywords" and "C APIs at the SIMT Language Extension Layer".</li><li style="font-size:14px">In "Operator Practice References", added "SIMT Operator Implementation" and "SIMD and SIMT Operator Implementation" chapters.</li><li style="font-size:14px">In "Operator Practice References", added the "SIMD and SIMT Operator Performance Optimization" chapter.</li><li style="font-size:14px">In the API reference, added the SIMT APIs chapter.</li><li style="font-size:14px">Added a compatibility migration guide (migrating from 220x architecture to 351x architecture).</li><li style="font-size:14px">Added 90+ Reg programming APIs. Reg vector computation APIs are developed for the RegBase architecture. You can use these APIs to directly operate registers involved in Vector computation on the chips, achieving greater flexibility and better performance.</li><li style="font-size:14px">In the Ascend community, added a visualization section in the "Ascend C Operator Development" that presents the execution process of Cube and Vector operators through videos.</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/900/programug/Ascendcopdevg/atlas_ascendc_map_10_0002.html">Ascend C Operator Development</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">3</td>
      <td style="font-size:14px">Communication Operator Development documentation</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">Separated *Communication Operator Development* from *Huawei Collective Communication Library (HCCL)* and published it as a standalone manual under "Programming Guide".</li><li style="font-size:14px">Added the "AIV Communication Operator Development" chapter.</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/900/programug/commopdev/hcclopdev_000001.html">Communication Operator Development</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">4</td>
      <td style="font-size:14px">Application Development documentation</td>
      <td style="font-size:14px">Adjusted the *Application Development* documentation outline. The first-level directory was adjusted by functional features as follows: <ul><li style="font-size:14px">Promoted the content under the "Runtime Management" chapter by one level.</li><li style="font-size:14px">Supplemented development guidance for more runtime functional features, such as ACL graph, multi-device programming, and inter-process communication.</li><li style="font-size:14px">Moved the API call flow content down into the chapters of specific functional features.</li><li style="font-size:14px">Distinguished built-in operators and custom operators in the content under the single-operator call chapters.</li><li style="font-size:14px">Moved media data processing and feature vector retrieval to the "Dedicated Accelerator" chapter, and added an introduction to random number generation under the "Dedicated Accelerator" chapter.</li><li style="font-size:14px">Split the acl API reference by component into Runtime APIs, GE APIs, DVPP APIs, Feature Vector Retrieval APIs, and API reference.</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/900/programug/acldevg/acldevg_0001.html">Application Development</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">5</td>
      <td style="font-size:14px">Graph development guide and migration guide</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">Outline adjustment: Integrated and restructured the content, and moved development-phase content to the "Programming Guide" chapter.</li><li style="font-size:14px">Merged *AutoFuse User Guide* into the "AutoFuse" chapter of *Graph Development*.</li><li style="font-size:14px">In *Graph Development*, added the "Appendix > Session to GeSession Migration Guide" chapter.</li><li style="font-size:14px">Added the "Programming Guide" > "Integrating a Triton Operator into a Graph" chapter.</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/900/programug/graphdevg/atlasag_25_0081.html">Graph Development</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">6</td>
      <td style="font-size:14px">GE APIs</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">Categorized the API reference by language into C++, Python, and C APIs, where "Python APIs" was newly added.</li><li style="font-size:14px">In "C APIs", added "Model Management and Single-Operator Call APIs", which originated from the acl APIs.</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/900/API/ascendgraphapi/atlasgeapi_07_0001.html">GE APIs</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">7</td>
      <td style="font-size:14px">HCCL Atlas 350 configuration and AIV development</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">In *Huawei Collective Communication Library (HCCL)*, under "References > Cluster Configuration", added a new chapter "Rank Table Configuration (Atlas 350 Accelerator Card)".</li><li style="font-size:14px">In *Huawei Collective Communication Library (HCCL)*, under "Communication Operator Development", added a new chapter "AIV Operator Development".</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/900/API/hcclug/hcclug_000001.html">Huawei Collective Communication Library (HCCL)</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">8</td>
      <td style="font-size:14px">Manual name</td>
      <td style="font-size:14px">Renamed *Memory Leak Detection Tool (msLeaks)* to *Memory Profiler*.</td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/en/CANNCommunityEdition/900/devaids/msMemScope/docs/en/quick_start.md">Memory Profiler</a></td>
    </tr>
  </tbody>
</table>
