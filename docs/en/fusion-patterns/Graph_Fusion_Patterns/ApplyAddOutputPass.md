# ApplyAddOutputPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:42:10.087Z pushedAt=2026-11-16T06:27:04.205Z nl=2 -->

## Description

Adds optional outputs and prechecks for operators in Table 1.

**Table 1** Supported operators

|Operator|Output 1|Output 2|Output 3|Precheck|
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

None.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
