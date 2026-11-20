# Model Unloading

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:21:21.573Z pushedAt=2026-10-22T06:00:04.714Z nl=2 -->

After model execution is complete, unload the model in a timely manner to release model resources.

After model inference is complete, call the **aclmdlUnload** API to unload the model, destroy the model description of the **aclmdlDesc** type, and free the working memory and weight memory used for model running.

The following sample code shows the key steps. It cannot be directly copied, compiled, and run, and are for reference only. After calling an API, add branches for exception handling and record error logs and prompt logs. These are not listed one by one here.

```cpp
// 1. Unload the model.
aclError ret = aclmdlUnload(modelId_);

// 2. Free the model description.
if (modelDesc_ != nullptr) {
    (void)aclmdlDestroyDesc(modelDesc_);
    modelDesc_ = nullptr;
}

// 3. Free the working memory used for model running.
if (modelWorkPtr_ != nullptr) {
    (void)aclrtFree(modelWorkPtr_);
    modelWorkPtr_ = nullptr;
    modelWorkSize_ = 0;
}

// 4. Free the weight memory used for model running.
if (modelWeightPtr_ != nullptr) {
    (void)aclrtFree(modelWeightPtr_);
    modelWeightPtr_ = nullptr;
    modelWeightSize_ = 0;
}
```
