# VENC Video Encoding

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:32:10.610Z pushedAt=2026-10-26T03:10:39.422Z nl=2 -->

This section describes the API call process of VENC video encoding, and provides sample code to help you understand the process.

VENC (Video Encoder) encodes images in YUV420SP format into video streams in H264/H265 format. For details about the VENC functions and usage constraints, see [DVPP Media Acceleration Library](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/dvpp/dvpp_03_0000.html).

## API Call Process

**Figure 1** Video encoding process  
![](figures/VENC_API_call_process_V1.png "Video encoding process")

The key APIs for implementing video encoding are described as follows:

1. **Call aclvencCreateChannel to create a channel for video encoding.**
    - Before creating a video encoding channel, perform the following operations:
        1. Call **aclvencCreateChannelDesc** to **create channel description information**.
        2. Call **aclvencSetChannelDescParam** to **set the attributes of the channel description information**, including **thread, callback function, video encoding protocol, and input image format**. Note the following:

            1. The callback function must be created by the user in advance. It is used to obtain the encoded data after video encoding and release related resources in a timely manner. For the prototype of the callback function, see **aclvencCallback**.

                After video encoding is complete, you are advised to release the input image memory and the corresponding image description information in the callback function in a timely manner. The output memory of video encoding is managed by the system, not by the user, so it does not need to be released by the user.

            2. The thread must be created by the user in advance, and a custom thread function must be defined. In the thread function, call **aclrtProcessReport** to wait for a specified period of time and then trigger the callback function in the preceding step.

            >**Note:** 
            >It is recommended that you use the **aclvencSetChannelDescParam** API to set the attributes of the channel description information, and select the attribute whose value is to be set through this API by using an enumeration value.
            >However, for compatibility with earlier versions, you can also call the **aclvencSetChannelDesc** series APIs to set the attributes of the channel description information. Each attribute corresponds to a **set** API.

    - The **aclvencCreateChannel** API encapsulates the following APIs internally, so you do not need to call them separately:
        1. **aclrtCreateStream** API: explicitly creates a stream for internal use by VENC.
        2. **aclrtSubscribeReport** API: specifies the thread that processes the callback function on the stream. The callback function and thread are specified when you call the **aclvencSetChannelDescParam** API.

2. **Call the aclvencSendFrame API to encode images in YUV420SP format into H264/H265 video streams.**
    - **Before video encoding**, perform the following operations:
        - Call the **acldvppCreatePicDesc** API to create the input image description information, and call the **acldvppSetPicDesc** series APIs to set the memory address, memory size, image format, and other attributes of the input image.
        - Call the **aclvencCreateFrameConfig** API to create the single-frame encoding configuration data, and call the **aclvencSetFrameConfig** series APIs to set whether to forcibly restart the I-frame interval and whether the frame is the last frame.

    - **During video encoding**, the **aclvencSendFrame** API encapsulates the **aclrtLaunchCallback** API internally to add a callback function to be executed to the task queue of the stream. You do not need to call the **aclrtLaunchCallback** API separately.
    - **After video encoding**, the video encoding result data is obtained through the callback function.

3. **Call aclvencDestroyChannel to destroy the video processing channel.**
    - The system waits until the sent frames are encoded and the user's callback function finishes processing before destroying the channel.
    - **aclvencDestroyChannel** internally encapsulates the following APIs, which do not need to be called separately by the user:
        - **aclrtUnSubscribeReport**: Unsubscribes the thread (the callback function on the stream is no longer processed by the specified thread).
        - **aclrtDestroyStream**: Destroys the stream.

    - After the channel is destroyed, call **aclvencDestroyChannelDesc** to destroy the channel description information.
    - After the channel description information is destroyed, the user can destroy the thread created in step 1.

## Sample Code

The following sample code shows the key steps of the VENC video encoding function. They are for reference only and cannot be directly copied, compiled, and run. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

You can click [venc\_image](https://gitee.com/ascend/samples/tree/master/cplusplus/level2_simple_inference/0_data_process/venc_image) to obtain the sample code.

```cpp
// 1. Create the thread and thread function for executing the callback function.
static bool runFlag = true;
void *ThreadFunc(void *arg)
{
     // Notice: create context for this thread.
    int deviceId = 0;
    aclrtContext context = nullptr;
    aclError ret = aclrtCreateContext(&context, deviceId);
    INFO_LOG("process callback thread start ");
    while (runFlag) {
        // Notice: timeout 1000ms
        (void)aclrtProcessReport(1000);
    }
    // ......
    ret = aclrtDestroyContext(context);
    return (void*)0;
}

int createThreadErr = pthread_create(&threadId_, nullptr, ThreadFunc, nullptr);

// 2. Create the callback function.
void callback(acldvppPicDesc *input, acldvppStreamDesc *outputStreamDesc, void *userdata)
{
    // Obtain the video encoding result data and write it to a file.
    void *outputDev = acldvppGetStreamDescData(outputStreamDesc);
    uint32_t streamDescSize = acldvppGetStreamDescSize(outputStreamDesc);
    if (!Utils::WriteToFile(g_outFileFp, outputDev, streamDescSize)) {
        ERROR_LOG("write file:%s failed.", g_outFile.c_str());
    }
    INFO_LOG("callback success, stream size:%u", streamDescSize);
}

// 3. Create the channel description for the video encoding processing channel and set its attributes. The thread and callback function must be created by the user in advance.
// vencChannelDesc_ is of the aclvdecChannelDesc type.
vencChannelDesc_ = aclvencCreateChannelDesc();
aclError ret = aclvencSetChannelDescThreadId(vencChannelDesc_, threadId_);
ret = aclvencSetChannelDescCallback(vencChannelDesc_, callback);
ret = aclvencSetChannelDescEnType(vencChannelDesc_, enType_);
ret = aclvencSetChannelDescPicFormat(vencChannelDesc_, format_);
ret = aclvencSetChannelDescPicWidth(vencChannelDesc_, 128);
ret = aclvencSetChannelDescPicHeight(vencChannelDesc_, 128);
ret = aclvencSetChannelDescKeyFrameInterval(vencChannelDesc_, 16);

// 4. Create the channel for video stream processing and the single-frame encoding configuration data.
ret = aclvencCreateChannel(vencChannelDesc_);
// vencFrameConfig_ is of the aclvencFrameConfig type.
vencFrameConfig_ = aclvencCreateFrameConfig();

// 5. Allocate device memory dataDev to store the input data for video encoding.
// Read the image data.
const char *fileName = "../dvpp_venc_128x128_nv12.yuv";
FILE *fp = fopen(fileName, "rb+");
fseek(fp, 0, SEEK_END);
long fileLenLong = ftell(fp);
fseek(fp, 0, SEEK_SET);
auto fileLen = static_cast<uint32_t>(fileLenLong);
uint32_t dataSize = fileLen;

// Call aclrtGetRunMode to obtain the running mode of the software stack. If the running mode obtained by aclrtGetRunMode is ACL_HOST, use aclrtMemcpy to transfer the input image data to the device. After the data transfer is complete, release the memory in a timely manner. Otherwise, directly allocate and use the device memory.
aclrtRunMode runMode;
ret = aclrtGetRunMode(&runMode);
if(runMode == ACL_HOST){ 
    void *dataHost = malloc(fileLen);
    size_t readSize = fread(dataHost, 1, fileLen, fp);
    void *dataDev = nullptr;
    ret = acldvppMalloc(&dataDev, dataSize);
    ret = aclrtMemcpy(dataDev, dataSize, dataHost, fileLen, ACL_MEMCPY_HOST_TO_DEVICE);
    // After the data transfer is complete, release the memory in a timely manner.
    free(dataHost);
} 
else { 
    ret = acldvppMalloc(&dataDev, dataSize);
}

// 6. Perform video encoding.
size_t g_vencCnt = 16;
// 6.1 Create the input image description information, and set the memory address and memory size of the input image data.
inputPicputDesc_ = acldvppCreatePicDesc();
ret = acldvppSetPicDescData(inputPicputDesc_, dataDev);
ret = acldvppSetPicDescSize(inputPicputDesc_, dataSize);
// 6.2 Set the single-frame encoding configuration data, which is not the end frame.
ret = aclvencSetFrameConfigEos(vencFrameConfig_, 0);
ret = aclvencSetFrameConfigForceIFrame(vencFrameConfig_, 0);
// 6.3 Create the output stream description information.
acldvppStreamDesc *outputStreamDesc = nullptr;
// 6.4 Perform video encoding.
while (g_vencCnt > 0) {
        ret = aclvencSendFrame(vencChannelDesc_, inputPicputDesc_,
            static_cast<void *>(outputStreamDesc), vencFrameConfig_, nullptr);
        g_vencCnt--;
    }
// 6.5 Set the single-frame encoding configuration data, which is the end frame.
ret = aclvencSetFrameConfigEos(vencFrameConfig_, 1);
ret = aclvencSetFrameConfigForceIFrame(vencFrameConfig_, 0);
// 6.6 Perform video encoding of the last frame.
ret = aclvencSendFrame(vencChannelDesc_, nullptr, nullptr, vencFrameConfig_, nullptr);

// 7. Release resources.
(void)aclvencDestroyChannel(vencChannelDesc_);
(void)aclvencDestroyChannelDesc(vencChannelDesc_);
(void)acldvppDestroyPicDesc(inputPicputDesc_);
(void)aclvencDestroyFrameConfig(vencFrameConfig_);
// Release the memory and destroy the thread.
(void)acldvppFree(inBufferDev_);
void *res = nullptr;
int joinThreadErr = pthread_join(threadId_, &res);

......
```

If you call **aclvencSetChannelDescParam** to set the attributes of the channel description information and call **aclvencGetChannelDescParam** to obtain the attribute values in the channel description information, the example code is as follows:

```cpp
// Set the callback function.
void *func = (void *)callback;
aclvencSetChannelDescParam(vencChannelDesc_, ACL_VENC_CALLBACK_PTR, 8, &func);
// Obtain the callback function.
void *func1 = nullptr;
aclvencGetChannelDescParam(vencChannelDesc_, ACL_VENC_CALLBACK_PTR, 8, &len, &func1);

// Set the input image format.
acldvppPixelFormat format = PIXEL_FORMAT_YUV_SEMIPLANAR_420;
aclvencSetChannelDescParam(vencChannelDesc_, ACL_VENC_PIXEL_FORMAT_UINT32, 4, &format);
// Obtain the input image format.
acldvppPixelFormat format1 = PIXEL_FORMAT_YUV_SEMIPLANAR_420;
aclvencGetChannelDescParam(vencChannelDesc_, ACL_VENC_PIXEL_FORMAT_UINT32, 4, &len, &format1);

// Set the image width.
uint32_t width = 128;
aclvencSetChannelDescParam(vencChannelDesc_, ACL_VENC_PIC_WIDTH_UINT32, 4, &width);
// Obtain the image width.
uint32_t width1 = 0;
aclvencGetChannelDescParam(vencChannelDesc_, ACL_VENC_PIC_WIDTH_UINT32, 4, &len, &width1);

// Set the image height.
uint32_t height = 128;
aclvencSetChannelDescParam(vencChannelDesc_, ACL_VENC_PIC_HEIGHT_UINT32, 4, &height);
// Obtain the image height.
uint32_t height1 = 0;
aclvencGetChannelDescParam(vencChannelDesc_, ACL_VENC_PIC_HEIGHT_UINT32, 4, &len, &height1);

// Set the encoding output buffer address.
ret = acldvppMalloc(&buf, bufSize);
aclvencSetChannelDescParam(vencChannelDesc_, ACL_VENC_BUF_ADDR_PTR, 8, &buf);
// Obtain the encoding output buffer address.
void *buf1 = nullptr;
aclvencGetChannelDescParam(vencChannelDesc_, ACL_VENC_BUF_ADDR_PTR, 8, &len, &buf1);

```
