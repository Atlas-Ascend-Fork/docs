# Sample Code
<!-- npu="910,310p,310b" id1 -->
[Click here](https://gitee.com/ascend/samples/tree/master/python/level2_simple_inference/1_classification/resnet50_async_imagenet_classification) to view the complete code.
<!-- end id1 -->
<!-- npu="910,310p,310b" id2 -->
In the acl_resnet50_async sample:
<!-- end id2 -->
- When running the executable file without parameters:
  - By default, model asynchronous inference is performed for 10 times.
  - The device ID defaults to `0`.
  - The callback interval defaults to `1`, indicating that a callback task is issued every asynchronous inference.
  - By default, there are 10 memory blocks in a memory pool.

- Run the executable file with parameters:
  - The first parameter indicates the device ID.
  - The second parameter indicates the number of model asynchronous inference times.
  - The third parameter indicates the interval for delivering the callback task. `0` indicates the callback task is not delivered. A non-zero value (for example, *m*) indicates that the callback task is delivered after *m* times of asynchronous inference.
  - The fourth parameter indicates the number of memory blocks in the memory pool. The argument must be greater than or equal to the number of model asynchronous inference times. The number of memory blocks can be modified based on the number of input images.
    - Example 1: If the number of input images is 2, and the number of memory blocks is 2, each image is allocated with one memory block.
    - Example 2: If the number of input images is 3, and the number of memory blocks is 10, 10 loops are executed. Each image is allocated with 3 memory blocks (10/3 = 3, remainder 1), and the remained memory block is allocated to an image.
    - The memory blocks store the input and output data for model inference. If multiple memory blocks correspond to the same image, the input and output data are the same in those memory blocks. This setting is applicable to scenarios where a large amount of image data needs to be simulated with a small amount of input.

  - The fifth parameter indicates the path of the model to be loaded and executed.
  - The sixth parameter indicates the path of the input image. The following image formats are supported:

        ```text
        IMG_EXT = ['.jpg', '.JPG', '.png', '.PNG', '.bmp', '.BMP', '.jpeg', '.JPEG']
        ```

```python
import acl
import argparse
# ......

images_list = [os.path.join(args.images_path, img) for img in os.listdir(args.images_path) \
               if os.path.splitext(img)[1] in IMG_EXT]
data_list = []
for image in images_list:
    # Customize the transfer_pic function to implement the following functions:
    # Load the image to the memory and resize it to 224 x 224.
    transfer_pic(image)
    dst_im = np.fromfile(image.replace(".jpg", ".bin"), dtype=np.byte)
    data_list.append(dst_im)

# 1. Initialize resources: In the example, the Net class is used to initialize resources.
# 1.1 Perform initialization.
ret = acl.init()
# 1.2 Allocate runtime resources.
ret = acl.rt.set_device(self.device_id)
self.context, ret = acl.rt.create_context(self.device_id)
self.stream, ret = acl.rt.create_stream()
# Obtain the run mode of the Ascend AI software stack. The API calls for memory allocation and memory copy are different in different run modes.
self.run_mode, ret = acl.rt.get_run_mode()
# 1.3 Allocate model inference resources.
# 1.4 Load a model.
# Load an offline model file. If the model is successfully loaded, a model ID is returned.
self.model_id, ret = acl.mdl.load_from_file(self.model_path)
# 1.5 Obtain the model description based on the model ID.
self.model_desc = acl.mdl.create_desc()
ret = acl.mdl.get_desc(self.model_desc, self.model_id)

# 2 Perform model inference.
# 2.1 Allocate memory based on the number of memory blocks in the memory pool and copy the image data to the device.
def _data_interaction(self, images_dataset_list):
    for idx in range(self.memory_pool):
        img_idx = idx % len(images_dataset_list)
        img_input = self._load_input_data(images_dataset_list[img_idx])
        infer_output = self._load_output_data()
        self.dataset_list.append([img_input, infer_output])
# 2.2 Create a thread tid and specify the tid thread for processing the callback function in the stream.
# ProcessCallback is a thread function. Call acl.rt.process_report in the thread function, and the callback function is triggered after a specified period of time.
tid, ret = acl.util.start_thread(self._process_callback, [self.context, 50])
# 2.3 Specify a thread for processing the callback function in a stream.
ret = acl.rt.subscribe_report(tid, self.stream)
# 2.4 Create a callback function for processing the model inference result. The callback function is user-defined.
def callback_func(self, delete_list):
    for temp in delete_list:
        _, infer_output = temp
        # device to host
        num = acl.mdl.get_dataset_num_buffers(infer_output)
        for i in range(num):
            temp_output_buf = acl.mdl.get_dataset_buffer(infer_output, i)
            infer_output_ptr = acl.get_data_buffer_addr(temp_output_buf)
            infer_output_size = acl.get_data_buffer_size(temp_output_buf)
            output_host, ret = acl.rt.malloc_host(infer_output_size)
            ret = acl.rt.memcpy(output_host,
                                 infer_output_size,
                                 infer_output_ptr,
                                 infer_output_size,
                                 ACL_MEMCPY_DEVICE_TO_HOST)
            output_host_dict = [{"buffer": output_host, "size": infer_output_size}]
            result = self.get_result(output_host_dict)
            st = struct.unpack("1000f", bytearray(result[0]))
            vals = np.array(st).flatten()
            top_k = vals.argsort()[-1:-6:-1]
            print("\n======== top5 inference results: =============")
            for n in top_k:
                print("[%d]: %f" % (n, vals[n]))
            ret = acl.rt.free_host(output_host)
# 2.5 Customize the forward function to perform model inference.
def forward(self):
    self.execute_dataset = []
    for idx in range(self.execute_times):
        img_data, infer_output = self.dataset_list.pop(0)
        ret = acl.mdl.execute_async(self.model_id,
                                      img_data,
                                      infer_output,
                                      self.stream)
        if self.is_callback:
            self.execute_dataset.append([img_data, infer_output])
            self._get_callback(idx)
# 2.6 For asynchronous inference, app needs to be blocked until all tasks in the specified stream are complete.
ret = acl.rt.synchronize_stream(self.stream)
# 2.7 Unsubscribe from a thread. The callback function in the stream is no longer processed by the specified thread.
ret = acl.rt.unsubscribe_report(tid, self.stream)
self.is_exist = True
ret = acl.util.stop_thread(tid)

# 3. Deallocate runtime resources.
ret = acl.rt.destroy_stream(self.stream)
ret = acl.rt.destroy_context(self.context)
ret = acl.rt.reset_device(self.model_id)

# 4. Perform deinitialization.
ret = acl.finalize()
# ......
```
