# 头文件和库文件说明

在AI算子、算法和应用开发方面，CANN向用户开放编程接口，并提供配套的文档说明，这些接口统称为开放接口。开放接口的兼容性将在CANN软件版本演进中得到保障，如有废弃或影响用户的变更，将在版本说明中提前预告。通常，这些接口放置在安装环境的include目录下。

>[!NOTE]说明
>与许多大型软件平台相似，CANN包含多个相互协作的部件，以实现其完整功能。CANN抽象出一组接口用于系统内部交互，定义为非SDK接口，这些接口通常位于CANN开源项目代码仓的pkg\_inc目录下，其内容更改不会发布预告或记录。对于参与CANN开源软件贡献的开发者，可以按需参考相关开源代码，了解这些接口的功能。对于AI算子、算法和应用开发者，无需依赖此类接口即可完成开发任务；如认为某些非SDK接口对于AI算子、算法和应用的开发不可或缺，可以在[CANN开源社区](https://gitcode.com/cann)相应的项目中创建issue，请求新增开放接口，由该开源项目评估需求和方案的合理性。

各组件详细的头文件和库文件列表如下。

-   [Ascend C](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/API/ascendcopapi/docs/api/api_list.md)
-   [Runtime运行时](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/API/runtimeapi/aclcppdevg_03_1952.html)
-   GE图引擎
    -   [图开发](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/API/ascendgraphapi/docs/zh/api/graph_engine_api/header_and_library_files_description.md)
    -   [DataFlow](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/others/dataflowdevg/docs/zh/user_guides/dflow/dflow_api/cpp/dflow_header_files_and_library_files.md)
    -   [UDF](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/others/dataflowdevg/docs/zh/user_guides/dflow/dflow_api/cpp/udf_header_files_and_library_files.md)
    -   [LLM-DataDist](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/others/llmdatadistdev/docs/zh/user_guides/llm_datadist/llm_datadist_api/cpp/header_files_and_library_files.md)

-   [算子库](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/API/aolapi/docs/zh/ops-lib/header_and_library.md)
-   通信库
    -   [HCCL](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/commlib/hcclug/docs/zh/api_ref/hccl_header_and_lib.md)
    -   [HCOMM](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/commlib/hcclug/docs/zh/api_ref/hcomm_header_and_lib.md)
    -   [HIXL](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/commlib/hixlug/docs/zh/api/cpp/header_files_and_library_files.md)

-   [ATB加速库](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/acce/ascendtb/ascendtb_01_0005.html)
-   [SiP加速库](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/acce/SiP/docs/header_files_library_files.md)
-   [DVPP媒体库](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/acce/dvpp/dvpp_03_0001.html)
-   [PTO-ISA](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/920/compiler/ptoisa/docs/PTO-ISA-Header-and-Library-Description_zh.md)
