# JPEGE Image Encoding

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:33:22.806Z pushedAt=2026-10-26T03:10:39.425Z nl=2 -->

This section describes the API call process of JPEGE image encoding, with sample code provided to help you understand the process.

JPEGE (JPEG Encoder) implements image encoding, converting YUV images into .jpg images. For details about JPEGE and its usage constraints, see [DVPP Media Acceleration Library](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/dvpp/dvpp_03_0000.html).

## API Call Process

**Figure 1**  JPEGE image encoding call process  
![](figures/JPEGE_API_call_process_V2.png "JPEGE image encoding call process")

The current system supports encoding YUV images into JPEG compressed image files. The key APIs are described as follows:

1. **Resource initialization**:
    1. Call **aclInit** to initialize the system.
    2. Call **aclrtSetDevice** to specify the compute device.
    3. Call **hi\_mpi\_sys\_init** to initialize the media data processing system.
    4. Call **hi\_mpi\_venc\_create\_chn** to create a channel.

        After the channel is created, you can set advanced encoding parameters as required, such as the scenario mode and advanced parameters of the bitstream controller. For details, see the API description in the **hi\_mpi\_venc\_set\_jpeg\_param** to **hi\_mpi\_venc\_compact\_jpeg\_tables** sections.

    5. Call **hi\_mpi\_venc\_get\_fd** to convert the channel ID into a file handle.
    6. Call **hi\_mpi\_sys\_create\_epoll** to create a DVPP epoll instance.

        **Note:** In the control CPU open form, for compatibility with earlier versions, when waiting for encoding to complete, applications of earlier versions can still use the **select** or **poll** function of the Linux operating system. It is recommended to use the API call process shown in the preceding figure to ensure evolution of subsequent versions.

    7. Call **hi\_mpi\_sys\_ctl\_epoll** to add the file handle of the encoding channel to the epoll instance for processing by the epoll instance.

        This step is not required for the **select** or **poll** method.

2. **Image encoding**:
    1. Call **hi\_mpi\_venc\_start\_chn** to notify the channel to prepare for encoding.
    2. Call **hi\_mpi\_dvpp\_malloc** to allocate memory for storing input data on the device.
    3. Start a user-mode thread and call **hi\_mpi\_sys\_wait\_epoll** to wait for encoding to complete.
    4. After that, the user can call **hi\_mpi\_venc\_send\_frame** to send the bitstream to be encoded.
    5. Once encoding is complete, the **hi\_mpi\_sys\_wait\_epoll**, **select**, or **poll** function returns, and the user can call the **hi\_mpi\_venc\_query\_status** API to query the encoding status, and then call the **hi\_mpi\_venc\_get\_stream** function to obtain the encoding result.
    6. Note that after the encoding result data is used, call the **hi\_mpi\_venc\_release\_stream** function in a timely manner to release the buffer. Otherwise, subsequent encoding will fail because the encoding buffers are exhausted.
    7. Call the **hi\_mpi\_dvpp\_free** API to release the input memory.
    8. When you no longer need to send images to the destination channel for encoding, call the **hi\_mpi\_venc\_stop\_chn** function to notify the channel that it will no longer receive new input images.

3. **Resource release**:
    1. Call the **hi\_mpi\_sys\_ctl\_epoll** function to remove the file handle of the encoding channel from the epoll instance.
    2. After all encoding is complete, call **hi\_mpi\_venc\_destroy\_chn** to release the encoding channel and its internal memory resources.
    3. Call the **hi\_mpi\_sys\_close\_epoll** function to destroy the DVPP epoll instance.
    4. Call the **hi\_mpi\_sys\_exit** API to deinitialize the media data processing system.
    5. Call the **aclrtResetDevice** API to reset the device and release the resources on the device.
    6. Call the **aclFinalize** API to deinitialize the system and release the resources used by the ACL APIs in the process.

## Sample Code

The following sample code shows the key steps of the JPEGE image encoding function. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

<!-- npu="310p" id1 -->
You can click [jpege\_sample](https://gitee.com/ascend/samples/tree/master/cplusplus/level1_single_api/7_dvpp/jpege_sample) to obtain the sample code.
<!-- end id1 -->

```cpp
// ....

// 1. Initialize the media data processing system.
int32_t ret = hi_mpi_sys_init();

// 2. Create a channel.
hi_venc_chn chn = 0;
hi_venc_chn_attr attr{};
attr.venc_attr.type = HI_PT_JPEG;
attr.venc_attr.profile = 0;
attr.venc_attr.max_pic_width = 128;
attr.venc_attr.max_pic_height = 128;
attr.venc_attr.pic_width = 128;
attr.venc_attr.pic_height = 128;
attr.venc_attr.buf_size = 2 * 1024 * 1024;
attr.venc_attr.is_by_frame = HI_TRUE;
attr.venc_attr.jpeg_attr.dcf_en = HI_FALSE;
attr.venc_attr.jpeg_attr.recv_mode = HI_VENC_PIC_RECV_SINGLE;
attr.venc_attr.jpeg_attr.mpf_cfg.large_thumbnail_num = 0;
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
// Read the input data into the memory. The custom function JpegeReadYuvFile is implemented by the user.
JpegeReadYuvFile(streamName, inputAddr, inputSize);

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
// Before encoding is complete, the process blocks here until timeout. It proceeds only after encoding is complete.
ret = hi_mpi_sys_wait_epoll(epollFd, event, 3, 1000, &eventCount);

// 5.2 Obtain the encoding result.
hi_venc_chn_status stat;
ret = hi_mpi_venc_query_status(chn, &stat);
hi_venc_stream stream;
stream.pack_cnt = stat.cur_packs;
stream.pack = new hi_venc_pack[stream.pack_cnt];
ret = hi_mpi_venc_get_stream(chn, &stream, 1000);

// 5.3 Obtain the encoded output stream data, which is in the memory pointed to by stream.pack[0].addr.
......

// 6. Release the input memory and output stream.
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
