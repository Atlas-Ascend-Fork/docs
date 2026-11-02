# VDEC

The video decoder (VDEC) decodes H.264/H.265 video streams into YUV/RGB images. For details about the VDEC functions and restrictions, see [DVPP Media Acceleration Library](https://hiascend.com/en/document/redirect/CannCommunityDvppApi).

This section describes the API call sequence of VDEC, and sample code is also provided to help you better understand the process.

## API Call Sequence

If video decoding is involved during app development, ensure that your app contains the code logic for video decoding. **For details about the API call sequence, see [API Calling Process](interface_calling_process.md).**

**Figure 1** Video decoding process
![](figures/video-decoding.png)

This module implements video decoding. The key APIs are described as follows:

1. Call `acl.media.vdec_create_channel` to create a channel for video decoding.
    - Perform the following steps before creating a channel for video decoding.
        1. Call `acl.media.vdec_create_channel_desc` to **create a channel description**.
        2. Call the **acl.media.vdec_set_channel_desc** APIs to set attributes of the channel description, including the decoding channel ID, thread, callback function, and video coding protocol.

            1. Create the callback function beforehand to get the decoding output and free memory promptly. See `acl.media.vdec_set_channel_desc_callback` for the callback function prototype.

                Call `acl.media.dvpp_get_pic_desc_ret_code` in the callback function to obtain the return code `ret_code`. The value `0` indicates the success of decoding, while `1` indicates failure. If the decoding fails, locate the fault based on the return code in the log. For details about the return codes, see [Return Codes](#return-codes).

                After the decoding is complete, you are advised to free the buffer for storing the input streams and output images of the VDEC, and the corresponding video stream description and image description in the callback function in a timely manner.

            2. The user needs to create a thread in advance and customize a thread function. Calling `acl.rt.process_report` in the thread function triggers the callback function in the previous step after a specified period of time.

            >[!NOTE]NOTE
            >If `acl.media.vdec_set_channel_desc_out_pic_format` is not called to set the output format, YUV420SP NV12 is used by default.

    - The following APIs are encapsulated in `acl.media.vdec_create_channel` and do not need to be called separately:
        1. `acl.rt.create_stream`: explicitly creates a stream. It is internally used for VDEC.
        2. `acl.rt.subscribe_report`: specifies a thread for processing the callback function in a stream. The callback function and thread are specified by calling the `acl.media.vdec_set_channel_desc` series.

2. Decode a video stream into a YUV420SP image by calling `acl.media.vdec_send_frame`.
    - Perform the following steps **before decoding a video stream:**
        - Call `acl.media.dvpp_create_stream_desc` to create the description of the input video stream, and call `acl.media.dvpp_set_stream_desc` to configure the input video, such as the memory address, memory size, and stream format.
        - Call `acl.media.dvpp_create_pic_desc` to create the description of the output image, and call the `acl.media.dvpp_set_pic_desc` APIs to set attributes such as buffer address, buffer size, and image format of the output image.

    - **During video decoding:**

        `acl.media.vdec_send_frame` encapsulates `acl.rt.launch_callback` to insert a callback function to be executed to the stream. `acl.rt.launch_callback` does not need to be called separately.

    - **After video decoding,** use the callback function to obtain the result:

        But before that, obtain the value of `ret_code`. The value `0` indicates the success of decoding, while `1` indicates failure. If the decoding fails, locate the fault based on the return code in the log. For details about the return codes, see [Return Codes](#return-codes).

        To obtain the frame sequence number returned after decoding, define the `user_data` parameter of `acl.media.vdec_send_frame`. Then, the frame sequence number can be passed to the VDEC callback function to determine the frame data to be processed.

        To skip a specific frame, call `acl.media.vdec_send_skipped_frame` to feed the frame (the input buffer) to the decoder. In this case, the decoding result is not output, and the value of `dvpp_pic_desc` returned by the callback function after decoding is `0`.

3. Call `acl.media.vdec_destroy_channel` to destroy a video processing channel.
    - The channel is destroyed only after the transmitted frames are decoded and the callback function is processed.
    - The following APIs are encapsulated in `acl.media.vdec_destroy_channel` and do not need to be called separately:
        - `acl.rt.unsubscribe_report`: unsubscribes from a thread. (The callback function in the stream is no longer processed by the specified thread.)
        - `acl.rt.destroy_stream`: destroys a stream.

    - Call `acl.media.vdec_destroy_channel_desc` to destroy the channel description after the channel is destroyed.
    - After destroying the channel description, destroy the thread created in the first step.

## Sample Code

[Click here](https://gitee.com/ascend/samples/tree/master/python/level2_simple_inference/1_classification/vdec_resnet50_classification) to view the complete code.

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......

# 1. Perform initialization.
ret = acl.init()

# 2. Allocate runtime resources.
# 3. Create a callback function.
def _callback(self, input_stream_desc, output_pic_desc, user_data):
    # Input stream description
    if input_stream_desc:
        ret = acl.media.dvpp_destroy_stream_desc(input_stream_desc)
        if ret != 0:
            print("acl.media.dvpp_destroy_stream_desc failed")
    # Output image description.
    if output_pic_desc:
        vdec_out_buffer = acl.media.dvpp_get_pic_desc_data(output_pic_desc)
        ret_code = acl.media.dvpp_get_pic_desc_ret_code(output_pic_desc)
        data_size = acl.media.dvpp_get_pic_desc_size(output_pic_desc)
        self.images_buffer.append(dict({"buffer": vdec_out_buffer,
                                        "size": data_size}))
        ret = acl.media.dvpp_destroy_pic_desc(output_pic_desc)
        if ret != 0:
            print("acl.media.dvpp_destroy_pic_desc failed")
    self.output_count += 1
    print("[Vdec] [_callback] _callback exit success")
    # In this example, release vdec_out_buffer after the VDEC process.

# 4. Create a thread for processing a callback function, submit and register the thread to execute the callback function.
timeout = 100
cb_thread_id, ret = acl.util.start_thread(self._thread_func, [timeout])
acl.rt.subscribe_report(cb_thread_id, self.stream)

# 5. Create the description of the video stream processing channel, and set the attributes of the video processing channel description. The thread and callback function need to be created in advance.
def init_resource(self, cb_thread_id):
    print("[Vdec] class Vdec init resource stage:")
    self.vdec_channel_desc = acl.media.vdec_create_channel_desc()
    acl.media.vdec_set_channel_desc_channel_id(self.vdec_channel_desc, self._channel_id)
    acl.media.vdec_set_channel_desc_thread_id(self.vdec_channel_desc, cb_thread_id)
    acl.media.vdec_set_channel_desc_callback(self.vdec_channel_desc, self._callback)
    acl.media.vdec_set_channel_desc_entype(self.vdec_channel_desc, self._en_type)
    acl.media.vdec_set_channel_desc_out_pic_format(self.vdec_channel_desc, self._format)
    print("[Vdec] class Vdec init resource stage success")

# 6. Create a channel for processing video streams.
ret = acl.media.vdec_create_channel(self.vdec_channel_desc)
# ......
# 7. Allocate the device buffer `dataDev` to store the input video data for decoding.
# Copy image data from the host to the device by calling `acl.rt.memcpy`. After data copy is complete, call `acl.rt.free_host` to free the host memory in a timely manner.
# Set the alignment mode of the output image size.
output_pic_size = (self.input_width * self.input_height * 3) // 2
img = np.fromfile(img_path, dtype=self.dtype)
input_stream_size = img.size
bytes_data = img.tobytes()
img_ptr = acl.util.bytes_to_ptr(bytes_data)
self.input_stream_mem, ret = acl.media.dvpp_malloc(input_stream_size)
ret = acl.rt.memcpy(self.input_stream_mem,
                    input_stream_size,
                    img_ptr,
                    input_stream_size,
                    ACL_MEMCPY_HOST_TO_DEVICE)

# 8. Perform video decoding for 10 times and output 10 YUV420SP NV12 images.
def forward(self, output_pic_size, input_stream_size):
    self.frame_config = acl.media.vdec_create_frame_config()
    for i in range(self.rest_len):
        print("[Vdec] forward index:{}".format(i))
        # 8.1 Create the description of the input video stream and set the stream attributes.
        self.dvpp_stream_desc = acl.media.dvpp_create_stream_desc()
        ret = acl.media.dvpp_set_stream_desc_data(self.dvpp_stream_desc, self.input_stream_mem)
        ret = acl.media.dvpp_set_stream_desc_size(self.dvpp_stream_desc, input_stream_size)
        # 8.2 Create the description of the output image and set the attributes of the image description.
        output_pic_mem, ret = acl.media.dvpp_malloc(output_pic_size)
        self.dvpp_pic_desc = acl.media.dvpp_create_pic_desc()
        acl.media.dvpp_set_pic_desc_data(self.dvpp_pic_desc, output_pic_mem)
        acl.media.dvpp_set_pic_desc_size(self.dvpp_pic_desc, output_pic_size)
        acl.media.dvpp_set_pic_desc_format(self.dvpp_pic_desc, PIXEL_FORMAT_YVU_SEMIPLANAR_420)
        # 8.3 Decode video streams. The callback function is called after each decoded frame to write data to the file, and free resources in a timely manner.
        ret = acl.media.vdec_send_frame(self.vdec_channel_desc,
                                        self.dvpp_stream_desc,
                                        self.dvpp_pic_desc,
                                        self.frame_config,
                                        None)
        check_ret("acl.media.vdec_send_frame", ret)
        print('[Vdec] vdec_send_frame stage success')

# 9. Release the image processing channel and image description.
ret = acl.media.vdec_destroy_channel(self.vdec_channel_desc)
acl.media.vdec_destroy_channel_desc(self.vdec_channel_desc)

# 10. Destroy runtime allocations.
# Perform deinitialization.
ret = acl.finalize()
# ....
```

## Return Codes

**Table 1** Return codes

| Return Code| Definition| Possible Cause and Solution|
| --- | --- | --- |
| AICPU_DVPP_KERNEL_STATE_SUCCESS = 0 | Decoding success| - |
| AICPU_DVPP_KERNEL_STATE_FAILED = 1 | Other errors.| - |
| AICPU_DVPP_KERNEL_STATE_DVPP_ERROR = 2 | Failure of calling APIs of other modules| - |
| AICPU_DVPP_KERNEL_STATE_PARAM_INVALID = 3 | Argument verification failure| Check whether the API arguments meet the API requirements.|
| AICPU_DVPP_KERNEL_STATE_OUTPUT_SIZE_INVALID = 4 | Output buffer size verification failure| Check whether the output buffer size meets the API requirements.|
| AICPU_DVPP_KERNEL_STATE_INTERNAL_ERROR = 5 | Internal system error| - |
| AICPU_DVPP_KERNEL_STATE_QUEUE_FULL = 6 | Full internal queue| - |
| AICPU_DVPP_KERNEL_STATE_QUEUE_EMPTY = 7 | Empty internal queue| - |
| AICPU_DVPP_KERNEL_STATE_QUEUE_NOT_EXIST = 8 | Nonexistent internal queue| - |
| AICPU_DVPP_KERNEL_STATE_GET_CONTEX_FAILED = 9 | Internal context obtaining failure| - |
| AICPU_DVPP_KERNEL_STATE_SUBMIT_EVENT_FAILED = 10 | Internal event submission failure| - |
| AICPU_DVPP_KERNEL_STATE_MEMORY_FAILED = 11 | Internal memory allocation failure| Check whether the system has available memory.|
| AICPU_DVPP_KERNEL_STATE_SEND_NOTIFY_FAILED = 12 | Internal notification sending failure| - |
| AICPU_DVPP_KERNEL_STATE_VPC_OPERATE_FAILED = 13 | Internal API operation failure| - |
| AICPU_DVPP_KERNEL_STATE_CHANNEL_ABNORMAL = 14 | Abnormal channel| - |
| ERR_INVALID_STATE = 0x10001 | Abnormal VDEC state| - |
| ERR_HARDWARE = 0x10002 | Hardware error, including decoder starts, execution, and stops| - |
| ERR_SCD_CUT_FAIL = 0x10003 | Abnormal video stream-to-frame cutting| Check that the input video stream is valid.|
| ERR_VDM_DECODE_FAIL = 0x10004 | Single-frame decoding failure| Check that the input video stream is valid.|
| ERR_ALLOC_MEM_FAIL = 0x10005 | Internal memory allocation failure| Check whether the system has available memory. **If this error is ignored, no decoding result may be output with the continuously sent streams.**|
| ERR_ALLOC_DYNAMIC_MEM_FAIL = 0x10006 | Out-of-range input video resolution and dynamic memory allocation failure| Check the resolution of the input video stream and whether the system has available memory. **If this error is ignored, no decoding result may be output with the continuously sent streams.**|
| ERR_ALLOC_IN_OR_OUT_PORT_MEM_FAIL = 0x10007 | Internal VDEC input and output buffer allocation failure| Check whether the system has available memory. **If this error is ignored, no decoding result may be output with the continuously sent streams.**|
| ERR_BITSTREAM = 0x10008 | Invalid stream (for example, syntax error, eos retried, or eos detected in the first frame)| Check that the input video stream is valid.|
| ERR_VIDEO_FORMAT = 0x10009 | Incorrect input video format| Check whether the input video format is H.264 or H.265.|
| ERR_IMAGE_FORMAT = 0x1000a | Incorrect output format| Check whether the output image format is NV12 or NV21.|
| ERR_CALLBACK = 0x1000b | Empty callback function| Check whether the callback function is empty.|
| ERR_INPUT_BUFFER = 0x1000c | Empty input buffer| Check whether the input buffer is empty.|
| ERR_INBUF_SIZE = 0x1000d | Input buffer size ≤ 0| Check whether the buffer size is less than or equal to 0.|
| ERR_THREAD_CREATE_FBD_FAIL = 0x1000e | Abnormal thread (thread where the callback function returns the decoding result)| Check whether the resources (such as threads and memory) in the system are available.|
| ERR_CREATE_INSTANCE_FAIL = 0x1000f | Decoding instance creation failure| - |
| ERR_INIT_DECODER_FAIL = 0x10010 | Decoder initialization failure. For example, the number of decoding instances exceeds the maximum of 16.| - |
| ERR_GET_CHANNEL_HANDLE_FAIL = 0x10011 | Channel handle obtaining failure| - |
| ERR_COMPONENT_SET_FAIL = 0x10012 | Decoding instance setting failure| Check whether the input arguments of VDEC are correct, such as the input video format (`video_format`) and output frame format (`image_format`).|
| ERR_COMPARE_NAME_FAIL = 0x10013 | Decoding instance naming failure| Check whether the input arguments of VDEC are correct, such as the input video format (`video_format`) and output frame format (`image_format`).|
| ERR_OTHER = 0x10014 | Other errors.| - |
| ERR_DECODE_NOPIC = 0x20000 | Can be ignored. In the interlaced scenario where two fields are transmitted every frame, one of every two transmitted fields has no decoding output. This is expected. The decoding output of an interlaced stream is stored in the output buffers of the odd fields.| - |
| 0x20001 | Reference frame count setting failure| Check that the actual number of reference frames of the stream is the same as the configured number of reference frames. For Atlas inference products, the default number of reference frames is 8.|
| 0x20002 | Size of VDEC frame buffer setting failure| Check that the actual width and height of the input stream are the same as the configured width and height.|
| 0xA0058001 | Invalid device ID.| Check the device ID.|
| 0xA0058002 | Invalid channel ID.| Check that the input channel ID is correct or whether the total number of channels reaches the upper limit.|
| 0xA0058003 | Invalid argument, such as an invalid enum value| Check the incorrect argument based on the logs.|
| 0xA0058004 | Existing resource| Check whether the channel has been repeatedly created.|
| 0xA0058005 | Non-existent channel resource| Check whether a non-existent channel ID or channel handle is used.|
| 0xA0058006 | Null pointer| Check the input argument of the API based on the logs.|
| 0xA0058007 | No configuration made to corresponding parameters before the system, device, or channel is enabled.| Check the input argument of the API based on the logs.|
| 0xA0058008 | Unsupported argument or function.| Check the input argument of the API based on the logs.|
| 0xA0058009 | Unallowed operation, for example, an attempt to update a static attribute.| - |
| 0xA005800C | Memory allocation failure due to memory insufficiency or other reasons.| Check whether the system has available memory. **If this error is ignored, no decoding result may be output with the continuously sent streams.**|
| 0xA005800D | Buffer allocation failure due to too large requested data buffer or other reasons.| - |
| 0xA005800E | Empty buffer.| Decoding is not complete, so there is no decoding result in the buffer. Try again after the decoding result is loaded to the buffer.|
| 0xA005800F | Full buffer.| The input stream data transmission is too fast, which causes full buffer. Slow down the transmission of input stream data, or increase the buffer size when creating a channel.|
| 0xA0058010 | Uninitialized system or absent dependencies.| Check that the system initialization API is called.|
| 0xA0058011 | The address is incorrect.| - |
| 0xA0058012 | System busy.| Check whether the total number of VDEC channels reaches the upper limit.|
| 0xA0058013 | Not enough buffer.| - |
| 0xA0058014 | Hardware or software processing timeout.| - |
| 0xA0058015 | System error.| - |
| 0xA005803F | Maximum return. The error code value of the module must be less than this value.| - |
