# JPEGD Image Decoding

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:30:29.265Z pushedAt=2026-10-26T03:10:39.420Z nl=2 -->

This section describes the API call process of JPEGD image decoding, and provides sample code to help you understand the process.

JPEGD (JPEG Decoder) is responsible for image decoding, decoding .jpg, .jpeg, .JPG, and .JPEG images into YUV format images. For details about the JPEGD functions and usage constraints, see [DVPP Media Acceleration Library](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/dvpp/dvpp_03_0000.html).

## API Call Process

**Figure 1** JPEG image decoding  
![](figures/JPEGD_API_call_process_V1.png "JPEG image decoding")

The current system supports decoding of .jpg, .jpeg, .JPG, and .JPEG images. For different source image encoding formats, images in different encoding formats are output. The key APIs are described as follows:

1. Call **aclInit** to initialize the system.
2. Call **aclrtSetDevice** to specify the compute device.
3. Call **aclrtCreateStream** to create a stream.
4. Call **acldvppCreateChannel** to **create a channel for image data processing**.

    Before creating a channel for image data processing, call **acldvppCreateChannelDesc** to create the channel description.

5. Before implementing JPEG image decoding, if you need to **allocate memory on the device** to store input or output data, call **acldvppMalloc** to allocate memory.

    Before allocating output memory, you can call **acldvppJpegPredictDecSize** based on the memory that stores the JPEG image data to estimate the size of the output memory required after JPEG image decoding.

    The actual output memory size may differ from the size estimated by calling **acldvppJpegPredictDecSize**. To obtain the actual output memory size after decoding, call **acldvppGetPicDescSize** of the **acldvppPicDesc** type.

6. Call the **acldvppJpegDecodeAsync** asynchronous API to perform **decoding**.

    For asynchronous APIs, you also need to call **aclrtSynchronizeStream** to block the program until all tasks in the specified stream are complete.

7. After decoding is complete, call **acldvppFree** in a timely manner to **release the input and output memory**.
8. Call **acldvppDestroyChannel** to **destroy the image data processing channel**.

    After destroying the image data processing channel, call **acldvppDestroyChannelDesc** to destroy the channel description.

9. Call **aclrtDestroyStream** to destroy the stream.
10. Call **aclrtResetDevice** to reset the device and release the resources on the device.
11. Call **aclFinalize** to deinitialize the system and release the resources used by the ACL APIs in the process.

## Sample Code

The following sample code shows the key steps of the JPEGD image decoding function. They are for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

You can click [vpc\_jpeg\_resnet50\_imagenet\_classification](https://gitee.com/ascend/samples/tree/master/cplusplus/level2_simple_inference/1_classification/vpc_jpeg_resnet50_imagenet_classification) to obtain the sample code.

```cpp
// 1. Channel description for creating an image data processing channel. dvppChannelDesc_ is of the acldvppChannelDesc type.
dvppChannelDesc_ = acldvppCreateChannelDesc();

// 2. Create an image data processing channel.
aclError ret = acldvppCreateChannel(dvppChannelDesc_);

// 3. Allocate input memory (distinguish the running status).
// Call aclrtGetRunMode to obtain the running mode of the software stack. If the running mode returned by aclrtGetRunMode is ACL_HOST, call aclrtMemcpy to transfer the input image data to the device. After the data transfer is complete, release the memory in a timely manner. Otherwise, directly allocate and use the device memory.
aclrtRunMode runMode;
ret = aclrtGetRunMode(&runMode);
if(runMode == ACL_HOST){
    // Allocate host memory inputHostBuff and read the input image into this address. inDevBufferSize is the size of the read image.
    void* inputHostBuff = nullptr;
    inputHostBuff = malloc(inDevBufferSize);
    // Read the input image into the memory. The custom function ReadPicFile is implemented by the user.
    ReadPicFile(picName, inputHostBuff, inDevBufferSize);
    // Allocate device memory inDevBuffer_.
    ret = acldvppMalloc(&inDevBuffer_, inDevBufferSize);
    // Call aclrtMemcpy to transfer the input image data to the device.
    ret = aclrtMemcpy(inDevBuffer_, inDevBufferSize, inputHostBuff, inDevBufferSize, ACL_MEMCPY_HOST_TO_DEVICE);

} else {
    // Allocate device input memory inDevBuffer_.
    ret = acldvppMalloc(&inDevBuffer_, inBufferSize);
    // Read the input image into the memory. The custom function ReadPicFile is implemented by the user.
    ReadPicFile(picName, inDevBuffer_, inBufferSize);
}

// 4. Allocate the decoding output memory decodeOutDevBuffer_.
// Estimate the memory size required for the JPEGD processing result.
uint32_t decodeOutBufferSize = 0;
ret = acldvppJpegPredictDecSize(inputHostBuff, inDevBufferSize, PIXEL_FORMAT_YVU_SEMIPLANAR_420, &decodeOutBufferSize);
ret = acldvppMalloc(&decodeOutDevBuffer_, decodeOutBufferSize);
// Release the memory in a timely manner.
free(inputHostBuff);

// 5. Create the description of the decoding output image and set the attribute values.
// decodeOutputDesc is of the acldvppPicDesc type.
decodeOutputDesc_ = acldvppCreatePicDesc();
acldvppSetPicDescData(decodeOutputDesc_, decodeOutDevBuffer_);
acldvppSetPicDescFormat(decodeOutputDesc_, PIXEL_FORMAT_YUV_SEMIPLANAR_420); 
acldvppSetPicDescWidth(decodeOutputDesc_, inputWidth_);
acldvppSetPicDescHeight(decodeOutputDesc_, inputHeight_);
acldvppSetPicDescWidthStride(decodeOutputDesc_, decodeOutWidthStride);
acldvppSetPicDescHeightStride(decodeOutputDesc_, decodeOutHeightStride);
acldvppSetPicDescSize(decodeOutputDesc_, decodeOutBufferSize);

// 6. Execute asynchronous decoding, and then call aclrtSynchronizeStream to block the program until all tasks in the specified stream are complete.
ret = acldvppJpegDecodeAsync(dvppChannelDesc_, inDevBuffer_, inDevBufferSize, decodeOutputDesc_, stream_);
ret = aclrtSynchronizeStream(stream_);

// 7. After decoding is complete, release the resources, including the description of the decoding output image, the decoding output memory, the channel description, and the channel.
acldvppDestroyPicDesc(decodeOutputDesc_);

if(runMode == ACL_HOST){ 
    // In this mode, because the processing result is on the device side, call the memory copy API to transfer the result data before releasing the device-side memory.
    // Allocate the host memory vpcOutHostBuffer.
    void* vpcOutHostBuffer = nullptr;
    vpcOutHostBuffer = malloc(decodeOutBufferSize);
    // Copy the processing result data from the device to the host through the aclrtMemcpy API.
    ret = aclrtMemcpy(vpcOutHostBuffer, decodeOutBufferSize, decodeOutDevBuffer_, decodeOutBufferSize, ACL_MEMCPY_DEVICE_TO_HOST);
    // Release the input and output device memory.
    (void)acldvppFree(inDevBuffer_);
    (void)acldvppFree(decodeOutDevBuffer_);
    // Release the memory after the data is used.
    free(vpcOutHostBuffer);
} else { 
    // The code is running on the device side and the processing result is also on the device side. You can process the result as needed and then release the device-side memory.
    (void)acldvppFree(inDevBuffer_);
    (void)acldvppFree(decodeOutDevBuffer_);
}
acldvppDestroyChannel(dvppChannelDesc_);
(void)acldvppDestroyChannelDesc(dvppChannelDesc_);
dvppChannelDesc_ = nullptr;

....
```
