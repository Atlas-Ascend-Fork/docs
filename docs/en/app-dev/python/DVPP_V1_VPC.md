# VPC

Vision Preprocessing Core (**VPC**) supports image cropping, resizing, and format conversion. For details about the VPC functions and restrictions, see [DVPP Media Acceleration Library](https://hiascend.com/en/document/redirect/CannCommunityDvppApi).

Taking image cropping and scaling as an example, this section explains the API call sequence during VPC-based image processing. Sample code of typical functions is also provided to help you better understand the API call sequence:

- [Sample Code for Image Resizing](#sample-code-for-image-resizing)
- [Sample Code for Format Conversion](#sample-code-for-format-conversion)
- [Sample Code for Image Cropping and Resizing (Single-Image, Single-ROI)](#sample-code-for-image-cropping-and-resizing-single-image-single-roi)
- [Sample Code for Image Cropping, Resizing, and Pasting (Single-Image, Single-ROI)](#sample-code-for-image-cropping-resizing-and-pasting-single-image-single-roi)
- [Sample Code for Image Cropping and Pasting (Single-Image, Multi-ROI)](#sample-code-for-image-cropping-and-pasting-single-image-multi-roi)

## API Call Sequence (for Cropping and Resizing)

If image cropping and resizing are involved during app development, ensure that your app contains the code logic for such image processing. **For details about the API call sequence, see [API Calling Process](interface_calling_process.md)**.

**Figure 1** Image cropping and resizing process
![](figures/cropping-and-resizing.png)

The key APIs are described as follows (taking cropping and resizing as an example):

1. Call `acl.media.dvpp_create_channel_desc` to **create a channel description**.
2. Call `acl.media.dvpp_create_channel` to **create a channel for image data processing**.
3. Call `acl.media.dvpp_create_roi_config` and `acl.media.dvpp_create_resize_config` to **create the crop ROI position configuration and resizing configuration**, respectively.
4. Before cropping and resizing, call `acl.media.dvpp_malloc` to **allocate device buffers** for storing the input or output data.
5. **Perform cropping and resizing.**
    - About cropping:
        - Call the asynchronous API `acl.media.dvpp_vpc_crop_async` to crop a selected ROI from the input image according to `crop_area` and load the crop ROI to the output buffer.

            The cropped image will be resized again if `crop_area` is different from that of the output image.

        - Call the asynchronous API `acl.media.dvpp_vpc_crop_and_paste_async` to crop a selected ROI from the input image, and paste the crop ROI to the specified area in the target image as the output image.
            - The cropped image will be resized again if the size of the `crop_area` is inconsistent with that of the `paste_area`
            - To paste the `paste_area` on a canvas loaded to the output buffer, modify the code logic as follows: **allocate the output buffer and then load a canvas to the allocated buffer**.

    - About resizing:
        - Call the asynchronous API `acl.media.dvpp_vpc_resize_async` to **resize the input image to the size of the canvas**.
        - Calculate the buffer for storing the resized image based on the YUV420SP format as follows: `widthStride` x `heightStride` x 3/2.

    - For asynchronous APIs, call `acl.rt.synchronize_stream` to block the application until all tasks in the specified stream are complete.

6. Call `acl.media.dvpp_free` to **free the input and output buffers**.
7. Call `acl.media.dvpp_destroy_roi_config` and `acl.media.dvpp_destroy_resize_config` to **destroy the crop ROI position configuration and resizing configuration**, respectively.
8. Call `acl.media.dvpp_destroy_channel` to **destroy the image data processing channel**.

    Call `acl.media.dvpp_destroy_channel_desc` to destroy the channel description after the channel is destroyed.

## Sample Code for Image Resizing

- Call `acl.media.dvpp_create_channel` to create an image data processing channel and call `acl.media.dvpp_destroy_channel` to destroy the channel.
- Call the asynchronous API `acl.media.dvpp_vpc_resize_async` to resize the input image to the size of the output image. For asynchronous APIs, call `acl.rt.synchronize_stream` to block the application until all tasks in the specified stream are complete.

- Call `acl.media.dvpp_create_resize_config` to create an image resizing configuration.

    You can also specify a desired algorithm by calling `acl.media.dvpp_set_resize_config_interpolation`.
<!-- npu="910b,910,310p,310b" id2 -->
[Click here](https://gitee.com/ascend/samples/tree/master/python/level2_simple_inference/1_classification/vpc_resnet50_imagenet_classification) to view the complete code.
<!-- end id2 -->
Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......

# 1. Perform initialization.
ret = acl.init()

# 2. Allocate runtime resources.
# 3. Create resizing configuration data. The algorithm nearest neighbor interpolation is used by default, which cannot be modified.
# self.resize_config is of the acldvppResizeConfig type.
self.resize_config = acl.media.dvpp_create_resize_config()

# 4. Create the description of the data processing channel. self.dvpp_channel_desc is of type acldvppChannelDesc.
self.dvpp_channel_desc = acl.media.dvpp_create_channel_desc()

# 5. Create a data processing channel.
ret = acl.media.dvpp_create_channel(self.dvpp_channel_desc)

# 6. Allocate an input buffer. The buffer size is calculated based on the formula. w and h indicate the actual sizes of the input image.
width_stride = ((w + 15) // 16) * 16
height_stride = ((h + 1) // 2) * 2
buffer_size = (width_stride * height_stride * 3) // 2
dev_in, ret = acl.media.dvpp_malloc(buffer_size )
self.dev_buffer['input_0'] = dev
# 7. Allocate an output buffer. The buffer size is calculated based on the formula. w and h indicate the resizing sizes of the input image.
width_stride = ((w + 15) // 16) * 16
height_stride = ((h + 1) // 2) * 2
buffer_size = (width_stride * height_stride * 3) // 2
dev_out, ret = acl.media.dvpp_malloc(buffer_size )
self.dev_buffer['output_0'] = dev_out

# 8. Create the description of the input image and set the attribute values.
# self.input_desc is of type acldvppPicDesc.
self.input_desc = acl.media.dvpp_create_pic_desc()
ret = acl.media.dvpp_set_pic_desc_data(self.input_desc, buffer)
ret = acl.media.dvpp_set_pic_desc_format(self.input_desc, YUV420)
ret = acl.media.dvpp_set_pic_desc_width(self.input_desc, width)
ret = acl.media.dvpp_set_pic_desc_height(self.input_desc, height)
ret = acl.media.dvpp_set_pic_desc_width_stride(self.input_desc, wstride)
ret = acl.media.dvpp_set_pic_desc_height_stride(self.input_desc, hstride)
ret = acl.media.dvpp_set_pic_desc_size(self.input_desc, size)

# 9. Create the description of the output image and set the attribute values.
# If the resized output image is used as the input for model inference, the width and height of the output image must meet the requirements of the model.
# self.output_desc is of type acldvppPicDesc.
self.output_desc= acl.media.dvpp_create_pic_desc()
ret = acl.media.dvpp_set_pic_desc_data(self.output_desc, buffer)
ret = acl.media.dvpp_set_pic_desc_format(self.output_desc, YUV420)
ret = acl.media.dvpp_set_pic_desc_width(self.output_desc, width)
ret = acl.media.dvpp_set_pic_desc_height(self.output_desc, height)
ret = acl.media.dvpp_set_pic_desc_width_stride(self.output_desc, wstride)
ret = acl.media.dvpp_set_pic_desc_height_stride(self.output_desc, hstride)
ret = acl.media.dvpp_set_pic_desc_size(self.output_desc, size)

# 10. Perform asynchronous resizing and call acl.rt.synchronize_stream to block the host until all tasks in the specified stream are complete.
ret = acl.media.dvpp_vpc_resize_async(self.dvpp_channel_desc, self.input_desc,
                                          self.output_desc, self.resize_config,
                                          self.stream)
ret = acl.rt.synchronize_stream(self.stream)

# 11. After resizing is complete, destroy the input and output image descriptions and free the input and output buffers.
ret = acl.media.dvpp_destroy_pic_desc(self.output_desc)
ret = acl.media.dvpp_destroy_pic_desc(self.input_desc)
ret = acl.media.dvpp_free(self.dev_buffer['input_0'] )
ret = acl.media.dvpp_free(self.dev_buffer['output_0'] )

# 12. Deallocate runtime resources.
# Perform deinitialization.
ret = acl.finalize()
# ......
```

<!-- npu="910b,910,310p,310b" id3 -->
## Sample Code for Format Conversion

You can convert formats by using either of the following methods:

- When cropping or resizing an image, you can call the corresponding API (for example, `acl.media.dvpp_vpc_crop_async`) and **set the formats of the input and output images to different values**.
- **To convert image format only**, you can call `acl.media.dvpp_vpc_convert_color_async`.

    The following is a code snippet of key steps for format conversion. It is for reference only. Do not copy, build, or run it directly. Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......

ACL_MEMCPY_HOST_TO_DEVICE = 1
ACL_MEMCPY_DEVICE_TO_HOST = 2
PIXEL_FORMAT_YUV_400 = 0
PIXEL_FORMAT_YUV_SEMIPLANAR_420 = 1

# 1. Perform initialization.
ret = acl.init()

# 2. Allocate runtime resources.
# 3. Create the description of the data processing channel. dvpp_channel_desc is of type acldvppChannelDesc.
dvpp_channel_desc = acl.media.dvpp_create_channel_desc()

# 4. Create a data processing channel.
ret = acl.media.dvpp_create_channel(dvpp_channel_desc)

# 5. Allocate input buffer.
input_width_stride = ((input_width + 15) // 16) * 16
input_height_stride = ((input_height + 1) // 2) * 2
# input_width_stride and input_height_stride indicate the width and height after image alignment respectively. The following uses a YUV420SP image as an example.
in_buffer_size = (input_width_stride * input_height_stride * 3) // 2
in_dev_buffer, ret = acl.media.dvpp_malloc(in_buffer_size)
np_yuv = np.fromfile(path, dtype=np.byte)
buffer_size = np_yuv.itemsize * np_yuv.size
bytes_data = np_yuv.tobytes()
np_yuv_ptr = acl.util.bytes_to_ptr(bytes_data)
ret = acl.rt.memcpy(in_dev_buffer, buffer_size, np_yuv_ptr,
                      buffer_size, ACL_MEMCPY_HOST_TO_DEVICE)

# 6. Allocate the CSC output buffer.
output_width_stride = ((output_width + 15) // 16) * 16
output_height_stride = ((output_height + 1) // 2) * 2
# output_width_stride and output_height_stride indicate the width and height after image alignment respectively. The following uses a YUV420SP image as an example.
out_buffer_size = (output_width_stride * output_height_stride * 3) // 2
out_dev_buffer, ret = acl.media.dvpp_malloc(out_buffer_size)

# 7. Create the description of the input image for CSC and set the attribute values.
input_desc = acl.media.dvpp_create_pic_desc()
ret = acl.media.dvpp_set_pic_desc_data(input_desc, in_dev_buffer)
ret = acl.media.dvpp_set_pic_desc_format(input_desc, PIXEL_FORMAT_YUV_SEMIPLANAR_420)
ret = acl.media.dvpp_set_pic_desc_width(input_desc, input_width)
ret = acl.media.dvpp_set_pic_desc_height(input_desc, input_height)
ret = acl.media.dvpp_set_pic_desc_width_stride(input_desc, input_width_stride)
ret = acl.media.dvpp_set_pic_desc_height_stride(input_desc, input_height_stride)
ret = acl.media.dvpp_set_pic_desc_size(input_desc, in_buffer_size)

# 8. Create the description of the output image for CSC and set the attribute values. The output height and width must be the same as those of the input.
# If the CSC output image is used as the input for model inference, the width and height of the output image must meet the requirements of the model.
output_desc = acl.media.dvpp_create_pic_desc()
ret = acl.media.dvpp_set_pic_desc_data(output_desc, out_dev_buffer)
ret = acl.media.dvpp_set_pic_desc_format(output_desc, PIXEL_FORMAT_YUV_400)
ret = acl.media.dvpp_set_pic_desc_width(output_desc, output_width)
ret = acl.media.dvpp_set_pic_desc_height(output_desc, output_height)
ret = acl.media.dvpp_set_pic_desc_width_stride(output_desc, output_width_stride)
ret = acl.media.dvpp_set_pic_desc_height_stride(output_desc, output_height_stride)
ret = acl.media.dvpp_set_pic_desc_size(output_desc, out_buffer_size)

# 9. Perform asynchronous CSC and call `acl.rt.synchronize_stream` to block the program until all tasks in the specified streams are complete.
ret = acl.media.dvpp_vpc_convert_color_async(dvpp_channel_desc, input_desc,
                                                  output_desc, stream)
ret = acl.rt.synchronize_stream(stream)

# 10. After CSC is complete, destroy the input and output image descriptions and free the input and output buffers.
ret = acl.media.dvpp_destroy_pic_desc(input_desc)
ret = acl.media.dvpp_destroy_pic_desc(output_desc)

np_output = np.zeros(out_buffer_size, dtype=np.byte)
bytes_data = np_output.tobytes()
np_output_ptr = acl.util.bytes_to_ptr(bytes_data)
# Transfer the processing result of the device to the host.
ret = acl.rt.memcpy(np_output_ptr, out_buffer_size, out_dev_buffer,
                     out_buffer_size, ACL_MEMCPY_DEVICE_TO_HOST)
ret = acl.media.dvpp_free(in_dev_buffer)
ret = acl.media.dvpp_free(out_dev_buffer)

# 11. Deallocate runtime resources.
# Perform deinitialization.
ret = acl.finalize()
# ......
```
<!-- end id3 -->
<!-- npu="910b,910,310p,310b" id4 -->
## Sample Code for Image Cropping and Resizing (Single-Image, Single-ROI)

Call the asynchronous API `acl.media.dvpp_vpc_crop_async` to crop a selected ROI from the input image according to `crop_area` and load the crop ROI to the output buffer.
<!-- npu="910b,910,310p,310b" id5 -->
[Click here](https://gitee.com/ascend/samples/tree/master/python/level2_simple_inference/1_classification/vpc_jpeg_resnet50_imagenet_classification) to view the complete code.
<!-- end id5 -->
Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......

# 1. Perform initialization.
ret = acl.init()

# 2. Allocate runtime resources.
# 3. Set the crop ROI and paste ROI.
# Set the top-left corner of the image as the coordinate origin. w and h indicate the original width and height of the image, respectively.
self.crop_area = acl.media.dvpp_create_roi_config(w // 2, w - 1, h // 2, h - 1)

# 4. Create the description of the data processing channel. dvpp_channel_desc is of type acldvppChannelDesc.
self.dvpp_channel_desc = acl.media.dvpp_create_channel_desc()

# 5. Create a data processing channel.
ret = acl.media.dvpp_create_channel(self.dvpp_channel_desc)

# 6. Create the description of the input/output image and set the attribute values.
self.input_desc = acl.media.dvpp_create_pic_desc()
assert self.input_desc is not None
# 6.1 User-defined method: Call set_picture_desc to set the input image description.
# Calculate the buffer size to store the image data, and set the image description and other attributes.
self.set_picture_desc(self.input_desc, w, h, "input", 0)
self.output_desc = acl.media.dvpp_create_pic_desc()
assert self.output_desc is not None
# 6.2 User-defined method: Call set_picture_desc to set the output image description.
out_buffer_size = self.set_picture_desc(self.output_desc, w // 2, h // 2, "output", 0)

# 7. Perform asynchronous cropping and call acl.rt.synchronize_stream to block the host until all tasks in the specified stream are complete.
ret = acl.media.dvpp_vpc_crop_async(self.dvpp_channel_desc, self.input_desc, self.output_desc, self.crop_area, self.stream)
ret = acl.rt.synchronize_stream(self.stream)

# 8. Destroy the allocations, including the input and output image descriptions, input and output buffers, channel description, and the channel.
ret = acl.media.dvpp_destroy_roi_config(self.crop_area)
ret = acl.media.dvpp_destroy_pic_desc(self.input_desc)
ret = acl.media.dvpp_destroy_pic_desc(self.output_desc)
# dev_buffer is a dictionary object, which is used to store the buffer allocated on the device.
for key in self.dev_buffer.keys():
    if self.dev_buffer[key]:
        ret = acl.media.dvpp_free(self.dev_buffer[key])
if self.dvpp_channel_desc:
    ret = acl.media.dvpp_destroy_channel(self.dvpp_channel_desc)
    assert ret == 0
    ret = acl.media.dvpp_destroy_channel_desc(self.dvpp_channel_desc)
    assert ret == 0

# 9. Deallocate runtime resources.
# 10. Perform deinitialization.
ret = acl.finalize()
# ......
```
<!-- end id4 -->
<!-- npu="910b,910,310p,310b" id6 -->
## Sample Code for Image Cropping, Resizing, and Pasting (Single-Image, Single-ROI)

- Call the asynchronous API `acl.media.dvpp_vpc_crop_resize_paste_async` to crop a selected ROI and paste the crop ROI on the canvas for output. For asynchronous APIs, call `acl.rt.synchronize_stream` to block the application until all tasks in the specified stream are complete.

    Call `acl.media.dvpp_vpc_crop_resize_paste_async` to implement cropping, resizing, and pasting. You can specify a resizing algorithm.

- The cropped image will be resized again if the size of the `crop_area` is inconsistent with that of the `paste_area`
- To paste the `paste_area` on a canvas loaded to the output buffer, modify the code logic as follows: allocate the output buffer and then load a canvas to the allocated buffer.
<!-- npu="910b,910,310p,310b" id7 -->
[Click here](https://gitee.com/ascend/samples/tree/master/python/level2_simple_inference/1_classification/vpc_jpeg_resnet50_imagenet_classification) to view the complete code.
<!-- end id7 -->
Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......

# 1. Perform initialization.
ret = acl.init()

# 2. Allocate runtime resources.
# 3. Create the description of the data processing channel. dvpp_channel_desc is of type acldvppChannelDesc.
self.dvpp_channel_desc = acl.media.dvpp_create_channel_desc()

# 4. Create a data processing channel.
ret = acl.media.dvpp_create_channel(self.dvpp_channel_desc)

# 5. Create the description of the output image and set the attribute values.
self.output_desc = acl.media.dvpp_create_pic_desc()
assert self.output_desc is not None
out_buffer_size = self.set_picture_desc(self.output_desc, w // 2, h // 2, "output", 0)

# 6. Create the description of the input image and set the attribute values.
self.input_desc = acl.media.dvpp_create_pic_desc()
assert self.input_desc is not None
self.set_picture_desc(self.input_desc, w, h, "input", 0)

# 7. Load image data and copy it to the device.
np_yuv = np.fromfile(path, dtype=np.byte)
in_buffer_size = np_yuv.itemsize * np_yuv.size
bytes_data = np_yuv.tobytes()
np_yuv_ptr = acl.util.bytes_to_ptr(bytes_data)
ret = acl.rt.memcpy(self.dev_buffer["input_0"], in_buffer_size, np_yuv_ptr,
                      in_buffer_size, ACL_MEMCPY_HOST_TO_DEVICE)
assert ret == 0

# 8. Set the crop ROI and paste ROI.
self.crop_area = acl.media.dvpp_create_roi_config(w // 2, w - 1, h // 2, h - 1)
self.paste_area = acl.media.dvpp_create_roi_config(w // 4, w // 2 - 1, h // 4, h // 2 - 1)

# 9. Perform asynchronous cropping and resizing.
self.resize_config = acl.media.dvpp_create_resize_config()
ret = acl.media.dvpp_vpc_crop_resize_paste_async(self.dvpp_channel_desc,
                                                       self.input_desc, self.output_desc,
                                                       self.crop_area, self.paste_area,
                                                       self.resize_config, self.stream)
assert ret == 0
ret = acl.rt.synchronize_stream(self.stream)
assert ret == 0

# 10. Copy output data to the host.
np_output = np.zeros(out_buffer_size, dtype=np.byte)
bytes_data = np_output.tobytes()
np_output_ptr = acl.util.bytes_to_ptr(bytes_data)
ret = acl.rt.memcpy(np_output_ptr, out_buffer_size, self.dev_buffer["output_0"],
                      out_buffer_size, ACL_MEMCPY_DEVICE_TO_HOST)
assert ret == 0

# 11. Destroy the allocations, including the input and output image descriptions, input and output buffers, channel description, and the channel.
ret = acl.media.dvpp_destroy_pic_desc(self.input_desc)
ret = acl.media.dvpp_destroy_pic_desc(self.output_desc)
# dev_buffer is a dictionary object, which is used to store the buffer allocated on the device.
for key in self.dev_buffer.keys():
    if self.dev_buffer[key]:
        ret = acl.media.dvpp_free(self.dev_buffer[key])
if self.dvpp_channel_desc:
    ret = acl.media.dvpp_destroy_channel(self.dvpp_channel_desc)
    assert ret == 0
    ret = acl.media.dvpp_destroy_channel_desc(self.dvpp_channel_desc)
    assert ret == 0

# 12. Deallocate runtime resources.
# 13. Perform deinitialization.
ret = acl.finalize()
# ......
```
<!-- end id6 -->
<!-- npu="910b,910,310p,310b" id8 -->
## Sample Code for Image Cropping and Pasting (Single-Image, Multi-ROI)

- Call the asynchronous API `dvpp_vpc_batch_crop_and_paste_async` to crop a selected ROI and paste the crop ROI on the canvas for output. For asynchronous APIs, call `acl.rt.synchronize_stream` to block the application until all tasks in the specified stream are complete.
- The cropped image will be resized again if the size of the `crop_area` is inconsistent with that of the `paste_area`
- To paste the `paste_area` on a canvas loaded to the output buffer, modify the code logic as follows: allocate the output buffer and then load a canvas to the allocated buffer.

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......

# 1. Perform initialization.
ret = acl.init()

# 2. Allocate runtime resources.
# 3. Create the description of output batch size and input batch size.
self.out_batch_pic_desc = acl.media.dvpp_create_batch_pic_desc(self.out_batch_size)
self.in_batch_pic_desc = acl.media.dvpp_create_batch_pic_desc(self.in_batch_size)
# 3.1 Set the crop ROIs and paste ROIs.
# 3.2 If the cropped and pasted output image is used as the input for model inference, the width and height of the output image must meet the requirements of the model.
for i in range(self.in_batch_size):
    input_desc = acl.media.dvpp_get_pic_desc(self.in_batch_pic_desc, i)
    assert input_desc is not None
    # Allocate a buffer and set the description of output image.
    self.set_picture_desc(input_desc, w, h, "input", i)
    # copy from host to device.
    key = "input" + '_' + str(i)
    ret = acl.rt.memcpy(self.dev_buffer[key], in_buffer_size, np_yuv_ptr,
                         in_buffer_size, 1)
    assert ret == 0
    # Create a roiNums. Each image corresponds to the number of images to be cropped and pasted.
    roiList.append(self.out_batch_size // self.in_batch_size)
for i in range(self.out_batch_size):
    output_desc = acl.media.dvpp_get_pic_desc(self.out_batch_pic_desc, i)
    assert output_desc is not None
    # User-defined method: Allocate a buffer and set the description of output image.
    self.set_picture_desc(output_desc, w, h, "output", i)
    if i == 0:
        crop_area = acl.media.dvpp_create_roi_config(w // 2, w - 1, h // 2, h - 1)
    else:
        crop_area = acl.media.dvpp_create_roi_config(0, w - 1, h // 2, h - 1)
    paste_area = acl.media.dvpp_create_roi_config(w // 2, w - 1, h // 2, h - 1)
    self.cropList.append(crop_area)
    self.pasteList.append(paste_area)
# 3.3. roiList: number of images to be cropped and pasted. If the number of output images is greater than that of input images, the extra images are added to the output of the last input image.
total_num = 0
for i in range(self.in_batch_size):
    total_num += roiList[i]
if self.out_batch_size % self.in_batch_size != 0:
    roiList[-1] = self.out_batch_size - total_num + roiList[-1]

# 4. Create the description of the data processing channel. dvppChannelDesc_ is of type acldvppChannelDesc.
self.dvpp_channel_desc = acl.media.dvpp_create_channel_desc()

# 5. Create a data processing channel.
ret = acl.media.dvpp_create_channel(self.dvpp_channel_desc)

# 6. Perform asynchronous resizing and call acl.rt.synchronize_stream to block the app until all tasks in the specified stream are complete.
_, ret = acl.media.dvpp_vpc_batch_crop_and_paste_async(self.dvpp_channel_desc, self.in_batch_pic_desc,
                                                             roiList, self.out_batch_pic_desc, self.cropList,
                                                             self.pasteList, self.stream)
ret = acl.rt.synchronize_stream(self.stream)

# 7. Destroy the allocations, including the input and output image descriptions, input and output buffers, channel description, and the channel.
# 7.1 Destroy image description and description of a batch of images.
self._free_pic_desc()
for i in range(len(self.cropList)):
    ret = acl.media.dvpp_destroy_roi_config(self.cropList[i])
    assert ret == 0
for i in range(len(self.pasteList)):
    ret = acl.media.dvpp_destroy_roi_config(self.pasteList[i])
    assert ret == 0
for key in self.dev_buffer.keys():
    if self.dev_buffer[key]:
        ret = acl.media.dvpp_free(self.dev_buffer[key])
# 7.2 Destroy the channel and channel description.
if self.dvpp_channel_desc:
    ret = acl.media.dvpp_destroy_channel(self.dvpp_channel_desc)
    assert ret == 0
    ret = acl.media.dvpp_destroy_channel_desc(self.dvpp_channel_desc)
    assert ret == 0

# 8. Deallocate runtime resources.
# 9. Perform deinitialization.
ret = acl.finalize()
```
<!-- end id8 -->
