# Typical VPC Image Processing Functions

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:32:52.575Z pushedAt=2026-10-26T03:10:39.425Z nl=2 -->

This section uses image cropping and resizing as examples to describe the API call process for VPC image processing, and provides sample code for the following typical functions to help you understand the API call process.

VPC (Vision Preprocessing Core) is responsible for image processing functions and supports operations such as cropping, resizing, and format conversion on images. For details about VPC functions and usage constraints, see [DVPP Media Acceleration Library](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/dvpp/dvpp_03_0000.html).

## API Call Process (Image Cropping and Resizing as an Example)

**Figure 1** Image cropping and resizing process  
![](figures/crop_resize_process.png "Image cropping and resizing process")

The key APIs are described as follows (using image cropping and resizing as an example):

1. Call **aclInit** to initialize the system.
2. Call **aclrtSetDevice** to specify the compute device.
3. Call **aclrtCreateStream** to create a stream.
4. Call **acldvppCreateChannel** to **create a channel for image data processing**.

    Before creating a channel for image data processing, call **acldvppCreateChannelDesc** to create the channel description.

5. Call **acldvppCreateRoiConfig** and **acldvppCreateResizeConfig** to **create the cropping region configuration and the resizing configuration**, respectively, and call **acldvppSetResizeConfigInterpolation** to specify the resizing algorithm.
6. Before implementing image cropping and resizing, if you need to **allocate memory on the device** to store input or output data, call **acldvppMalloc** to allocate memory.
7. **Perform image cropping and resizing.**
    - About cropping:
        - Call the **acldvppVpcCropAsync** asynchronous API to crop from the input image in a specified region, and then store the cropped image in the output memory as the output image.

            When the output image region is inconsistent with the cropping region **cropArea**, the image is resized once again.

        - The system also provides the **acldvppVpcCropAndPasteAsync** asynchronous API, which supports cropping from the input image in a specified region and then pasting the cropped image to a specified position of the target image as the output image.
            - When the width and height of the cropping region **cropArea** are inconsistent with those of the pasting region **pasteArea**, the image is resized once again.
            - If the user needs to read the target image into memory for storing the output image and overlay the pasting region on the target image, they need to write code logic: after allocating output memory, read the target image into the output memory.

    - About resizing:
        - Call the **acldvppVpcResizeAsync** asynchronous API to resize the input image to the output image size.
        - After resizing, the output image memory is calculated based on the YUV420SP format. Calculation formula: aligned width \* aligned height \*3/2

    - For asynchronous APIs, you also need to call the **aclrtSynchronizeStream** API to block program execution until all tasks in the specified stream are complete.

8. Call the **acldvppFree** API to **release the input and output memory**.
9. Call the **acldvppDestroyRoiConfig** API and the **acldvppDestroyResizeConfig** API to **destroy the cropping region configuration and the resizing configuration**, respectively.
10. Call the **acldvppDestroyChannel** API to **destroy the channel for image data processing**.

    After destroying the channel for image data processing, call the **acldvppDestroyChannelDesc** API to destroy the channel description information.

11. Call the **aclrtDestroyStream** API to destroy the stream.
12. Call the **aclrtResetDevice** API to reset the device and release resources on the device.
13. Call the **aclFinalize** API to deinitialize the system and release the resources used by the acl APIs in the process.

## Image Resizing Sample Code

The following sample code shows the key steps of the image resizing function. They are for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

You can click [vpc\_resnet50\_imagenet\_classification](https://gitee.com/ascend/samples/tree/master/cplusplus/level2_simple_inference/1_classification/vpc_resnet50_imagenet_classification) to obtain the sample code.

```cpp
// 1. Create image resizing configuration data and specify the resizing algorithm.
// resizeConfig_ is of the acldvppResizeConfig type.
acldvppResizeConfig *resizeConfig_ = acldvppCreateResizeConfig();
aclError ret = acldvppSetResizeConfigInterpolation(resizeConfig_, 0);

// 2. Channel description information used when creating an image data processing channel. dvppChannelDesc_ is of the acldvppChannelDesc type.
dvppChannelDesc_ = acldvppCreateChannelDesc();

// 3. Create an image data processing channel.
ret = acldvppCreateChannel(dvppChannelDesc_);

// 4. Allocate input memory (distinguish the running status).
// Call aclrtGetRunMode to obtain the running mode of the software stack. If the running mode obtained by calling aclrtGetRunMode is ACL_HOST, use aclrtMemcpy to transfer the input image data to the device. After the data transfer is complete, release the memory in a timely manner. Otherwise, directly allocate and use the device memory.
aclrtRunMode runMode;
ret = aclrtGetRunMode(&runMode);
// inputPicWidth and inputPicHeight indicate the aligned width and aligned height of the image, respectively. Here, an image in YUV420SP format is used as an example.
uint32_t resizeInBufferSize = inputPicWidth * inputPicHeight * 3 / 2;
if(runMode == ACL_HOST){ 
    // Allocate host memory vpcInHostBuffer.
    void* vpcInHostBuffer = nullptr;
    vpcInHostBuffer = malloc(resizeInBufferSize);
    // Read the input image into memory. The custom function ReadPicFile is implemented by the user.
    ReadPicFile(picName, vpcInHostBuffer, resizeInBufferSize);
    // Allocate device memory resizeInDevBuffer_.
    ret = acldvppMalloc(&resizeInDevBuffer_, resizeInBufferSize);
    // Transfer the input image data to the device through the aclrtMemcpy API.
    ret = aclrtMemcpy(resizeInDevBuffer_, resizeInBufferSize, vpcInHostBuffer, resizeInBufferSize, ACL_MEMCPY_HOST_TO_DEVICE);
    // Release the memory in time after the data transfer is complete.
    free(vpcInHostBuffer);
} else {
    // Allocate device input memory resizeInDevBuffer_.
    ret = acldvppMalloc(&resizeInDevBuffer_, resizeInBufferSize);
    // Read the input image into memory. The custom function ReadPicFile is implemented by the user.
    ReadPicFile(picName, resizeInDevBuffer_, resizeInBufferSize);
}

// 5. Allocate resizing output memory resizeOutBufferDev_. The memory size resizeOutBufferSize_ is obtained based on the calculation formula.
// outputPicWidth and outputPicHeight represent the aligned width and aligned height of the image respectively. Here, an image in YUV420SP format is used as an example.
uint32_t resizeOutBufferSize_ = outputPicWidth * outputPicHeight * 3 / 2;
ret = acldvppMalloc(&resizeOutBufferDev_, resizeOutBufferSize_);

// 6. Create the description information of the resizing input image and set each attribute value.
// resizeInputDesc_ is of the acldvppPicDesc type.
resizeInputDesc_ = acldvppCreatePicDesc();
acldvppSetPicDescData(resizeInputDesc_, resizeInDevBuffer_);
acldvppSetPicDescFormat(resizeInputDesc_, PIXEL_FORMAT_YUV_SEMIPLANAR_420);
acldvppSetPicDescWidth(resizeInputDesc_, inputWidth_);
acldvppSetPicDescHeight(resizeInputDesc_, inputHeight_);
acldvppSetPicDescWidthStride(resizeInputDesc_, inputWidthStride);
acldvppSetPicDescHeightStride(resizeInputDesc_, inputHeightStride);
acldvppSetPicDescSize(resizeInputDesc_, resizeInBufferSize);

// 7. Create the description of the resized output image and set each attribute value.
// If the resized output image is used as the input of model inference, the width and height of the output image must be consistent with those required by the model.
// resizeOutputDesc_ is of the acldvppPicDesc type.
resizeOutputDesc_ = acldvppCreatePicDesc();
acldvppSetPicDescData(resizeOutputDesc_, resizeOutBufferDev_);
acldvppSetPicDescFormat(resizeOutputDesc_, PIXEL_FORMAT_YUV_SEMIPLANAR_420); 
acldvppSetPicDescWidth(resizeOutputDesc_, resizeOutputWidth_);
acldvppSetPicDescHeight(resizeOutputDesc_, resizeOutputHeight_);
acldvppSetPicDescWidthStride(resizeOutputDesc_, resizeOutputWidthStride);
acldvppSetPicDescHeightStride(resizeOutputDesc_, resizeOutputHeightStride);
acldvppSetPicDescSize(resizeOutputDesc_, resizeOutBufferSize_);

// 8. Execute asynchronous resizing, and then call aclrtSynchronizeStream to block the program until all tasks in the specified stream are complete.
ret = acldvppVpcResizeAsync(dvppChannelDesc_, resizeInputDesc_,
        resizeOutputDesc_, resizeConfig_, stream_);
ret = aclrtSynchronizeStream(stream_);

// 9. After resizing is complete, release resources, including the descriptions of the resized input/output images and the resized input/output memory.
acldvppDestroyPicDesc(resizeInputDesc_);
acldvppDestroyPicDesc(resizeOutputDesc_);

if(runMode == ACL_HOST){ 
    // In this mode, because the processing result is on the device side, call the memory copy API to transfer the result data before releasing the device-side memory.
    // Allocate host memory vpcOutHostBuffer.
    void* vpcOutHostBuffer = nullptr;
    vpcOutHostBuffer = malloc(resizeOutBufferSize_);
    // Transfer the processing result data from the device to the host through the aclrtMemcpy API.
    ret = aclrtMemcpy(vpcOutHostBuffer, resizeOutBufferSize_, resizeOutBufferDev_, resizeOutBufferSize_, ACL_MEMCPY_DEVICE_TO_HOST);
    // Release the input and output device memory.
    (void)acldvppFree(resizeInDevBuffer_);
    (void)acldvppFree(resizeOutBufferDev_);
    // Release the memory after the data is used.
    free(vpcOutHostBuffer);
} else { 
    // The code is running on the device side, and the processing result is also on the device side. You can process the result as needed and then release the memory on the device side.
    (void)acldvppFree(resizeInDevBuffer_);
    (void)acldvppFree(resizeOutBufferDev_);
}
acldvppDestroyChannel(dvppChannelDesc_);
(void)acldvppDestroyChannelDesc(dvppChannelDesc_);
dvppChannelDesc_ = nullptr;

 ....
```

## Format Conversion Sample Code

Format conversion supports the following two implementation methods:

- When implementing functions such as cropping and resizing, call the corresponding API (for example, **acldvppVpcCropAsync**) and set the input image format and output image format to different values to achieve image format conversion.
- If only image format conversion is required, you can also directly call the **acldvppVpcConvertColorAsync** API.

The following sample code shows the key steps of the format conversion function. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

```cpp
// 1. Create the channel description information for the image data processing channel. dvppChannelDesc_ is of the acldvppChannelDesc type.
dvppChannelDesc_ = acldvppCreateChannelDesc();

// 2. Create the image data processing channel.
aclError ret = acldvppCreateChannel(dvppChannelDesc_);

// 3. Allocate input memory (distinguish the running status).
// Call the aclrtGetRunMode API to obtain the running mode of the software stack. If the running mode obtained by calling the aclrtGetRunMode API is ACL_HOST, use the aclrtMemcpy API to transfer the input image data to the device. After the data transfer is complete, release the memory in a timely manner. Otherwise, directly allocate and use the device memory.
aclrtRunMode runMode;
ret = aclrtGetRunMode(&runMode);
// inputPicWidth and inputPicHeight indicate the aligned width and aligned height of the image, respectively. This example uses an image in YUV420SP format.
uint32_t inBufferSize = inputPicWidth * inputPicHeight * 3 / 2;
if(runMode == ACL_HOST){ 
    // Allocate host memory vpcInHostBuffer.
    void* vpcInHostBuffer = nullptr;
    vpcInHostBuffer = malloc(inBufferSize);
    // Read the input image into memory. The custom function ReadPicFile is implemented by the user.
    ReadPicFile(picName, vpcInHostBuffer, inBufferSize);
    // Allocate device memory inDevBuffer_.
    ret = acldvppMalloc(&inDevBuffer_, inBufferSize);
    // Transfer the input image data to the device by calling aclrtMemcpy.
    ret = aclrtMemcpy(inDevBuffer_, inBufferSize, vpcInHostBuffer, inBufferSize, ACL_MEMCPY_HOST_TO_DEVICE);
    // Release the memory in time after the data transfer is complete.
    free(vpcInHostBuffer);
} else {
    // Allocate device input memory inDevBuffer_.
    ret = acldvppMalloc(&inDevBuffer_, inBufferSize);
    // Read the input image into memory. The custom function ReadPicFile is implemented by the user.
    ReadPicFile(picName, inDevBuffer_, inBufferSize);
}

// 4. Allocate color space conversion output memory outBufferDev_. The memory size outBufferSize_ is obtained based on the calculation formula.
// outputPicWidth and outputPicHeight indicate the aligned width and aligned height of the image, respectively. Here, an image in YUV420SP format is used as an example.
uint32_t outBufferSize_ = outputPicWidth * outputPicHeight * 3 / 2;
ret = acldvppMalloc(&outBufferDev_, outBufferSize_);

// 5. Create the description of the color space conversion input image and set each attribute value
// inputDesc_ is of the acldvppPicDesc type.
inputDesc_ = acldvppCreatePicDesc();
acldvppSetPicDescData(inputDesc_, inDevBuffer_);
acldvppSetPicDescFormat(inputDesc_, PIXEL_FORMAT_YUV_SEMIPLANAR_420);
acldvppSetPicDescWidth(inputDesc_, inputWidth_);
acldvppSetPicDescHeight(inputDesc_, inputHeight_);
acldvppSetPicDescWidthStride(inputDesc_, inputWidthStride);
acldvppSetPicDescHeightStride(inputDesc_, inputHeightStride);
acldvppSetPicDescSize(inputDesc_, inBufferSize);

// 6. Create the description of the output image for color space conversion, and set each attribute value. The output width and height must be the same as those of the input.
// If the output image of color space conversion is used as the input of model inference, the width and height of the output image must be consistent with those required by the model.
// outputDesc_ is of the acldvppPicDesc type.
outputDesc_= acldvppCreatePicDesc();
acldvppSetPicDescData(outputDesc_, outBufferDev_);
acldvppSetPicDescFormat(outputDesc_, PIXEL_FORMAT_YUV_400); 
acldvppSetPicDescWidth(outputDesc_, outputWidth_);
acldvppSetPicDescHeight(outputDesc_, outputHeight_);
acldvppSetPicDescWidthStride(outputDesc_, outputWidthStride);
acldvppSetPicDescHeightStride(outputDesc_, outputHeightStride);
acldvppSetPicDescSize(outputDesc_, outBufferSize_);

// 7. Perform asynchronous color space conversion, and then call aclrtSynchronizeStream to block the program until all tasks in the specified stream are complete.
ret = acldvppVpcConvertColorAsync(dvppChannelDesc_, inputDesc_, outputDesc_, stream_);
ret = aclrtSynchronizeStream(stream_);

// 8. After color space conversion is complete, release resources, including the description of the input/output image and the input/output memory.
acldvppDestroyPicDesc(inputDesc_);
acldvppDestroyPicDesc(outputDesc_);

if(runMode == ACL_HOST){ 
    // In this mode, because the processing result is on the device side, call the memory copy API to transfer the result data before releasing the device-side memory.
    // Allocate the host memory vpcOutHostBuffer.
    void* vpcOutHostBuffer = nullptr;
    vpcOutHostBuffer = malloc(outBufferSize_);
    // Transfer the processing result data from the device to the host through the aclrtMemcpy API.
    ret = aclrtMemcpy(vpcOutHostBuffer, outBufferSize_, outBufferDev_, outBufferSize_, ACL_MEMCPY_DEVICE_TO_HOST);
    // Release the input and output device memory.
    (void)acldvppFree(inDevBuffer_);
    (void)acldvppFree(outBufferDev_);
    // Release the memory after the data is used.
    free(vpcOutHostBuffer);
} else { 
    // The process is running on the device side, and the processing result is also on the device side. You can process the result as needed and then release the memory on the device side.
    (void)acldvppFree(inDevBuffer_);
    (void)acldvppFree(outBufferDev_);
}
acldvppDestroyChannel(dvppChannelDesc_);
(void)acldvppDestroyChannelDesc(dvppChannelDesc_);
dvppChannelDesc_ = nullptr;

....
```

## Image Cropping and Resizing (One Image per Frame) Sample Code

Call the **acldvppVpcCropResizeAsync** asynchronous API to crop from the input image in a specified region, and then store the cropped image in the output memory as the output image. In addition, you can specify a resizing algorithm. When the output image region is inconsistent with the **cropArea**, the image is resized again.

The following sample code shows the key steps of image cropping and resizing. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

You can click [vpc\_jpeg\_resnet50\_imagenet\_classification](https://gitee.com/ascend/samples/tree/master/cplusplus/level2_simple_inference/1_classification/vpc_jpeg_resnet50_imagenet_classification) to obtain the sample code.

```cpp
// 1. Create the resizing configuration data and specify the position of the cropping region.
// resizeConfig_ is of the acldvppResizeConfig type.
resizeConfig_ = acldvppCreateResizeConfig();
aclError ret = acldvppSetResizeConfigInterpolation(resizeConfig_, 0);
// cropArea_ is of the acldvppRoiConfig type.
cropArea_ = acldvppCreateRoiConfig(550, 749, 480, 679);

// 2. Create the channel description information for the image data processing channel. dvppChannelDesc_ is of the acldvppChannelDesc type.
dvppChannelDesc_ = acldvppCreateChannelDesc();

// 3. Create the image data processing channel.
ret = acldvppCreateChannel(dvppChannelDesc_);

// 4. Allocate input memory (distinguish the running status).
// Call aclrtGetRunMode to obtain the running mode of the software stack. If the running mode obtained by aclrtGetRunMode is ACL_HOST, use aclrtMemcpy to transfer the input image data to the device. After the data transfer is complete, release the memory in time. Otherwise, directly allocate and use the device memory.
aclrtRunMode runMode;
ret = aclrtGetRunMode(&runMode);
// inputPicWidth and inputPicHeight indicate the aligned width and aligned height of the image respectively. This example uses an image in YUV420SP format.
uint32_t cropInBufferSize = inputPicWidth * inputPicHeight * 3 / 2;
if(runMode == ACL_HOST){ 
    // Allocate host memory cropInHostBuffer.
    void* cropInHostBuffer = nullptr;
    cropInHostBuffer = malloc(cropInBufferSize);
    // Read the input image into the memory. The custom function ReadPicFile is implemented by the user.
    ReadPicFile(picName, cropInHostBuffer, cropInBufferSize);
    // Allocate device memory cropInDevBuffer_.
    ret = acldvppMalloc(&cropInDevBuffer_, cropInBufferSize);
    // Use aclrtMemcpy to transfer the image data to the device.
    ret = aclrtMemcpy(cropInDevBuffer_, cropInBufferSize, cropInHostBuffer, cropInBufferSize, ACL_MEMCPY_HOST_TO_DEVICE);
    // Release the memory in time after the data transfer is complete.
    free(cropInHostBuffer);
} else { 
    // Allocate device input memory cropInDevBuffer_.
    ret = acldvppMalloc(&cropInDevBuffer_, cropInBufferSize);
    // Read the input image into the memory. The custom function ReadPicFile is implemented by the user.
    ReadPicFile(picName, cropInDevBuffer_, cropInBufferSize);
}

// 5. Allocate device output memory cropOutBufferDev_. The memory size cropOutBufferSize_ is calculated using the formula.
// outputPicWidth and outputPicHeight indicate the aligned width and aligned height of the image respectively. This example uses a YUV420SP image.
uint32_t cropOutBufferSize_ = outputPicWidth * outputPicHeight * 3 / 2;
ret = acldvppMalloc(&cropOutBufferDev_, cropOutBufferSize_);

// 6. Create the description of the input image and set each attribute value. cropInputDesc_ is of the acldvppPicDesc type.
cropInputDesc_ = acldvppCreatePicDesc();
acldvppSetPicDescData(cropInputDesc_, cropInDevBuffer_);
acldvppSetPicDescFormat(cropInputDesc_, PIXEL_FORMAT_YUV_SEMIPLANAR_420);
acldvppSetPicDescWidth(cropInputDesc_, inputWidth_);
acldvppSetPicDescHeight(cropInputDesc_, inputHeight_);
acldvppSetPicDescWidthStride(cropInputDesc_, inputWidthStride);
acldvppSetPicDescHeightStride(cropInputDesc_, inputHeightStride);
acldvppSetPicDescSize(cropInputDesc_, cropInBufferSize);

// 7. Create the description of the output image and set each attribute value. cropOutputDesc_ is of the acldvppPicDesc type.
// If the output image of cropping is used as the input of model inference, the width and height of the output image must be consistent with those required by the model.
cropOutputDesc_ = acldvppCreatePicDesc();
acldvppSetPicDescData(cropOutputDesc_, cropOutBufferDev_);
acldvppSetPicDescFormat(cropOutputDesc_, PIXEL_FORMAT_YUV_SEMIPLANAR_420); 
acldvppSetPicDescWidth(cropOutputDesc_, OutputWidth_);
acldvppSetPicDescHeight(cropOutputDesc_, OutputHeight_);
acldvppSetPicDescWidthStride(cropOutputDesc_, OutputWidthStride);
acldvppSetPicDescHeightStride(cropOutputDesc_, OutputHeightStride);
acldvppSetPicDescSize(cropOutputDesc_, cropOutBufferSize_);

// 8. Perform asynchronous image cropping and resizing, and then call aclrtSynchronizeStream to block the program until all tasks in the specified stream are complete.
ret = acldvppVpcCropResizeAsync(dvppChannelDesc_, cropInputDesc_,
        cropOutputDesc_, cropArea_, resizeConfig_, stream_);
ret = aclrtSynchronizeStream(stream_);

// 9. Release resources, including the descriptions of the input/output images, input/output memory, channel description, and channel.
acldvppDestroyRoiConfig(cropArea_);
acldvppDestroyResizeConfig(resizeConfig_);
acldvppDestroyPicDesc(cropInputDesc_);
acldvppDestroyPicDesc(cropOutputDesc_);
if(runMode == ACL_HOST){ 
    // In this mode, because the processing result is on the device side, call the memory copy API to transfer the result data before releasing the device-side memory.
    // Allocate host memory cropOutHostBuffer.
    void* cropOutHostBuffer = nullptr;
    cropOutHostBuffer = malloc(cropOutBufferSize_);
    // Transfer the processing result data from the device to the host through the aclrtMemcpy API.
    ret = aclrtMemcpy(cropOutHostBuffer, cropOutBufferSize_, cropOutBufferDev_, cropOutBufferSize_, ACL_MEMCPY_DEVICE_TO_HOST);
    // Release the input and output device memory.
    (void)acldvppFree(cropInDevBuffer_);
    (void)acldvppFree(cropOutBufferDev_);
    // Release the memory after the data is used.
    free(cropOutHostBuffer);
} else { 
    // The code is running on the device side, and the processing result is also on the device side. You can process the cropped image as needed, and then release the device-side memory.
    (void)acldvppFree(cropInDevBuffer_);
    (void)acldvppFree(cropOutBufferDev_);
}
acldvppDestroyChannel(dvppChannelDesc_);
(void)acldvppDestroyChannelDesc(dvppChannelDesc_);
dvppChannelDesc_ = nullptr;

....
```

## Image Cropping, Pasting, and Resizing (One Image per Frame) Sample Code

Call the **acldvppVpcCropResizePasteAsync** asynchronous API to crop from the input image in a specified region, then paste the cropped image to a specified position of the target image as the output image. In addition, a resizing algorithm can be specified. When the width and height of the cropping region **cropArea** are different from those of the pasting region **pasteArea**, the image is resized once more. If the user needs to read the target image into memory for storing the output image and overlay the pasting region on the target image, they need to write code logic: after allocating output memory, read the target image into the output memory.

The following sample code shows the key steps of the image cropping, pasting, and resizing function. They are for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

You can click [vpc\_jpeg\_resnet50\_imagenet\_classification](https://gitee.com/ascend/samples/tree/master/cplusplus/level2_simple_inference/1_classification/vpc_jpeg_resnet50_imagenet_classification) to obtain the sample code.

```cpp
// 1. Create the resizing configuration data, and specify the position of the cropping region and the position of the pasting region.
// resizeConfig_ is of the acldvppResizeConfig type.
resizeConfig_ = acldvppCreateResizeConfig();
aclError ret = acldvppSetResizeConfigInterpolation(resizeConfig_, 0);
// cropArea_ and pasteArea_ are of the acldvppRoiConfig type.
cropArea_ = acldvppCreateRoiConfig(512, 711, 512, 711);
pasteArea_ = acldvppCreateRoiConfig(16, 215, 16, 215);

// 2. Create the channel description information when creating the image data processing channel. dvppChannelDesc_ is of the acldvppChannelDesc type.
dvppChannelDesc_ = acldvppCreateChannelDesc();

// 3. Create the image data processing channel.
ret = acldvppCreateChannel(dvppChannelDesc_);

// 4. Allocate input memory (distinguish the running status).
// Call aclrtGetRunMode to obtain the run mode of the software stack. If the run mode obtained by calling aclrtGetRunMode is ACL_HOST, use aclrtMemcpy to transfer the input image data to the device. After the data transfer is complete, release the memory in time. Otherwise, directly allocate and use the device memory.
aclrtRunMode runMode;
ret = aclrtGetRunMode(&runMode);
// inputPicWidth and inputPicHeight indicate the aligned width and aligned height of the image, respectively. This example uses an image in YUV420SP format.
uint32_t vpcInBufferSize = inputPicWidth * inputPicHeight * 3 / 2;
if(runMode == ACL_HOST){ 
    // Allocate host memory vpcInHostBuffer.
    void* vpcInHostBuffer = nullptr;
    vpcInHostBuffer = malloc(vpcInBufferSize);
    // Read the input image into the memory. The custom function ReadPicFile is implemented by the user.
    ReadPicFile(picName, vpcInHostBuffer, vpcInBufferSize);
    // Allocate device memory vpcInDevBuffer_.
    ret = acldvppMalloc(&vpcInDevBuffer_, vpcInBufferSize);
    // Use aclrtMemcpy to transfer the input image data to the device.
    ret = aclrtMemcpy(vpcInDevBuffer_, vpcInBufferSize, vpcInHostBuffer, vpcInBufferSize, ACL_MEMCPY_HOST_TO_DEVICE);
    // After the data transfer is complete, release the memory in time.
    free(vpcInHostBuffer);
} else {
    // Allocate device input memory vpcInDevBuffer_.
    ret = acldvppMalloc(&vpcInDevBuffer_, vpcInBufferSize);
    // Read the input image into the memory. The custom function ReadPicFile is implemented by the user.
    ReadPicFile(picName, vpcInDevBuffer_, vpcInBufferSize);
}

// 5. Allocate output memory vpcOutBufferDev_. The memory size vpcOutBufferSize_ is obtained based on the calculation formula.
// outputPicWidth and outputPicHeight indicate the aligned width and aligned height of the image respectively. This example uses an image in YUV420SP format.
uint32_t vpcOutBufferSize_ = outputPicWidth * outputPicHeight * 3 / 2;
ret = acldvppMalloc(&vpcOutBufferDev_, vpcOutBufferSize_);

// 6. Create the description information of the input image and set each attribute value.
// In this example, the output memory of decoding is used as the input of cropping and pasting. vpcInputDesc_ is of the acldvppPicDesc type.
vpcInputDesc_ = acldvppCreatePicDesc();
acldvppSetPicDescData(vpcInputDesc_, decodeOutBufferDev_); 
acldvppSetPicDescFormat(vpcInputDesc_, PIXEL_FORMAT_YUV_SEMIPLANAR_420);
acldvppSetPicDescWidth(vpcInputDesc_, inputWidth_);
acldvppSetPicDescHeight(vpcInputDesc_, inputHeight_);
acldvppSetPicDescWidthStride(vpcInputDesc_, jpegOutWidthStride);
acldvppSetPicDescHeightStride(vpcInputDesc_, jpegOutHeightStride);
acldvppSetPicDescSize(vpcInputDesc_, jpegOutBufferSize);

// 7. Create the description information of the output image and set each attribute value.
// If the output image of cropping and pasting is used as the input of model inference, the width and height of the output image must be consistent with those required by the model.
// vpcOutputDesc_ is of the acldvppPicDesc type.
vpcOutputDesc_ = acldvppCreatePicDesc();
acldvppSetPicDescData(vpcOutputDesc_, vpcOutBufferDev_);
acldvppSetPicDescFormat(vpcOutputDesc_, PIXEL_FORMAT_YUV_SEMIPLANAR_420);
acldvppSetPicDescWidth(vpcOutputDesc_, dvppOutWidth);
acldvppSetPicDescHeight(vpcOutputDesc_, dvppOutHeight);
acldvppSetPicDescWidthStride(vpcOutputDesc_, dvppOutWidthStride);
acldvppSetPicDescHeightStride(vpcOutputDesc_, dvppOutHeightStride);
acldvppSetPicDescSize(vpcOutputDesc_, vpcOutBufferSize_);

// 8. Perform asynchronous cropping, pasting, and resizing, and then call the aclrtSynchronizeStream API to block program running until all tasks in the specified stream are complete.
ret = acldvppVpcCropResizePasteAsync(dvppChannelDesc_, vpcInputDesc_,
        vpcOutputDesc_, cropArea_, pasteArea_, resizeConfig_, stream_);
ret = aclrtSynchronizeStream(stream_);

// 9. Release resources, including the description information of the input/output images, input/output memory, channel description information, and channels.
acldvppDestroyRoiConfig(cropArea_);
acldvppDestroyRoiConfig(pasteArea_);
acldvppDestroyResizeConfig(resizeConfig_);
acldvppDestroyPicDesc(vpcInputDesc_);
acldvppDestroyPicDesc(vpcOutputDesc_);

if(runMode == ACL_HOST){ 
    // In this mode, since the processing result is on the device side, call the memory copy API to transfer the result data before releasing the device-side memory.
    // Allocate host memory vpcOutHostBuffer.
    void* vpcOutHostBuffer = nullptr;
    vpcOutHostBuffer = malloc(vpcOutBufferSize_);
    // Transfer the processing result data from the device to host through the aclrtMemcpy API.
    ret = aclrtMemcpy(vpcOutHostBuffer, vpcOutBufferSize_, vpcOutBufferDev_, vpcOutBufferSize_, ACL_MEMCPY_DEVICE_TO_HOST);
    // Release the input and output device memory.
    (void)acldvppFree(vpcInDevBuffer_);
    (void)acldvppFree(vpcOutBufferDev_);
    // Release the memory after the data is used.
    free(vpcOutHostBuffer);
} else { 
    // At this point, the code runs on the device side, and the processing result is also on the device side. You can process the result as needed and then release the device-side memory.
    (void)acldvppFree(vpcInDevBuffer_);
    (void)acldvppFree(vpcOutBufferDev_);
}

acldvppDestroyChannel(dvppChannelDesc_);
(void)acldvppDestroyChannelDesc(dvppChannelDesc_);
dvppChannelDesc_ = nullptr;

....
```

## Cropping and Pasting (Multiple Frames per Image) Sample Code

Call the **acldvppVpcBatchCropAndPasteAsync** asynchronous API to crop from image in the specified region, then crop the image and paste image to the specified position of the target image as output image. When the width and height of the cropping region **cropArea** and the pasting region **pasteArea** are different, the image then undergoes one resizing operation. If users need to read target image into memory for storing the output image and overlay the pasting region on the target image, they need to write code logic: when allocating output memory, read target image into output memory.

The following sample code shows the key steps. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

```cpp
// 1. Specify the positions of the batch cropping regions and the batch pasting regions. cropAreas_ and pasteAreas_ are of the acldvppRoiConfig type.
acldvppRoiConfig *cropAreas_[2], pasteAreas_[2];
cropAreas_[0] = acldvppCreateRoiConfig(512, 711, 512, 711);
cropAreas_[1] = acldvppCreateRoiConfig(512, 711, 512, 711);
pasteAreas_[0] = acldvppCreateRoiConfig(16, 215, 16, 215);
pasteAreas_[1] = acldvppCreateRoiConfig(16, 215, 16, 215);

// 2. Channel description information for creating an image data processing channel. dvppChannelDesc_ is of the acldvppChannelDesc type.
dvppChannelDesc_ = acldvppCreateChannelDesc();

// 3. Create an image data processing channel.
aclError ret = acldvppCreateChannel(dvppChannelDesc_);

// 4. Allocate input memory (distinguish the running status)
// Call aclrtGetRunMode to obtain the running mode of the software stack. If the running mode obtained by calling aclrtGetRunMode is ACL_HOST, call aclrtMemcpy to transfer the input image data to the device. After the data transfer is complete, release the memory in a timely manner. Otherwise, directly allocate and use the device memory.
aclrtRunMode runMode;
ret = aclrtGetRunMode(&runMode);
// inputPicWidth and inputPicHeight indicate the aligned width and aligned height of the image respectively. This example uses an image in YUV420SP format.
uint32_t vpcInBufferSize = inputPicWidth * inputPicHeight * 3 / 2;
if(runMode == ACL_HOST){ 
    // Allocate host memory vpcInHostBuffer
    void* vpcInHostBuffer = nullptr;
    vpcInHostBuffer = malloc(vpcInBufferSize);
    // Read the input image into memory. The custom function ReadPicFile is implemented by the user.
    ReadPicFile(picName, vpcInHostBuffer, vpcInBufferSize);
    // Allocate the device memory vpcInDevBuffer_.
    ret = acldvppMalloc(&vpcInDevBuffer_, vpcInBufferSize);
    // Transfer the image data from the host to the device through the aclrtMemcpy API.
    ret = aclrtMemcpy(vpcInDevBuffer_, vpcInBufferSize, vpcInHostBuffer, vpcInBufferSize, ACL_MEMCPY_HOST_TO_DEVICE);
    // Release the memory in time after the data transfer is complete.
    free(vpcInHostBuffer);
} else {
    // Allocate the device input memory vpcInDevBuffer_.
    ret = acldvppMalloc(&vpcInDevBuffer_, vpcInBufferSize);
    // Read the input image into memory. The custom function ReadPicFile is implemented by the user.
    ReadPicFile(picName, vpcInDevBuffer_, vpcInBufferSize);
}

// 5. Allocate the output memory vpcOutBufferDev_. The memory size vpcOutBufferSize_ is obtained based on the calculation formula.
// outputPicWidth and outputPicHeight indicate the aligned width and aligned height of the image, respectively. Here, a YUV420SP image is used as an example.
uint32_t vpcOutBufferSize_ = outputPicWidth * outputPicHeight * 3 / 2;
ret = acldvppMalloc(&vpcOutBufferDev_, vpcOutBufferSize_);

// 6. Create the description of the input image and set each attribute value.
// In this example, the output memory of decoding is used as the input for image cropping and pasting. vpcInputDesc_ is of the acldvppPicDesc type.
vpcInputBatchDesc_ = acldvppCreateBatchPicDesc(1);
vpcInputDesc_ = acldvppGetPicDesc(vpcInputBatchDesc_, 0);
acldvppSetPicDescData(vpcInputDesc_, decodeOutBufferDev_); 
acldvppSetPicDescFormat(vpcInputDesc_, PIXEL_FORMAT_YUV_SEMIPLANAR_420);
acldvppSetPicDescWidth(vpcInputDesc_, inputWidth_);
acldvppSetPicDescHeight(vpcInputDesc_, inputHeight_);
acldvppSetPicDescWidthStride(vpcInputDesc_, jpegOutWidthStride);
acldvppSetPicDescHeightStride(vpcInputDesc_, jpegOutHeightStride);
acldvppSetPicDescSize(vpcInputDesc_, jpegOutBufferSize);

// 7. Create the description information of the batch output images, and set each attribute value.
// If the output image of cropping and pasting is used as the input of model inference, the width and height of the output image must be consistent with those required by the model.
// vpcOutputDesc_ is of the acldvppPicDesc type.
vpcOutputBatchDesc_ = acldvppCreateBatchPicDesc(2);
for (uint32_t index=0; index<2; ++index){
     vecOutPtr_.push_back(vpcOutBufferDev_);
     vpcOutputDesc_ = acldvppGetPicDesc(vpcInputBatchDesc_, index);
    acldvppSetPicDescData(vpcOutputDesc_, vpcOutBufferDev_);
    acldvppSetPicDescFormat(vpcOutputDesc_, PIXEL_FORMAT_YUV_SEMIPLANAR_420);
    acldvppSetPicDescWidth(vpcOutputDesc_, dvppOutWidth);
    acldvppSetPicDescHeight(vpcOutputDesc_, dvppOutHeight);
    acldvppSetPicDescWidthStride(vpcOutputDesc_, dvppOutWidthStride);
    acldvppSetPicDescHeightStride(vpcOutputDesc_, dvppOutHeightStride);
    acldvppSetPicDescSize(vpcOutputDesc_, vpcOutBufferSize_);
}

// 8. Create roiNums. Each image corresponds to the number of crops and pastes required.

uint32_t totalNum = 0;
std::unique_ptr<uint32_t[]> roiNums(new (std::nothrow) uint32_t[1]);
roiNums[0]=2;
// 9. Perform asynchronous cropping and pasting, then call the aclrtSynchronizeStream API to block program execution until all tasks in the specified stream are complete.
ret = acldvppVpcBatchCropAndPasteAsync(dvppChannelDesc_, vpcInputBatchDesc_, roiNums.get(), 1,
        vpcOutputBatchDesc_, cropAreas_, pasteAreas_, stream_);
ret = aclrtSynchronizeStream(stream_);

// 10. After cropping and pasting is complete, release resources, including the description information of input/output images, input/output memory, channel description information, and channels.
acldvppDestroyRoiConfig(cropAreas_[0]);
acldvppDestroyRoiConfig(cropAreas_[1]);
acldvppDestroyRoiConfig(pasteAreas_[0]);
acldvppDestroyRoiConfig(pasteAreas_[1]);
(void)acldvppFree(vpcInDevBuffer_);
for(uint32_t index=0; index<2; ++index){
if(runMode == ACL_HOST){ 
    // In this mode, because the processing result is on the device side, call the memory copy API to transfer the result data before releasing the device-side memory.
    // Allocate host memory vpcOutHostBuffer.
    void* vpcOutHostBuffer = nullptr;
    vpcOutHostBuffer = malloc(vpcOutBufferSize_);
    // Use the aclrtMemcpy API to transfer the device processing result data to the host.
    ret = aclrtMemcpy(vpcOutHostBuffer, vpcOutBufferSize_, vpcOutBufferDev_, vpcOutBufferSize_, ACL_MEMCPY_DEVICE_TO_HOST);
    // Release the input and output device memory.
    (void)acldvppFree(vpcOutBufferDev_);
    // Release the memory after the data is used.
    free(vpcOutHostBuffer);
} else { 
    // At this point, the code runs on the device side and the processing result is also on the device side. You can process the result as needed and then release the memory on the device side.
    
    (void)acldvppFree(vpcOutBufferDev_);
}
}
acldvppDestroyBatchPicDesc(vpcInputDesc_);
acldvppDestroyBatchPicDesc(vpcOutputDesc_);
acldvppDestroyChannel(dvppChannelDesc_);
(void)acldvppDestroyChannelDesc(dvppChannelDesc_);
dvppChannelDesc_ = nullptr;

....
```
