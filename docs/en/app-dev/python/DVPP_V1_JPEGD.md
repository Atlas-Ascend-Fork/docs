# JPEGD

The JPEG decoder (JPEGD) can decode .jpg, .jpeg, .JPG, and .JPEG images into YUV images. For details about the JPEGD functions and restrictions, see [DVPP Media Acceleration Library](https://hiascend.com/en/document/redirect/CannCommunityDvppApi).

This section describes the API call sequence of JPEGD, and sample code is also provided to help you better understand the sequence.

## API Call Sequence

If JPEG image decoding is involved during app development, ensure that your app contains the code logic for such image decoding. **For details about the API call sequence, see [API Calling Process](interface_calling_process.md)**.

**Figure 1** JPEG image decoding
![](figures/jpeg-image-decoding.png)

The current system supports .jpg, .jpeg, .JPG, and .JPEG image decoding. Different source image encoding formats lead to different output formats. The key APIs are described as follows:

1. Call `acl.media.dvpp_create_channel_desc` to **create a channel description**.
2. Call `acl.media.dvpp_create_channel` to **create a channel for image data processing**.
3. Before decoding JPEG images, call `acl.media.dvpp_malloc` to **allocate device buffers** for storing the input or output data.

    **Before allocating an output buffer**, call `acl.media.dvpp_jpeg_predict_dec_size` to **predict the required output allocation size based on the JPEG image size**.

4. Call the asynchronous API `acl.media.dvpp_jpeg_decode_async` for decoding.

    For asynchronous APIs, call `acl.rt.synchronize_stream` to block the application until all tasks in the specified stream are complete.

5. After the decoding is complete, call `acl.media.dvpp_free` to **free the input and output buffers**.
6. Call `acl.media.dvpp_destroy_channel` to **destroy the image data processing channel**.

    Call `acl.media.dvpp_destroy_channel_desc` to destroy the channel description after the channel is destroyed.

## Sample Code

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
# Load the YUV image data.
# Allocate the device buffer inputDevBuff.
# Copy image data from the host to the device by calling acl.rt.memcpy. After data copy is complete, free the host memory in a timely manner.
np_jpg = np.fromfile(self.path, dtype=np.byte)
self.in_buffer_size = np_jpg.itemsize * np_jpg.size
bytes_data = np_jpg.tobytes()
np_jpg_ptr = acl.util.bytes_to_ptr(bytes_data)
self.in_buffer_dev, ret = acl.media.dvpp_malloc(self.in_buffer_size)
ret = acl.rt.memcpy(self.in_buffer_dev, self.in_buffer_size, np_jpg_ptr,
                     self.in_buffer_size, 1)

# 6. Calculate and allocate output device buffer self.out_buffer_dev aligned to 16 bytes to store the encoded output data.
height_stride = ((h + 1) // 2) * 2
width_stride = ((w + 15) // 16) * 16
# malloc for output
self.out_buffer_size = (width_stride * height_stride * 3) // 2
self.out_buffer_dev, ret = acl.media.dvpp_malloc(self.out_buffer_size)

# 7. Create the description of the decoded image and set the attribute values.
# Set the output buffer and size to the picture description for data placeholder.
self.pic_desc = acl.media.dvpp_create_pic_desc()
ret = acl.media.dvpp_set_pic_desc_data(self.pic_desc, self.out_buffer_dev)
ret = acl.media.dvpp_set_pic_desc_size(self.pic_desc, self.out_buffer_size)
ret = acl.media.dvpp_set_pic_desc_format(
            self.pic_desc, PIXEL_FORMAT_YUV_SEMIPLANAR_420)
ret = acl.media.dvpp_set_pic_desc_width(self.pic_desc, w)
ret = acl.media.dvpp_set_pic_desc_height(self.pic_desc, h)
ret = acl.media.dvpp_set_pic_desc_width_stride(self.pic_desc, width_stride)
ret = acl.media.dvpp_set_pic_desc_height_stride(self.pic_desc, height_stride)

# 8. Perform asynchronous decoding and call acl.rt.synchronize_stream to block the host until all tasks in the specified stream are complete.
ret = acl.media.dvpp_jpeg_decode_async(self.dvpp_channel_desc,
                                           self.in_buffer_dev,
                                           self.in_buffer_size,
                                           self.pic_desc, self.stream)
ret = acl.rt.synchronize_stream(self.stream)

# 9. After the decoding is complete, destroy the allocations, including the description of the output image, output buffer, description of the channel as well as the channel.
ret = acl.media.dvpp_destroy_pic_desc(self.pic_desc)
ret = acl.media.dvpp_free(self.in_buffer_dev)
ret = acl.media.dvpp_free(self.out_buffer_dev)
ret = acl.media.dvpp_destroy_channel(self.dvpp_channel_desc)
ret = acl.media.dvpp_destroy_channel_desc(self.dvpp_channel_desc)

# 10. Deallocate runtime resources.
# Perform deinitialization.
ret = acl.finalize()

# ......
```
