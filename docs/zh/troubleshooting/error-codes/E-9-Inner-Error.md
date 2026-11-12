# E\*9\*\*\* Internal error

E\*9\*\*\*表示系统内部错误码，请根据报错信息进行问题排查。若无法解决问题，您可以获取日志后单击[Link](https://www.hiascend.com/support)反馈问题。

内部错误码的报错格式如下：

```text
ErrorCode[PID: xxxxxx] DateTimeMS ErrorMessage [FUNC:FuncName][FILE:FileName][LINE:LineNumber]
```

在上述报错格式中，ErrorCode表示错误码，DateTimeMS表示时间戳，ErrorMessage表示具体的报错信息，FuncName表示报错的函数名称，FileName表示报错的文件名，LineNumber表示报错的行号。内部错误码的报错示例如下：

```text
EE9999[PID: 2545712] 2026-03-24-21:23:19:464:314 (EE9999): Failed to obtain the kernel address based on the kernel name, kernel_name=RunCpuKernel, retCode=0x0711000E. [FUNC:StreamLaunchCpuKernel][FILE:aicpu_stars.cc][LINE:224]
```
