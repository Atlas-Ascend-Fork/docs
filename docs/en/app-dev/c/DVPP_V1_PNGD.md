# PNGD Image Decoding

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:31:22.457Z pushedAt=2026-10-26T03:10:39.422Z nl=2 -->

This section describes the API call process of PNGD image decoding, with sample code provided to help you understand the process.

PNGD (PNG decoder) is responsible for decoding PNG images. For details about the functions and usage constraints of PNGD, see [DVPP Media Acceleration Library](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/dvpp/dvpp_03_0000.html).

## API Call Process

**Figure 1**  PNG image decoding  
![](figures/PNGD_API_call_process_V1.png "PNG image decoding")

The current system supports PNG image decoding and can output images in RGB and RGBA encoding formats. The key APIs are described as follows:

1. Call **aclInit** to initialize the system.
2. Call **aclrtSetDevice** to specify the compute device.
3. Call **aclrtCreateStream** to create a stream.
4. Call **acldvppCreateChannel** to **create a channel for image data processing**.

    Before creating a channel for image data processing, call **acldvppCreateChannelDesc** to create the channel description.

5. Before implementing PNG image decoding, if you need to **allocate memory on the device** to store input or output data, call **acldvppMalloc** to allocate memory.

    Before allocating output memory, you can call **acldvppPngPredictDecSize** to calculate the output memory size required after PNG image decoding based on the memory that stores the PNG image data.

6. Call the **acldvppPngDecodeAsync** asynchronous API for **decoding**.

    For an asynchronous API, also call the **aclrtSynchronizeStream** API to block program execution until all tasks in the specified stream are complete.

7. After decoding is complete, call the **acldvppFree** API in a timely manner to **release the input and output memory**.
8. Call the **acldvppDestroyChannel** API to **destroy the image data processing channel**.

    After destroying the image data processing channel, call the **acldvppDestroyChannelDesc** API to destroy the channel description information.

9. Call the **aclrtDestroyStream** API to destroy the stream.
10. Call the **aclrtResetDevice** API to reset the device and release resources on the device.
11. Call the **aclFinalize** API to deinitialize the system and release the related resources used by the ACL APIs in the process.

## Sample Code

The following sample code shows the key steps of the PNGD image decoding function. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

```cpp
// 1. Create the channel description information for the image data processing channel. dvppChannelDesc_ is of the acldvppChannelDesc type.
dvppChannelDesc_ = acldvppCreateChannelDesc();

// 2. Create a channel for image data processing.
aclError ret = acldvppCreateChannel(dvppChannelDesc_);

// 3. Allocate input memory (distinguish the running status).
// Call aclrtGetRunMode to obtain the running mode of the software stack. If the running mode obtained by aclrtGetRunMode is ACL_HOST, use aclrtMemcpy to transfer the input image data to the device. After the data transfer is complete, release the memory in time. Otherwise, directly allocate and use the device memory.
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
    // Use aclrtMemcpy to transfer the input image data to the device.
    ret = aclrtMemcpy(inDevBuffer_, inDevBufferSize, inputHostBuff, inDevBufferSize, ACL_MEMCPY_HOST_TO_DEVICE);

} else {
    // Allocate device input memory inDevBuffer_.
    ret = acldvppMalloc(&inDevBuffer_, inDevBufferSize);
    // Read the input image into the memory. The custom function ReadPicFile is implemented by the user.
    ReadPicFile(picName, inDevBuffer_, inDevBufferSize);
}

// 4. Allocate decode output memory decodeOutDevBuffer_.
// Calculate the memory size required for the PNGD processing result.
uint32_t decodeOutBufferSize = 0;
ret = acldvppPngPredictDecSize(inputHostBuff, inDevBufferSize, PIXEL_FORMAT_RGB_888, &decodeOutBufferSize);
ret = acldvppMalloc(&decodeOutDevBuffer_, decodeOutBufferSize);
// Release the memory in time.
free(inputHostBuff);

// 5. Create the description of the decoded output image and set each attribute value.
// decodeOutputDesc is of the acldvppPicDesc type.
decodeOutputDesc_ = acldvppCreatePicDesc();
acldvppSetPicDescData(decodeOutputDesc_, decodeOutDevBuffer_);
acldvppSetPicDescFormat(decodeOutputDesc_, PIXEL_FORMAT_RGB_888); 
acldvppSetPicDescSize(decodeOutputDesc_, decodeOutBufferSize);

// 6. Execute asynchronous decoding, and then call aclrtSynchronizeStream to block program execution until all tasks in the specified stream are complete.
ret = acldvppPngDecodeAsync(dvppChannelDesc_, inDevBuffer_, inDevBufferSize, decodeOutputDesc_, stream_);
ret = aclrtSynchronizeStream(stream_);

// 7. After decoding is complete, release resources, including the description of the decoded output image, the decoded output memory, the channel description, and the channel.
acldvppDestroyPicDesc(decodeOutputDesc_);

if(runMode == ACL_HOST){ 
    // In this mode, because the processing result is on the device side, call the memory copy API to transfer the result data before releasing the device-side memory.
    // Allocate host memory OutHostBuffer.
    void* OutHostBuffer = nullptr;
    OutHostBuffer = malloc(decodeOutBufferSize);
    // Transfer the device processing result data to the host through aclrtMemcpy.
    ret = aclrtMemcpy(OutHostBuffer, decodeOutBufferSize, decodeOutDevBuffer_, decodeOutBufferSize, ACL_MEMCPY_DEVICE_TO_HOST);
    // Release the input and output device memory.
    (void)acldvppFree(inDevBuffer_);
    (void)acldvppFree(decodeOutDevBuffer_);
    // After the data is used, release the memory.
    free(OutHostBuffer);
} else { 
    // At this point, the program runs on the device side, and the processing result is also on the device side. You can process the result as needed, and then release the device-side memory.
    (void)acldvppFree(inDevBuffer_);
    (void)acldvppFree(decodeOutDevBuffer_);
}
acldvppDestroyChannel(dvppChannelDesc_);
(void)acldvppDestroyChannelDesc(dvppChannelDesc_);
dvppChannelDesc_ = nullptr;

....
```
