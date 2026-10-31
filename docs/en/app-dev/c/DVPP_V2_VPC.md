# Typical VPC Image Processing Functions

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:35:30.433Z pushedAt=2026-10-26T03:10:39.429Z nl=2 -->

This section uses cropping and resizing as examples to describe the API call process for VPC image processing, and provides sample code for the following typical functions to help you understand the call flow.

Vision Preprocessing Core (VPC) is responsible for image processing and supports operations such as cropping, resizing, and format conversion on images. For details about VPC functions and usage constraints, see [DVPP Media Acceleration Library](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/dvpp/dvpp_03_0000.html).

## Typical Function API Call Flow (Resizing as an Example)

**Figure 1**  Resizing call flow  
![](figures/resize_API_call_process.png "Resizing call flow")

The current system supports cropping, resizing, and other processing on input images. The key APIs are described as follows:

1. Call **aclInit** to initialize the system.
2. Call **aclrtSetDevice** to specify the compute device.
3. Call the **hi\_mpi\_sys\_init** API to perform **media data processing system initialization**.
4. Call the **hi\_mpi\_vpc\_sys\_create\_chn** API to **create a channel**.
5. Call the **hi\_mpi\_dvpp\_malloc** API to **allocate memory on the device** to store input or output data.
6. **Execute the image processing task.** This step uses resizing as an example.

    Call the **hi\_mpi\_vpc\_resize** API to resize the image. The **hi\_mpi\_vpc\_resize** API is an asynchronous API. A successful call to this API only indicates that the task has been delivered. You also need to call the **hi\_mpi\_vpc\_get\_process\_result** API to wait for the task to complete.

    - You can call the **hi\_mpi\_vpc\_get\_process\_result** API in the same thread as the **hi\_mpi\_vpc\_resize** API, or start a new thread to call the **hi\_mpi\_vpc\_get\_process\_result** API. The latter enables multi-thread parallelism to improve efficiency, but you need to implement inter-thread synchronization by yourself.
    - When calling the resizing API, you can convert the image format by setting the input image format and output image format to different values.
    <!-- npu="950,A3,910b,910,310p,310b" id1 -->
    - If DVPP APIs are called on the host, the result data of image processing is stored in the memory of the device. To access the result data, you need to transfer the result data back to the host side.
    <!-- end id1 -->

7. Call the **hi\_mpi\_dvpp\_free** API to **release the input and output memory**.
8. Call the **hi\_mpi\_vpc\_destroy\_chn** API to **destroy the channel**.
9. Call the **hi\_mpi\_sys\_exit** API to **deinitialize the media data processing system**.
10. Call the **aclrtResetDevice** API to reset the device and release the resources on the device.
11. Call the **aclFinalize** API to deinitialize the system and release the resources used by the ACL APIs in the process.

## Image Resizing Sample Code

The following sample code shows the key steps of the image resizing function. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

<!-- npu="310p" id2 -->
You can click [vpc\_sample](https://gitee.com/ascend/samples/tree/master/cplusplus/level1_single_api/7_dvpp/vpc_sample) to obtain the sample code.
<!-- end id2 -->

```cpp
// ....

// 1. Initialize the media data processing system.
int32_t ret = hi_mpi_sys_init();

// 2. Create a channel.
hi_vpc_chn chnId;
hi_vpc_chn_attr stChnAttr;
ret = hi_mpi_vpc_sys_create_chn(&chnId, &stChnAttr);

// 3. Perform resizing.
// 3.1 Construct the structure for storing input image information.
hi_vpc_pic_info inputPic;
inputPic.picture_width = 1920;
inputPic.picture_height = 1080;
inputPic.picture_format = HI_PIXEL_FORMAT_YUV_SEMIPLANAR_420;
inputPic.picture_width_stride = 1920;
inputPic.picture_height_stride = 1080;
inputPic.picture_buffer_size = inputPic.picture_width_stride * inputPic.picture_height_stride * 3 / 2;

// 3.2 Prepare the input image data.
// Read the input image into the device memory. The custom function ReadPicFile is implemented by the user.
ReadPicFile(picName, inputPic.picture_address, inputPic.picture_buffer_size);

// 3.3 Construct the structure for storing output image information.
hi_vpc_pic_info outputPic;
outputPic.picture_width = 960;
outputPic.picture_height  = 540;
outputPic.picture_format = HI_PIXEL_FORMAT_YUV_SEMIPLANAR_420;
outputPic.picture_width_stride = 960;
outputPic.picture_height_stride = 540;
outputPic.picture_buffer_size = outputPic.picture_width_stride * outputPic.picture_height_stride * 3 / 2;
ret = hi_mpi_dvpp_malloc(0, &outputPic.picture_address, outputPic.picture_buffer_size);

// Initialize the memory.
memset(outputPic.picture_address, 0, outputPic.picture_buffer_size);

// 3.4 Call the resizing API.
uint32_t taskID = 0;
ret = hi_mpi_vpc_resize(chnId, &inputPic, &outputPic, 0, 0, 0, &taskID, -1);

// 3.5 Wait for the task to complete. After the task is complete, the output image data is in the memory pointed to by outputPic.picture_address.
uint32_t taskIDResult = taskID;
ret = hi_mpi_vpc_get_process_result(chnId, taskIDResult, -1);

// 3.6 The output image data of VPC can be directly used as the input for model inference.
// The output image data of VPC can be directly used, in the memory pointed to by outputPic.picture_address.
// TODO: Code logic related to inference


// 3.7 Release the input and output memory.
ret = hi_mpi_dvpp_free(inputPic.picture_address);
ret = hi_mpi_dvpp_free(outputPic.picture_address);

// 4. Destroy the channel.
ret = hi_mpi_vpc_destroy_chn(chnId);

// 5. Deinitialize the media data processing system.
ret = hi_mpi_sys_exit();

// ....
```

## Cropping Sample Code

The following sample code shows the key steps of the cropping function. It is for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

<!-- npu="310p" id3 -->
You can click [vpc\_sample](https://gitee.com/ascend/samples/tree/master/cplusplus/level1_single_api/7_dvpp/vpc_sample) to obtain the sample code.
<!-- end id3 -->

```cpp
// ....

// 1. Initialize the media data processing system.
int32_t ret = hi_mpi_sys_init();

// 2. Create a channel.
hi_vpc_chn chnId;
hi_vpc_chn_attr stChnAttr;
ret = hi_mpi_vpc_sys_create_chn(&chnId, &stChnAttr);

// 3. Perform cropping.
// 3.1 Construct the structure for storing input image information.
hi_vpc_pic_info inputPic;
inputPic.picture_width = 1920;
inputPic.picture_height = 1080;
inputPic.picture_format = HI_PIXEL_FORMAT_YUV_SEMIPLANAR_420;
inputPic.picture_width_stride = 1920;
inputPic.picture_height_stride = 1080;
inputPic.picture_buffer_size = inputPic.picture_width_stride * inputPic.picture_height_stride * 3 / 2;

// 3.2 Prepare the input image data.
// Allocate device memory for media data processing.
ret = hi_mpi_dvpp_malloc(0, &inputPic.picture_address, inputPic.picture_buffer_size);

// Read the input image into the device memory. The custom function ReadPicFile is implemented by the user.
ReadPicFile(picName, inputPic.picture_address, inputPic.picture_buffer_size);

// 3.3 Construct the structure for storing output image information.
// This parameter indicates the number of crops.
uint32_t multiCount = 1;
// The size of the cropRegionInfos array must be consistent with the number of crops.
hi_vpc_crop_region_info cropRegionInfos[1];
hi_vpc_pic_info outputPic;
for (uint32_t i = 0; i < multiCount; i++) {
    outputPic.picture_width = 960;
    outputPic.picture_height  = 540;
    outputPic.picture_format = HI_PIXEL_FORMAT_YUV_SEMIPLANAR_420;
    outputPic.picture_width_stride = 960;
    outputPic.picture_height_stride = 540;
    outputPic.picture_buffer_size = outputPic.picture_width_stride * outputPic.picture_height_stride * 3 / 2;
    ret = hi_mpi_dvpp_malloc(0, &outputPic.picture_address, outputPic.picture_buffer_size);

    // Initialize the memory.
    memset(outputPic.picture_address, 0, outputPic.picture_buffer_size);
    
    // Crop a sub-image with a resolution of 960*540 from the input image, using the upper-left corner as the origin.
    cropRegionInfos[i].dest_pic_info = outputPic;
    cropRegionInfos[i].crop_region.left_offset = 0;
    cropRegionInfos[i].crop_region.top_offset = 0;
    cropRegionInfos[i].crop_region.crop_width = 960;
    cropRegionInfos[i].crop_region.crop_height = 540;
}

// 3.4 Call the cropping API.
uint32_t taskID = 0;
ret = hi_mpi_vpc_crop(chnId, &inputPic, cropRegionInfos, 1, &taskID, -1);

// 3.5 Wait for the task to complete. After the task is complete, the output image data is in the memory pointed to by outputPic.picture_address.
uint32_t taskIDResult = taskID;
ret = hi_mpi_vpc_get_process_result(chnId, taskIDResult, -1);

// 3.6 The VPC output image data can be directly used as the input for model inference.
// The VPC output image data can be directly used, in the memory pointed to by outputPic.picture_address.
// TODO: Code logic related to inference

// 3.7 Release the input and output memory.
ret = hi_mpi_dvpp_free(inputPic.picture_address);
inputPic.picture_address = nullptr;
for (uint32_t i = 0; i < multiCount; i++) {
     hi_mpi_dvpp_free(cropRegionInfos[i].dest_pic_info.picture_address);
     cropRegionInfos[i].dest_pic_info.picture_address = nullptr;
}

// 4. Destroy the channel.
ret = hi_mpi_vpc_destroy_chn(chnId);

// 5. Deinitialize the media data processing system.
ret = hi_mpi_sys_exit();

// ....
```
