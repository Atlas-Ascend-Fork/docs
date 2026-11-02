<!-- npu="910b,910,310p,310b" id1 -->
# JPEGE Image Encoding

The JPEG encoder (JPEGE) encodes YUV images into JPG images. For details about the JPEGE functions, see [DVPP Media Acceleration Library](https://hiascend.com/en/document/redirect/CannCommunityDvppApi).

This section describes the API call sequence of JPEGE, and sample code is also provided to help you better understand the sequence.

## API Call Sequence

During application development, if YUV images need to be encoded into JPEG images, the application must contain the encoding code logic. For details about the encoding API call sequence, see [API Calling Process](interface_calling_process.md) and then the process description in this section.

**Figure 1** API call sequence
![](figures/api-call-sequence-7.png)

The current system supports encoding YUV images into JPEG images. The key APIs are described as follows:

1. Call `acl.himpi.sys_init` to initialize the media data processing system.
2. Call `acl.himpi.venc_create_chn` to create a channel.

    After a channel is created, you can set advanced encoding parameters as required, such as the scenario mode and advanced parameters of the stream controller. For details, see the API description in `acl.himpi.venc_set_jpeg_param` to `acl.himpi.venc_compact_jpeg_tables`.

3. Call `acl.himpi.venc_get_fd` to convert the channel ID into a file descriptor.
4. Call `acl.himpi.sys_create_epoll` to create a DVPP epoll instance.
5. Call `acl.himpi.sys_ctl_epoll` to add the file descriptor of the encoding channel to the epoll instance. Skip this step if the select or poll function is used.
6. Call `acl.himpi.venc_start_chn` to notify the channel to start encoding.
7. Call `acl.himpi.dvpp_malloc` to allocate device buffers for storing the input data.
    <!-- npu="910b,310b" id2 -->
    For Atlas 200I/500 A2 inference products and Atlas A2 products, `acl.himpi.dvpp_malloc` allocates a dedicated buffer for processing media data. However, the address space of the dedicated buffer is limited. If buffer planning is cared or buffer resources are limited, you are advised to allocate buffer by calling `acl.rt.malloc`.
    <!-- end id2 -->
8. Start a user-mode thread and call `acl.himpi.sys_wait_epoll` to wait until the encoding is complete.
9. Call `acl.himpi.venc_send_frame` to feed your stream to the encoder.
10. Once the encoding is complete, the `acl.himpi.sys_wait_epoll`, select, or poll function returns. You can call `acl.himpi.venc_query_status` to query the encoding status and then call `acl.himpi.venc_get_stream` to obtain the encoding result.
11. Call `acl.himpi.venc_release_stream` to free the buffer in time when the encoding result is no longer needed. Otherwise, no more encoding task can be performed because the encoding buffer is used up.
12. Call `acl.himpi.dvpp_free` to free the input buffer.
    <!-- npu="310b" id3 -->
    For Atlas 200I/500 A2 inference products, if `acl.rt.malloc` is used to allocate buffers, `acl.rt.free` needs to be used to free buffers.
    <!-- end id3 -->
    <!-- npu="910b" id4 -->
    For Atlas A2 products, if `acl.rt.malloc` is used to allocate buffers, `acl.rt.free` needs to be used to free buffers.
    <!-- end id4 -->
13. When the source images have been completely fed, call `acl.himpi.venc_stop_chn` to stop the channel from receiving new images.
14. Call `acl.himpi.sys_ctl_epoll` to delete the file descriptor of the encoding channel from the epoll instance.
15. After all encoding tasks are complete, call `acl.himpi.venc_destroy_chn` to destroy the encoding channel and free the buffer.
16. Call `acl.himpi.sys_close_epoll` to destroy the DVPP epoll instance.
17. Call `acl.himpi.sys_exit` to deinitialize the media data processing system.

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
venc_attr = {'type': HI_PT_JPEG, 'profile': 0,
             'max_pic_width': 128, 'pic_width': 128,
             'max_pic_height': 128, 'pic_height': 128,
             'buf_size': 1024 * 1024 * 2, 'is_by_frame': 1}
jpeg_attr = {'recv_mode':HI_VENC_PIC_RECV_SINGLE,
            'mpf_cfg':{'large_thumbnail_num': 0}}
attr = {'venc_attr':venc_attr, 'jpeg_attr':jpeg_attr}
ret = acl.himpi.venc_create_chn(channel_id, attr)

# 6. Set JPEGE parameters.
param, ret = acl.himpi.venc_get_jpeg_param(channel_id)
param['qfactor'] = 100
ret = acl.himpi.venc_set_jpeg_param(channel_id, param)

# 7. Notify the encoder to start receiving input data.
recv_param = {'recv_pic_num': -1}
ret = acl.himpi.venc_start_chn(channel_id, recv_param)

# 8. Send the input data.
# 8.1 Allocate the input buffer.
input_size = 128 * 128 * 3 // 2
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

# 8.2 Send the input data and start encoding.
v_frame = {'width': 128,
           'height': 128,
           'field': HI_VIDEO_FIELD_FRAME,
           'pixel_format': HI_PIXEL_FORMAT_YUV_SEMIPLANAR_420,
           'video_format': HI_VIDEO_FORMAT_LINEAR,
           'compress_mode': HI_COMPRESS_MODE_NONE,
           'dynamic_range': HI_DYNAMIC_RANGE_SDR8,
           'color_gamut': HI_COLOR_GAMUT_BT709,
           'header_stride': [0, 0, 0],
           'width_stride': [128, 0, 0],
           'height_stride': [0, 0, 0],
           'header_phys_addr': [0, 0, 0],
           'phys_addr': [0, 0, 0],
           'header_virt_addr': [0, 0, 0],
           'virt_addr': [input_addr, 0, 0],
           'time_ref': 0, 'pts': cur_time}
frame = {'v_frame':v_frame, 'pool_id':0, 'mod_id':HI_ID_VGS}
ret = acl.himpi.venc_send_frame(channel_id, frame, 0)

# 9. Obtain the encoding result.
# 9.1 Handle the encoding completion event through epoll.
fd = acl.himpi.venc_get_fd(channel_id)
epoll_fd, ret = acl.himpi.sys_create_epoll(10)

event['data'] = fd
event['events'] = HI_DVPP_EPOLL_IN
ret = acl.himpi.sys_ctl_epoll(epoll_fd, HI_DVPP_EPOLL_CTL_ADD, fd, event)

# Before the encoding is complete, timeout occurs. The next step is not performed until the encoding is complete.
events, eventCount, ret = acl.himpi.sys_wait_epoll(epoll_fd, 3, 1000)

# 9.2 Obtain the encoding result.
status, ret = acl.himpi.venc_query_status(channel_id)
stream = {'pack_cnt': status['cur_packs']}
stream, ret = acl.himpi.venc_get_stream(channel_id, stream, 1000)
# 9.3 If the run mode is ACL_HOST and the host needs to use the encoded streams, allocate the host buffer and call acl.rt.memcpy to transfer the output streams from the device to the host. In other modes, directly use the encoded streams.
# Obtain the encoded streams.
if run_mode == ACL_HOST:
    # Allocate the host buffer.
    output_buffer, ret= acl.rt.malloc_host(output_size)
    # Data transfer:
    ret = acl.rt.memcpy(output_buffer, output_size, stream['pack'][0]['addr'], output_size, ACL_MEMCPY_DEVICE_TO_HOST)
    # ......
    # After data is used, free the buffer in a timely manner.
    ret = acl.rt.free_host(output_buffer)
else:
    # You can directly use the encoded streams, which are stored in the buffer specified by stream['pack'][0]['addr'].
    # ......

# 10. Free the input buffer and release the output streams.
ret = acl.himpi.dvpp_free(input_addr)
ret = acl.himpi.venc_release_stream(channel_id, stream)

# 11. Notify the encoder to stop receiving input data.
ret = acl.himpi.venc_stop_chn(channel_id)
ret = acl.himpi.sys_ctl_epoll(epoll_fd, HI_DVPP_EPOLL_CTL_DEL, fd, event)
ret = acl.himpi.sys_close_epoll(epoll_fd)

# 12. Destroy the channel.
ret = acl.himpi.venc_destroy_chn(channel_id)

# 13. Deinitialize the media data processing system.
ret = acl.himpi.sys_exit()

# 14. Deallocate runtime resources.
# 15. Perform deinitialization.
ret = acl.finalize()
```
<!-- end id1 -->
