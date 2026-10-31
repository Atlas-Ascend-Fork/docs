# Case Introduction

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:40:27.990Z pushedAt=2026-10-26T03:10:39.440Z nl=2 -->

## Case Description

For the FastRCNN network, during model conversion, when the default high-performance mode and **force\_fp16** precision mode are retained, the inference precision is incorrect, and the MAP result is 0.

Then, during model conversion, when the high-precision mode (**precision\_mode=allow\_fp32\_to\_fp16**) is set for the model, the inference precision is correct.

## Case Analysis

1. During model conversion, keep the default high-performance mode and force\_fp16 precision mode, perform inference, and obtain the dump data file in this mode.
2. Perform model conversion again, set the high-precision mode of the model (**precision\_mode=allow\_fp32\_to\_fp16**), perform inference again, and obtain the dump data file in this mode.
3. Use the accuracy comparison tool to compare the dump data obtained in step 1 and step 2.

    The following is an example of the comparison result:

    ![](figures/image_0000001265081974.png)

4. From the figure, look at the **CosineSimilarity** column. The result is obtained by the cosine similarity algorithm, and its range is \[-1,1\]. The closer the comparison result is to 1, the more similar the two values are; the closer it is to -1, the more opposite the two values are. For most operators, a value lower than 0.95 indicates a precision problem.

    In the preceding figure, the cosine similarity of the 0th output of the AddN operator is only 0.72, indicating that this operator may have a precision problem. Therefore, further analyze the dump data file of the 0th output of this operator in high-precision mode (the dump data file obtained in step 2).

5. Because the dump data file cannot be directly viewed with a text tool, before analyzing the dump data file, refer to the "Extended Functions \> Viewing Dump Files" section in [Precision Debugging Tool](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/devaids/ModelAccuracyAnalyzer/atlasaccuracy_16_0001.html) to first convert the dump data file to numpy format, and then convert the numpy format file to a TXT format file.

    When converting the numpy format file to a TXT format file, you can obtain the maximum and minimum values of the 0th output of the AddN operator. The following is an example command (**\*\*\*\*_.npy_** indicates the path of the numpy format file):

    ```python
    $ python3
    Python 3 (default, Mar  5 2020, 16:07:54)[GCC 5.4.0 20160609] on linuxType ....
    >>> import numpy as np
    >>> a = np.load("****.npy")
    >>> a.max()
    >>> 109508.0
    >>> a.min()
    >>> 70683.0
    ```

6. Based on the maximum and minimum values of the 0th output of the AddN operator obtained in step 5, it can be seen that in high-precision mode, the maximum value of the output tensor of the AddN operator is 109508.0, while in high-performance mode (fp16), the maximum value of the output tensor is 65504.0. The maximum value range that FP16 can express is (-65505, 65504). Therefore, it can be concluded that in high-precision mode, the output value of the AddN operator exceeds the value range that the fp16 type can express. As a result, this operator needs to be configured to run in high-precision mode. For details, see [Configuring Some Operators to Retain the Data Type in the Original Network](config_precision_mode.md).
