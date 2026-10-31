# PNGD Image Decoding

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:34:02.106Z pushedAt=2026-10-26T03:10:39.426Z nl=2 -->

This section describes the API call process of PNGD image decoding, and provides sample code to help you understand the process.

PNGD (PNG decoder) is responsible for image decoding of PNG images. For details about the PNGD functions and usage constraints, see [DVPP Media Acceleration Library](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/dvpp/dvpp_03_0000.html).

## API Call Process

**Figure 1**  PNGD image decoding call process  
![](figures/PNGD_API_call_process_V2.png "PNGD image decoding call process")

The current system supports decoding PNG images. The key APIs are described as follows:

1. Call **aclInit** to initialize the system.
2. Call **aclrtSetDevice** to specify the compute device.
3. Call **hi\_mpi\_sys\_init** to initialize the media data processing system.
4. Call **hi\_mpi\_pngd\_create\_chn** to create a channel.
5. Call **hi\_mpi\_dvpp\_malloc** to allocate memory on the device for storing input or output data.
6. Call **hi\_mpi\_pngd\_send\_stream** to send the bitstream for decoding. **hi\_mpi\_pngd\_send\_stream** is an asynchronous API. Calling this API only indicates that the task has been successfully delivered. You also need to call **hi\_mpi\_pngd\_get\_image\_data** to obtain the decoding result data.
7. Call **hi\_mpi\_dvpp\_free** to release the input and output memory.
8. Call **hi\_mpi\_pngd\_destroy\_chn** to destroy the channel.
9. Call **hi\_mpi\_sys\_exit** to deinitialize the media data processing system.
10. Call **aclrtResetDevice** to reset the device and release resources on the device.
11. Call **aclFinalize** to deinitialize the system and release the resources used by the ACL APIs in the process.

## Sample Code

The following sample code shows the key steps of the PNGD image decoding function. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

<!-- npu="310p" id1 -->
You can click [pngd\_sample](https://gitee.com/ascend/samples/tree/master/cplusplus/level1_single_api/7_dvpp/pngd_sample) to obtain the sample code.
<!-- end id1 -->

```cpp
// ....

// 1. Initialize the media data processing system.
int32_t ret = hi_mpi_sys_init();

// 2. Create a channel.
hi_pngd_chn chnId;
hi_pngd_chn_attr chnAttr; // hi_pngd_chn_attr is a reserved parameter and does not need to be set.
ret = hi_mpi_pngd_create_chn(chnId, &chnAttr);

// 3. Send the bitstream.
// 3.1 Allocate input memory.
uint8_t* inputAddr = nullptr;
// inputsize indicates the memory size occupied by the input image. Here, 1024 bytes is used as an example. You need to calculate the memory size based on the actual situation.
int32_t inputSize = 1024;
ret = hi_mpi_dvpp_malloc(0, &inputAddr, inputSize);
// Read the input image into the memory. The custom function ReadStreamFile is implemented by the user.
ReadStreamFile(fileName, inputAddr, inputSize);

// 3.2 Build the structure that stores the input image information.
hi_img_stream stStream{};
hi_img_info stImgInfo{};
stStream.pts = 0;
if (g_runMode == ACL_HOST) {
    stStream.addr  = (uint8_t *)hostInputAddr;
} else {
    stStream.addr  = (uint8_t *)inputAddr;
}
stStream.len  = inputSize;
stStream.type = HI_PT_PNG;

ret = hi_mpi_png_get_image_info(&stStream, &stImgInfo);
if (g_runMode == ACL_HOST) {
    // If the data on the host is not used, release it in time.
    aclrtFreeHost(hostInputAddr);
    hostInputAddr = nullptr;
}
stStream.addr = (uint8_t *)inputAddr;

// 3.3 Build the structure that stores the output image information, and allocate output memory.
hi_pic_info outPicInfo{};
void *outBuffer = nullptr;
outPicInfo.picture_width  = stImgInfo.width;
outPicInfo.picture_height = stImgInfo.height;
outPicInfo.picture_width_stride  = stImgInfo.width_stride;
outPicInfo.picture_height_stride = stImgInfo.height_stride;
outPicInfo.picture_buffer_size   = stImgInfo.img_buf_size;
outPicInfo.picture_format = HI_PIXEL_FORMAT_UNKNOWN;

ret = hi_mpi_dvpp_malloc(0, &outBuffer, outPicInfo.buffer_size);

outPicInfo.picture_address = (uint64_t)outBuffer;

// 3.4 Send the input image to be decoded.
ret = hi_mpi_pngd_send_stream(chnId, &stream, &outPicInfo, 0);

// 4. Receive the decoding result.
// 4.1 Obtain the decoding result.
hi_pic_info picInfo;
hi_img_stream stream;
ret = hi_mpi_pngd_get_image_data(chnId, &picInfo, &stream, 0);
if (ret == HI_SUCCESS) { // Decode success
    printf("[%s][%d] Chn %u GetFrame Success, Decode Success \n",__FUNCTION__, __LINE__, chnId);
} else if (ret == HI_ERR_PNGD_BUF_EMPTY){ // Decoding
    printf("[%s][%d] Chn %u Decoding, try again \n",__FUNCTION__, __LINE__, chnId);
} else { // Decode fail
    printf("[%s][%d] Chn %u GetFrame Success, Decode Fail \n",__FUNCTION__, __LINE__, chnId);
}

// 4.2 Obtain the output image data of PNGD, which is in the memory pointed to by outputPic.picture_address.
......

// 4.3 Release the input and output memory.
ret = hi_mpi_dvpp_free(frame.v_frame.virt_addr[0]);
ret = hi_mpi_dvpp_free(stream.addr);

// 5. Destroy the channel.
ret = hi_mpi_pngd_destroy_chn(chnId);

// 6. Deinitialize the media data processing system.
ret = hi_mpi_sys_exit();

// ....
```
