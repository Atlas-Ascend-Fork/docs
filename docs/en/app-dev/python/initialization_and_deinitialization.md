# Initialization and Deinitialization

For the API call sequence for initialization and deinitialization, see [API Calling Process](interface_calling_process.md).

## Basic Principles

You must call `acl.init` to perform **initialization**. The configuration file is in JSON format. For details, see `acl.init`.

If the current default configurations meet the requirements and do not need to be modified, you do not need to input parameters to `acl.init`, or you can set the configuration file to an empty JSON string (that is, only \{\} exists in the configuration file). Do not input parameters to `acl.init`. The following is an example:

```bash
ret = acl.init()
```

Deinitialize pyACL by calling `acl.finalize` after all pyACL API calls are complete or before the app exits.

## Sample code

Following the API calls, add exception handling branches and specify log printing of error and information levels. The following is a code snippet of key steps only, which is not ready to use.

```python
import acl
# ......
# Initialize basic configurations.
# The .. path is relative to the directory of the executable file.
acl_config_path = "../src/acl.json"
ret = acl.init(acl_config_path)
# ......

# Perform deinitialization.
ret = acl.finalize()
# ......
```
