# FIXPIPEFUSIONPASS

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:45:54.886Z pushedAt=2026-11-16T06:27:04.304Z nl=2 -->

## Description

On hardware with FixPipe support, when a cube operator has `support_fixpipe_ability` configured in [FixPipeAbilityProcessPass](FixPipeAbilityProcessPass.md), it will sequentially attempt to match the convert, activation, and transform units as shown in the figure below. If at least one of these units exists (nonexistent units are skipped), the matched operators will be fused into a FixPipe operator.

- convert unit: format conversion unit, which is typically a quant or cast operator.
- activation unit: activation unit, which is typically a ReLU operator.
- transform unit: format conversion unit for converting ND to NZ, which is typically a TransData operator.

![](../figures/FIXPIPEFUSIONPASS_1.png)

## Constraints

- Only static networks are supported.
- This fusion pattern cannot be disabled.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
