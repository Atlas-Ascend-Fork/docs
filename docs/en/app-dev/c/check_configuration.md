# Checking Data Processing or Configuration

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:27:09.767Z pushedAt=2026-10-26T03:10:39.415Z nl=2 -->

1. Check whether the input data of the OM model and the benchmark network inference as well as the processing of the input data are consistent. If not, adjust them to be consistent.
2. Check the AIPP configuration.

    Artificial Intelligence Pre-Processing (AIPP) is used to complete image preprocessing on the AI Core, including resizing images, color space conversion (converting image formats), and mean subtraction/coefficient multiplication (changing image pixels). After data processing, the actual model inference is performed.

    If the AIPP configuration is incorrect, the input data for model inference may be inaccurate. See the "Advanced Features \> Enabling AIPP" section in [Ascend Tensor Compiler (ATC)](https://gitcode.com/cann/ge/blob/9.2.0/docs/en/user_guides/atc_tools/README.md) to check the AIPP configuration. If any AIPP configuration is incorrect, correct it, reconvert the model, and perform inference again.

3. Check whether the post-processing methods of the OM model and the benchmark network inference results are consistent. If not, adjust them to be consistent.
