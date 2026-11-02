# JPEGE Image Encoding

The JPEG encoder (JPEGE) encodes YUV images into JPG images. For details about the JPEGE functions and restrictions, see [DVPP Media Acceleration Library](https://hiascend.com/en/document/redirect/CannCommunityDvppApi).

This section describes the API call sequence of JPEGE, and sample code is also provided to help you better understand the sequence.

## API Call Sequence

If a YUV image needs to be encoded into a JPEG image during app development, ensure that your app contains the code logic for such image encoding. For details about the API call sequence, see [API Calling Process](interface_calling_process.md).

**Figure 1** JPEG image encoding
![](figures/jpeg-image-encoding.png)

The current system supports YUV to JPG image encoding. The key APIs are described as follows:

1. Call `acl.media.dvpp_create_channel_desc` to **create a channel description**.
2. Call `acl.media.dvpp_create_channel` to **create a channel for image data processing**.
3. Call `acl.media.dvpp_create_jpege_config` to **create image encoding configuration data**.
4. Before encoding JPEG images, call `acl.media.dvpp_malloc` to **allocate device buffers for storing the input or output data**.

    **Before allocating an output buffer**, you can call `acl.media.dvpp_jpeg_predict_enc_size` to **predict the output allocation size required for the encoded image** based on the input image description and image encoding configuration data.

5. Call the asynchronous API `acl.media.dvpp_jpeg_encode_async` for encoding.

    For asynchronous APIs, call `acl.rt.synchronize_stream` to block the application until all tasks in the specified stream are complete.

6. Call `acl.media.dvpp_destroy_jpege_config` to **destroy the image encoding configuration data**.
7. After the encoding is complete, call `acl.media.dvpp_free` to **free the input and output buffers** in a timely manner.
8. Call `acl.media.dvpp_destroy_channel` to **destroy the image data processing channel**.

    Call `acl.media.dvpp_destroy_channel_desc` to **destroy the channel description after the channel is destroyed**.

## Sample code

[Click here](https://gitee.com/ascend/samples/tree/master/python/level2_simple_inference/1_classification/vpc_jpeg_resnet50_imagenet_classification) to view the complete code.

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......

# 1. Perform initialization.
ret = acl.init()

# 2. Allocate runtime resources.
# 3. Create a description of the data processing channel. self.dvpp_channel_desc is of type acldvppChannelDesc.
self.dvpp_channel_desc = acl.media.dvpp_create_channel_desc()

# 4. Create a data processing channel.
ret = acl.media.dvpp_create_channel(self.dvpp_channel_desc)

# 5. Allocate buffer.
# 5.1 Input buffer.
#  Load the YUV image data. Copy image data from the host to the device by calling acl.rt.memcpy.
np_jpg = np.fromfile(self.path, dtype=np.byte)
self.in_buffer_size = np_jpg.itemsize * np_jpg.size
bytes_data = np_jpg.tobytes()
np_jpg_ptr = acl.util.bytes_to_ptr(bytes_data)
self.in_buffer_dev, ret = acl.media.dvpp_malloc(self.in_buffer_size)
ret = acl.rt.memcpy(self.in_buffer_dev, self.in_buffer_size, np_jpg_ptr,
                    self.in_buffer_size, 1)

# 5.2 Calculate and allocate the output device buffer self.out_buffer_dev in 16-pixel-aligned mode to store the encoded output data.
height_stride = ((h + 1) // 2) * 2
width_stride = ((w + 15) // 16) * 16
# malloc for output
self.out_buffer_size = (width_stride * height_stride * 3) // 2
self.out_buffer_dev, ret = acl.media.dvpp_malloc(self.out_buffer_size)

# 6. Create the description of the input image and set the attribute values.
# JPEG encoding: Sets the input YUV image data and size to the image description.
self.pic_desc = acl.media.dvpp_create_pic_desc()
ret = acl.media.dvpp_set_pic_desc_data(self.pic_desc, self.in_buffer_dev)
ret = acl.media.dvpp_set_pic_desc_size(self.pic_desc, self.in_buffer_size)
ret = acl.media.dvpp_set_pic_desc_format(self.pic_desc, PIXEL_FORMAT_YUV_SEMIPLANAR_420)
ret = acl.media.dvpp_set_pic_desc_width(self.pic_desc, w)
ret = acl.media.dvpp_set_pic_desc_height(self.pic_desc, h)
ret = acl.media.dvpp_set_pic_desc_width_stride(self.pic_desc, width_stride)
ret = acl.media.dvpp_set_pic_desc_height_stride(self.pic_desc, height_stride)

# 7. Create image encoding configuration data, set the encoding quality, and predict the output image size, and allocate buffer.
# Encoding quality in a range of [0, 100]. The encoding quality of level 0 is similar to that of level 100. For the value range of [1, 100], a smaller value indicates poorer output image quality.
self.jpege_config = acl.media.dvpp_create_jpege_config()
ret = acl.media.dvpp_set_jpege_config_level(self.jpege_config, 100)
self.out_buffer_size, ret = acl.media.dvpp_jpeg_predict_enc_size(
         self.pic_desc, self.jpege_config)
self.out_buffer_dev, ret = acl.media.dvpp_malloc(self.out_buffer_size)

# 8. Perform asynchronous encoding and call acl.rt.synchronize_stream to block the host until all tasks in the specified stream are complete.
acl.rt.set_context(self.context)
np_out_size = np.array([self.out_buffer_size], dtype=np.int32)
bytes_data = np_out_size.tobytes()
np_out_size_ptr = acl.util.bytes_to_ptr(bytes_data)
ret = acl.media.dvpp_jpeg_encode_async(self.dvpp_channel_desc, self.pic_desc,
                                       self.out_buffer_dev, np_out_size_ptr,
                                       self.jpege_config, self.stream)
ret = acl.rt.synchronize_stream(self.stream)

# 9. Allocate host memory hostPtr.
# 9.1 Load the encoded output image to the host, write the host memory data to the file, and free the host memory by calling acl.rt.free_host in a timely manner.
# 9.2 Create a NumPy object and convert it into data on the host to store the output.
np_output = np.zeros(size, dtype=np.byte)
bytes_data = np_output.tobytes()
np_output_ptr = acl.util.bytes_to_ptr(bytes_data)
size = int(np_out_size[0])
ret = acl.rt.memcpy(np_output_ptr, size, self.out_buffer_dev, size, 2)

# 10. Destroy the allocations, including the description of the input and output image, input and output buffer, channel description, channel.
ret = acl.media.dvpp_destroy_jpege_config(self.jpege_config)
ret = acl.media.dvpp_destroy_pic_desc(self.pic_desc)
ret = acl.media.dvpp_free(self.in_buffer_dev)
ret = acl.media.dvpp_free(self.out_buffer_dev)
ret = acl.media.dvpp_destroy_channel(self.dvpp_channel_desc)
ret = acl.media.dvpp_destroy_channel_desc(self.dvpp_channel_desc)

# 11. Destroy runtime allocations.
# Perform deinitialization.
ret = acl.finalize()
# ....
```
