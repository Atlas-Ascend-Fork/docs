# Introduction

## Application Scenarios

If your AI app involves not only model inference but also mathematical operations, such as Basic Linear Algebra Subprogram (BLAS) and data type conversion, Ascend CANN can also play its role to provide related computing capabilities.

Ascend CANN supports single-operator calling, a lightweight mode allowing you to load and execute single-operators directly using the pyACL APIs, which requires no model building and training.

In addition, you can verify the functions of a custom operator via single-operator calling.

## Difference Between Single-Operator Calling and Model Inference

The following flowchart shows the basic common points and difference between single-operator calling and model inference.

- Common points:
  - Both need initialization/deinitialization and allocating/destroying runtime resources.
  - Both involve loading and execution steps, though they use different API calls.

- Difference:
  - Model inference involves model unloading, but single-operator calling does not.

**Figure 1** Workflow comparison
![](figures/workflow-comparison.png)
