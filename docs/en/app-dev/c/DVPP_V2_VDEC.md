# VDEC Video Decoding

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:34:51.343Z pushedAt=2026-10-26T03:10:39.427Z nl=2 -->

This section describes the API call process of VDEC video decoding, with sample code provided to help you understand the process.

VDEC (Video Decoder) decodes H.264/H.265 video streams into YUV/RGB images. For details about the VDEC functions and usage constraints, see [DVPP Media Acceleration Library](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/dvpp/dvpp_03_0000.html).

## API Call Process

When developing an application, if video decoding is involved, the application must include the decoding code logic.

**Figure 1**  VDEC video decoding API call process  
![](figures/VDEC_API_call_process_V2.png "VDEC video decoding API call process")

The current system supports decoding H264/H265 video streams. The key APIs are described as follows:

1. Call **aclInit** to initialize the system.
2. Call **aclrtSetDevice** to specify the compute device.
3. Call **hi\_mpi\_sys\_init** to initialize the media data processing system.
4. Call **hi\_vdec\_get\_pic\_buf\_size** to obtain the frame buffer size required for decoding, and call **hi\_vdec\_get\_tmv\_buf\_size** to obtain the size of the vector prediction buffer. These values are required when creating a channel.
5. Call **hi\_mpi\_vdec\_create\_chn** to create a channel.
6. Call **hi\_mpi\_dvpp\_malloc** to allocate memory on the device for storing input or output data.
7. Before decoding, call the **hi\_mpi\_vdec\_start\_recv\_stream** API to notify the decoder to start receiving streams, and then call the **hi\_mpi\_vdec\_send\_stream** API to send the stream to be decoded. The **hi\_mpi\_vdec\_send\_stream** API is an asynchronous API. Calling this API only indicates that the task has been successfully delivered. You also need to call the **hi\_mpi\_vdec\_get\_frame** API to obtain the decoding result data. After the decoding data is successfully obtained, you can call the **hi\_mpi\_vdec\_release\_frame** API to release frame-related resources. After decoding is complete, call the **hi\_mpi\_vdec\_stop\_recv\_stream** API to notify the decoder to stop receiving streams.
8. Call the **hi\_mpi\_dvpp\_free** API to release the input and output memory.
9. Call the **hi\_mpi\_vdec\_destroy\_chn** API to destroy the channel.
10. Call the **hi\_mpi\_sys\_exit** API to deinitialize the media data processing system.
11. Call the **aclrtResetDevice** API to reset the device and release resources on the device.
12. Call the **aclFinalize** API to deinitialize the system and release the resources used by the ACL APIs in the process.

## Sample Code

The following sample code shows the key steps of the VDEC video decoding function. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

<!-- npu="310p" id1 -->
You can click [vdec\_sample](https://gitee.com/ascend/samples/tree/master/cplusplus/level1_single_api/7_dvpp/vdec_sample) to obtain the sample code.
<!-- end id1 -->

```cpp
// ....

// 1. Initialize the media data processing system.
int32_t ret = hi_mpi_sys_init();

// 2. Create a channel.
hi_vdec_chn chnId;
hi_vdec_chn_attr chnAttr;
hi_pic_buf_attr buf_attr{1920, 1080, 0, 8, HI_PIXEL_FORMAT_YUV_SEMIPLANAR_420, HI_COMPRESS_MODE_NONE};

chnAttr.type = HI_PT_H264;
chnAttr.mode = HI_VDEC_SEND_MODE_FRAME;
chnAttr.pic_width = 1920;
chnAttr.pic_height = 1080;
chnAttr.stream_buf_size = 1920 * 1080 * 3 / 2;
chnAttr.frame_buf_cnt = 16;
chnAttr.frame_buf_size = hi_vdec_get_pic_buf_size(HI_PT_H264, &buf_attr);
chnAttr.video_attr.ref_frame_num = 12;
chnAttr.video_attr.temporal_mvp_en = HI_TRUE;
chnAttr.video_attr.tmv_buf_size = hi_vdec_get_tmv_buf_size(HI_PT_H264, 1920, 1080);

ret = hi_mpi_vdec_create_chn(chnId, &chnAttr);

// 3. Set the channel attributes.
hi_vdec_chn_param chnParam;
ret = hi_mpi_vdec_get_chn_param(chnId, &chnParam);

chnParam.video_param.dec_mode = HI_VIDEO_DEC_MODE_IPB;        
chnParam.video_param.compress_mode = HI_COMPRESS_MODE_HFBC;        
chnParam.video_param.video_format = HI_VIDEO_FORMAT_TILE_64x16;        
chnParam.display_frame_num = 3;
chnParam.video_param.out_order = HI_VIDEO_OUT_ORDER_DISPLAY;

ret = hi_mpi_vdec_set_chn_param(chnId, &chnParam);

// 4. Start the decoder to receive the stream.
ret = hi_mpi_vdec_start_recv_stream(chnId);

// 5. Send the stream.
// 5.1 Allocate input memory.
uint8_t* inputAddr = nullptr;
// inputsize indicates the memory size occupied by each frame of the stream. Here 1024 bytes is used as an example. You need to calculate the actual memory size based on the actual situation.
int32_t inputSize = 1024;
ret = hi_mpi_dvpp_malloc(0, &inputAddr, inputSize);

// Read the input stream data directly into the device memory.
// Read the input stream into the device memory. The custom function ReadStreamFile is implemented by the user.
ReadStreamFile(streamName, inputAddr, inputSize);

// 5.2 Allocate output memory.
uint8_t* outputAddr = nullptr;
// The memory size occupied by the output image data depends on the output image format.
int32_t outputSize = 1920 * 1080 * 3 / 2;
ret = hi_mpi_dvpp_malloc(0, &outputAddr, outputSize);

// 5.3 Build the structure that stores the information of one frame of the input stream.
hi_vdec_stream stream;
stream.addr = inputAddr;
stream.len = inputSize;
stream.end_of_frame = HI_TRUE;
stream.end_of_stream = HI_FALSE;
stream.need_display = HI_TRUE;

// 5.4 Construct the structure for storing one frame of output result information.
hi_vdec_pic_info outPicInfo;
outPicInfo.width = 1920;
outPicInfo.height = 1080;
outPicInfo.width_stride = 1920;
outPicInfo.height_stride = 1080;
outPicInfo.pixel_format = HI_PIXEL_FORMAT_YUV_SEMIPLANAR_420;
outPicInfo.vir_addr = outputAddr;
outPicInfo.buffer_size = outputSize;

// 5.5 Send one frame of stream.
ret = hi_mpi_vdec_send_stream(chnId, &stream, &outPicInfo, 0);

// 6. Receive the decoding result.
// 6.1 Obtain the decoding result.
hi_video_frame_info frame;    
hi_vdec_stream stream;
hi_vdec_supplement_info stSupplement;
ret = hi_mpi_vdec_get_frame(chnId, &frame, &stSupplement, &stream, 0);
if (ret == HI_SUCCESS) {
   decResult = frame.v_frame.frame_flag;
   if (decResult == 0) { // 0: Decode success
       printf("[%s][%d] Chn %u GetFrame Success, Decode Success \n",__FUNCTION__, __LINE__, chnId);
   } else if (decResult == 1) { // 1: Decode fail
       printf("[%s][%d] Chn %u GetFrame Success, Decode Fail \n",__FUNCTION__, __LINE__, chnId);
   } else if (decResult == 2) { // 2:This result is returned for the second field of
       printf("[%s][%d] Chn %u GetFrame Success, No Picture \n", __FUNCTION__, __LINE__, chnId);
   } else if (decResult == 3) { // 3: Reference frame number set error
       printf("[%s][%d] Chn %u GetFrame Success, RefFrame Num Error \n",__FUNCTION__, __LINE__, chnId);
   } else if (decResult == 4) { // 4: Reference frame size set error
       printf("[%s][%d] Chn %u GetFrame Success, RefFrame Size Error \n",__FUNCTION__, __LINE__, chnId);
  }
}

// 6.2 Obtain the decoding result data.
// You can directly use the VDEC output image data, which is in the memory pointed to by frame.v_frame.virt_addr[0].
// TODO: Code logic related to inference.


// 6.3 Release the input and output memory.
ret = hi_mpi_dvpp_free(frame.v_frame.virt_addr[0]);
ret = hi_mpi_dvpp_free(stream.addr);

// 6.4 Release resources.
ret = hi_mpi_vdec_release_frame(chnId, &frame);

// 7. The decoder stops receiving streams.
ret = hi_mpi_vdec_stop_recv_stream(chnId);

// 8. Destroy the channel.
ret = hi_mpi_vdec_destroy_chn(chnId);

// 9. Deinitialize the media data processing system.
ret = hi_mpi_sys_exit();

// ....
```
