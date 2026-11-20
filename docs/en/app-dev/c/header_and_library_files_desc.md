# Header Files and Library Files

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:12:35.055Z pushedAt=2026-10-22T02:51:13.339Z nl=2 -->

The CANN application development scenarios involve APIs provided by components such as Runtime, Graph Engine (GE), and Digital Vision Pre-Processing (DVPP). For the APIs provided by each component and their detailed descriptions, see the API reference of each component. This section only describes the API categories and the header files and library files that the APIs depend on when being called.

## API Categories

API names use **acl** as the prefix, and the naming style is: acl+_*API category abbreviation*_+\*, where \* usually indicates the operation verb and object, both using initial capitalization. For ease of description, all APIs in this document are collectively referred to as acl APIs.

In acl APIs, the parameter order generally follows the principle that input parameters come first and output parameters come last. Note that you should not arbitrarily append a newly added parameter to the end of an API. Instead, place a new input-only parameter before the output parameters. For parameters that serve as both input and output, the situation is relatively complex, and consistency with other APIs may also need to be considered, requiring flexible handling.

**Table 1** API categories

| API Name Prefix | Description | Component |
| --- | --- | --- |
| acl | System configuration APIs | Runtime |
| aclrt | Runtime management APIs | Runtime |
| aclop | Single-operator model execution APIs | Runtime |
| aclblas | BLAS APIs | Graph Engine |
| aclmdl | Model inference APIs | Graph Engine |
| acldvpp, aclvdec, or aclvenc | Media data processing APIs<br>Among them, the API naming under Media Data Processing V2 is an exception. These APIs are named with the **hi_mpi** prefix. | DVPP (Digital Vision Pre-Processing) |
| aclprof | Profiling configuration APIs | Runtime |
| acltdt | Data transfer APIs | Runtime |
| aclfv | Feature vector search APIs | Feature Vector |

Due to differences in software and hardware, the API categories supported by each product model vary. For details, see the description of each API.

## Header Files and Library Files Required for API Call

After the firmware, driver, and CANN software packages are installed, you can reference the acl API header files and library files when compiling and running an application.

The acl API header files are under the **$\{INSTALL\_DIR\}/include/** directory, and the library files are under the **$\{INSTALL\_DIR\}/lib64/** directory. Replace **$\{INSTALL\_DIR\}** with the file storage path after the CANN software is installed. For example, when it is installed by the **root** user, the default file storage path is **/usr/local/Ascend/cann**.

You need to include the required files based on the acl APIs you actually use. The purpose of each header file is described in the following table.

>**Note:** 
>When compiling an acl API program, include the library files corresponding to the included header files. If redundant library files (for example, **libascendcl.a**) are referenced, version function exceptions or compatibility issues may occur during later version upgrades.

**Table 2** Runtime header files and library files

| Header File | Purpose | Corresponding Library File |
| --- | --- | --- |
| acl/acl_rt.h | Used to define APIs for initialization/deinitialization, device management, context management, stream management, synchronization waiting, and memory management. | libacl_rt.so<br>Note: For compatibility with older versions, older versions support the use of **libascendcl.so**, but this method will be deprecated in later versions. It is recommended to use **libacl_rt.so** to prevent future version compatibility issues. |
| acl/acl_dump.h | Used to define the model and operator dump APIs. | libascend_dump.so |
| acl/acl_prof.h | Used to define the Profiling data collection APIs. | libmsprofiler.so<br>Note: For compatibility with older versions, older versions support the use of **libascendcl.so**, but in later versions this method will be deprecated. It is recommended to use **libmsprofiler.so** to prevent future version compatibility issues. |
| acl/acl_tdt.h | Used to define the tensor data transfer APIs. | libacl_tdt_channel.so |
| acl/acl_tdt_queue.h | Used to define the shared queue management and shared buffer management APIs. | libacl_tdt_queue.so |
| acl/acl_rt_api.h | Used to define C++ extension APIs, providing function overloading and template encapsulation (applicable only to C++ programs).<br>Depends on **acl_rt.h**. | libacl_rt.so |

**Table 3** Graph Engine component header files and library files

| Header File | Purpose | Corresponding Library File |
| --- | --- | --- |
| acl/acl_mdl.h | Used to define model management APIs. | libacl_mdl.so<br>Note: For compatibility with older versions, older versions support the use of **libascendcl.so**, but in later versions this method will be deprecated. It is recommended to use **libacl_mdl.so** to prevent future version compatibility issues. |
| acl/acl_op.h<br>acl/acl_op_compiler.h | Used to define single-operator call APIs (including only single-operator model execution APIs). | libacl_op_executor.so<br>libacl_op_compiler.so<br>Note: For compatibility with older versions, older versions support the use of **libascendcl.so**, but in later versions this method will be deprecated. It is recommended to use **libacl_op_executor.so** and **libacl_op_compiler.so** to prevent future version compatibility issues. |
| acl/ops/acl_cblas.h | Used to define CBLAS APIs. | libacl_cblas.so |

**Table 4** DVPP component header files and library files

| Category | Header File | Purpose | Corresponding Library File |
| --- | --- | --- | --- |
| Media data processing operator | Under the **acldvppop** directory:<br>acldvpp_base.h<br>acldvpp_op_api.h | Used to define the functional APIs of DVPP media data processing operators. | libacl_dvpp_op.so |
| Media data processing operator | Under the **aclnn** directory:<br>acl_meta.h<br>aclnn_base.h | Common Meta APIs that the operator APIs depend on when called, such as creating **aclTensor**, **aclScalar**, and **aclIntArray**. | libnnopbase.so |
| Media data processing V2 | acl/dvpp/hi_dvpp.h | Used to define the DVPP APIs in Media Data Processing V2. | libacl_dvpp_mpi.so |
| Media data processing V2 | Under the **acl/media** directory:<br>hi_mpi_vi.h<br>hi_common_vi.h<br>hi_common_dis.h<br>hi_common_gdc.h<br>hi_media_common.h<br>hi_media_type.h<br>hi_mpi_sys.h | Used to define the APIs for Video Input (VI) video data obtaining. | libacl_vi_mpi.so<br>libacl_dvpp_mpi.so |
| Media data processing V2 | Under the **acl/media** directory:<br>hi_mpi_isp.h<br>hi_common_isp.h<br>hi_common_3a.h<br>hi_mpi_ae.h<br>hi_common_ae.h<br>hi_mpi_awb.h<br>hi_common_awb.h<br>hi_common_sns.h<br>hi_media_common.h<br>hi_media_type.h<br>hi_mpi_sys.h | Used to define the APIs for Image Signal Processing (ISP) system control. | libacl_isp_ae_mpi.so<br>libacl_isp_awb_mpi.so<br>libacl_isp_mpi.so<br>libacl_dvpp_mpi.so |
| Media data processing V2 | Under the **acl/media** directory:<br>hi_mpi_vpss.h<br>hi_media_common.h<br>hi_media_type.h<br>hi_mpi_sys.h | Used to define the APIs for Video Process Sub-System (VPSS) image processing. | libacl_vpss_mpi.so<br>libacl_dvpp_mpi.so |
| Media data processing V2 | acl/media/hi_mipi_rx.h | Used to define MIPI Rx ioctl command words. | - |
| Media data processing V2 | Under the **acl/media** directory:<br>hi_mpi_audio.h<br>hi_common_aio.h | Used to define the APIs for audio input and audio output. | libacl_audio_mpi.so |
| Media data processing V2 | acl/media/hi_acodec.h | Used to define the command words for volume adjustment. | - |
| Media data processing V2 | Under the **acl/media** directory:<br>hi_common_vo.h<br>hi_mpi_vo.h | Used to define the video output APIs. | libacl_vo_mpi.so |
| Media data processing V2 | acl/media/hi_mpi_hdmi.h | Used to define the HDMI APIs for connecting to peripherals. | libacl_hdmi_mpi.so |
| Media data processing V2 | acl/media/hi_mpi_tde.h | Used to define the TDE graphics drawing APIs. | libacl_tde_mpi.so |
| Media data processing V2 | acl/media/hifb.h | Used to define the overlay graphics layer management APIs. | - |
| Media data processing V1 | acl/ops/acl_dvpp.h | Used to define the APIs of media data processing V1. | libacl_dvpp.so |

**Table 5** Feature vector search header files and library files

| Header File | Purpose | Corresponding Library File |
| --- | --- | --- |
| acl/ops/acl_fv.h | Used to define the APIs for feature vector search. | libacl_retr.so |
