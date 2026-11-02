# Concepts and Restrictions

## What Is AIPP?

The Artificial Intelligence Pre-Processing (AIPP) module is introduced for image preprocessing including Color Space Conversion (CSC), image normalization (by subtracting the mean value or multiplying a factor), image cropping (by specifying the crop start and cropping the image to the size required by the NN), and much more.

Static AIPP and dynamic AIPP modes are supported. However, the two modes are mutually exclusive.

- Static AIPP: During model conversion, set the AIPP mode to static and set the AIPP parameters. After the model is generated, the AIPP parameter values are saved in the offline model (.om files). The same AIPP parameter configurations are used in each model inference phase.

    In static AIPP mode, batches share the same set of AIPP parameters.

- Dynamic AIPP: If you use this mode when converting a model, you can set dynamic AIPP parameters each time before running the model for inference.

    In dynamic AIPP mode, batches can use different sets of AIPP parameters.

## Usage Restrictions

- If the dynamic AIPP and dynamic batch size are both enabled:
  - The `batchSize` parameter passed to the `acl.mdl.create_aipp` call must be set to the allowed maximum value.
  - For data nodes that require dynamic AIPP, the corresponding input buffer must be allocated based on the allowed maximum batch size.

- If the dynamic AIPP and dynamic image size are both enabled:
  - If the image cropping, resizing, or padding function is `enabled` in setting the dynamic AIPP parameters, the dynamic image size becomes unavailable.
  - If the image cropping, resizing, or padding function is `not enabled` in setting the dynamic AIPP parameters, the dynamic AIPP and dynamic image size are both available. However, ensure that the width and height configured by calling `acl.mdl.set_aipp_src_image_size` are consistent with those configured by calling `acl.mdl.set_dynamic_hw_size`.
  - For data nodes that require dynamic AIPP processing, allocating the input buffer must be based on the maximum allowed image size.

- When dynamic AIPP and dynamic shape input (setting the shape range) are used at the same time, the width and height of the output image of dynamic AIPP must be within the configured shape range.
- For a single model, AIPP (static or dynamic) and dynamic dimensions (ND format) are mutually exclusive.
- pyACL also supports Digital Vision Pre-Processing (DVPP), which introduces hardware-based media data processing techniques, including resizing, cropping, format conversion, image encoding and decoding, and video encoding and decoding. Compared with AIPP, DVPP offers a wider set of processing operations, but it has particular restrictions on the image input/output and memory allocation.

    For details about the DVPP APIs, see [Media Data Processing (DVPP)](DVPP.md).
