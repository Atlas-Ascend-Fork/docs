# Video Decoding, Processing, and Display in NVR Scenarios

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:40:24.999Z pushedAt=2026-10-26T03:10:39.441Z nl=2 -->

This section describes the typical process, key APIs, and precautions of NVR video service processing.

Network Video Recorder (NVR) is the storage and forwarding component of a network video system. NVR works with network cameras to record, store, and forward audio and video. In addition, NVR provides a local human-machine interaction API, video decoding, video display, and voice intercom functions.

## NVR Video Scenario Description

**This section describes the NVR video service processing flow, including the following two types:**

1. **[Video decoding display process](#section4761182923310)**

    The video decoding display process involves the video decoding module \(VDEC\), video processing module \(VPSS\), video output module \(VO\), and HDMI module, as well as enhanced functions such as the [Region Management](NVR_video_decoding_processing_displaying.md#section13836172315012), [TDE Graph Drawing](NVR_video_decoding_processing_displaying.md#section107971821203), and [HIFB Overlay Graph Layer Management](NVR_video_decoding_processing_displaying.md#section53701215202019) functions.

    In this process, the **hi\_mpi\_sys\_bind** API is called to bind the VDEC channel to the VPSS group and bind the VPSS group to the VO device, enabling automatic data transmission from VDEC to VPSS and from VPSS to VO. Through the underlying registers, the VO automatically reads the output data of HIFB.

    If TDE, HIFB, and VO are not in the same application process, ensure that the process where VO resides is started first, and the processes where TDE and HIFB reside must also call the **hi\_mpi\_sys\_init** API to initialize the media data processing system and call the **hi\_mpi\_sys\_exit** API to deinitialize the media data processing system before the process exits.

2. **[Video decoding intelligent analysis process](#section14704382225)**

    The video decoding intelligent analysis process involves the video decoding module \(VDEC\), video processing module \(VPSS\), and intelligent analysis (model inference), as well as enhanced functions such as the region management module. For the API call process of the region management function, see [Region Management](NVR_video_decoding_processing_displaying.md#section13836172315012).

![](figures/video_intelligent_analysis_process.png)

<a id="section4761182923310"></a>

## Video Decoding Display Process

The video decoding display process involves the video decoding module \(VDEC\), video processing module \(VPSS\), video output module \(VO\), and HDMI module, as well as enhanced functions such as the [region management function](#section13836172315012), [TDE graph drawing function](#section107971821203), and [HIFB overlay graph layer management function](#section53701215202019)

**Figure 1** **Service startup and runtime API call process**  
![](figures/video_display_sevice_start_run.png "Service startup - runtime API call process")

The NVR video decoding display service startup and runtime API call process is described as follows:

1. Call the **hi\_mpi\_sys\_init** API to complete **media system initialization**.
2. **Create VDEC video decoding channels** (create multiple channels on demand), and notify the decoder to start receiving streams.
    1. Call the **hi\_mpi\_vdec\_create\_chn** API to create a channel.
    2. Call the **hi\_mpi\_vdec\_get\_chn\_param** API to obtain channel attributes, set the channel attributes as needed, and then call the **hi\_mpi\_vdec\_set\_chn\_param** API to set the channel parameters.
    3. Before decoding, call the **hi\_mpi\_vdec\_start\_recv\_stream** API to notify the decoder to start receiving streams.

3. **Create and enable VPSS groups** (create multiple VPSS groups on demand).
    1. Call the **hi\_mpi\_vpss\_create\_grp** API to create a VPSS group.
    2. Call the **hi\_mpi\_vpss\_start\_grp** API to enable the VPSS group.
    3. Call the **hi\_mpi\_vpss\_set\_chn\_attr** API to set the channel attributes. When working with the VO module, the channel attributes must be set to Auto mode.
    4. Call the **hi\_mpi\_vpss\_enable\_chn** API to start the VPSS channel.

   <a id="li178971210115019"></a>

4. Call the **hi\_mpi\_sys\_bind** API to **bind the video decoding channel and the VPSS group**. The output data after VDEC video decoding is directly sent to the corresponding VPSS group for further processing.
For example, when a single display outputs four video channels, the binding information is as shown in the following table:

   | VDEC Channel | VPSS Group | VO Channel | VO Video Layer | VO Device Number | HDMI Number |
   | --- | --- | --- | --- | --- | --- |
   | 1 | 1 | 1 | VHD0 | 0 | HDMI0 |
   | 2 | 2 | 2 | VHD0 | 0 | HDMI0 |
   | 3 | 3 | 3 | VHD0 | 0 | HDMI0 |
   | 4 | 4 | 4 | VHD0 | 0 | HDMI0 |

   For example, when two displays are used and each display outputs four video channels, the binding information is as shown in the following table:

   | VDEC Channel | VPSS Group | VO Channel | VO Video Layer | VO Device Number | HDMI Number |
   | --- | --- | --- | --- | --- | --- |
   | 1 | 1 | 1 | VHD0 | 0 | HDMI0 |
   | 2 | 2 | 2 | VHD0 | 0 | HDMI0 |
   | 3 | 3 | 3 | VHD0 | 0 | HDMI0 |
   | 4 | 4 | 4 | VHD0 | 0 | HDMI0 |
   | 5 | 5 | 5 | VHD1 | 1 | HDMI1 |
   | 6 | 6 | 6 | VHD1 | 1 | HDMI1 |
   | 7 | 7 | 7 | VHD1 | 1 | HDMI1 |
   | 8 | 8 | 8 | VHD1 | 1 | HDMI1 |

5. **Enable the VO device and VO channel** (create multiple VO channels on demand).
    1. Call **hi\_mpi\_vo\_set\_pub\_attr** to configure the display device attributes, and call **hi\_mpi\_vo\_enable** to enable the display device.
    2. Call **hi\_mpi\_vo\_set\_video\_layer\_attr** to configure the display video layer attributes, and call **hi\_mpi\_vo\_enable\_video\_layer** to enable the display video layer.
    3. Call **hi\_mpi\_vo\_set\_chn\_attr** to configure the display channel attributes, and call **hi\_mpi\_vo\_enable\_chn** to enable the display channel.

6. **Initialize the HDMI peripheral**.
    1. Call **hi\_mpi\_hdmi\_init** to initialize the HDMI device, and call **hi\_mpi\_hdmi\_open** to open HDMI.
    2. Call **hi\_mpi\_hdmi\_set\_attr** to configure the HDMI attributes.
    3. Call **hi\_mpi\_hdmi\_start** to start the HDMI peripheral so that video can be displayed.

7. Call **hi\_mpi\_sys\_bind** to **bind the VPSS group and the VO channel**. The output data processed by VPSS is directly sent to the corresponding VO channel for further processing.

    For the binding information, see [4](#li178971210115019).

8. Call the **hi\_mpi\_vdec\_send\_stream** API in a loop to **send each frame of the decoded stream**.

    **Note:**

    1. After the video decoding channel is bound to the VPSS group, when the user calls **hi\_mpi\_vdec\_send\_stream** to send the stream, **vdec\_pic\_info** in the API parameters can be set to **NULL**. In this case, the video decoding channel is bound to the VPSS module (see [4](#li178971210115019)), and the decoding result data is directly sent to the corresponding VPSS group for further processing. Obtaining the decoding result data through the **hi\_mpi\_vdec\_get\_frame** API is not supported.
    2. Video decoding supports two modes: playback mode and preview mode. They can be queried and set through the **hi\_mpi\_vdec\_get\_display\_mode** and **hi\_mpi\_vdec\_set\_display\_mode** APIs. For video recording playback, the playback mode is required, which supports playback control.

<br>

**Figure 2** **Resource release API call process**  
![](figures/video_display_resource_release.png "Resource release API call process")

The resource release API call process for NVR video decoding display services is described as follows:

1. Call the **hi\_mpi\_sys\_unbind** API to **unbind the VO channel from the VPSS group**.
2. Call the **hi\_mpi\_sys\_unbind** API to **unbind the VPSS group from the VDEC channel**.
3. **Release the HDMI peripheral resources**.
    1. First call **hi\_mpi\_hdmi\_stop** to stop HDMI.
    2. Call **hi\_mpi\_hdmi\_close** to close HDMI.
    3. Call **hi\_mpi\_hdmi\_deinit** to deinitialize the HDMI device.

4. **Release VO device and channel resources.**
    1. Call **hi\_mpi\_vo\_disable\_chn** to disable the channel.
    2. Call **hi\_mpi\_vo\_disable\_video\_layer** to disable the video layer.
    3. Call **hi\_mpi\_vo\_disable** to disable the display device.

5. **Destroy the VPSS group.**
    1. Call the **hi\_mpi\_vpss\_disable\_chn** API to close the VPSS channel.
    2. Call the **hi\_mpi\_vpss\_stop\_grp** API to stop the VPSS group.
    3. Call the **hi\_mpi\_vpss\_destroy\_grp** API to destroy the VPSS group.

6. **Destroy the VDEC video decoding channel**.
    1. Call the **hi\_mpi\_vdec\_stop\_recv\_stream** API to notify the decoder to stop receiving streams.
    2. Call the **hi\_mpi\_vdec\_destroy\_chn** API to destroy the channel.

7. Call the **hi\_mpi\_sys\_exit** API to complete **media data processing system deinitialization**.

<a id="section14704382225"></a>

## Video Decoding Intelligent Analysis Process

The video decoding intelligent analysis process involves the video decoding module \(VDEC\), video processing module \(VPSS\), intelligent analysis (model inference), and enhanced functions such as the region management module. For the API call process of the region management function, see the [region management function](#section13836172315012).

**Figure 3** **Service startup and runtime API call process**  
![](figures/video_intelligent_analysis_sevice_start_run.png "Service startup - runtime API call process")

The video decoding intelligent analysis service startup and runtime process is as follows:

1. Call the **hi\_mpi\_sys\_init** API to complete **media system initialization**.
2. **Create VDEC video decoding channels** (create multiple channels on demand), and notify the decoder to start receiving streams.
    1. Call the **hi\_mpi\_vdec\_create\_chn** API to create a channel.
    2. Call the **hi\_mpi\_vdec\_get\_chn\_param** API to obtain channel attributes, set the channel attributes on demand, and then call the **hi\_mpi\_vdec\_set\_chn\_param** API to set the channel parameters.
    3. Before decoding, call the **hi\_mpi\_vdec\_start\_recv\_stream** API to notify the decoder to start receiving streams.

3. **Create and enable VPSS groups** (create multiple VPSS groups on demand).
    1. Call the **hi\_mpi\_vpss\_create\_grp** API to create a VPSS group.
    2. Call the **hi\_mpi\_vpss\_start\_grp** API to enable the VPSS group.
    3. Call the **hi\_mpi\_vpss\_set\_chn\_attr** API to set the channel attributes, which must be set to user mode.
    4. Call the **hi\_mpi\_vpss\_enable\_chn** API to start the VPSS channel.

4. Call the **hi\_mpi\_sys\_bind** API to **bind the video decoding channel and the VPSS group**. The output data from VDEC video decoding is directly sent to the corresponding VPSS group for further processing.

    For binding information, see [4](#li178971210115019).

5. Call the **hi\_mpi\_vdec\_send\_stream** API in a loop to **send each frame of the decoded stream**.

    **Note:**

    After the video decoding channel and the VPSS group are bound, when the user calls **hi\_mpi\_vdec\_send\_stream** to send the stream, **vdec\_pic\_info** in the API parameters can be set to **NULL**. In this case, the video decoding channel and the VPSS module are bound (see [4](#li178971210115019)), and the decoding result data is directly sent to the corresponding VPSS group for further processing. Obtaining the decoding result data through the **hi\_mpi\_vdec\_get\_frame** API is not supported.

6. Call the **hi\_mpi\_vpss\_get\_chn\_frame** API to **obtain the image data processed by VPSS**, which can be sent to model inference. After the inference is complete, call **hi\_mpi\_vpss\_release\_chn\_frame** to **release one frame of channel image**.

    **Note**:

    In multi-channel scenarios, users can call the **hi\_mpi\_vpss\_get\_chn\_fd** API to obtain the handle of the specified VPSS channel, and wait for the VPSS processing result by calling the epoll API (see the related APIs in **hi\_mpi\_sys\_create\_epoll**). After VPSS processing is complete, the epoll wait is automatically woken up, and the **hi\_mpi\_vpss\_get\_chn\_frame** API can then be called to obtain the image data processed by VPSS.

    Before the VPSS-processed image is sent for model inference, if the image size, format, or other attributes do not meet the requirements, it needs to be further processed by the VPC function module and AIPP function of DVPP. See the introduction to VPC and AIPP in [Media Data Processing Function Overview](DVPP_overview.md).

**Figure 4** **Resource release API call process**  
![](figures/video_intelligent_analysis_resource_release.png "Resource release API call process-9")

The resource release API call prcoess of the NVR video decoding intelligent analysis service is described as follows:

1. Call the **hi\_mpi\_sys\_unbind** API to **unbind the VPSS group from the VDEC channel**.
2. **Destroy the VPSS group**.
    1. Call the **hi\_mpi\_vpss\_disable\_chn** API to disable the VPSS channel.
    2. Call the **hi\_mpi\_vpss\_stop\_grp** API to stop the VPSS group.
    3. Call the **hi\_mpi\_vpss\_destroy\_grp** API to destroy the VPSS group.

3. **Destroy the VDEC video decoding channel**.
    1. Call the **hi\_mpi\_vdec\_stop\_recv\_stream** API to notify the decoder to stop receiving streams.
    2. Call the **hi\_mpi\_vdec\_destroy\_chn** API to destroy the channel.

4. Call the **hi\_mpi\_sys\_exit** API to complete the **media data processing system deinitialization**.

<a id="section13836172315012"></a>

## Region Management Function

The OSD \(On Screen Display\) overlaid on the video and the color blocks that occlude the video are collectively referred to as regions. The **region management module** is used to uniformly manage these region resources, for displaying specific information on the video (such as the channel number and timestamp), or filling color blocks in the video for occlusion.

The region management function must be used together with the VPSS module, and the VPSS group and VPSS channel associated with the region management function must have been created. The API call process is as follows.

![](figures/Region_API_call_process.png)

1. **Initialization**:
    1. Call **hi\_mpi\_rgn\_create** to create a region.
    2. Call the **hi\_mpi\_rgn\_attach\_to\_chn** API to overlay the region onto the VPSS channel.

2. **Modify region information on demand**:
    - Set the region channel display attributes:
        1. Call the **hi\_mpi\_rgn\_get\_display\_attr** API to obtain the current channel display attributes of the region.
        2. Call the **hi\_mpi\_rgn\_set\_display\_attr** API to set the channel display attributes of the region.

    - Set the display canvas information of the region:
        1. Call the **hi\_mpi\_rgn\_get\_canvas\_info** API to obtain the current display canvas information of the region.
        2. Call the **hi\_mpi\_rgn\_update\_canvas** API to update the display canvas information.

3. **Release resources**:
    1. Call the **hi\_mpi\_rgn\_detach\_from\_chn** API to remove the specified region from the VPSS channel.
    2. Call the **hi\_mpi\_rgn\_destroy** API to destroy the region.

<a id="section107971821203"></a>

## TDE Graph Drawing Function

TDE is a 2D graph acceleration engine. It uses hardware to provide fast graph drawing functions for On Screen Display (OSD) and Graphical User Interface (GUI), mainly including fast copy, fast color fill, and pattern fill (currently only Alpha Blending is supported).

**Figure 5** **TDE API call process**  
![](figures/TDE_API_call_process.png "TDE API call process")

1. Call the **hi\_tde\_open** API to **open the TDE device**.
2. Call the **hi\_tde\_begin\_job** API to **create a TDE task**.
3. Call each **command execution** API, for example **hi\_tde\_quick\_copy**, **hi\_tde\_quick\_fill**, and **hi\_tde\_pattern\_fill**.

    Before calling a command execution API, call the **int ioctl \(int fd,  FBIOGET\_FSCREENINFO,  fb\_fix\_screeninfo \*fix\)** API provided by HIFB to obtain the user-mode address of the video memory, which is used as the memory address of the target bitmap. After the TDE task is executed, the data of the target bitmap is stored at this memory address and used as the input data of HIFB.

4. If adding a command fails, call the **hi\_tde\_cancel\_job** API to cancel the task. If adding a command succeeds, call the **hi\_tde\_end\_job** API to submit the task.
5. **Wait for the TDE task to complete**.

    Currently, there are two methods: waiting for a specified TDE task to complete (by calling the **hi\_tde\_wait\_for\_done** API) and waiting for all tasks on the current TDE device to complete (by calling the **hi\_tde\_wait\_all\_done** API).

<a id="section53701215202019"></a>

## HIFB Overlay Graph Layer Management Function

HIFB is used to manage overlay graphics layers. It not only provides the basic functions of Linux Framebuffer, but also adds extended functions such as modifying the display start position of layers and inter-layer Alpha on top of Linux Framebuffer.

**Figure 6**  HIFB API call process  
![](figures/HIFB_API_call_process.png "HIFB API call process")

1. Call **open** to **open the fb device** through system calls. The device files fb0 to fb4 correspond to layers G0 to G4. G0 and G1 are HD layers, G2 is the mouse layer, and G3 and G4 are SD layers.

    For details about the fb device, VO device, supported color formats, and resolution corresponding to each layer, see the description of the HIFB overlay graphics layer management function in [DVPP Media Acceleration Library](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/dvpp/dvpp_03_0000.html).

2. Call **ioctl** and pass the command code **FBIOGET\_VSCREENINFO** to **obtain the basic screen attributes**.
3. Call **ioctl** and pass the command code **FBIOPUT\_VSCREENINFO** to **set the basic screen attributes**.
4. Call **ioctl** and pass the command code **FBIOGET\_FSCREENINFO** to **obtain the user-space address of the video memory**.
5. Call **mmap** to **map the user-space virtual address**.
6. Call **ioctl** and pass the function-related command code to **set the function attributes**.
7. Call **munmap** to **unmap the user-mode virtual address mapping**.
8. Call **close** to **close the fb device**.

    If HIFB and VO are used together in the same process, close the fb device after disabling the VO device (that is, calling **hi\_mpi\_vo\_disable**).

    If HIFB and VO are not in the same process, stop the application process where VO resides first.
