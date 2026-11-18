# What's New

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T10:02:43.418Z pushedAt=2026-11-16T03:10:48.324Z nl=2 -->

This section describes the latest changes to the CANN documentation.

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
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/en/cann/download?versionId=734&ids=d806%2Ch0501%2Ch0601%2Ch0702&currentTab=0">CANN Installation</a></td>
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
