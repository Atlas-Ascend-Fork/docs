<!-- npu="910b,910,310p,310b" id1 -->
# VENC

The video encoder (VENC) encodes YUV420SP images into H.264/H.265 video streams. For details about the VENC functions, see [DVPP Media Acceleration Library](https://hiascend.com/en/document/redirect/CannCommunityDvppApi).

This section describes the API call sequence of VENC, and sample code is also provided to help you better understand the sequence.

## API Call Sequence
<!-- npu="310p,310b" id2 -->
If video encoding is involved during app development, ensure that your app contains the code logic for such video encoding. For details about the API call sequence, see [API Calling Process](interface_calling_process.md).
<!-- end id2 -->
**Figure 1** API call sequence
![](figures/api-call-sequence-10.png)

The current system supports encoding H.264 and H.265 video streams. The key APIs are described as follows:

1. Call `acl.himpi.sys_init` to initialize the media data processing system.
2. Call `acl.himpi.venc_create_chn` to create a channel.

    After a channel is created, you can set advanced encoding parameters as required, such as the scenario mode and advanced parameters of the stream controller. For details, see the API description in `acl.himpi.venc_set_jpeg_param` to `acl.himpi.venc_compact_jpeg_tables`.

3. Call `acl.himpi.venc_get_fd` to convert the channel ID into a file descriptor.
4. Call `acl.himpi.sys_create_epoll` to create a DVPP epoll instance.

    In open Ctrl CPU form, to ensure compatibility, it is allowed to call the `select` or `poll` function of the Linux OS for an older version of an app to wait for the encoding to complete. You are advised to use the API call sequence shown in the preceding figure to ensure the evolution of later versions.

5. Call `acl.himpi.sys_ctl_epoll` to add the file descriptor of the encoding channel to the epoll instance.

    Skip this step if the `select` or `poll` function is used.

6. Call `acl.himpi.venc_start_chn` to notify the channel to start encoding.
7. Call `acl.himpi.dvpp_malloc` to allocate device buffers for storing the input data.
    <!-- npu="310b" id3 -->
    For Atlas 200I/500 A2 inference products, `acl.himpi.dvpp_malloc` allocates a dedicated buffer for processing media data. However, the address space of the dedicated buffer is limited. If buffer planning is cared or buffer resources are limited, you are advised to allocate buffer by calling `acl.rt.malloc`.
    <!-- end id3 -->
8. Start a user-mode thread and call `acl.himpi.sys_wait_epoll` to wait until the encoding is complete.
9. Call `acl.himpi.venc_send_frame` to feed your stream to the encoder.
10. Once the encoding is complete, the `acl.himpi.sys_wait_epoll`, select, or poll function returns. You can call `acl.himpi.venc_query_status` to query the encoding status and then call `acl.himpi.venc_get_stream` to obtain the encoding result.
11. Call `acl.himpi.venc_release_stream` to free the buffer in time when the encoding result is no longer needed. Otherwise, no more encoding task can be performed because the encoding buffer is used up.
12. Call `acl.himpi.dvpp_free` to free the input buffer.
    <!-- npu="310b" id4 -->
    For Atlas 200I/500 A2 inference products, if `acl.rt.malloc` is used to allocate buffers, `acl.rt.free` needs to be used to free buffers.
    <!-- end id4 -->
13. When the source images have been completely fed, call `acl.himpi.venc_stop_chn` to stop the channel from receiving new images.
14. Call `acl.himpi.sys_ctl_epoll` to delete the file descriptor of the encoding channel from the epoll instance.
15. After all encoding tasks are complete, call `acl.himpi.venc_destroy_chn` to destroy the encoding channel and free the buffer.
16. Call `acl.himpi.sys_close_epoll` to destroy the DVPP epoll instance.
17. Call `acl.himpi.sys_exit` to deinitialize the media data processing system.

## Optimization of Video Encoding Quality

When implementing the VENC function, you can set basic parameters during channel creation or set advanced parameters by calling the corresponding `set` API to optimize the video encoding quality. The following optimization settings are available and can be used jointly:

- Settings for H.264 monitoring with the resolution of 720p, GOP of 60, frame rate of 30 FPS, and bit rate of 1 Mbit/s: CBR mode, HI\_VENC\_SCENE\_0, stats\_time = 2, profile = 2, and macroblock-level bit rate control = disabled.
- Settings for H.265 movies with the resolution of 1080p, GOP of 30, frame rate of 25 FPS, and bit rate of 2 Mbit/s: CBR mode, HI\_VENC\_SCENE\_1, stats\_time = 1, and macroblock-level bit rate control = disabled.

**You can optimize the video encoding quality using the following methods:**

- **Setting basic parameters for overall quality optimization**

    The encoding quality of videos with different resolutions is subject to the video frame rate, GOP, and bit rate. When a channel is created by calling `acl.himpi.venc_create_chn`, you can set the encoding profile and parameters such as the frame rate, GOP, and bit rate in CBR/VBR/AVBR/CVBR/QVBR mode for H.264/H.265 encoding to optimize the video encoding quality.

    - Encoding profile, determined by the `profile` attribute in the `hi_venc_chn_attr`["venc_attr"] dictionary.
    - Frame rate, determined by the `src_frame_rate` input frame rate and `dst_frame_rate` output frame rate in the `hi_venc_chn_attr`["rc_attr"] dictionary.
    - GOP, determined by the `gop` attribute in the `hi_venc_chn_attr`["rc_attr"] dictionary.
    - Bit rate, determined by the `bit_rate`, `max_bit_rate`, or `target_bit_rate` attribute in the `hi_venc_chn_attr`["rc_attr"] dictionary.

    **Table 1** Values of the frame rate, GOP, and bit rate in typical scenarios
    <!-- npu="310p,310b" id5 -->
    | Image Quality/Resolution| Frame Rate| GOP | Bit Rate (Mbit/s)|
    | --- | --- | --- | --- |
    | 4K<br>3840\*2160/4096\*2160 | 25 or 30| It is recommended that the GOP value be an integral multiple of the frame rate. For example, if the frame rate is 25, the recommended GOP value is 25 or 50.| Video data obtaining<br>8 to 12 for H.264/H.265 streams<br>Show/Livestreaming/Short video<br>6 to 12 for H.265 streams<br>N/A for H.264 streams<br>Game video<br>10 to 16 for H.264/H.265 streams<br>MDC<br>Greater than 16 for H.264/H.265 streams|
    | 2K<br>2560\*1440 | 25 or 30| It is recommended that the GOP value be an integral multiple of the frame rate. For example, if the frame rate is 25, the recommended GOP value is 25 or 50.| Video data obtaining<br>6 to 10 for H.264/H.265 streams<br>Show/Livestreaming/Short video<br>4.8 to 8 for H.265 streams<br>N/A for H.264 streams<br>Game video<br>6 to 10 for H.264/H.265 streams<br>MDC<br>Greater than 12 for H.264/H.265 streams|
    | 1080p (Blu-ray)<br>1920\*1080 | 25 or 30| It is recommended that the GOP value be an integral multiple of the frame rate. For example, if the frame rate is 25, the recommended GOP value is 25 or 50.| Video data obtaining<br>1 to 4 for H.265 streams<br>2 to 6 for H.264 streams<br>Show/Livestreaming/Short video<br>1.4 to 3.6 for H.265 streams<br>2 to 4.8 for H.264 streams<br>Game video<br>3 to 6 for H.264/H.265 streams<br>MDC<br>Greater than 8 for H.264/H.265 streams|
    | 720p (HD)<br>1280\*720 | 25 or 30| It is recommended that the GOP value be an integral multiple of the frame rate. For example, if the frame rate is 25, the recommended GOP value is 25 or 50.| Video data obtaining<br>0.8 to 2 for H.265 streams<br>1 to 3 for H.264 streams<br>Show/Livestreaming/Short video<br>1 to 2 for H.265 streams<br>1 to 3 for H.264 streams<br>Game video<br>2 to 4 for H.264/H.265 streams<br>MDC<br>Greater than 4 for H.264/H.265 streams|
    | 480p/D1_N (SD)<br>854\*480/720\*480 | 25 or 30| It is recommended that the GOP value be an integral multiple of the frame rate. For example, if the frame rate is 25, the recommended GOP value is 25 or 50.| Video data obtaining<br>0.3 to 0.7 for H.265 streams<br>0.6 to 1.4 for H.264 streams<br>Show/Livestreaming/Short video<br>0.25 to 0.6 for H.265 streams<br>0.3 to 0.7 for H.264 streams<br>Game video<br>N/A<br>MDC<br>N/A|
    | 576p/D1 (SD)<br>720\*576 | 25 or 30| It is recommended that the GOP value be an integral multiple of the frame rate. For example, if the frame rate is 25, the recommended GOP value is 25 or 50.| Video data obtaining<br>0.3 to 0.7 for H.265 streams<br>0.6 to 1.4 for H.264 streams<br>Show/Livestreaming/Short video<br>0.25 to 0.6 for H.265 streams<br>0.3 to 0.7 for H.264 streams<br>Game video<br>N/A<br>MDC<br>N/A|
    | 270p (smooth)<br>480\*270 | 25 or 30| It is recommended that the GOP value be an integral multiple of the frame rate. For example, if the frame rate is 25, the recommended GOP value is 25 or 50.| Video data obtaining<br>N/A<br>Show/Livestreaming/Short video<br>0.2 for H.265 streams<br>0.3 for H.264 streams<br>Game video<br>N/A<br>MDC<br>N/A|
    | CIF P/N<br>352\*288/320\*240 | 25 or 30| It is recommended that the GOP value be an integral multiple of the frame rate. For example, if the frame rate is 25, the recommended GOP value is 25 or 50.| Video data obtaining<br>0.25 for H.264/H.265 streams<br>Show/Livestreaming/Short video<br>N/A<br>Game video<br>N/A<br>MDC<br>N/A|
    <!-- end id5 -->
- **Setting advanced parameters for quality tuning**

    You can call the APIs listed in the following table to set the bit rate control mode, macroblock-level bit rate control parameters, and encoding scene mode to tune video encoding quality.

    **Table 2** Advanced settings

    | Item| API| Parameter| Description|
    | --- | --- | --- | --- |
    | Bit rate control mode| `acl.himpi.venc_create_chn` | `rc_mode` in the `hi_venc_chn_attr`["rc_attr"] dictionary| Set this parameter to `CBR` if a stable bit rate or a large peak signal to noise ratio (PSNR) and qualified bit rate is required.<br>Set this parameter to `VBR` to save the bit rate and improve the subjective quality of encoding.<br>Set this parameter to `AVBR` to save the bit rate and improve the subjective quality of encoding with lots of still images in the scene.<br>Set this parameter to `QVBR` if a large PSNR is required and there is no strict requirement on the bit rate increase.<br>Set this parameter to `CVBR` to save the bit rate and improve the subjective quality of encoding when the bandwidth and storage space can also be used for optimization.|
    | Statistical time of the bit rate control model| `acl.himpi.venc_create_chn` | `stats_time` in the `hi_venc_chn_attr`["rc_attr"] dictionary| Set this parameter to a large value in the scenario where long-term bit rate stability is required without considering short-term fluctuations, for example, DVR storage. This setting increases the threshold for re-encoding to cut the number of re-encoding times, but also increases bit rate fluctuations at the same time.|
    | Macroblock-level bit rate control| `acl.himpi.venc_set_rc_param` | `threshold_i`, `threshold_p`, `threshold_b`, `direction` and `row_qp_delta` in the `hi_venc_rc_param` dictionary| Disable this function when encoding complex images with rich details, or when objective indicators such as the PSNR are concerned.|
    | Start QP value of the first frame| `acl.himpi.venc_create_chn` | `first_frame_start_qp` in the `hi_venc_rc_param` dictionary| In typical use cases, if the configured bit rate is less than the reference value in Table 1 and the first frame of the encoded video is blurry, you are advised to configure the `first_frame_start_qp` attribute and set the parameter value to the intermediate value of [min_i_qp, max_i_qp]. For example, if [min_i_qp, max_i_qp] is [30, 40], set `first_frame_start_qp` to `35` and `max_reencode_times` to `0` to obtain better encoding quality.|
    | Encoding scene mode| `acl.himpi.venc_set_scene_mode` | `hi_venc_scene_mode` class| Set this parameter to `HI_VENC_SCENE_0` for security scenes. Set this parameter to `HI_VENC_SCENE_1` for autonomous driving, livestreaming, gaming, animations, and movies.|

<!-- npu="310p,310b" id6 -->
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

# 5. Set VENC parameters.
param = {'mod_type':HI_VENC_MOD_H265}
param, ret = acl.himpi.venc_get_mod_param(param)
param['jpeg_mod_param']['one_stream_buf'] = 1
ret = acl.himpi.venc_set_mod_param(param)

# 6. Create a channel.
channel_id = 0
venc_attr = {'type': HI_VENC_MOD_H265, 'profile': 0,
             'max_pic_width': 128, 'pic_width': 128,
             'max_pic_height': 128, 'pic_height': 128,
             'buf_size': 1024 * 1024 * 2, 'is_by_frame': 1}
rc_attr = {'rc_mode':HI_VENC_RC_MODE_H265_VBR,
           'h265_vbr':{'gop': 30, 'stats_time': 1,
                       'src_frame_rate': 30, 'dst_frame_rate': 30,
                       'max_bit_rate': 4000}}
gop_attr = {'gop_mode':0, 'normal_p':{'ip_qp_delta':3}}
attr = {'venc_attr':venc_attr, 'rc_attr':rc_attr, 'gop_attr':gop_attr}
ret = acl.himpi.venc_create_chn(channel_id, attr)

# 7. Notify the encoder to start receiving input data.
recv_param = {'recv_pic_num':-1}
ret = acl.himpi.venc_start_chn(channel_id, recv_param)

# 8. Send the input data.
# 8.1 Allocate the input buffer.
input_size = 128 * 128 * 3 // 2
input_addr, ret = acl.himpi.dvpp_malloc(0, input_size)

# If the run mode is ACL_HOST, allocate the host buffer, load the input data into the host buffer, and call acl.rt.memcpy to transfer the host data to the device. After the data transfer is complete, free the host buffer in a timely manner. In other modes, directly load the input data into the device buffer.
# Directly load the input data into the device buffer.
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
           'time_ref': 0,'pts': cur_time}
frame = {'v_frame':v_frame, 'pool_id':0, 'mod_id':HI_ID_VENC}
ret = acl.himpi.venc_send_frame(channel_id, frame, 0)

# 9. Obtain the encoding result.
# 9.1 Handle the encoding completion event through epoll.
fd = acl.himpi.venc_get_fd(channel_id)
epoll_fd, ret = acl.himpi.sys_create_epoll(10)

event = {'data': fd, 'events': HI_DVPP_EPOLL_IN}
ret = acl.himpi.sys_ctl_epoll(epoll_fd, HI_DVPP_EPOLL_CTL_ADD, fd, event)

# Before the encoding is complete, timeout occurs. The next step is not performed until the encoding is complete.
events, eventCount, ret = acl.himpi.sys_wait_epoll(epoll_fd, 3, 1000)

# 9.2 Obtain the encoding result.
status, ret = acl.himpi.venc_query_status(channel_id)
stream = {'pack_cnt': status['cur_packs']}
stream, ret = acl.himpi.venc_get_stream(self.channel_id, stream, 1000)
# 9.3 If the run mode is ACL_HOST and the host needs to use the encoded streams, allocate the host buffer and call acl.rt.memcpy to transfer the output streams from the device to the host.
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
<!-- end id6 -->
<!-- end id1 -->
