# ApplyAddOutputPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:39:17.377Z pushedAt=2026-10-15T12:44:18.223Z -->

## Description

Adds optional outputs and prechecks for operators in Table 1.

**Table 1** Supported operators

|Operator|Output1|Output2|Output3|Precheck|
|--|--|--|--|--|
|ApplyRMSProp|ms|mom|-|ApplyRmsPropPreCheck|
|FusedMulApplyMomentumWithoutAccumOut|accum|-|-|FusedMulApplyMomentumPreCheck|
|FusedMulApplyMomentumExtern|accum|-|-|FusedMulApplyMomentumExternPreCheck|
|FusedMulApplyKerasMomentum|accum|-|-|FusedMulApplyKerasMomentumPreCheck|
|ApplyAdagrad|accum|-|-|-|
|ApplyAdagradDA|gradient_accumulator|gradient_squared_accumulator|-|-|
|ApplyAdadelta|accum|accum_update|-|-|
|ApplyPowerSign|m|-|-|-|
|ApplyProximalAdagrad|accum|-|-|-|
|ApplyAdaMax|m|v|-|-|
|ApplyAdagradV2|accum|-|-|ApplyAdagradV2PreCheck|
|ApplyKerasMomentum|accum|-|-|ApplyKerasMomentumPreCheck|
|ApplyFtrlV2|accum|linear|-|-|
|ApplyMomentum|accum|-|-|-|
|ApplyFtrl|accum|linear|-|-|
|ApplyAdam|m|v|-|-|
|ApplyCenteredRMSProp|mg|ms|mom|-|
|ApplyAddSign|m|-|-|-|
|ApplyAdamWithAmsgrad|m|v|vhat|-|

## Constraints

None

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
