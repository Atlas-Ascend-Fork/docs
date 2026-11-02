# VENC

The video encoder (VENC) encodes YUV420SP images into H.264/H.265 video streams. For details about the VENC functions and restrictions, see [DVPP Media Acceleration Library](https://hiascend.com/en/document/redirect/CannCommunityDvppApi).

This section describes the API call sequence of VENC, and sample code is also provided to help you better understand the sequence.

## API Call Sequence

If video encoding is involved during app development, ensure that your app contains the code logic for such video encoding. **For details about the API call sequence, see [API Calling Process](interface_calling_process.md).**

**Figure 1** Video encoding process
![](figures/video-encoding.png)

This module implements video encoding. The key APIs are described as follows:

1. Call `acl.media.venc_create_channel` to create a channel for video encoding.
    - Perform the following steps before creating a channel for video encoding.
        1. Call `acl.media.venc_create_channel_desc` to create channel description.
        2. Call `acl.media.venc_set_channel_desc_param` to set the channel description attributes, including the thread, callback function, video coding protocol, and input image format.

            1. Create the callback function beforehand to get the encoding output and free resources promptly. See `acl.media.venc_set_channel_desc_callback` for the callback function prototype.

                After the encoding is complete, you are advised to free the buffer for storing the input images and the corresponding image description in the callback function in a timely manner. The output buffer is managed by the system. Therefore, the output buffer does not need to be freed by the user.

            2. The user needs to create a thread in advance and customize a thread function. Calling `acl.rt.process_report` in the thread function triggers the callback function in the previous step after a specified period of time.

            >[!NOTE]NOTE
            >`acl.media.venc_set_channel_desc_param` is recommended for setting the channel description attributes. You can set a particular attribute by passing the corresponding enum value to this API call.
            >The `acl.media.venc.set_channel_desc` series of earlier versions are also supported, where each attribute is set using a separate API.

    - The following APIs are encapsulated in `acl.media.venc_create_channel` and do not need to be called separately:
        1. `acl.rt.create_stream`: explicitly creates a stream. It is internally used for VENC.
        2. `acl.rt.subscribe_report`: specifies a thread for processing the callback function in a stream. The callback function and thread are specified by calling `acl.media.venc_set_channel_desc_param`.

2. **Call `acl.media.venc_send_frame` to encode a YUV420SP image into H.264/H.265 video streams.**
    - Perform the following steps **before encoding a video stream:**
        - Call `acl.media.dvpp_create_pic_desc` to create the description of the input image, and call `acl.media.dvpp_set_pic_desc` to configure the input image, such as the memory address, memory size, and image format.
        - Call `acl.media.venc_create_frame_config` to create the single-frame configuration data, and call `acl.media.venc_set_frame_config series` to configure whether to forcibly restart the I-frame interval or end the frame.

    - **During video encoding**, `acl.media.venc_send_frame` encapsulates `acl.rt.launch_callback` to insert a callback function to be executed to the stream. `acl.rt.launch_callback` does not need to be called separately.
    - **After video encoding**, use the callback function to obtain the result:

3. Call `acl.media.venc_destroy_channel` to destroy a video processing channel.
    - The channel is destroyed only after the transmitted frames are encoded and the callback function is processed.
    - The following APIs are encapsulated in `acl.media.venc_destroy_channel` and do not need to be called separately:
        - `acl.rt.unsubscribe_report`: unsubscribes from a thread. (The callback function in the stream is no longer processed by the specified thread.)
        - `acl.rt.destroy_stream`: destroys a stream.

    - Call `acl.media.venc_destroy_channel_desc` to destroy the channel description after the channel is destroyed.
    - After destroying the channel description, destroy the thread created in the first step.

## Sample Code

[Click here](https://gitee.com/ascend/samples/tree/master/python/level2_simple_inference/0_data_process/venc_image) to view the complete code.

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......

# 1. Resource initialization: Create an AclVenc object for initialization.
# 1.1 Perform initialization.
ret = acl.init()
# 1.2 Allocate runtime resources.
# Call acl.rt.get_run_mode to obtain the run mode of the software stack and determine the logic of the memory allocation API call based on the run mode.
runMode, ret = acl.rt.get_run_mode()

# 2. Create a thread for executing the callback function and thread function.
def cb_thread_func(self, args_list):
    ctx = args_list[0]
    timeout = args_list[1]
    print("[info] thread args_list = ", self.ctx, timeout, self.g_callbackRunFlag, "\n")
    ret = acl.rt.set_context(ctx)
    assert ret == 0

    while self.g_callbackRunFlag is True:
        print("[info] thread g_callbackRunFlag = ", self.g_callbackRunFlag, "\n")
        ret = acl.rt.process_report(timeout)
        print("[info] acl.rt.process_report =", ret)

timeout = 1000
g_callbackRunFlag = True
self.cb_thread_id, ret = acl.util.start_thread(self.cb_thread_func, [self.ctx, timeout])

# 3. Create a callback function.
# 3.1 Obtain stream data output.
def get_stream_data(self, stream_desc):
    stream_data = acl.media.dvpp_get_stream_desc_data(stream_desc)
    assert stream_data is not None
    stream_data_size = acl.media.dvpp_get_stream_desc_size(stream_desc)
    print("[info] stream_data size", stream_data_size)
    # stream memcpy d2h
    np_data = np.zeros(stream_data_size, dtype=np.byte)

    bytes_data = np_data.tobytes()
    np_data_ptr = acl.util.bytes_to_ptr(bytes_data)
    ret = acl.rt.memcpy(np_data_ptr, stream_data_size,
                         stream_data, stream_data_size,
                         memcpy_kind.get("ACL_MEMCPY_DEVICE_TO_HOST"))
    assert ret == 0
    return np_data
# 3.2 Save the video stream to a file using the callback function.
def callback_func(self, input_pic_desc, output_stream_desc, user_data):
    # Obtain the video encoding result and convert it into a NumPy object.
    output_numpy = self.get_stream_data(output_stream_desc)
    with open('./data/output.h265', 'ab') as f:
        f.write(output_numpy)
    print("[INFO] [callback_func] stream size =", acl.media.dvpp_get_stream_desc_size(output_stream_desc))

# 4. Create the description of a video encoding channel.
self.venc_channel_desc = acl.media.venc_create_channel_desc()

# 5. Set the description of a video encoding channel. The thread and callback function need to be created in advance.
# venc_channel_desc is of the aclvencChannelDesc type.
venc_format = 1
venc_entype = 0
input_width = 1280
input_height = 720
ret = acl.media.venc_set_channel_desc_thread_id(self.venc_channel_desc, self.cb_thread_id)
ret = acl.media.venc_set_channel_desc_callback(self.venc_channel_desc, self.callback_func)
ret = acl.media.venc_set_channel_desc_entype(self.venc_channel_desc, venc_entype)
ret = acl.media.venc_set_channel_desc_pic_format(self.venc_channel_desc, venc_format)
ret = acl.media.venc_set_channel_desc_key_frame_interval(self.venc_channel_desc, 16)
ret = acl.media.venc_set_channel_desc_pic_height(self.venc_channel_desc, input_height)
ret = acl.media.venc_set_channel_desc_pic_width(self.venc_channel_desc, input_width )

# 6. Create a channel for processing video streams and the single-frame encoding configuration.
ret = acl.media.venc_create_channel(self.venc_channel_desc)
# vencFrameConfig_ is of the aclvencFrameConfig type.
frame_config = acl.media.venc_create_frame_config()

# 7. Allocate the device buffer dataDev to store the input video data for encoding.
# 7.1 Read image data.
output_pic_size = (input_width * input_height * 3) // 2
print("[INFO] output_pic_size:", output_pic_size, " load vdec file:", venc_file_path)
file_context = np.fromfile(venc_file_path, dtype=np.byte)
file_size = file_context.size
bytes_data = file_context.tobytes()
file_mem = acl.util.bytes_to_ptr(bytes_data)
input_size = file_size
# If the run mode of the software stack obtained by calling acl.rt.get_run_mode is ACL_HOST, transmit image data of the host to the device by calling acl.rt.memcpy. After the data transfer is complete, call acl.rt.free_host to release the host memory in a timely manner.
# If the run mode of the software stack obtained by calling acl.rt.get_run_mode is ACL_DEVICE, allocate device buffers directly to store the input image data.
# The run mode is ACL_HOST.
input_mem, ret = acl.media.dvpp_malloc(input_size)
assert ret == 0
ret = acl.rt.memcpy(input_mem, input_size, file_mem,
                     file_size, memcpy_kind.get("ACL_MEMCPY_HOST_TO_DEVICE"))
assert ret == 0

# 8. Perform video encoding.
def venc_set_frame_config(self, frame_config, eos, iframe):
    ret = acl.media.venc_set_frame_config_eos(frame_config, eos)
    assert ret == 0
    ret = acl.media.venc_set_frame_config_force_i_frame(frame_config, iframe)
    assert ret == 0

def venc_process(self, venc_channel_desc, input_mem, input_size, frame_config):
   # Set the frame to a non-end frame.
    self.venc_set_frame_config(frame_config, 0, 0)
    print("[INFO] set frame config")
    self.test_get_frame_config(frame_config)

    # set picture description
    dvpp_pic_desc = acl.media.dvpp_create_pic_desc()
    assert dvpp_pic_desc is not None
    ret = acl.media.dvpp_set_pic_desc_data(dvpp_pic_desc, input_mem)
    assert ret == 0
    ret = acl.media.dvpp_set_pic_desc_size(dvpp_pic_desc, input_size)
    assert ret == 0
    print("[INFO] set pic desc")

    # Send one image to the encoder for encoding.
    venc_cnt = 16
    while venc_cnt:
        ret = acl.media.venc_send_frame(venc_channel_desc, dvpp_pic_desc, 0, frame_config, 0)
        assert ret == 0
        print("[INFO] venc send frame")
        venc_cnt -= 1
    # When an empty image with eos set to 1 is sent, the current encoding ends.
    self.venc_set_frame_config(frame_config, 1, 0)
    ret = acl.media.venc_send_frame(venc_channel_desc, 0, 0, frame_config, 0)
    assert ret == 0

# 9. Destroy allocations.
ret = acl.media.dvpp_free(input_mem)
ret = acl.media.venc_destroy_frame_config(frame_config)
assert ret == 0
print("[INFO] free resources")
g_callbackRunFlag = False
ret = acl.util.stop_thread(self.cb_thread_id)
print("[INFO] thread join")

# 10. Destroy runtime allocations.
# Perform deinitialization.
ret = acl.finalize()
# ....
```

You can call `acl.media.venc_set_channel_desc_param` to set the channel description attributes and call `acl.media.venc_get_channel_desc_param` to obtain the attribute values of the channel description. The sample code is as follows:

```bash
ACL_VENC_THREAD_ID_UINT64 = 0          # Callback thread ID
ACL_VENC_CALLBACK_PTR = 1              # Callback function
ACL_VENC_PIXEL_FORMAT_UINT32 = 2       # Input image format
ACL_VENC_ENCODE_TYPE_UINT32 = 3        # Video encoding protocol
ACL_VENC_PIC_WIDTH_UINT32 = 4          # Input image width
ACL_VENC_PIC_HEIGHT_UINT32 = 5         # Input image height
ACL_VENC_KEY_FRAME_INTERVAL_UINT32 = 6 # Keyframe interval
ACL_VENC_BUF_ADDR_PTR = 7              # Address of the encoding output buffer
ACL_VENC_BUF_SIZE_UINT32 = 8           # Size of the encoding output buffer
ACL_VENC_RC_MODE_UINT32 = 9            # Bit rate control mode
ACL_VENC_SRC_RATE_UINT32 = 10          # Frame rate of the input stream
ACL_VENC_MAX_BITRATE_UINT32 = 11       # Output bit rate
ACL_VENC_MAX_IP_PROP_UINT32 = 12       # I-frame to P-frame bit allocation ratio within a GOP

# Set the callback functions.
ret = acl.media.venc_set_channel_desc_param(self.venc_channel_desc, ACL_VENC_CALLBACK_PTR, self.callback_func)
# Obtain the callback function.
get_cb_func, ret = acl.media.venc_get_channel_desc_param(self.venc_channel_desc, ACL_VENC_CALLBACK_PTR)

PIXEL_FORMAT_YUV_SEMIPLANAR_420 = 1
# Set the input image format.
ret = acl.media.venc_set_channel_desc_param(self.venc_channel_desc, ACL_VENC_PIXEL_FORMAT_UINT32, PIXEL_FORMAT_YUV_SEMIPLANAR_420)
# Obtain the input image format.
get_pic_format, ret = acl.media.venc_get_channel_desc_param(self.venc_channel_desc, ACL_VENC_PIXEL_FORMAT_UINT32)

width = 128
# Set the image width.
ret = acl.media.venc_set_channel_desc_param(self.venc_channel_desc, ACL_VENC_PIC_WIDTH_UINT32, width)
# Obtain the image width.
get_width, ret = acl.media.venc_get_channel_desc_param(self.venc_channel_desc, ACL_VENC_PIC_WIDTH_UINT32)

height = 128
# Set the image height.
ret = acl.media.venc_set_channel_desc_param(self.venc_channel_desc, ACL_VENC_PIC_HEIGHT_UINT32, height)
# Obtain the image height.
get_height, ret = acl.media.venc_get_channel_desc_param(self.venc_channel_desc, ACL_VENC_PIC_HEIGHT_UINT32)
```
