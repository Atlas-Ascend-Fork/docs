<!-- npu="910b,910,310p,310b" id1 -->
# VPC

Vision Preprocessing Core (VPC) supports image cropping, resizing, and format conversion. For details about the VPC functions and restrictions, see [DVPP Media Acceleration Library](https://hiascend.com/en/document/redirect/CannCommunityDvppApi).

Taking image cropping and scaling as an example, this section explains the API call sequence during VPC-based image processing. Sample code of typical functions is also provided to help you better understand the API call sequence:

- [Sample Code for Image Resizing](#sample-code-for-image-resizing)
- [Sample Code for Image Cropping](#sample-code-for-image-cropping)

## Typical API Call Sequence (Image Resizing)

If image cropping and resizing are involved during app development, ensure that your app contains the code logic for such image processing. For details about the API call sequence, see [API Calling Process](interface_calling_process.md).
<!-- npu="910b,910,310p,310b" id2 -->
If the DVPP APIs are called on the host, the image processing result will be stored in the device memory. To access this result, transfer the result data to the host.
<!-- end id2 -->
**Figure 1** API call sequence (image resizing)
![](figures/api-call-sequence-(taking-resizing-as-an-example).png)

The current system supports image cropping and resizing. The key APIs are described as follows:

1. Call `acl.himpi.sys_init` to initialize the media data processing system.
2. Call `acl.himpi.vpc_create_chn` to create a channel.
3. Call `acl.himpi.dvpp_malloc` to allocate device buffers to store the input or output data.
    <!-- npu="310b" id3 -->
    For Atlas 200I/500 A2 inference products, the `acl.rt.malloc` API can also be used to allocate memory.
    <!-- end id3 -->
    <!-- npu="910b" id4 -->
    For Atlas A2 products, the `acl.rt.malloc` API can also be used to allocate memory.
    <!-- end id4 -->
    <!-- npu="910b,310b" id5 -->
    For Atlas 200I/500 A2 inference products and Atlas A2 products, `acl.himpi.dvpp_malloc` allocates a dedicated buffer for processing media data. However, the address space of the dedicated buffer is limited. If buffer planning is cared or buffer resources are limited, you are advised to allocate buffer by calling `acl.rt.malloc`.
    <!-- end id5 -->
4. Perform operations such as cropping and resizing. Take resizing as an example. For details about other functions (such as format conversion and pyramid), see the API description under [DVPP Media Acceleration Library](https://hiascend.com/en/document/redirect/CannCommunityDvppApi).

    Call `acl.himpi.vpc_resize` to resize the image. `acl.himpi.vpc_resize` is an asynchronous API. The API call only delivers a task. You also need to call `acl.himpi.vpc_get_process_result` to wait for the task to complete.

    - You can call `acl.himpi.vpc_get_process_result` in the same thread as `acl.himpi.vpc_resize`, or start a new thread. Multiple threads can improve efficiency, but require inter-thread synchronization.
    - To reformat the input image during cropping and resizing, you can set different formats for the input and output images.
    <!-- npu="310p" id6 -->
    - For Atlas inference products, call `acl.rt.get_run_mode` to obtain the run mode of the software stack. If the run mode is `ACL_HOST` and the image data output by VPC needs to be displayed on the host, allocate the host buffer and call `acl.rt.memcpy` to transfer the output image data from the device to the host. If the data does not need to be displayed on the host, it can be used as the input of model inference. For details about model inference, see [Model Management](model_management.md) and [Dynamic AIPP Model Inference](dynamic_AIPP_inference.md).
    <!-- end id6 -->
5. Call `acl.himpi.dvpp_free` to free the input and output buffers.
    <!-- npu="310b" id7 -->
    For Atlas 200I/500 A2 inference products, if `acl.rt.malloc` is used to allocate buffers, `acl.rt.free` needs to be used to free buffers.
    <!-- end id7 -->
    <!-- npu="910b" id8 -->
    For Atlas A2 products, if `acl.rt.malloc` is used to allocate buffers, `acl.rt.free` needs to be used to free buffers.
    <!-- end id8 -->
6. Call `acl.himpi.vpc_destroy_chn` to destroy the channel.
7. Call `acl.himpi.sys_exit` to deinitialize the media data processing system.

## Sample Code for Image Resizing

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
chn_attr = {'attr': 0, 'pic_width': 0, 'pic_height': 0}
ret = acl.himpi.vpc_create_chn(channel_id, chn_attr)

# 6. Perform resizing.
# 6.1 Construct a dictionary for storing input image information.
input_pic = {'picture_width': 1920,
             'picture_height': 1080,
             'picture_width_stride': 1920,
             'picture_height_stride': 1080,
             'picture_format': HI_PIXEL_FORMAT_YUV_SEMIPLANAR_420}
input_pic["picture_buffer_size"] = input_pic["picture_width_stride"] * input_pic["picture_height_stride"] * 3 // 2
picture_address, ret = acl.himpi.dvpp_malloc(0, input_pic["picture_buffer_size"])
input_pic["picture_address"] = picture_address

# 6.2 If the run mode is ACL_HOST, allocate the host buffer, load the input image data into the host buffer, and call acl.rt.memcpy to transfer the image data from the host to the device. After the data transfer is complete, free the host buffer in a timely manner. In other modes, directly load the input image data into the device buffer.
# Directly load the input image data into the device buffer.
if run_mode == ACL_HOST:
    # Read the input image to the buffer.
    vpc_file = np.fromfile(vpc_file_path, dtype=np.byte)
    vpc_file_size = vpc_file.itemsize * vpc_file.size

    bytes_data = vpc_file.tobytes()
    vpc_file_ptr = acl.util.bytes_to_ptr(bytes_data)
    # Data transfer:
    ret = acl.rt.memcpy(input_pic["picture_address"], input_pic["picture_buffer_size"],
                        vpc_file_ptr, vpc_file_size, ACL_MEMCPY_HOST_TO_DEVICE)
else:
    # Read the input image to the buffer.
    vpc_file = np.fromfile(vpc_file_path, dtype=np.byte)
    vpc_file_size = vpc_file.itemsize * vpc_file.size

    bytes_data = vpc_file.tobytes()
    vpc_file_ptr = acl.util.bytes_to_ptr(bytes_data)
    # Data transfer:
    ret = acl.rt.memcpy(input_pic["picture_address"], input_pic["picture_buffer_size"],
                        vpc_file_ptr, vpc_file_size, ACL_MEMCPY_DEVICE_TO_DEVICE)


# 6.3 Construct a dictionary for storing output image information.
output_pic = {'picture_width': 960,
                'picture_height': 540,
                'picture_width_stride': 960,
                'picture_height_stride': 540,
                'picture_format': HI_PIXEL_FORMAT_YUV_SEMIPLANAR_420}
output_pic["picture_buffer_size"] = output_pic["picture_width_stride"] * output_pic["picture_height_stride"] * 3 // 2
picture_address, ret = acl.himpi.dvpp_malloc(0, output_pic["picture_buffer_size"])
output_pic["picture_address"] = picture_address
# Initialize the buffer.
ret = acl.rt.memset(output_pic["picture_address"], output_pic["picture_buffer_size"], 0, output_pic["picture_buffer_size"])

# 6.4 Call the image resizing API.
task_id, ret = acl.himpi.vpc_resize(channel_id, input_pic, output_pic, 0, 0, 0, -1)

# 6.5 Wait until the task processing is complete. The output image data is stored in the buffer specified by outputPic.picture_address.
ret = acl.himpi.vpc_get_process_result(channel_id, task_id, -1)

# 6.6 If the run mode is ACL_HOST and the image data output by VPC needs to be displayed on the host, allocate the host buffer and call acl.rt.memcpy to transfer the output image data from the device to the host. If the data does not need to be displayed on the host, it can be used as the input of model inference.
# The output image data of VPC can be directly used as the input for model inference.
if run_mode == ACL_HOST:
        np_output = np.zeros(output_pic.get('picture_buffer_size'), dtype=np.byte)

        bytes_data = np_output.tobytes()
        np_output_ptr = acl.util.bytes_to_ptr(bytes_data)
        ret = acl.rt.memcpy(np_output_ptr, output_pic.get('picture_buffer_size'), output_pic.get("picture_address"),
                            output_pic.get('picture_buffer_size'), ACL_MEMCPY_DEVICE_TO_HOST)
        # ......
else
    # You can directly use the output image data of VPC in the buffer specified by outputPic.picture_address.
    # ......

# 6.7 Free the input and output buffers.
ret = acl.himpi.dvpp_free(input_pic['picture_address'])
ret = acl.himpi.dvpp_free(output_pic['picture_address'])

# 7. Destroy the channel.
ret = acl.himpi.vpc_destroy_chn(channel_id)

# 8. Deinitialize the media data processing system.
ret = acl.himpi.sys_exit()

# 9. Deallocate runtime resources.
# 10. Perform deinitialization.
ret = acl.finalize()
```

## Sample Code for Image Cropping

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
chn_attr = {'attr': 0, 'pic_width': 0, 'pic_height': 0}
ret = acl.himpi.vpc_create_chn(channel_id, chn_attr)

# 6. Perform cropping.
# 6.1 Construct a dictionary for storing input image information.
input_pic = {'picture_width': 1920,
             'picture_height': 1080,
             'picture_width_stride': 1920,
             'picture_height_stride': 1080,
             'picture_format': HI_PIXEL_FORMAT_YUV_SEMIPLANAR_420}
input_pic["picture_buffer_size"] = input_pic["picture_width_stride"] * input_pic["picture_height_stride"] * 3 // 2
picture_address, ret = acl.himpi.dvpp_malloc(0, input_pic["picture_buffer_size"])
input_pic["picture_address"] = picture_address

# 6.2 If the run mode is ACL_HOST, allocate the host buffer, load the input image data into the host buffer, and call acl.rt.memcpy to transfer the image data from the host to the device. After the data transfer is complete, free the host buffer in a timely manner. In other modes, directly load the input image data into the device buffer.
# Directly load the input image data into the device buffer.
if run_mode == ACL_HOST:
    # Read the input image to the buffer.
    vpc_file = np.fromfile(vpc_file_path, dtype=np.byte)
    vpc_file_size = vpc_file.itemsize * vpc_file.size

    bytes_data = vpc_file.tobytes()
    vpc_file_ptr = acl.util.bytes_to_ptr(bytes_data)
    # Data transfer:
    ret = acl.rt.memcpy(input_pic["picture_address"], input_pic["picture_buffer_size"],
                        vpc_file_ptr, vpc_file_size, ACL_MEMCPY_HOST_TO_DEVICE)
else:
    # Read the input image to the buffer.
    vpc_file = np.fromfile(vpc_file_path, dtype=np.byte)
    vpc_file_size = vpc_file.itemsize * vpc_file.size

    bytes_data = vpc_file.tobytes()
    vpc_file_ptr = acl.util.bytes_to_ptr(bytes_data)
    # Data transfer:
    ret = acl.rt.memcpy(input_addr, input_size, vpc_file_ptr, vpc_file_size, ACL_MEMCPY_DEVICE_TO_DEVICE)

# 6.3 Construct a dictionary for storing output image information.
multithreading_count = 1
crop_region_infos = []
for i in range(multithreading_count):
    output_pic = {'picture_width': 960,
                  'picture_height': 540,
                  'picture_width_stride': 960,
                  'picture_height_stride': 540,
                  'picture_format': HI_PIXEL_FORMAT_YUV_SEMIPLANAR_420}
    output_pic["picture_buffer_size"] = output_pic["picture_width_stride"] * output_pic["picture_height_stride"] * 3 // 2
    picture_address, ret = acl.himpi.dvpp_malloc(0, output_pic["picture_buffer_size"])
    output_pic["picture_address"] = picture_address

    ret = acl.rt.memset(output_pic["picture_address"], output_pic["picture_buffer_size"], 0, output_pic["picture_buffer_size"])
    crop_region = {'top_offset': 0, 'left_offset': 0, 'crop_width': 960, 'crop_height': 540}
    crop_region_info = {'dest_pic_info': output_pic, 'crop_region': crop_region}
    crop_region_infos.append(crop_region_info)

# 6.4 Call the image cropping API.
task_id, ret = acl.himpi.vpc_crop(channel_id, input_pic, crop_region_infos, 1, -1)

# 6.5 Wait until the task processing is complete. The output image data is stored in the buffer specified by outputPic.picture_address.
ret = acl.himpi.vpc_get_process_result(channel_id, task_id, -1)

# 6.6 If the run mode is ACL_HOST and the image data output by VPC needs to be displayed on the host, allocate the host buffer and call acl.rt.memcpy to transfer the output image data from the device to the host. If the data does not need to be displayed on the host, it can be used as the input of model inference.
# The output image data of VPC can be directly used as the input for model inference.
if run_mode == ACL_HOST:
    np_output = np.zeros(output_pic.get('picture_buffer_size'), dtype=np.byte)

    bytes_data = np_output.tobytes()
    np_output_ptr = acl.util.bytes_to_ptr(bytes_data)
    ret = acl.rt.memcpy(np_output_ptr, output_pic.get('picture_buffer_size'), output_pic.get("picture_address"),
                        output_pic.get('picture_buffer_size'), ACL_MEMCPY_DEVICE_TO_HOST)
    # ......
else
    # You can directly use the output image data of VPC in the buffer specified by outputPic.picture_address.
    # ......

# 6.7 Free the input and output buffers.
ret = acl.himpi.dvpp_free(input_pic['picture_address'])
ret = acl.himpi.dvpp_free(output_pic['picture_address'])

# 7. Destroy the channel.
ret = acl.himpi.vpc_destroy_chn(channel_id)

# 8. Deinitialize the media data processing system.
ret = acl.himpi.sys_exit()

# 9. Deallocate runtime resources.
# 10. Perform deinitialization.
ret = acl.finalize()
```
<!-- end id1 -->
