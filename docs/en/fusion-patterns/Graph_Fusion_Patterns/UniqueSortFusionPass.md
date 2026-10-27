# UniqueSortFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:56:54.936Z pushedAt=2026-10-15T12:44:18.504Z -->

## Description

Splits the Unique or UniqueWithCount operator into a combination of Sort+AdjacentDifference+Cumsum+Scatter+UniqueConsecutive operators to complete the computation.

The Unique or UniqueWithCount operator before splitting is an AI CPU operator, and the five operators (Sort, AdjacentDifference, Cumsum, Scatter, and UniqueConsecutive) after splitting are all AI Core operators.

Scenario 1:

![](../figures/UniqueSortFusionPass_1.png)

Scenario 2:

![](../figures/UniqueSortFusionPass_2.png)

## Constraints

- The output data types of idx and count are int32 and int64.
- The data types of the input x can be int64, int32, int16, int8, uint64, uint32, uint16, uint8, bfloat16, float16, and float32.
<!-- npu="950" id2 -->
- For Ascend 950PR/Ascend 950DT products, this fusion pattern cannot be disabled.
<!-- end id2 -->

## Applicable Products

<!-- npu="950" id1 -->
Ascend 950PR&950DT products
<!-- end id1 -->
