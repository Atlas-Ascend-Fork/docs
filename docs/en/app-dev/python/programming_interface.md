# Programming APIs

## API Naming Conventions

The APIs are named according to the following rules:

1. acl+*API class*+*Operation verb*+*Object noun*.
2. The *Operation verb* and *Object noun* fields are written with the first letter capitalized.

## API Classes

| API Class| Abbreviation| Description|
| --- | --- | --- |
| runtime | rt | Runtime|
| DVPP | media | Digital Vision Pre-Processing|
| AIPP | aipp | AI Pre-Processing|
| CBLAS | blas | Basic Linear Algebra Subprograms|
| model | mdl | Model inference|
| OP | op | Operator execution|
| fv | fv | Feature vector retrieval|
| Profiling | prof | Profiling configurations|

>[!NOTE]
>
>- The abbreviation of each class name contains a maximum of four letters.
>- If the class name coincides with the operation object name, the object name is omitted. For example, `acl.mdl.load_from_file_with_mem` is a model API for loading model from file and `mdl` after `Load` is omitted in the API name.

## Variable Naming

In the code examples provided in this guide, a variable with an underscore (_) suffix (for example, *_deviceId_*) is private to the corresponding class.
