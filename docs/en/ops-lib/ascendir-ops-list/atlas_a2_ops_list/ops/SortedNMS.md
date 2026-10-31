# SortedNMS

```c
REG_OP(SortedNMS)
    .INPUT(boxes, TensorType({DT_FLOAT16, DT_FLOAT}))
    .INPUT(sorted_scores, TensorType({DT_FLOAT16, DT_FLOAT}))
    .INPUT(input_indices, TensorType({DT_INT32}))
    .INPUT(max_output_size, TensorType({DT_INT32}))
    .INPUT(iou_threshold, TensorType({DT_FLOAT16, DT_FLOAT}))
    .INPUT(score_threshold, TensorType({DT_FLOAT16, DT_FLOAT}))
    .OUTPUT(selected_indices, TensorType({DT_INT32}))
    .ATTR(offset, Int, 0)
    .OP_END_FACTORY_REG(SortedNMS)
```

## Brief

Greedily selects non-suppressed boxes in the supplied descending score order.

## Inputs

- boxes: A 2-D tensor of shape [num_boxes, 4].
- sorted_scores: A 1-D tensor of shape [num_boxes], sorted in descending order.
- input_indices: A 1-D int32 tensor of shape [num_boxes], with values in [0, num_boxes).
- max_output_size: A scalar int32 tensor giving the maximum number of selected boxes.
- iou_threshold: A scalar float tensor in [0, 1].
- score_threshold: A scalar float tensor.
boxes and iou_threshold must have the same type (float16 or float32). sorted_scores and
score_threshold must have the same type (float16 or float32), independently of boxes.

## Outputs

selected_indices: A 1-D int32 tensor of shape [M], where M is computed at runtime and
M <= min(max_output_size, num_boxes).

## Data Types

Note: The preceding prototypes are applicable to all chips, but the Data Types listed below are applicable only to the current chip.
### AI Core
- input0 boxes: float16,float32
- input1 sorted_scores: float16,float32
- input2 input_indices: int32
- input3 max_output_size: int32
- input4 iou_threshold: float16,float32
- input5 score_threshold: float16,float32
- output0 selected_indices: int32


---

[Back to Operator Specifications (Atlas A2 products)](../README.md)
