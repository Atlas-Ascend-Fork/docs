# Header Files and Library Files<a name="EN-US_TOPIC_0000002773075391"></a>

CANN offers open APIs and documentation for AI operators, algorithms, and applications. These APIs are called open APIs. CANN guarantees their compatibility as the software evolves. Any deprecated APIs or user-impacting changes will be announced in the Release Notes. Typically, these APIs are found in the  **include**  directory of the installation environment.

>[!NOTE]NOTE
>CANN, like many large software platforms, has multiple parts that work together. It uses a set of internal APIs, called non-SDK APIs, for system interactions. These APIs are found in the  **pkg\_inc**  directory of the CANN open source code. Any changes to them are not announced or recorded. Developers contributing to CANN can look at the open source code to learn about these APIs. However, AI operator, algorithm, and app developers do not need these APIs to complete their tasks. If certain non-SDK APIs are deemed essential for your AI projects, you can request new open APIs by creating an issue in the  [CANN community](https://gitcode.com/cann). The project team will review your request and evaluate the feasibility.

The following table lists the header files and library files of each component.

-   [Ascend C](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/API/ascendcopapi/docs/api/api_list.md)
-   [Runtime](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/API/runtimeapi/aclcppdevg_03_1952.html)
-   Graph Engine GE
    -   [Graph development](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/API/ascendgraphapi/atlasgeapi_07_1058.html)
    -   [DataFlow](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/others/dataflowdevg/dfrefc_23_0001.html)
    -   [UDF](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/others/dataflowdevg/udfrefc_23_00001.html)
    -   [LLM-DataDist](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/others/llmdatadistdev/llmcrv1_42_02.html)

-   [Operator libraries](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/API/aolapi/operatorlist_00533.html)
-   Communication libraries
    -   [HCCL](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/commlib/hcclug/docs/zh/api_ref/hccl_header_and_lib.md)
    -   [HCOMM](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/commlib/hcclug/docs/zh/api_ref/header_and_lib.md)
    -   [HIXL](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/commlib/hixlug/llmcrv2_42_03.html)

-   [Ascend Transformer Boost ATB](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/acce/ascendtb/ascendtb_01_0005.html)
-   [Signal Processing Boost SiP](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/acce/SiP/docs/header_files_library_files.md)
-   [DVPP Media Library](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/acce/dvpp/dvpp_03_0001.html)
-   [PTO-ISA](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/910/compiler/ptoisa/docs/PTO-ISA-Header-and-Library-Description.md)
