# Configuring skip\_layers to Skip Layers with Large Quantization Loss

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:31:26.261Z pushedAt=2026-10-22T07:28:17.858Z nl=2 -->

Use the accuracy comparison tool to compare the precision of each layer in the original model and the quantized model, identify layers with large precision loss, and configure **skip\_layers** to skip layers with large quantization loss during precision-based automatic quantization.

1. Modify the precision-based automatic quantization code and add the **skip\_layers** configuration to skip layers that do not support quantization.

    The following sample code shows how to skip a layer. If multiple layers need to be skipped, separate them with commas, for example: skip\_layers=\['op1','op2','op3'\]

    ```py
    config_json_file = './config.json'
    skip_layers = ['Default/network-DeepLabV3/resnet-Resnet/layer4-SequentialCell/0-Bottleneck/downsample-SequentialCell/0-Conv2d/Conv2D-op311']
    batch_num = 1
    amct.create_quant_config(config_json_file, model, input_data,
                              skip_layers, batch_num)
    
    scale_offset_record_file = os.path.join(TMP, 'scale_offset_record.txt')
    result_path = os.path.join(RESULT, 'model')
    ```

2. Execute precision-based automatic quantization.
3. Perform inference again.

    If skipping layers that do not support quantization affects the inference result data of the model, you need to adjust the model and then quantize the model again.
