# VDEC Video Decoding

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:32:26.697Z pushedAt=2026-10-26T03:10:39.424Z nl=2 -->

This section describes the API call process of VDEC video decoding, and provides sample code to help you understand the process.

VDEC (Video Decoder) decodes H264/H265 video bitstreams into YUV/RGB images. For details about VDEC functions and usage constraints, see [DVPP Media Acceleration Library](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/dvpp/dvpp_03_0000.html).

## API Call Process

**Figure 1** Video decoding process  
![](figures/VDEC_API_call_process_V1.png "Video decoding process")

The key APIs for implementing video decoding are described as follows:

1. **Call aclvdecCreateChannel to create a channel for video decoding.**
    - Before creating a video decoding channel, perform the following operations:
        1. Call **aclvdecCreateChannelDesc** to **create the channel description information**.
        2. Call the **aclvdecSetChannelDesc** series APIs to **set the properties of the channel description information**, including the **decoding channel number, thread, callback function, and video encoding protocol**. Note the following:

            1. The callback function must be created by the user in advance. It is used to obtain the decoded data and release related resources in a timely manner after video decoding. For the prototype of the callback function, see **aclvdecCallback**.

                In the callback function, the user needs to call **acldvppGetPicDescRetCode** to obtain the **retCode** return code to determine whether decoding is successful. A **retCode** of **0** indicates successful decoding, and a **retCode** of **1** indicates decoding failure. If decoding fails, determine the specific problem based on the return code in the log. For details about the return codes, see [Return Code Description](#section197765691414).

                After decoding is complete, it is recommended that the user release the VDEC input bitstream memory, output image memory, and the corresponding video bitstream description information and image description information in the callback function in a timely manner.

            2. The thread must be created by the user in advance, and a custom thread function must be defined. In the thread function, call **aclrtProcessReport** to wait for a specified period and then trigger the callback function in the previous step.

            >**Note:** 
            >If **aclvdecSetChannelDescOutPicFormat** is not called to set the output format, YUV420SP NV12 is used by default.

    - **aclvdecCreateChannel** internally encapsulates the following APIs, which do not need to be called separately by the user:
        1. **aclrtCreateStream**: explicitly creates a stream for internal use by VDEC.
        2. **aclrtSubscribeReport**: specifies the thread that processes the callback function on the stream. The callback function and thread are specified by the user when calling the **aclvdecSetChannelDesc** series APIs.

2. **Call aclvdecSendFrame to decode the video bitstream into images in YUV420SP format.**
    - **Before video decoding,** perform the following operations:
        - Call **acldvppCreateStreamDesc** to create the input video bitstream description information, and call the **acldvppSetStreamDesc** series APIs to set the memory address, memory size, and bitstream format of the input video.
        - Call **acldvppCreatePicDesc** to create the output image description information, and call the **acldvppSetPicDesc** series APIs to set the memory address, memory size, and image format of the output image.

    - **During video decoding:**

        The **aclvdecSendFrame** API internally encapsulates the **aclrtLaunchCallback** API, which is used to add a callback function to be executed to the task queue of a stream. Users do not need to call the **aclrtLaunchCallback** API separately.

    - **After video decoding**, the result data of video decoding is obtained through the callback function:

        Before obtaining the decoded data, obtain the value of **retCode** to determine whether decoding is successful. **0** indicates successful decoding, and **1** indicates failed decoding. If decoding fails, determine the specific problem based on the return code in the log. For details about the return code, see [Return Code Description](#section197765691414).

        If users need to obtain the frame sequence number of decoding, they can define it in the **userData** parameter of the **aclvdecSendFrame** API. Then the frame sequence number of decoding can be passed to the VDEC callback function through the **userData** parameter, which is used to determine which frame of data is being processed in the callback function.

        If users do not want to obtain the decoding result of a certain frame, they can call the **aclvdecSendSkippedFrame** API to pass the bitstream to be decoded (input memory) to the decoder for decoding. In this case, the decoding result is not output, and the output returned in the callback function after decoding is **nullptr**.

3. **Call the aclvdecDestroyChannel API to destroy the channel for video processing.**
    - The system waits until the decoding of the sent frames is complete and the user's callback function has finished processing before destroying the channel.
    - The **aclvdecDestroyChannel** API internally encapsulates the following APIs, so users do not need to call them separately:
        - **aclrtUnSubscribeReport** API: Unsubscribes thread registration (the callback function on the stream is no longer processed by the specified thread).
        - **aclrtDestroyStream** API: Destroys the stream.

    - After destroying the channel, call the **aclvdecDestroyChannelDesc** API to destroy the channel description information.
    - After destroying the channel description information, the user can destroy the thread created in step 1.

## Sample Code

The following sample code shows the key steps of the VDEC video decoding function. They are for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

You can click [vdec\_resnet50\_classification](https://gitee.com/ascend/samples/tree/master/cplusplus/level2_simple_inference/1_classification/vdec_resnet50_classification) to obtain the sample code.

```cpp
// 1. Create the callback function.
void callback(acldvppStreamDesc *input, acldvppPicDesc *output, void *userdata)
{
    static int count = 1;
    if (output != nullptr) {
        // Obtain the output memory of VDEC decoding, call the custom function WriteToFile to write the data in the output memory to a file, and then call the acldvppFree API to release the output memory.
        void *vdecOutBufferDev = acldvppGetPicDescData(output);
        if (vdecOutBufferDev != nullptr) {
            // 0: vdec success; others: vdec failed
            // retCode 0 indicates successful decoding, and 1 indicates decoding failure.
            int retCode = acldvppGetPicDescRetCode(output);
            if (retCode == 0) {
                // process task: write file
                uint32_t size = acldvppGetPicDescSize(output);
                std::string fileNameSave = "outdir/image" + std::to_string(count);
                // The VDEC output result is on the device side. Perform the following processing in the WriteToFile method.
                if (!Utils::WriteToFile(fileNameSave.c_str(), vdecOutBufferDev, size)) {
                    ERROR_LOG("write file failed.");
                }
            } else {
                ERROR_LOG("vdec decode frame failed.");
            }

            // free output vdecOutBufferDev
            aclError ret = acldvppFree(vdecOutBufferDev);
        }
        // Release the data of the acldvppPicDesc type, which indicates the output image description data after decoding.
        aclError ret = acldvppDestroyPicDesc(output);
    }

    // free input vdecInBufferDev and destroy stream desc
    if (input != nullptr) {
        void *vdecInBufferDev = acldvppGetStreamDescData(input);
        if (vdecInBufferDev != nullptr) {
            aclError ret = acldvppFree(vdecInBufferDev);
        }
        // Release the data of the acldvppStreamDesc type, which indicates the input bitstream description data for decoding.
        aclError ret = acldvppDestroyStreamDesc(input);
    }

    INFO_LOG("callback success %d.", count);
    count++;
}

// 2. Create the channel description information for the video bitstream processing channel, and set the properties of the video processing channel description information. The thread (threadId indicates the thread ID) and callback function need to be created by the user in advance.
// vdecChannelDesc is of the aclvdecChannelDesc type.
vdecChannelDesc = aclvdecCreateChannelDesc();
aclError ret = aclvdecSetChannelDescChannelId(vdecChannelDesc, 10);
ret = aclvdecSetChannelDescThreadId(vdecChannelDesc, threadId);
ret = aclvdecSetChannelDescCallback(vdecChannelDesc, callback);
// The H265_MAIN_LEVEL video encoding protocol is used in this example.
ret = aclvdecSetChannelDescEnType(vdecChannelDesc, static_cast<acldvppStreamFormat>(H265_MAIN_LEVEL));
// PIXEL_FORMAT_YVU_SEMIPLANAR_420 is used in this example.
ret = aclvdecSetChannelDescOutPicFormat(vdecChannelDesc, static_cast<acldvppPixelFormat>(PIXEL_FORMAT_YUV_SEMIPLANAR_420));

// 3. Create the video bitstream processing channel.
ret = aclvdecCreateChannel(vdecChannelDesc);


// 4. Call the aclrtGetRunMode API to obtain the running mode of the software stack. If the running mode obtained by calling the aclrtGetRunMode API is ACL_HOST, use the aclrtMemcpy API to transfer the input image data to the device. After the data transfer is complete, release the memory in a timely manner. Otherwise, directly allocate and use the device memory.
aclrtRunMode runMode;
ret = aclrtGetRunMode(&runMode);

// 5. Send the bitstream frame by frame and decode it.
count = 0;
while (count < 10) { // Assume that the bitstream has 10 frames of data and needs to be sent 10 times.
    //  5.1 Allocate the input bitstream memory (distinguish the running state), and read one frame of bitstream data. inBufferSize is the actual size of one frame of bitstream to be read, and the user needs to assign a value based on the actual bitstream size of each frame.
    if (runMode == ACL_HOST){ 
        // Allocate the host memory inputHostBuff.
        void* inputHostBuff= nullptr;
        // inBufferSize is the input bitstream size.
        inputHostBuff= malloc(inBufferSize);
        // Read one frame of the input bitstream into the memory. The custom function ReadStreamFile is implemented by the user.
        ReadStreamFile(picName, inputHostBuff, inBufferSize);
        // Allocate the device memory inBufferDev.
        ret = acldvppMalloc(&inBufferDev, inBufferSize);
        // Transfer the input image data to the device through the aclrtMemcpy API.
        ret = aclrtMemcpy(inBufferDev, inBufferSize, inputHostBuff, inBufferSize, ACL_MEMCPY_HOST_TO_DEVICE);
        // Release the host memory in time after the data transfer is complete.
        free(inputHostBuff);
    } else {
        // Allocate the device input memory dataDev. inBufferSize is the input bitstream size of each frame.
        ret = acldvppMalloc(&inBufferDev, inBufferSize);
        // Read one frame of the input bitstream into the memory. The custom function ReadStreamFile is implemented by the user.
        ReadStreamFile(picName, inBufferDev, inBufferSize);
    }

    // 5.2 Create the input video bitstream description information and set the bitstream information attributes.
    streamInputDesc = acldvppCreateStreamDesc(); 
    // inBufferDev indicates the device memory that stores the input video data, and inBufferSize indicates the memory size  
    ret = acldvppSetStreamDescData(streamInputDesc, inBufferDev);
    ret = acldvppSetStreamDescSize(streamInputDesc, inBufferSize);

    // 5.3 Allocate the device memory picOutBufferDev to store the output data decoded by VDEC. size is the decoded image size, which must be calculated based on the image format and the aligned image width and height, and then assigned.
    ret = acldvppMalloc(&picOutBufferDev, size);

    // 5.4 Create the output image description information and set its attributes.
    // picOutputDesc is of the acldvppPicDesc type.
    picOutputDesc = acldvppCreatePicDesc();
    ret = acldvppSetPicDescData(picOutputDesc, picOutBufferDev);
    ret = acldvppSetPicDescSize(picOutputDesc, size);
    ret = acldvppSetPicDescFormat(picOutputDesc, static_cast<acldvppPixelFormat>(PIXEL_FORMAT_YUV_SEMIPLANAR_420));

    // 5.5 Decode the video bitstream. After each frame is decoded, the system automatically calls the callback function to write the decoded data to a file, and then releases the related resources in a timely manner.
    ret = aclvdecSendFrame(vdecChannelDesc, streamInputDesc, picOutputDesc, nullptr, nullptr);
    // ......
    count++;
    // Note that aclvdecSendFrame is an asynchronous API. The input memory (inBufferDev), output memory (picOutBufferDev), input descriptor (streamInputDesc), and output descriptor (picOutputDesc) cannot be released in advance and must be released in the callback function.
}

// 6. Release the image processing channel and image description information.
ret = aclvdecDestroyChannel(vdecChannelDesc);
aclvdecDestroyChannelDesc(vdecChannelDesc);

......
```

<a id="section197765691414"></a>

## Return Code Description

**Table 1** Return code list

| Return Code | Meaning | Possible Cause and Solution |
| --- | --- | --- |
| AICPU_DVPP_KERNEL_STATE_SUCCESS = 0 | Decoding succeeded. | - |
| AICPU_DVPP_KERNEL_STATE_FAILED = 1 | Other error. | - |
| AICPU_DVPP_KERNEL_STATE_DVPP_ERROR = 2 | The API failed to call an API of another module internally. | - |
| AICPU_DVPP_KERNEL_STATE_PARAM_INVALID = 3 | Parameter verification failed. | Check whether the API parameters meet the API requirements. |
| AICPU_DVPP_KERNEL_STATE_OUTPUT_SIZE_INVALID = 4 | Output memory size verification failed. | Check whether the output memory size meets the API requirements. |
| AICPU_DVPP_KERNEL_STATE_INTERNAL_ERROR = 5 | System internal error. | - |
| AICPU_DVPP_KERNEL_STATE_QUEUE_FULL = 6 | The system internal queue is full. | - |
| AICPU_DVPP_KERNEL_STATE_QUEUE_EMPTY = 7 | The system internal queue is empty. | - |
| AICPU_DVPP_KERNEL_STATE_QUEUE_NOT_EXIST = 8 | The system internal queue does not exist. | - |
| AICPU_DVPP_KERNEL_STATE_GET_CONTEXT_FAILED = 9 | Failed to obtain the system internal context. | - |
| AICPU_DVPP_KERNEL_STATE_SUBMIT_EVENT_FAILED = 10 | Failed to submit a system internal event. | - |
| AICPU_DVPP_KERNEL_STATE_MEMORY_FAILED = 11 | Failed to allocate memory in the system. | Check whether the system has available memory. |
| AICPU_DVPP_KERNEL_STATE_SEND_NOTIFY_FAILED = 12 | Failed to send a system internal notification. | - |
| AICPU_DVPP_KERNEL_STATE_VPC_OPERATE_FAILED = 13 | System internal API processing failed. | - |
| AICPU_DVPP_KERNEL_STATE_CHANNEL_ABNORMAL = 14 | The current channel is abnormal. | - |
| ERR_INVALID_STATE = 0x10001 | The VDEC decoder is in an abnormal state. | - |
| ERR_HARDWARE = 0x10002 | Hardware error, including exceptions during decoder startup, execution, and stopping. | - |
| ERR_SCD_CUT_FAIL = 0x10003 | An exception occurred when splitting the video bitstream into multiple frames. | Check whether the input video stream data is correct. |
| ERR_VDM_DECODE_FAIL = 0x10004 | An exception occurred when decoding a frame. | Check whether the input video stream data is correct. |
| ERR_ALLOC_MEM_FAIL = 0x10005 | Failed to allocate memory internally. | Check whether the system has available memory. If this error is ignored, the user may keep sending bitstreams without any decoding result output. |
| ERR_ALLOC_DYNAMIC_MEM_FAIL = 0x10006 | Includes exceptions such as input video resolution out of range and internal dynamic memory allocation failure. | Check the resolution of the input video stream and whether the system has available memory. If this error is ignored, the user may keep sending bitstreams without any decoding result output. |
| ERR_ALLOC_IN_OR_OUT_PORT_MEM_FAIL = 0x10007 | An exception occurred when the system allocated the input and output buffers of VDEC internally. | Check whether the system has available memory. If this error is ignored, the user may keep sending bitstreams without any decoding result output. |
| ERR_BITSTREAM = 0x10008 | Bitstream error (for example, syntax parsing failure, resending EOS, or sending EOS in the first frame). | Check whether the input video stream data is correct. |
| ERR_VIDEO_FORMAT = 0x10009 | Input video format error. | Check whether the input video format is H264 or H265. |
| ERR_IMAGE_FORMAT = 0x1000a | Output format configuration error. | Check whether the output image format is nv12 or nv21. |
| ERR_CALLBACK = 0x1000b | The callback function is empty. | Check whether the configured callback function is empty. |
| ERR_INPUT_BUFFER = 0x1000c | The input memory is empty. | Check whether the input memory is empty. |
| ERR_INBUF_SIZE = 0x1000d | The input memory size is less than or equal to 0. | Check whether the input memory size is less than or equal to 0. |
| ERR_THREAD_CREATE_FBD_FAIL = 0x1000e | The thread that returns decoding results to the user through the callback function is abnormal. | Check whether system resources (for example, threads and memory) are available. |
| ERR_CREATE_INSTANCE_FAIL = 0x1000f | Failed to create a decoding instance. | - |
| ERR_INIT_DECODER_FAIL = 0x10010 | Failed to initialize the decoder, for example, the number of decoding instances exceeds the range (maximum 16). | - |
| ERR_GET_CHANNEL_HANDLE_FAIL = 0x10011 | Failed to obtain the decoding handle of a video stream in the system. | - |
| ERR_COMPONENT_SET_FAIL = 0x10012 | An exception occurred when setting the decoding instance in the system. | Check whether the input parameter values for decoding are correct, for example, the input video format **video_format** and the output frame format **image_format**. |
| ERR_COMPARE_NAME_FAIL = 0x10013 | An exception occurred when setting the decoding instance name in the system. | Check whether the input parameter values for decoding are correct, for example, the input video format **video_format** and the output frame format **image_format**. |
| ERR_OTHER = 0x10014 | Other error. | - |
| ERR_DECODE_NOPIC = 0x20000 | Used in the interlaced bitstream scenario. Each frame of an interlaced bitstream is sent as two fields. During decoding, one of the fields has no image output, which is normal, and this error code is returned. The decoding output data of an interlaced bitstream is all in the output buffer corresponding to the odd field. | - |
| 0x20001 | The number of reference frames is set incorrectly. | Check whether the actual number of reference frames in the bitstream is consistent with the number of reference frames set by the user. For Atlas inference products, the default number of reference frames is 8. |
| 0x20002 | The VDEC decoding frame memory size is set incorrectly. | Check whether the actual width and height of the input bitstream are consistent with the width and height set by the user. |
| 0xA0058001 | Invalid device ID. | Check the device ID. |
| 0xA0058002 | Invalid channel ID. | Check whether the channel number passed to the API is correct, or check whether the total number of channels has reached the upper limit. |
| 0xA0058003 | Invalid parameter, for example, an invalid enumeration value. | Check the parameter that caused the error based on the logs. |
| 0xA0058004 | The resource already exists. | Check whether a channel is created repeatedly. |
| 0xA0058005 | The channel resource does not exist. | Check whether a nonexistent channel number or channel handle is used. |
| 0xA0058006 | A null pointer exists in the function parameters. | Check the input parameters of the API based on the logs. |
| 0xA0058007 | The corresponding parameters are not configured before the system, device, or channel is enabled. | Check the input parameters of the API based on the logs. |
| 0xA0058008 | Unsupported parameter or function. | Check the input parameters of the API based on the logs. |
| 0xA0058009 | The operation is not allowed, for example, attempting to modify a static configuration parameter. | - |
| 0xA005800C | Failed to allocate memory, for example, insufficient system memory. | Check whether the system has available memory. If this error is ignored, the user may keep sending bitstreams without any decoding result output. |
| 0xA005800D | Failed to allocate a buffer, for example, the requested data buffer is too large. | - |
| 0xA005800E | No data in the buffer. | The system has not completed decoding, and there is no decoding result data in the buffer. Wait until there is data in the buffer before attempting to obtain data. |
| 0xA005800F | The buffer is full. | The user sends input bitstream data too fast, causing the input buffer to be full. Try to reduce the speed of sending input bitstream data, or set the buffer size to a larger value when creating a channel. |
| 0xA0058010 | The system is not initialized or the related dependent modules are not loaded. | Check whether the system initialization API is called. |
| 0xA0058011 | Address error. | - |
| 0xA0058012 | The system is busy. | Check whether the total number of VDEC decoding channels has reached the upper limit. |
| 0xA0058013 | The buffer is smaller than the actually required size. | - |
| 0xA0058014 | Hardware or software processing timed out. | - |
| 0xA0058015 | Internal system error. | - |
| 0xA005803F | Maximum return code. The error code of this module must be less than this value. | - |
