# FixPipeAbilityProcessPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:45:59.479Z pushedAt=2026-11-16T06:27:04.309Z nl=2 -->

## Description

Adds the `support_fixpipe_ability` attribute to a Fixpipe node. This attribute has the following enumerated values:

- `1`: The Conv2D and DepthwiseConv2D operators support Fixpipe dual outputs when the number of outputs is 2.
- `2`: Conv2DBackpropFilterD and DepthwiseConv2DBackpropFilterD use atomic write.
- `3`: Fixpipe processing is not supported.

## Constraints

This fusion pattern cannot be disabled.

The validity of this pass depends on whether the running product supports the corresponding operator types. For details, see [Ascend IR Operator Specifications](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/aolapi/docs/en/ops-lib/ascendIR_spec_intro.md) in the operator library.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->

<!-- npu="950" id2 -->
Ascend 950PR&950DT products
<!-- end id2 -->
