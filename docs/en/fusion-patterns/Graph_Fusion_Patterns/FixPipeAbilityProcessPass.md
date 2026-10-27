# FixPipeAbilityProcessPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:46:11.365Z pushedAt=2026-10-15T12:44:18.325Z -->

## Description

Adds the `support_fixpipe_ability` attribute to a Fixpipe node. This attribute has the following enumerated values:

- `1`: The Conv2D and DepthwiseConv2D operators support Fixpipe dual outputs when the number of outputs is 2.
- `2`: Conv2DBackpropFilterD and DepthwiseConv2DBackpropFilterD use atomic write.
- `3`: Fixpipe processing is not supported.

## Constraints

This fusion pattern cannot be disabled.

The validity of this pass depends on whether the running product supports the corresponding operator type. For details, see [Ascend IR Operator Specifications](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/aolapi/operatorlist_00094.html) in the operator library.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->

<!-- npu="950" id2 -->
Ascend 950PR&950DT products
<!-- end id2 -->
