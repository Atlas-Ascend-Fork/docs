# PNGD

This section describes the API call sequence of PNGD, and sample code is also provided to help you better understand the process.

The PNG decoder (PNGD) decodes images in PNG format. For details about the PNGD functions and restrictions, see [DVPP Media Acceleration Library](https://hiascend.com/en/document/redirect/CannCommunityDvppApi).

## API Call Sequence

If PNG image decoding is involved during app development, ensure that your app contains the code logic for such image decoding. **For details about the API call sequence, see [API Calling Process](interface_calling_process.md)**.

**Figure 1** PNG image decoding
![](figures/png-image-decoding.png)

The current system supports PNG image decoding and output of RGB and RGBA images. The key APIs are described as follows:

1. Call `acl.media.dvpp_create_channel_desc` to **create a channel description**.
2. Call `acl.media.dvpp_create_channel` to **create a channel for image data processing**.
3. Before decoding PNG images, call `acl.media.dvpp_malloc` to **allocate device buffers** for storing the input or output data.

    Before allocating an output buffer, call `acl.media.dvpp_png_predict_dec_size` to **predict** the output allocation size required for the decoded image based on the size of the PNG image.

4. Call the asynchronous API `acl.media.dvpp_png_decode_async` for **decoding**.

    For asynchronous APIs, call `acl.rt.synchronize_stream` to block the application until all tasks in the specified stream are complete.

5. After the decoding is complete, call `acl.media.dvpp_free` to **free the input and output buffers**.
6. Call `acl.media.dvpp_destroy_channel` to **destroy the image data processing channel**.

    Call `acl.media.dvpp_destroy_channel_desc` to **destroy the channel description after the channel is destroyed**.

## Sample Code

After the API calls, add an exception handling branch and specify log printing of different levels (such as **ERROR_LOG** and **INFO_LOG**). The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......

# 1. Perform initialization.
ACL_CONFIG_PATH = "../src/acl.json"
ret = acl.init(ACL_CONFIG_PATH)

# 2. Allocate runtime resources.
# 3. Create the description of the data processing channel. dvpp_channel_desc is of type acldvppChannelDesc.
dvpp_channel_desc = acl.media.dvpp_create_channel_desc()

# 4. Create a data processing channel.
ret = acl.media.dvpp_create_channel(dvpp_channel_desc)

# 5. Allocate input buffer.
pic_name = "../data/test_png_dec.png"
np_png = np.fromfile(pic_name, dtype=np.byte)
in_buffer_size = np_png.itemsize * np_png.size
bytes_data = np_png.tobytes()
np_png_ptr = acl.util.bytes_to_ptr(bytes_data)
in_dev_buffer, ret = acl.media.dvpp_malloc(in_buffer_size)
ACL_MEMCPY_HOST_TO_DEVICE = 1
ret = acl.rt.memcpy(in_dev_buffer, in_buffer_size, np_png_ptr, in_buffer_size,
    ACL_MEMCPY_HOST_TO_DEVICE)

# 6. Allocate a decoding output buffer.
PIXEL_FORMAT_RGB_888 = 12
out_buffer_size, ret = acl.media.dvpp_png_predict_dec_size(np_png_ptr, in_buffer_size,
    PIXEL_FORMAT_RGB_888)
out_dev_buffer, ret = acl.media.dvpp_malloc(out_buffer_size)

# 7. Create the description of the decoded image and set the attribute values.
output_desc = acl.media.dvpp_create_pic_desc()
width, height, components, ret = acl.media.dvpp_png_get_image_info(np_png_ptr, in_buffer_size)
ret = acl.media.dvpp_set_pic_desc_data(output_desc, out_dev_buffer)
ret = acl.media.dvpp_set_pic_desc_size(output_desc, out_buffer_size)
ret = acl.media.dvpp_set_pic_desc_format(output_desc, PIXEL_FORMAT_RGB_888)

# 8. Perform asynchronous decoding and call acl.rt.synchronize_stream to wait for the stream tasks to complete.
ret = acl.media.dvpp_png_decode_async(dvpp_channel_desc, in_dev_buffer, in_buffer_size,
    output_desc, stream)
ret = acl.rt.synchronize_stream(stream)

# 9. After the decoding is complete, destroy the allocations, including the description of the output image, output buffer, description of the channel as well as the channel.
ret = acl.media.dvpp_destroy_pic_desc(output_desc)
ret = acl.media.dvpp_free(in_dev_buffer)
ret = acl.media.dvpp_free(out_dev_buffer)
ret = acl.media.dvpp_destroy_channel(dvpp_channel_desc)
ret = acl.media.dvpp_destroy_channel_desc(dvpp_channel_desc)

# 10. Destroy runtime allocations.
# Perform deinitialization.
ret = acl.finalize()
# ....
```
