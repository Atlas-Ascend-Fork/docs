# 最新动态

本文介绍了CANN文档的最新上线新增、变更动态，欢迎体验。

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
      <th>序号</th>
      <th>更新点</th>
      <th>更新说明</th>
      <th>相关文档</th>
    </tr>
  </thead>
  <tbody style="font-size:14px">
    <tr>
      <td style="font-size:14px">1</td>
      <td style="font-size:14px">调整快速安装文档位置</td>
      <td style="font-size:14px">《CANN 快速开始》调整至“环境准备”节点下，并变更为《CANN 快速安装》。</td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/cann/download?versionId=734&ids=d806%2Ch0501%2Ch0601%2Ch0702&currentTab=0">CANN 快速安装</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">2</td>
      <td style="font-size:14px">新增Ascend C SIMT与Reg编程能力内容</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">快速入门新增SIMD、SIMT简介，新增基于SIMT编程的快速入门章节。</li><li style="font-size:14px">编程指南中编程模型新增“AI Core SIMT编程”、“SIMD与SIMT混合编程”章节。</li><li style="font-size:14px">编程指南中编译与运行新增“AI Core SIMT编译”章节。</li><li style="font-size:14px">编程指南中语言扩展层新增SIMT BuiltIn关键字、SIMT语言扩展层C API。</li><li style="font-size:14px">算子实践参考中新增SIMT算子实现、SIMD与SIMT混合算子实现章节。</li><li style="font-size:14px">算子实践参考中新增“SIMD与SIMT混合算子性能优化”章节。</li><li style="font-size:14px">API参考中新增SIMT API章节。</li><li style="font-size:14px">新增兼容性迁移指南（220x架构版本迁移到351x架构版本）。</li><li style="font-size:14px">新增90+ Reg编程接口API，Reg矢量计算API是面向RegBase架构开发的API，用户可通过该API直接对芯片中涉及Vector计算的寄存器进行操作，实现更大的灵活性和更好的性能。</li><li style="font-size:14px">昇腾社区中，Ascend C算子开发新增可视化专区，通过视频呈现Cube和Vector算子的执行过程。</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/programug/Ascendcopdevg/atlas_ascendc_map_10_0002.html">Ascend C算子开发</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">3</td>
      <td style="font-size:14px">独立发布通信算子开发文档</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">《通信算子开发》从《HCCL集合通信库》中独立出来，作为单本手册发布至“编程指南”节点下。</li><li style="font-size:14px">新增“AIV通信算子开发”章节。</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/programug/commopdev/hcclopdev_000001.html">通信算子开发</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">4</td>
      <td style="font-size:14px">重构应用开发文档章节</td>
      <td style="font-size:14px">《应用开发》文档大纲调整，按功能特性调整一级目录，调整点如下：<ul><li style="font-size:14px">将“运行时管理”章节下的内容提升一个级别。</li><li style="font-size:14px">增补Runtime更多功能特性的开发指导，例如ACL Graph、多设备编程、进程间通信等。</li><li style="font-size:14px">将接口调用流程的内容下沉到各个具体功能特性的章节中。</li><li style="font-size:14px">单算子调用章节下的内容区分内置算子、自定义算子。</li><li style="font-size:14px">媒体数据处理、特征向量检索功能变更至“专用加速器”章节，同时在“专用加速器”章节下增加随机数生成功能的介绍。</li><li style="font-size:14px">acl API参考按组件拆分，分成Runtime API、GE API、DVPP API、特征向量检索API、API参考。</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/programug/acldevg/acldevg_0001.html">应用开发</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">5</td>
      <td style="font-size:14px">重构图开发并新增迁移指导</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">手册大纲调整：内容进行整合与重构，开发态内容移入“编程指南”章节。</li><li style="font-size:14px">《AutoFuse自动融合用户手册》合并到《图开发》的“自动融合”章节。</li><li style="font-size:14px">《图开发》新增“附录>Session到GeSession的迁移指导”章节。</li><li style="font-size:14px">新增“编程指南>Triton入图”章节。</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/programug/graphdevg/atlasag_25_0081.html">图开发</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">6</td>
      <td style="font-size:14px">按语言分类重构GE接口内容</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">接口参考按照语言进行分类，分为C++语言、Python语言、C语言接口，其中Python语言接口为新增接口。</li><li style="font-size:14px">C语言接口新增“模型管理和单算子调用接口”，该部分内容来自原有的acl接口。</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/API/ascendgraphapi/atlasgeapi_07_0001.html">GE图引擎API</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">7</td>
      <td style="font-size:14px">新增HCCL Atlas 350配置与AIV开发内容</td>
      <td style="font-size:14px"><ul><li style="font-size:14px">《HCCL集合通信库》的“相关参考>集群信息配置”章节下，新增“rank table配置资源信息（Atlas 350 加速卡）”章节。</li><li style="font-size:14px">《HCCL集合通信库》的“通信算子开发”章节下，新增“AIV算子开发”章节。</li></ul></td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/API/hcclug/hcclug_000001.html">HCCL集合通信库</a></td>
    </tr>
    <tr>
      <td style="font-size:14px">8</td>
      <td style="font-size:14px">手册名称变更</td>
      <td style="font-size:14px">《msLeaks内存泄漏检测工具》命名变更为《内存分析工具》。</td>
      <td style="white-space: nowrap; font-size:14px"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/devaids/msMemScope/docs/zh/quick_start.md">内存分析工具</a></td>
    </tr>
  </tbody>
</table>
