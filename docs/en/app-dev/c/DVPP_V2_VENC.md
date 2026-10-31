# VENC Video Encoding

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:35:53.411Z pushedAt=2026-10-26T03:10:39.430Z nl=2 -->

This section describes the API call process of VENC video encoding, and provides sample code to help you understand the process.

VENC (Video Encoder) encodes images in YUV420SP format into H.264/H.265 video streams. For details about the VENC function and its usage constraints, see [DVPP Media Acceleration Library](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/dvpp/dvpp_03_0000.html).

When implementing VENC video encoding, you can set basic parameters when creating a channel, or call the corresponding set APIs to set advanced parameters to optimize video encoding quality. For details, see [Optimizing Video Encoding Quality](#section8439152116227).

## API Call Process

**Figure 1**  VENC video encoding call process  
![](figures/VENC_API_call_process_V2.png "VENC video encoding call process")

The current system supports H264/H265 video streams. The key APIs are described as follows:

1. **Resource initialization**:
    1. Call **aclInit** to initialize the system.
    2. Call **aclrtSetDevice** to specify the compute device.
    3. Use the **hi\_mpi\_sys\_init** API to initialize the media data processing system.
    4. Call the **hi\_mpi\_venc\_create\_chn** function to create a channel.

        After the channel is created, you can set advanced encoding parameters based on actual requirements, such as the scenario mode and advanced parameters of the stream controller. For details, see the API description in the **hi\_mpi\_venc\_set\_jpeg\_param\** to **hi\_mpi\_venc\_compact\_jpeg\_tables** sections.

    5. Call **hi\_mpi\_venc\_get\_fd** to convert the channel ID into a file handle.

        <!-- npu="310p" id1 -->
        **Note:** In the control CPU open form, to be compatible with earlier versions, when waiting for encoding to complete, applications of earlier versions can still use the **select** or **poll** function of the Linux operating system. It is recommended that you use the API call process shown in the preceding figure to ensure evolution of subsequent versions.
        <!-- end id1 -->

    6. Call the **hi\_mpi\_sys\_create\_epoll** function to create a DVPP epoll instance, and then call the **hi\_mpi\_sys\_ctl\_epoll** function to add the file handle of the encoding channel to the epoll instance for processing by the epoll instance.

        If the **select** or **poll** method is used, this step is not required.

2. **Video encoding**:
    1. Call the **hi\_mpi\_venc\_start\_chn** function to notify the channel to prepare to start encoding.
    2. Call the **hi\_mpi\_dvpp\_malloc** API to allocate the memory for storing input data on the device.
    3. Start a user-mode thread and call the **hi\_mpi\_sys\_wait\_epoll** function to wait for encoding to complete.
    4. After that, the user can call the **hi\_mpi\_venc\_send\_frame** function to send the stream to be encoded.
    5. Once encoding is complete, the **hi\_mpi\_sys\_wait\_epoll**, **select**, or **poll** function returns. The user can then call the **hi\_mpi\_venc\_query\_status** API to query the encoding status, and then call the **hi\_mpi\_venc\_get\_stream** function to obtain the encoding result.
    6. Note that after the encoding result data is used, the user must call the **hi\_mpi\_venc\_release\_stream** function in a timely manner to release the buffer. Otherwise, subsequent encoding cannot proceed because the encoding buffers are exhausted.
    7. Call the **hi\_mpi\_dvpp\_free** API to release the input memory.
    8. When the user no longer needs to send images to the destination channel for continued encoding, call the **hi\_mpi\_venc\_stop\_chn** function to notify the channel that it will no longer receive new input images.

3. **Resource release**:
    1. Call the **hi\_mpi\_sys\_ctl\_epoll** function to remove the file handle of the encoding channel from the epoll instance.
    2. After the user completes all encoding, call **hi\_mpi\_venc\_destroy\_chn** to release the encoding channel and its internal memory resources.
    3. Call the **hi\_mpi\_sys\_close\_epoll** function to destroy the DVPP epoll instance.
    4. Call the **hi\_mpi\_sys\_exit** API to deinitialize the media data processing system.
    5. Call the **aclrtResetDevice** API to reset the device and release the resources on the device.
    6. Call the **aclFinalize** API to deinitialize the system and release the resources used by the ACL APIs within the process.

<a id="section8439152116227"></a>

## Optimizing Video Encoding Quality

When implementing the VENC video encoding function, you can set basic parameters when creating a channel, or call the corresponding set API to set advanced parameters, to optimize video encoding quality. The following adjustment methods can be used in combination, and their effects are cumulative. For example:

- In the H264 video data obtaining scenario, with a resolution of 720P, gop = 60, a frame rate of 30 fps, and a bitrate of 1 Mbit/s, to improve encoding quality, you can use the following combination of optimization methods: CBR mode, HI\_VENC\_SCENE\_0, stats\_time equal to 2, profile equal to 2, and disabling macroblock-level rate control.
- In the H265 movie scenario, with a resolution of 1080P, gop = 30, a frame rate of 25 fps, and a bitrate of 2 Mbit/s, to improve encoding quality, you can use the following combination of optimization methods: CBR mode, HI\_VENC\_SCENE\_1, stats\_time equal to 1, and disabling macroblock-level rate control.

**The following methods are currently supported for optimizing video encoding quality**:

- **Set basic parameters to optimize video encoding quality.**

    For videos of different resolutions, the encoding quality is related to the frame rate, Group of Pictures (GOP), and bitrate of the video. When calling the **hi\_mpi\_venc\_create\_chn** API to create a channel, you can set the encoding level, and set the frame rate, GOP, bitrate, and other parameters in CBR/VBR/AVBR/CVBR/QVBR modes for H.264/H.265 protocol encoding scenarios, to adjust the video encoding quality:

    - Encoding level, set through the profile parameter within the **hi\_venc\_chn\_attr.venc\_attr** structure;
    - Frame rate, set through the **src\_frame\_rate** input frame rate parameter and the **dst\_frame\_rate** output frame rate parameter within the **hi\_venc\_chn\_attr.rc\_attr** structure;
    - GOP, set through the **gop** parameter within the **hi\_venc\_chn\_attr.rc\_attr** structure;
    - Bitrate, set through the **bit\_rate**, **max\_bit\_rate**, or **target\_bit\_rate** parameter within the **hi\_venc\_chn\_attr.rc\_attr** structure.

    **Table 1**  Frame rate, GOP, and bitrate values in typical scenarios

    | Image Quality/Resolution | Frame Rate | GOP | Bitrate (Mbps) |
    | --- | --- | --- | --- |
    | 4K<br>3840*2160/4096*2160 | 25 or 30 | It is recommended that the GOP be an integer multiple of the frame rate. For example, when the frame rate is 25, the recommended GOP is 25 or 50. | - In the video data obtaining scenario, for H264/H265 streams, the bitrate value is 8 to 12.<br>  - In the live streaming/streamer/short video scenario, for H265 streams, the bitrate value is 6 to 12.<br>For H264 streams, not involved.<br>  - In the gaming video scenario, for H264/H265 streams, the bitrate value is 10 to 16. |
    | 2K<br>2560*1440 | 25 or 30 | It is recommended that the GOP be an integer multiple of the frame rate. For example, when the frame rate is 25, the recommended GOP is 25 or 50. | - In the video data acquisition scenario, for H264/H265 streams, the bitrate value is 6 to 10.<br>  - In the live streaming/streamer/short video scenario, for H265 streams, the bitrate value is 4.8 to 8.<br>For H264 streams, not involved.<br>  - In the gaming video scenario, for H264/H265 streams, the bitrate value is 6 to 10. |
    | 1080P (Blu-ray)<br>1920*1080 | 25 or 30 | It is recommended that the GOP be an integer multiple of the frame rate. For example, when the frame rate is 25, the recommended GOP is 25 or 50. | - In the video data obtaining scenario, for H265 streams, the bitrate value is 1 to 4.<br>For H264 streams, the bitrate value is 2 to 6.<br>  - In the live streaming/streamer/short video scenario, for H265 streams, the bitrate value is 1.4 to 3.6.<br>For H264 streams, the bitrate value is 2 to 4.8.<br>  - In the gaming video scenario, for H264/H265 streams, the bitrate value is 3 to 6. |
    | 720P (HD)<br>1280*720 | 25 or 30 | It is recommended that the GOP be an integer multiple of the frame rate. For example, when the frame rate is 25, the recommended GOP is 25 or 50. | - In the video data obtaining scenario, for H265 streams, the bitrate value is 0.8 to 2.<br>For H264 streams, the bitrate value is 1 to 3.<br>  - In the live streaming/streamer/short video scenario, for H265 streams, the bitrate value is 1 to 2.<br>For H264 streams, the bitrate value is 1 to 3.<br>  - In the gaming video scenario, for H264/H265 streams, the bitrate value is 2 to 4. |
    | 480P/D1_N (SD)<br>854*480/720*480 | 25 or 30 | It is recommended that the GOP be an integer multiple of the frame rate. For example, when the frame rate is 25, the recommended GOP is 25 or 50. | - In the video data acquisition scenario, for H265 streams, the bitrate value is 0.3 to 0.7.<br>For H264 streams, the bitrate value is 0.6 to 1.4.<br>  - In the live streaming/streamer/short video scenario, for H265 streams, the bitrate value is 0.25 to 0.6.<br>For H264 streams, the bitrate value is 0.3 to 0.7.<br>  - In the gaming video scenario, not involved. |
    | 576P/D1 (SD)<br>720*576 | 25 or 30 | It is recommended that the GOP be an integer multiple of the frame rate. For example, when the frame rate is 25, the recommended GOP is 25 or 50. | - In the video data acquisition scenario, for H265 streams, the bitrate value is 0.3 to 0.7.<br>For H264 streams, the bitrate value is 0.6 to 1.4.<br>  - In the live streaming/streamer/short video scenario, for H265 streams, the bitrate value is 0.25 to 0.6.<br>For H264 streams, the bitrate value is 0.3 to 0.7.<br>  - In the gaming video scenario, not involved. |
    | 270P (Smooth)<br>480*270 | 25 or 30 | It is recommended that the GOP be an integer multiple of the frame rate. For example, when the frame rate is 25, the recommended GOP is 25 or 50. | - In the video data acquisition scenario, not involved.<br>  - In the live streaming/streamer/short video scenario, for H265 streams, the bitrate value is 0.2.<br>For H264 streams, the bitrate value is 0.3.<br>  - In the gaming video scenario, not involved. |
    | CIF P/N<br>352*288/320*240 | 25 or 30 | It is recommended that the GOP be an integer multiple of the frame rate. For example, when the frame rate is 25, the recommended GOP is 25 or 50. | - In the video data obtaining scenario, for H264/H265 streams, the bitrate value is 0.25.<br>  - In the live streaming/streamer/short video scenario, not involved.<br>  - In the gaming video scenario, not involved. |

- **Set advanced parameters to adjust video encoding details.**

    You can call APIs to set the rate control mode, macroblock-level rate control parameters, and encoding scenario mode to adjust the details of video encoding and further improve the encoding quality.

    **Table 2**  Advanced configuration items

    | Configuration Item | API | Parameter | Description |
    | --- | --- | --- | --- |
    | Rate control mode | hi_mpi_venc_create_chn | **rc_mode** parameter within the **hi_venc_chn_attr.rc_attr** structure | To pursue a stable bitrate or a large PSNR with the bitrate meeting the target value, configure it as CBR.<br>To pursue bitrate saving with a certain requirement on subjective encoding quality, configure it as VBR.<br>To pursue bitrate saving with a certain requirement on subjective encoding quality and with many static frames in the scenario, configure it as AVBR.<br>To pursue PSNR without a strict requirement on bitrate increase, configure it as QVBR.<br>To pursue bitrate saving with a certain requirement on subjective encoding quality and allow more adjustments based on bandwidth and storage requirements, configure it as CVBR. |
    | Rate control model statistics time | hi_mpi_venc_create_chn | **stats_time** parameter within the attribute value structure of each mode in **hi_venc_chn_attr.rc_attr** | If you care about long-term bitrate stability and do not mind short-term fluctuations, set a larger value, for example, for DVR storage. A larger value raises the threshold for re-encoding decisions, reducing the number of re-encodings, but increases bitrate fluctuations. |
    | Macroblock-level rate control parameters | hi_mpi_venc_set_rc_param | **threshold_i**, **threshold_p**, **threshold_b**, **direction**, and **row_qp_delta** parameters within the **hi_venc_rc_param** structure | If the image content is complex, has many details, or you care about objective metrics such as PSNR, disable macroblock-level rate control. |
    | Start QP value of the first frame | hi_mpi_venc_create_chn | **first_frame_start_qp** parameter within the **hi_venc_rc_param** structure | In typical scenarios, if the bitrate you configure is lower than the reference value in Table 1 and the first frame of the encoded video is obviously blurred, configure the **first_frame_start_qp** parameter to the median of [min_i_qp, max_i_qp]. For example, if [min_i_qp, max_i_qp] is [30, 40], configure **first_frame_start_qp** to **35** and **max_reencode_times** to **0** to obtain better encoding quality. |
    | Encoding scenario mode | hi_mpi_venc_set_scene_mode | hi_venc_scene_mode | For the security scenario, configure it as **HI_VENC_SCENE_0**. For assisted driving, live streaming, gaming, animation, and movies, configure it as **HI_VENC_SCENE_1**. |

## Sample Code

The following sample code shows the key steps of the VENC video encoding function. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

<!-- npu="310p" id2 -->
You can click [venc\_sample](https://gitee.com/ascend/samples/tree/master/cplusplus/level1_single_api/7_dvpp/venc_sample) to obtain the sample code.
<!-- end id2 -->

```cpp
// 1. Initialize the media data processing system.
int32_t ret = hi_mpi_sys_init();

// 2. Create a channel.
hi_venc_chn chn = 0;
hi_venc_chn_attr attr{};
attr.venc_attr.type = HI_PT_H265;
attr.venc_attr.profile = 0;
attr.venc_attr.max_pic_width = 128;
attr.venc_attr.max_pic_height = 128;
attr.venc_attr.pic_width = 128;
attr.venc_attr.pic_height = 128;
attr.venc_attr.buf_size = 2 * 1024 * 1024;
attr.venc_attr.is_by_frame = HI_TRUE;
attr.rc_attr.rc_mode = HI_VENC_RC_MODE_H265_VBR;
attr.rc_attr.h265_vbr.gop = 30;
attr.rc_attr.h265_vbr.stats_time = 1;
attr.rc_attr.h265_vbr.src_frame_rate = 30;
attr.rc_attr.h265_vbr.dst_frame_rate = 30;
attr.rc_attr.h265_vbr.max_bit_rate = 4000;
attr.gop_attr.gop_mode = HI_VENC_GOP_MODE_NORMAL_P;
attr.gop_attr.normal_p.ip_qp_delta = 3;
ret = hi_mpi_venc_create_chn(chn, &attr);

// 3. Notify the encoder to start receiving input data.
hi_venc_start_param recv_param{};
recv_param.recv_pic_num = -1;
ret = hi_mpi_venc_start_chn(chn, &recv_param);

// 4. Send input data.
// 4.1 Allocate input memory.
uint8_t* inputAddr = nullptr;
int32_t inputSize = 128 * 128 * 3 / 2;
ret = hi_mpi_dvpp_malloc(0, &inputAddr, inputSize);

// Read the input data into the device memory. The custom function VencReadYuvFile is implemented by the user.
VencReadYuvFile(streamName, inputAddr, inputSize);

// 4.2 Send input data to start encoding.
hi_video_frame_info frame{};
frame.mod_id = HI_ID_VENC;
frame.v_frame.width = 128;
frame.v_frame.height = 128;
frame.v_frame.field = HI_VIDEO_FIELD_FRAME;
frame.v_frame.pixel_format = HI_PIXEL_FORMAT_YUV_SEMIPLANAR_420;
frame.v_frame.video_format = HI_VIDEO_FORMAT_LINEAR;
frame.v_frame.compress_mode = HI_COMPRESS_MODE_NONE;
frame.v_frame.dynamic_range = HI_DYNAMIC_RANGE_SDR8;
frame.v_frame.color_gamut = HI_COLOR_GAMUT_BT709;
frame.v_frame.width_stride[0] = 128;
frame.v_frame.width_stride[1] = 128;
frame.v_frame.width_stride[2] = 128;
frame.v_frame.virt_addr[0] = inputAddr;
frame.v_frame.virt_addr[1] = (hi_void *)((uintptr_t)frame.v_frame.virt_addr[0] + 128 * 128);
frame.v_frame.frame_flag = 0;
frame.v_frame.time_ref = 0;
frame.v_frame.pts = 0;
ret = hi_mpi_venc_send_frame(chn, &frame, 0);

// 5. Obtain the encoding result.
// 5.1 Create an EPOLL instance.
int32_t epollFd = 0;
int32_t fd = hi_mpi_venc_get_fd(chn);
ret = hi_mpi_sys_create_epoll(10, &epollFd);

hi_dvpp_epoll_event event;
event.events = HI_DVPP_EPOLL_IN;
event.data = (void*)(unsigned long)(fd);
ret = hi_mpi_sys_ctl_epoll(epollFd, HI_DVPP_EPOLL_CTL_ADD, fd, &event);

int32_t eventCount = 0;
// Before encoding is complete, the process blocks here until timeout. Once encoding is complete, execution continues.
ret = hi_mpi_sys_wait_epoll(epollFd, events, 3, 1000, &eventCount);

// 5.2 Obtain the encoding result.
hi_venc_chn_status stat;
ret = hi_mpi_venc_query_status(chn, &stat);
hi_venc_stream stream;
stream.pack_cnt = stat.cur_packs;
stream.pack = new hi_venc_pack[stream.pack_cnt];
ret = hi_mpi_venc_get_stream(chn, &stream, 1000);

// 5.3 Obtain the encoded output bitstream data.
// The encoded output bitstream data can be used directly in the memory pointed to by stream.pack[0].addr.
// TODO: Code logic related to inference

// 6. Release the input memory and output bitstream
ret = hi_mpi_dvpp_free(inputAddr);
ret = hi_mpi_venc_release_stream(chn, &stream);
delete[] stream.pack;

// 7. Notify the encoder to stop receiving input data.
ret = hi_mpi_venc_stop_chn(chn);
ret = hi_mpi_sys_ctl_epoll(epollFd, HI_DVPP_EPOLL_CTL_DEL, fd, NULL);
ret = hi_mpi_sys_close_epoll(epollFd);

// 8. Destroy the channel.
ret = hi_mpi_venc_destroy_chn(chn);

// 9. Deinitialize the media data processing system.
ret = hi_mpi_sys_exit();

// ....
```
