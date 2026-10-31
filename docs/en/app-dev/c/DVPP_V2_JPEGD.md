# JPEGD Image Decoding

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:32:52.263Z pushedAt=2026-10-26T03:10:39.423Z nl=2 -->

This section describes the API call process of JPEGD image decoding, with sample code provided to help you understand the process.

JPEGD (JPEG Decoder) implements image decoding, decoding .jpg, .jpeg, .JPG, and .JPEG images into YUV format images. For details about JPEGD functions and usage constraints, see [DVPP Media Acceleration Library](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/dvpp/dvpp_03_0000.html).

## API Call Process

**Figure 1**  JPEGD image decoding call process  
![](figures/JPEGD_API_call_process_V2.png "JPEGD image decoding call process")

The current system supports decoding JPEG images. The key APIs are described as follows:

1. Call **aclInit** to initialize the system.
2. Call **aclrtSetDevice** to specify the compute device.
3. Call **hi\_mpi\_sys\_init** to initialize the media data processing system.
4. Call **hi\_mpi\_vdec\_create\_chn** to create a channel.
5. Call **hi\_mpi\_dvpp\_malloc** to allocate memory on the device for storing input or output data.
6. Before decoding, call **hi\_mpi\_vdec\_start\_recv\_stream** to notify the decoder to start receiving streams, and then call **hi\_mpi\_vdec\_send\_stream** to send the stream to be decoded. **hi\_mpi\_vdec\_send\_stream** is an asynchronous API. Calling it only indicates that the task has been successfully delivered. You also need to call **hi\_mpi\_vdec\_get\_frame** to obtain the decoding result data. After the decoding data is successfully obtained, you can call **hi\_mpi\_vdec\_release\_frame** to release frame-related resources. After decoding is complete, call **hi\_mpi\_vdec\_stop\_recv\_stream** to notify the decoder to stop receiving streams.
7. Call **hi\_mpi\_dvpp\_free** to release the input and output memory.
8. Call **hi\_mpi\_vdec\_destroy\_chn** to destroy the channel.
9. Call **hi\_mpi\_sys\_exit** to deinitialize the media data processing system.
10. Call **aclrtResetDevice** to reset the device and release the resources on the device.
11. Call **aclFinalize** to deinitialize the system and release the resources used by the ACL APIs in the process.

## Sample Code

The following sample code shows the key steps of the JPEGD image decoding function. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

<!-- npu="310p" id1 -->
You can click [jpegd\_sample](https://gitee.com/ascend/samples/tree/master/cplusplus/level1_single_api/7_dvpp/jpegd_sample) to obtain the sample code.
<!-- end id1 -->

```cpp
// ....

// 1. Initialize the media data processing system.
int32_t ret = hi_mpi_sys_init();

// 2. Create a channel.
hi_vdec_chn chnId;
hi_vdec_chn_attr chnAttr;

chnAttr.type = HI_PT_JPEG;
chnAttr.mode = HI_VDEC_SEND_MODE_FRAME;
chnAttr.pic_width = 1920;
chnAttr.pic_height = 1080;
chnAttr.stream_buf_size = 1920 * 1080;

ret = hi_mpi_vdec_create_chn(chnId, &chnAttr);

// 3. Set channel attributes.
hi_vdec_chn_param chnParam;
ret = hi_mpi_vdec_get_chn_param(chnId, &chnParam);

chnParam.pic_param.pixel_format = HI_PIXEL_FORMAT_YUV_SEMIPLANAR_420;
chnParam.pic_param.alpha = 255;
chnParam.display_frame_num = 0;
ret = hi_mpi_vdec_set_chn_param(chnId, &chnParam);

// 4. Start the decoder to receive the stream.
ret = hi_mpi_vdec_start_recv_stream(chnId);

// 5. Send the stream.
// 5.1 Allocate input memory.
uint8_t* inputAddr = nullptr;
// inputsize indicates the memory size occupied by the input image. This example uses 1024 bytes. You need to calculate the actual memory size based on the actual situation.
int32_t inputSize = 1024;
ret = hi_mpi_dvpp_malloc(0, &inputAddr, inputSize);
// Read the input image into the memory. The custom function ReadStreamFile is implemented by the user.
ReadStreamFile(fileName, inputAddr, inputSize);

// 5.2 Build the structure that stores the input image information.
hi_vdec_stream stStream{};
hi_img_info stImgInfo{};
stStream.pts = 0;
if (g_runMode == ACL_HOST) {
    stStream.addr  = (uint8_t *)hostInputAddr;
} else {
    stStream.addr  = (uint8_t *)inputAddr;
}
stStream.len = inputSize;
stStream.end_of_frame = HI_TRUE;
stStream.end_of_stream = HI_FALSE;
stStream.need_display  = HI_TRUE;

ret = hi_mpi_dvpp_get_image_info(HI_PT_JPEG, &stStream, &stImgInfo);
if (g_runMode == ACL_HOST) {
    // If the data on the host is not used, release it in a timely manner.
   aclrtFreeHost(hostInputAddr);
    hostInputAddr = nullptr;
}
stStream.addr = (uint8_t *)inputAddr;

// 5.3 Build the structure that stores the output image information, and allocate output memory.
hi_vdec_pic_info outPicInfo{};
void *outBuffer = nullptr;
outPicInfo.width  = stImgInfo.width;
outPicInfo.height = stImgInfo.height;
outPicInfo.width_stride  = stImgInfo.width_stride;
outPicInfo.height_stride = stImgInfo.height_stride;
outPicInfo.buffer_size   = stImgInfo.img_buf_size;
outPicInfo.pixel_format  = HI_PIXEL_FORMAT_UNKNOWN;

ret = hi_mpi_dvpp_malloc(0, &outBuffer, outPicInfo.buffer_size);

outPicInfo.vir_addr = (uint64_t)outBuffer;

// 5.4 Send the input image to be decoded.
ret = hi_mpi_vdec_send_stream(chnId, &stStream, &outPicInfo, 0);

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
   } else { // Decode fail
       printf("[%s][%d] Chn %u GetFrame Success, Decode Fail \n",__FUNCTION__, __LINE__, chnId);
   }
}

// 6.2 Obtain the output image data of JPEGD, which is in the memory pointed to by frame.v_frame.virt_addr[0].
......

// 6.3 Release the input and output memory.
ret = hi_mpi_dvpp_free(frame.v_frame.virt_addr[0]);
ret = hi_mpi_dvpp_free(stream.addr);

// 6.4 Release resources.
ret = hi_mpi_vdec_release_frame(chnId, &frame);

// 7. Stop the decoder from receiving streams.
ret = hi_mpi_vdec_stop_recv_stream(chnId);

// 8. Destroy the channel.
ret = hi_mpi_vdec_destroy_chn(chnId);

// 9. Deinitialize the media data processing system.
ret = hi_mpi_sys_exit();

// ....
```
