# JPEGE Image Encoding

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:31:04.138Z pushedAt=2026-10-26T03:10:39.421Z nl=2 -->

This section describes the API call process of JPEGE image encoding, and provides example code to help you understand the process.

JPEGE (JPEG Encoder) performs image encoding, converting YUV images into .jpg images. For details about JPEGE functions and usage constraints, see [DVPP Media Acceleration Library](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/dvpp/dvpp_03_0000.html).

## API Call Process

**Figure 1**  JPEG image encoding  
![](figures/JPEGE_API_call_process_V1.png "JPEG image encoding")

The current system supports encoding YUV images into .jpg images. The key APIs are described as follows:

1. Call **aclInit** to initialize the system.
2. Call **aclrtSetDevice** to specify the compute device.
3. Call **aclrtCreateStream** to create a stream.
4. Call **acldvppCreateChannel** to **create a channel for image data processing**.

    Before creating a channel for image data processing, call **acldvppCreateChannelDesc** to create the channel description.

5. Call **acldvppCreateJpegeConfig** to **create image encoding configuration data**.
6. Before implementing JPEG image encoding, if you need to **allocate memory on the device** to store input or output data, call **acldvppMalloc** to allocate memory.

    Before allocating the output memory, you can call the **acldvppJpegPredictEncSize** API to estimate the output memory size required after image encoding based on the input image description information and image encoding configuration data.

    The actual output memory size may differ from the size estimated by the **acldvppJpegPredictEncSize** API. If you need to obtain the actual output memory size after encoding, you can obtain it through the size output parameter of the **acldvppJpegEncodeAsync** API.

7. Call the **acldvppJpegEncodeAsync** asynchronous API to perform **encoding**.

    For asynchronous APIs, you also need to call the **aclrtSynchronizeStream** API to block program execution until all tasks in the specified stream are complete.

8. Call the **acldvppDestroyJpegeConfig** API to **destroy the image encoding configuration data**.
9. After encoding is complete, call the **acldvppFree** API in a timely manner to **release the input and output memory**.
10. Call the **acldvppDestroyChannel** API to **destroy the image data processing channel**.

    After destroying the image data processing channel, call the **acldvppDestroyChannelDesc** API to destroy the channel description information.

11. Call the **aclrtDestroyStream** API to destroy the stream.
12. Call the **aclrtResetDevice** API to reset the device and release resources on the device.
13. Call **aclFinalize** to deinitialize the system and release the resources used by the ACL APIs in the process.

## Sample Code

The following code examples show the key steps of the JPEGE image encoding function. They are for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

You can click [vpc\_jpeg\_resnet50\_imagenet\_classification](https://gitee.com/ascend/samples/tree/master/cplusplus/level2_simple_inference/1_classification/vpc_jpeg_resnet50_imagenet_classification) to obtain the sample code.

```cpp
// 1. Create the channel description information for the image data processing channel. dvppChannelDesc_ is of the acldvppChannelDesc type.
dvppChannelDesc_ = acldvppCreateChannelDesc();

// 2. Create the image data processing channel.
aclError ret = acldvppCreateChannel(dvppChannelDesc_);

// 3. Allocate input memory (distinguish the running status).
// Call aclrtGetRunMode to obtain the running mode of the software stack. If the running mode obtained by aclrtGetRunMode is ACL_HOST, call aclrtMemcpy to transfer the input image data to the device. After the data transfer is complete, release the memory in a timely manner. Otherwise, directly allocate and use the device memory.
aclrtRunMode runMode;
ret = aclrtGetRunMode(&runMode);
// inputPicWidth and inputPicHeight indicate the aligned width and aligned height of the image, respectively. Here, a YUV420SP image is used as an example.
uint32_t PicBufferSize = inputPicWidth * inputPicHeight * 3 / 2;
if(runMode == ACL_HOST){ 
    // Allocate the host memory vpcInHostBuffer.
    void* vpcInHostBuffer = nullptr;
    vpcInHostBuffer = malloc(PicBufferSize);
    // Read the input image into the memory. The custom function ReadPicFile is implemented by the user.
    ReadPicFile(picName, vpcInHostBuffer, PicBufferSize);
    // Allocate device memory inDevBuffer_
    ret = acldvppMalloc(&inDevBuffer_, PicBufferSize);
    // Transfer the input image data to the device through the aclrtMemcpy API.
    ret = aclrtMemcpy(inDevBuffer_, PicBufferSize, vpcInHostBuffer, PicBufferSize, ACL_MEMCPY_HOST_TO_DEVICE);
    // Release the memory in a timely manner after the data transfer is complete.
    free(vpcInHostBuffer);
} else {
    // Allocate device input memory inDevBuffer_
    ret = acldvppMalloc(&inDevBuffer_, PicBufferSize);
    // Read the input image into the memory. The custom function ReadPicFile is implemented by the user.
    ReadPicFile(picName, inDevBuffer_, PicBufferSize);
}

// 4. Create the description information of the encoded input image and set each attribute value.
// encodeInputDesc_ is of the acldvppPicDesc type.
encodeInputDesc_ = acldvppCreatePicDesc();
acldvppSetPicDescData(encodeInputDesc_, reinterpret_cast<void *>(inDevBuffer_));
acldvppSetPicDescFormat(encodeInputDesc_, PIXEL_FORMAT_YUV_SEMIPLANAR_420);
acldvppSetPicDescWidth(encodeInputDesc_, inputWidth_);
acldvppSetPicDescHeight(encodeInputDesc_, inputHeight_);
acldvppSetPicDescWidthStride(encodeInputDesc_, encodeInWidthStride);
acldvppSetPicDescHeightStride(encodeInputDesc_, encodeInHeightStride);
acldvppSetPicDescSize(encodeInputDesc_, inDevBufferSizeE_);

// 5. Create the image encoding configuration data and set the encoding quality.
// The encoding quality ranges from 0 to 100. Level 0 is similar to level 100 in encoding quality, and within [1, 100], a smaller value indicates poorer output image quality.
jpegeConfig_ = acldvppCreateJpegeConfig();
acldvppSetJpegeConfigLevel(jpegeConfig_, 100);

// 6. Allocate output memory, that is, allocate device memory encodeOutBufferDev_ to store the encoded output data.
uint32_t outBufferSize= 0;
ret = acldvppJpegPredictEncSize(encodeInputDesc_, jpegeConfig_, &outBufferSize);
ret = acldvppMalloc(&encodeOutBufferDev_, outBufferSize);

// 7. Execute asynchronous encoding, and then call aclrtSynchronizeStream to block the program until all tasks in the specified stream are complete.
ret = acldvppJpegEncodeAsync(dvppChannelDesc_, encodeInputDesc_, encodeOutBufferDev_,
            &outBufferSize, jpegeConfig_, stream_);
ret = aclrtSynchronizeStream(stream_);

// 8. After encoding is complete, release resources, including the description information of the input/output images, the input/output memory, the channel description information, and the channel.
acldvppDestroyPicDesc(encodeInputDesc_);

if(runMode == ACL_HOST){ 
    // In this mode, because the processing result is on the device side, call the memory copy API to transfer the result data before releasing the device-side memory.
    // Allocate the host memory outputHostBuffer. 
    void* outputHostBuffer = nullptr;
    outputHostBuffer = malloc(outBufferSize);
    // Call aclrtMemcpy to transfer the processing result data from the device to the host.
    ret = aclrtMemcpy(outputHostBuffer, outBufferSize, encodeOutBufferDev_, outBufferSize, ACL_MEMCPY_DEVICE_TO_HOST);
    // Release the input and output device memory.
    (void)acldvppFree(inDevBuffer_);
    (void)acldvppFree(encodeOutBufferDev_);
    // After the data is used, release the memory.
    free(outputHostBuffer);
} else { 
    // In this case, the program runs on the device side and the processing result is also on the device side. You can process the result as needed and then release the device-side memory.
    (void)acldvppFree(inDevBuffer_);
    (void)acldvppFree(encodeOutBufferDev_);
}
acldvppDestroyChannel(dvppChannelDesc_);
(void)acldvppDestroyChannelDesc(dvppChannelDesc_);
dvppChannelDesc_ = nullptr;

....
```
