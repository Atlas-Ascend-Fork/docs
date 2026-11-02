<!-- npu="910b,910,310p,310b" id1 -->
# JPEGD

The JPEG decoder (JPEGD) can decode .jpg, .jpeg, .JPG, and .JPEG images into YUV images. For details about the JPEGD functions and restrictions, see [DVPP Media Acceleration Library](https://hiascend.com/en/document/redirect/CannCommunityDvppApi).

This section describes the API call sequence of JPEGD, and sample code is also provided to help you better understand the sequence.

## API Call Sequence

If JPEG image decoding is involved during application development, the application must contain the decoding code logic. For details about the API call sequence of image decoding, see [API Calling Process](interface_calling_process.md).

**Figure 1** API call sequence
![](figures/api-call-sequence-9.png)

The current system supports decoding JPEG images. The key APIs are described as follows:

1. Call `acl.himpi.sys_init` to initialize the media data processing system.
2. Call `acl.himpi.vdec_create_chn` to create a channel.
3. Call `acl.himpi.dvpp_malloc` to allocate device buffers to store the input or output data.
    <!-- npu="910b,310b" id2 -->
    A dedicated buffer is allocated for processing media data. However, the address space of the dedicated buffer is limited. If buffer planning is cared or buffer resources are limited, you are advised to allocate buffer by calling `acl.rt.malloc`.
    <!-- end id2 -->
4. Before decoding, call `acl.himpi.vdec_start_recv_stream` to notify the decoder to start receiving streams, and then call `acl.himpi.vdec_send_stream` to send the streams to be decoded. `acl.himpi.vdec_send_stream` is an asynchronous API. The API call only delivers a task. You also need to call `acl.himpi.vdec_get_frame` to obtain the decode result data. You can call `acl.himpi.vdec_release_frame` to release frame-related resources.

    After the decoding is complete, call `acl.himpi.vdec_stop_recv_stream` to notify the decoder to stop receiving streams.

5. Call `acl.himpi.dvpp_free` to free the input and output buffers.
    <!-- npu="310b" id3 -->
    For Atlas 200I/500 A2 inference products, if `acl.rt.malloc` is used to allocate buffers, `acl.rt.free` needs to be used to free buffers.
    <!-- end id3 -->
    <!-- npu="910b" id4 -->
    For Atlas A2 products, if `acl.rt.malloc` is used to allocate buffers, `acl.rt.free` needs to be used to free buffers.
    <!-- end id4 -->

6. Call `acl.himpi.vdec_destroy_chn` to destroy the channel.
7. Call `acl.himpi.sys_exit` to deinitialize the media data processing system.

## Sample Code

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
# 1. Obtain the run mode of the software stack. Different run modes lead to different API call sequences (for example, whether data transfer is required).
run_mode, ret = acl.rt.get_run_mode()

# 2. Perform initialization.
ret = acl.init()

# 3. Allocate runtime resources.
# 4. Initialize the media data processing system.
ret = acl.himpi.sys_init()

# 5. Create a channel.
channel_id = 0
attr = {'type': HI_PT_JPEG, 'mode': HI_VDEC_SEND_MODE_FRAME,
        'pic_width': 1920, 'pic_height': 1080,
        'stream_buf_size': 1920 * 1080, 'frame_buf_size': 0,
        'frame_buf_cnt': 9}

ret = acl.himpi.vdec_create_chn(channel_id, attr)
# 6. Set channel attributes.
jpegd_param_dict, ret = acl.himpi.vdec_get_chn_param(channel_id)
jpegd_param_dict["pic_param"]["pixel_format"] = HI_PIXEL_FORMAT_YUV_SEMIPLANAR_420
jpegd_param_dict["pic_param"]["alpha"] = 255
jpegd_param_dict["display_frame_num"] = 0
ret = acl.himpi.vdec_set_chn_param(channel_id, jpegd_param_dict)

# 7. The decoder starts receiving streams.
ret = acl.himpi.vdec_start_recv_stream(channel_id)

# 8. Send streams.
# 8.1 Allocate the input buffer.
# input_size indicates the buffer size occupied by the input image. The following uses 1,024 bytes as an example. You need to calculate the actual buffer size.
input_size = 1024
input_addr, ret = acl.himpi.dvpp_malloc(0, input_size)

#If the run mode is ACL_HOST, allocate the host buffer, load the input image data into the host buffer, and call acl.rt.memcpy to transfer the image data from the host to the device. After the data transfer is complete, free the host buffer in a timely manner. In other modes, directly load the input image data into the device buffer.
#Directly load the input image data into the device buffer.
if run_mode == ACL_HOST:
    # Allocate the host buffer.
    input_buffer, ret= acl.rt.malloc_host(input_size)
    # Read the input image to the buffer.
    vdec_file = np.fromfile(vdec_file_path, dtype=np.byte)
    vdec_file_size = vdec_file.itemsize * vdec_file.size

    bytes_data = vdec_file.tobytes()
    vdec_file_ptr = acl.util.bytes_to_ptr(bytes_data)
    # Data transfer:
    ret = acl.rt.memcpy(input_addr, input_size, vdec_file_ptr, vdec_file_size, ACL_MEMCPY_HOST_TO_DEVICE)
else:
    # Read the input image to the buffer.
    vdec_file = np.fromfile(vdec_file_path, dtype=np.byte)
    vdec_file_size = vdec_file.itemsize * vdec_file.size

    bytes_data = vdec_file.tobytes()
    vdec_file_ptr = acl.util.bytes_to_ptr(bytes_data)
    # Data transfer:
    ret = acl.rt.memcpy(input_addr, input_size, vdec_file_ptr, vdec_file_size, ACL_MEMCPY_DEVICE_TO_DEVICE)

# 8.2 Construct a dictionary for storing input image information.
stream = {'end_of_frame': HI_TRUE, 'end_of_stream': HI_FALSE,
          'need_display': HI_TRUE, 'pts': 0,
          'len': input_size, 'addr': vdec_file_ptr}
img_info, ret = acl.himpi.dvpp_get_image_info(HI_PT_JPEG, stream)
if run_mode == ACL_HOST:
    # If the data on the host is not used, free the host buffer in a timely manner.
    ret = acl.rt.free_host(input_buffer)

stream['addr'] =  input_addr

# 8.3 Construct a dictionary for storing output image information and allocate the output buffer.
out_pic_info = {"width": img_info['width'],
                "height": img_info['height'],
                "width_stride": img_info['width_stride'],
                "height_stride": img_info['height_stride'],
                "pixel_format": HI_PIXEL_FORMAT_UNKNOWN,
                "buffer_size": img_info['img_buf_size']}
out_buffer, ret = acl.himpi.dvpp_malloc(0, out_pic_info['buffer_size'])
out_pic_info['vir_addr'] = out_buffer

# 8.4 Send the input image to be decoded.
ret = acl.himpi.vdec_send_stream(channel_id, stream, out_pic_info, 0)

# 9. Receive the decoding result.
# 9.1 Obtain the decoding result.
frame_info, supplement, stream, ret = acl.himpi.vdec_get_frame(channel_id, 0)
if ret == 0:
    dec_result = frame_info['v_frame']['frame_flag']
    if dec_result == 0: #  0: Decode success
        print("Chn %u GetFrame Success, Decode Success \n"%channel_id)
    else: # Decode fail
        print("Chn %u GetFrame Success, Decode Fail \n"%channel_id)

# 9.2 If the run mode is ACL_HOST and the image data output by JPEGD needs to be displayed on the host, allocate the host buffer and call aclrtMemcpy to transfer the output image data from the device to the host.
# Obtain the output image data of JPEGD.

if run_mode == ACL_HOST:
    # Allocate the host buffer.
    output_buffer, ret= acl.rt.malloc_host(out_pic_info['buffer_size'])
    # Data transfer:
    ret = acl.rt.memcpy(output_buffer, out_pic_info['buffer_size'], frame_info['v_frame']['virt_addr'][0], out_pic_info['buffer_size'], ACL_MEMCPY_DEVICE_TO_HOST)

    # ......
    # After data is used, free the buffer in a timely manner.
    ret = acl.rt.free_host(output_buffer)
else:
    # You can directly use the output image data of JPEGD in the buffer specified by outputPic.picture_address.
    # ......

# 9.3 Free the input and output buffers.
ret = acl.himpi.dvpp_free(frame_info['v_frame']['virt_addr'][0])
ret = acl.himpi.dvpp_free(stream['addr'])

# 9.4 Destroy allocations.
ret = acl.himpi.vdec_release_frame(channel_id, frame_info)

# 10. The decoder stops receiving streams.
ret = acl.himpi.vdec_stop_recv_stream(channel_id)

# 11. Destroy the channel.
ret = acl.himpi.vdec_destroy_chn(channel_id)

# 12. Deinitialize the media data processing system.
ret = acl.himpi.sys_exit()

# 13. Deallocate runtime resources.
# 14. Perform deinitialization.
ret = acl.finalize()
```
<!-- end id1 -->
