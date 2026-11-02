<!-- npu="910b,910,310p,310b" id1 -->
# PNGD

This section describes the API call sequence of PNGD, and sample code is also provided to help you better understand the process.

The PNG Decoder (PNGD) decodes images in PNG format. For details about the PNGD functions, see [DVPP Media Acceleration Library](https://hiascend.com/en/document/redirect/CannCommunityDvppApi).

## API Call Sequence

If PNG image decoding is involved during application development, the application must contain the decoding code logic. For details about the API call sequence of image decoding, see [API Calling Process](interface_calling_process.md).

**Figure 1** API call sequence
![](figures/api-call-sequence-8.png)

The current system supports decoding PNG images. The key APIs are described as follows:

1. Call `acl.himpi.sys_init` to initialize the media data processing system.
2. Call `acl.himpi.pngd_create_chn` to create a channel.
3. Call `acl.himpi.dvpp_malloc` to allocate device buffers to store the input or output data.
    <!-- npu="910b,310b" id2 -->
    For Atlas 200I/500 A2 inference products and Atlas A2 products, `acl.himpi.dvpp_malloc` allocates a dedicated buffer for processing media data. However, the address space of the dedicated buffer is limited. If buffer planning is cared or buffer resources are limited, you are advised to allocate buffer by calling `acl.rt.malloc`.
    <!-- end id2 -->
4. Call `acl.himpi.pngd_send_stream` to send the streams to be decoded. `acl.himpi.pngd_send_stream` is an asynchronous API. The API call only delivers a task. You also need to call `acl.himpi.pngd_get_image_data` to obtain the decoding result.
5. Call `acl.himpi.dvpp_free` to free the input and output buffers.
    <!-- npu="310b" id3 -->
    For Atlas 200I/500 A2 inference products, if `acl.rt.malloc` is used to allocate buffers, `acl.rt.free` needs to be used to free buffers.
    <!-- end id3 -->
    <!-- npu="910b" id4 -->
    For Atlas A2 products, if `acl.rt.malloc` is used to allocate buffers, `acl.rt.free` needs to be used to free buffers.
    <!-- end id4 -->
6. Call `acl.himpi.pngd_destroy_chn` to destroy the channel.
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
attr = {"stream_que_cnt": STREAM_QUE_CNT}
channel_id = 0
ret = acl.himpi.pngd_create_chn(channel_id, attr)

# 6. Send streams.
# 6.1 Allocate the input buffer.
input_addr, ret = acl.himpi.dvpp_malloc(0, input_size)

# If the run mode is ACL_HOST, allocate the host buffer, load the input image data into the host buffer, and call acl.rt.memcpy to transfer the image data from the host to the device. After the data transfer is complete, free the host buffer in a timely manner. In other modes, directly load the input image data into the device buffer.
# Directly load the input image data into the device buffer.
if run_mode == ACL_HOST:
    # Read the input image to the buffer.
    jpege_file = np.fromfile(jpege_file_path, dtype=np.byte)
    jpege_file_size = jpege_file.itemsize * jpege_file.size

    bytes_data = jpege_file.tobytes()
    jpege_file_ptr = acl.util.bytes_to_ptr(bytes_data)
    # Data transfer:
    ret = acl.rt.memcpy(input_addr, input_size, jpege_file_ptr, jpege_file_size, ACL_MEMCPY_HOST_TO_DEVICE)
else:
    # Read the input image to the buffer.
    jpege_file = np.fromfile(jpege_file_path, dtype=np.byte)
    jpege_file_size = jpege_file.itemsize * jpege_file.size

    bytes_data = jpege_file.tobytes()
    jpege_file_ptr = acl.util.bytes_to_ptr(bytes_data)
    # Data transfer:
    ret = acl.rt.memcpy(input_addr, input_size, jpege_file_ptr, jpege_file_size, ACL_MEMCPY_DEVICE_TO_DEVICE)

# 6.2 Construct a dictionary for storing input image information.
stream = {"type": HI_PT_PNG, "addr": input_addr, "len": input_size, "pts": 0}
img_info, ret = acl.himpi.png_get_image_info(stream)

# 6.3 Construct a dictionary for storing output image information and allocate the output buffer.
output_addr, ret = acl.himpi.dvpp_malloc(0, img_info['img_buf_size'])
out_pic_info =  {"picture_address": output_addr,
                 "picture_buffer_size": img_info['img_buf_size'],
                 "picture_width": img_info['width'],
                 "picture_height": img_info['height'],
                 "picture_width_stride": img_info['width_stride'],
                 "picture_height_stride": img_info['height_stride'],
                 "picture_format": HI_PIXEL_FORMAT_UNKNOWN}
ret = acl.himpi.pngd_send_stream(channel_id, stream, out_pic_info, 0)

# 7. Receive the decoding result.
# 7.1 Obtain the decoding result.
pic_info, get_stream, ret = acl.himpi.pngd_get_image_data(channel_id, -1)
if ret == 0: #  Decode success
    print("Chn %u GetFrame Success, Decode Success \n"%channel_id)
elif ret == HI_ERR_PNGD_BUF_EMPTY: # Decoding
    print("Chn %u Decoding, try again \n"%channel_id)
else: # Decode Fail
    print("Chn %u GetFrame Success, Decode Fail \n"%channel_id)

# 7.2 If the run mode is ACL_HOST and the image data output by PNGD needs to be displayed on the host, allocate the host buffer and call acl.rt.memcpy to transfer the output image data from the device to the host.
# Obtain the output image data of PNGD.
if run_mode == ACL_HOST:
    # Allocate the host buffer.
    output_buffer, ret= acl.rt.malloc_host(output_size)
    # Data transfer:
    ret = acl.rt.memcpy(output_buffer, output_size, stream['pack'][0]['addr'], output_size, ACL_MEMCPY_DEVICE_TO_HOST)
    # ......
    # After data is used, free the buffer in a timely manner.
    ret = acl.rt.free_host(output_buffer)
else:
    # You can directly use the output image data of PNGD in the buffer specified by outputPic.picture_address.
    # ......

# 7.3 Free the input buffer and release the output streams.
ret = acl.himpi.dvpp_free(input_addr)
ret = acl.himpi.dvpp_free(output_addr)

# 8. Destroy the channel.
ret = acl.himpi.pngd_destroy_chn(channel_id)

# 9. Deinitialize the media data processing system.
ret = acl.himpi.sys_exit()

# 10. Deallocate runtime resources.
# 11. Perform deinitialization.
ret = acl.finalize()
```
<!-- end id1 -->
