# Model Unloading

For details about the API call sequence for model unloading, see [API Calling Process](interface_calling_process.md).

## Basic Principles

After the model inference is complete, call `acl.mdl.unload` to unload the model and destroy the model description of the aclmdlDesc type.

## Sample Code

```python
# Unload the model.
ret = acl.mdl.unload(self.model_id)

# Destroy the model description.
if self.model_desc:
    ret = acl.mdl.destroy_desc(self.model_desc)
    self.model_desc = None
```
