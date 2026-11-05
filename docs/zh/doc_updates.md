# 最新动态

本文介绍了CANN文档的最新上线新增、变更动态，欢迎体验。

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
      <th>序号</th>
      <th>更新点</th>
      <th>更新说明</th>
      <th>相关文档</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>修改昇腾产品形态说明相关内容</td>
      <td>优化“产品系列”名称，新增NPU_ARCH、soc_series、soc_version参数说明内容。</td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/Glossary/productform/hardwaredesc_0001.html">昇腾产品形态说明</a></td>
    </tr>
    <tr>
      <td>2</td>
      <td>新增章节</td>
      <td><ul><li>补充L2 Cache切分优化说明。</li><li>新增NPU架构版本3510新特性使用说明。</li><li>“Aclnn算子工程化开发”章节进行优化调整，增加推荐阅读路径、快速入门等内容。</li><li>新增“高级编程 > 内存模型”章节，介绍缓存一致性和内存一致性的概念、原理、常见问题和解决方案等内容。</li><li>新增“基于Tensor的C++编程”章节。</li><li>新增“原子操作指令优化”章节。</li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/programug/Ascendcopdevg/asc-devkit/docs/zh/guide/getting_started/ascend_c_overview_and_learning_path.md">Ascend C算子开发</a></td>
    </tr>
    <tr>
      <td>3</td>
      <td>新增章节</td>
      <td>新增支持PyPTO Pro开发模式，支持面向Tile操作的Tile编程模型。</td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/programug/pyptoopdevg/docs/zh/guide/introduction.md">PyPTO算子开发</a></td>
    </tr>
    <tr>
      <td>4</td>
      <td>文档大纲调整、新增章节</td>
      <td><ul><li>“自定义算子入图”章节进行特性调整和目录结构调整。</li><li>优化“AutoFuse自动融合”章节：<ul><li>调整目录结构，新增“快速入门”、“启用AutoFuse”章节，环境变量的详细说明移至“附录”章节。</li><li>“启用AutoFuse”章节分两条路径分别介绍自动融合的开启模式，新增Inductor路径下的融合开启方式。</li></ul></li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/programug/graphdevg/docs/zh/user_guides/graph_dev/overview/GE_definition.md">图开发</a></td>
    </tr>
    <tr>
      <td>5</td>
      <td>新增文档</td>
      <td>新增《PTOAS》文档。</td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/compiler/ptoas/overview/what_is_ptoas.md">PTOAS</a></td>
    </tr>
    <tr>
      <td>6</td>
      <td>优化章节</td>
      <td>优化三个故障案例：“建链超时”、“notify_wait超时”和“通信域初始化topo探测超时”章节。</td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/commlib/hcclug/docs/zh/user_guide/hccl_intro.md">HCCL集合通信库</a></td>
    </tr>
    <tr>
      <td>7</td>
      <td>文档大纲调整、新增章节</td>
      <td><ul><li>“C API”章节重构Ascend 950PR&950DT系列产品资料，细化目录结构和优化资料内部结构，完善接口功能说明、调用示例和约束说明。</li><li>“Tensor API”章节完善cube_compute_load/store、layout_structure、data_move、tensor_structure等资料。</li><li>优化“SIMT API”章节：<ul><li>补充UB复用排布规则说明。</li><li>数学库接口更新精度说明。</li><li>协作组增加grid_group、thread_group说明。</li><li>新增“SIMT指令理论性能汇总”章节。</li><li>新增整型转换函数。</li><li>新增SIMT编程场景使用的编译选项。</li></ul></li><li>新增“CheckOpResSufficient”章节。</li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/API/ascendcopapi/docs/zh/api/api_list.md">Ascend C API</a></td>
    </tr>
    <tr>
      <td>8</td>
      <td>新增章节</td>
      <td>新增PyPTO Pro API章节。</td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/API/pyptoapi/docs/zh/api/tensor_api/tensor/pypto-Tensor_introduction.md">PyPTO API</a></td>
    </tr>
    <tr>
      <td>9</td>
      <td>新增章节</td>
      <td>《算子库》手册“算子库 > 算子接口（torch_extension）”新增“NN类接口”章节。</td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/API/aolapi/docs/zh/ops-lib/introduction.md">算子库API</a></td>
    </tr>
    <tr>
      <td>10</td>
      <td>文档大纲调整、新增章节</td>
      <td><ul><li>目录结构调整，以采集工具为粒度平铺章节。</li><li>Ascend PyTorch调优工具、MindSpore调优工具、使用TensorFlow框架接口采集性能数据、使用acl Python接口采集性能数据章节调整至各自源文档发布，《性能调优工具》手册在简介中保留跳转链接。</li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/devaids/Profiling/docs/zh/profiling/overview.md">性能调优工具</a></td>
    </tr>
    <tr>
      <td>11</td>
      <td>新增章节</td>
      <td><ul><li>新增显存OOM分析项，发生OOM时dump最新和最大内存块信息。</li><li>支持采集进程显存曲线和整卡显存曲线。</li><li>新增Host内存泄漏检测功能资料。</li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/devaids/msMemScope/docs/zh/quick_start/quick_start.md">内存分析工具</a></td>
    </tr>
    <tr>
      <td>12</td>
      <td>新增章节</td>
      <td>新增AMCT（acl）场景下的量化特性以及接口说明。</td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/latest/devaids/amct/atlasamct_16_0001.html">AMCT模型压缩工具</a></td>
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
      <th>序号</th>
      <th>更新点</th>
      <th>更新说明</th>
      <th>相关文档</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>CANN社区版和CANN商用版文档归一</td>
      <td>取消原“CANN社区版”和“CANN商用版”两个独立文档入口，全部资料归集至统一文档入口“CANN”。</td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/index/index.html">CANN文档</a></td>
    </tr>
    <tr>
      <td>2</td>
      <td>文档大纲调整、新增章节</td>
      <td><ul><li>优化“入门教程”章节：<ul><li>更新Ascend C学习路径。</li><li>新增异构系统和编程模型概括性描述。</li></ul></li><li>“编程指南”中SIMD编程模型章节进行优化调整，按照基于语言扩展层C API、基于Tensor的C++编程、基于Tpipe和TQue编程的维度进行分类。</li><li>“编程指南”新增高级编程 > SuperKernel、高级编程 > SIMT协作组章节。</li><li>对《Ascend C API》进行了大规模重构，变更点如下：<ul><li>对数据搬运API和矩阵计算API等进行了目录结构调整：相关性强的API放置在邻近位置，比如将矩阵计算相关的搬运接口放置在矩阵计算目录下。</li><li>按照场景进行API的目录结构组织：比如矩阵计算分为矩阵计算的搬入、Mmad计算、矩阵计算的搬出。</li><li>针对一类API增加必要的背景知识、概念原理介绍、通用的约束、关键特性等说明。</li><li>针对每一个API补充约束说明、参数特殊值相关说明。</li><li>新增API附录，附录中包含API流水类型汇总、理论性能汇总、接口边界值汇总等。</li></ul></li><li>新增Tensor API参考文档。Tensor API接口为试验接口，在后续版本中可能会调整或改进，不保证后续兼容性。请开发者在使用过程中关注后续版本更新。</li><li>新增矩阵计算概述和计算分形介绍的文档。</li><li>优化矢量计算API文档，补充指令约束等。</li><li>增加SIMD与SIMT混合编程性能优化概述。</li><li>搭建VitePress文档站点，提供AscendC资料预览功能。</li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/programug/Ascendcopdevg/docs/guide/%E5%85%A5%E9%97%A8%E6%95%99%E7%A8%8B/Ascend-C%E6%A6%82%E8%BF%B0%E4%B8%8E%E5%AD%A6%E4%B9%A0%E8%B7%AF%E5%BE%84.md">Ascend C算子开发</a></td>
    </tr>
    <tr>
      <td>3</td>
      <td>新增章节</td>
      <td><ul><li>新增“编程模型与概念 > CCU编程模型与概念”章节。</li><li>新增“通信算子开发 > CCU算子开发”章节。</li><li>通信算子开发API新增以下接口：<ul><li>控制面接口 > CCU Kernel生命周期与内存Token管理。</li><li>数据面接口 > CCU接口。</li></ul></li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/commlib/commopdev/docs/zh/comm_op_dev_guide/intro.md">通信算子开发</a></td>
    </tr>
    <tr>
      <td>4</td>
      <td>新增章节</td>
      <td><ul><li>自定义Pass开发 > 使用自定义Pass修改Graph > 基于Pattern匹配实现Pass（Python）。</li><li>编程指南 > SuperKernel融合范围标定。</li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/programug/graphdevg/atlasag_25_0081.html">图开发</a></td>
    </tr>
    <tr>
      <td>5</td>
      <td>文档大纲调整、新增章节</td>
      <td><ul><li>接口参考 > Python语言接口 > pyatc接口：新增Python场景的atc命令行工具。</li><li>图基础数据结构和接口 > options参数名说明 > ge.tiling_schedule_optimize：修改该参数级别，由原来global session级修改为all所有级别。</li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/API/ascendgraphapi/atlasgeapi_07_1058.html">GE图引擎 API</a></td>
    </tr>
    <tr>
      <td>6</td>
      <td>文档大纲调整、新增章节</td>
      <td><ul><li>将历史版本中“算子库 > AI框架算子支持清单”章节独立出来，在当前版本新增《AI框架算子支持清单》手册。</li><li>新增“算子库 > 算子接口（torch_extension）”章节。</li><li>“算子接口（aclnn）”新增RAS类接口章节。</li><li>ops-cv库新增算子多平台迁移指南文档，指导开发者将算子从Atlas A2系列产品迁移至Ascend 950PR&950DT系列产品。</li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/API/aolapi/operatorlist_00001.html">算子库API</a></td>
    </tr>
    <tr>
      <td>7</td>
      <td>新增章节</td>
      <td>相关参考 > 通信算子支持度清单：新增“Ascend 950PR&950DT系列产品”支持度清单。</td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/commlib/hcclug/docs/zh/user_guide/hccl_intro.md">HCCL集合通信库</a></td>
    </tr>
    <tr>
      <td>8</td>
      <td>新增章节</td>
      <td><ul><li>新增测试框架指南，补充testframework编译运行依赖使用说明。</li><li>补充cxx_abi版本判断方法说明。</li><li>更新文档链接至CANN 9.1.0和PyTorch 26.0.0。</li><li>修正ATB_BUILD_DEPENDENCY_PATH及ABI判断说明，覆盖README/FAQ/测试框架指南。</li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/acce/ascendtb/ascendtb_0001.html">ATB加速库</a></td>
    </tr>
    <tr>
      <td>9</td>
      <td>优化参数说明</td>
      <td>参数说明--framework：补充说明Caffe框架在当前形态已不再演进，转模型不保证可用性的说明。</td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/devaids/atctool/atlasatc_16_0001.html">ATC离线模型编译工具</a></td>
    </tr>
    <tr>
      <td>10</td>
      <td>新增章节</td>
      <td>新增“基于LLM的量化”章节。</td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/910/devaids/amct/atlasamct_16_0001.html">AMCT模型压缩工具</a></td>
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
      <th>序号</th>
      <th>更新点</th>
      <th>更新说明</th>
      <th>相关文档</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>文档目录调整</td>
      <td>《CANN 快速开始》调整至“环境准备”节点下，并变更为《CANN 快速安装》。</td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/cann/download?versionId=734&ids=d806%2Ch0501%2Ch0601%2Ch0702&currentTab=0">CANN 快速安装</a></td>
    </tr>
    <tr>
      <td>2</td>
      <td>新增章节</td>
      <td><ul><li>快速入门新增SIMD、SIMT简介，新增基于SIMT编程的快速入门章节。</li><li>编程指南中编程模型新增“AI Core SIMT编程”、“SIMD与SIMT混合编程”章节。</li><li>编程指南中编译与运行新增“AI Core SIMT编译”章节。</li><li>编程指南中语言扩展层新增SIMT BuiltIn关键字、SIMT语言扩展层C API。</li><li>算子实践参考中新增SIMT算子实现、SIMD与SIMT混合算子实现章节。</li><li>算子实践参考中新增“SIMD与SIMT混合算子性能优化”章节。</li><li>API参考中新增SIMT API章节。</li><li>新增兼容性迁移指南（220x架构版本迁移到351x架构版本）。</li><li>新增90+ Reg编程接口API，Reg矢量计算API是面向RegBase架构开发的API，用户可通过该API直接对芯片中涉及Vector计算的寄存器进行操作，实现更大的灵活性和更好的性能。</li><li>昇腾社区中，Ascend C算子开发新增可视化专区，通过视频呈现Cube和Vector算子的执行过程。</li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/programug/Ascendcopdevg/atlas_ascendc_map_10_0002.html">Ascend C算子开发</a></td>
    </tr>
    <tr>
      <td>3</td>
      <td>文档大纲调整、新增章节</td>
      <td><ul><li>《通信算子开发》从《HCCL集合通信库》中独立出来，作为单本手册发布至“编程指南”节点下。</li><li>新增“AIV通信算子开发”章节。</li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/programug/commopdev/hcclopdev_000001.html">通信算子开发</a></td>
    </tr>
    <tr>
      <td>4</td>
      <td>文档大纲调整</td>
      <td>《应用开发》文档大纲调整，按功能特性调整一级目录，调整点如下：<ul><li>将“运行时管理”章节下的内容提升一个级别。</li><li>增补Runtime更多功能特性的开发指导，例如ACL Graph、多设备编程、进程间通信等。</li><li>将接口调用流程的内容下沉到各个具体功能特性的章节中。</li><li>单算子调用章节下的内容区分内置算子、自定义算子。</li><li>媒体数据处理、特征向量检索功能变更至“专用加速器”章节，同时在“专用加速器”章节下增加随机数生成功能的介绍。</li><li>acl API参考按组件拆分，分成Runtime API、GE API、DVPP API、特征向量检索API、API参考。</li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/programug/acldevg/acldevg_0001.html">应用开发</a></td>
    </tr>
    <tr>
      <td>5</td>
      <td>文档大纲调整、新增章节</td>
      <td><ul><li>手册大纲调整：内容进行整合与重构，开发态内容移入“编程指南”章节。</li><li>《AutoFuse自动融合用户手册》合并到《图开发》的“自动融合”章节。</li><li>《图开发》新增“附录>Session到GeSession的迁移指导”章节。</li><li>新增“编程指南>Triton入图”章节。</li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/programug/graphdevg/atlasag_25_0081.html">图开发</a></td>
    </tr>
    <tr>
      <td>6</td>
      <td>文档大纲调整、新增章节</td>
      <td><ul><li>接口参考按照语言进行分类，分为C++语言、Python语言、C语言接口，其中Python语言接口为新增接口。</li><li>C语言接口新增“模型管理和单算子调用接口”，该部分内容来自原有的acl接口。</li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/API/ascendgraphapi/atlasgeapi_07_0001.html">GE图引擎API</a></td>
    </tr>
    <tr>
      <td>7</td>
      <td>新增章节</td>
      <td><ul><li>《HCCL集合通信库》的“相关参考>集群信息配置”章节下，新增“rank table配置资源信息（Atlas 350 加速卡）”章节。</li><li>《HCCL集合通信库》的“通信算子开发”章节下，新增“AIV算子开发”章节。</li></ul></td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/API/hcclug/hcclug_000001.html">HCCL集合通信库</a></td>
    </tr>
    <tr>
      <td>8</td>
      <td>手册名称变更</td>
      <td>《msLeaks内存泄漏检测工具》命名变更为《内存分析工具》。</td>
      <td style="white-space: nowrap"><a href="https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/900/devaids/msMemScope/docs/zh/quick_start.md">内存分析工具</a></td>
    </tr>
  </tbody>
</table>
