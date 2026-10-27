# GroupedMatmulTransFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:48:17.772Z pushedAt=2026-10-15T12:44:18.361Z -->

## Description

Pattern 1: Deletes Transpose or TransposeD from the graph and encodes the x/weight transformation information to operator attributes. See the following figure.

![](../figures/GroupedMatmulTransFusionPass_1.png)

![](../figures/GroupedMatmulTransFusionPass_2.png)

<!-- npu="950,A3,910b" id2 -->
Pattern 2: Deletes Reshape, Transpose/TransposeD, and Reshape connected to the x/weight from the graph and encodes the weight transformation information to operator attributes. See the following figure.

This fusion pattern supports the following products:

<!-- npu="910b" id3 -->
Atlas A2 products
<!-- end id3 -->

<!-- npu="A3" id4 -->
Atlas A3 products
<!-- end id4 -->

<!-- npu="950" id5 -->
Ascend 950PR&950DT products
<!-- end id5 -->

![](../figures/GroupedMatmulTransFusionPass_3.png)

![](../figures/GroupedMatmulTransFusionPass_4.png)

<!-- end id2 -->
<!-- npu="950" id1 -->
Pattern 3: In pseudo-quantization use cases for Ascend 950PR&950DT products, removes Reshape+Transpose/TransposeD+Reshape before weight/antiquantScale from the graph and attaches the weight transpose information to operator attributes, as shown below.

![](../figures/GroupedMatmulTransFusionPass_5.png)

Pattern 4: In MX/GB quantization use cases of Ascend 950PR&950DT products, removes Transpose or TransposeD from the graph, and attaches the transpose information of x and weight to the operator attributes, as shown below.

![](../figures/GroupedMatmulTransFusionPass_6.png)

>[!NOTE]
>In MX/GB quantization use cases of Ascend 950PR&950DT products, scale follows the transpose information of weight, and pertokenScale follows the transpose information of x.
<!-- end id1 -->

## Constraints

- Only the use case when x, weight, and y are single tensors is supported (a single tensor indicates that there is only one tensor in the tensorList input).
- Transpose/TransposeD supports transpose on the second and third axes.
