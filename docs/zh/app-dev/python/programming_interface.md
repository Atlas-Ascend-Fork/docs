# 编程接口

## 接口命名规则

pyACL接口的命名与访问方式如下：

1. 通常通过`acl.<子模块>.<函数名>`调用，例如`acl.rt.create_stream`和`acl.mdl.load_from_file_with_mem`。
2. 函数名采用小写字母，单词之间以下划线分隔。
3. 部分接口直接位于`acl`模块下，例如`acl.init`。

具体接口名称以接口参考为准。

## 接口类别

常见功能类别与Python子模块的对应关系如下：

| 接口类别 | Python子模块 | 描述 |
| --- | --- | --- |
| runtime | rt | 表示运行管理类的接口 |
| DVPP | media、himpi | 表示媒体数据处理类的接口 |
| AIPP | mdl | 表示aipp（AI Preprocessing）类的接口 |
| CBLAS | blas | 表示blas类的接口 |
| model | mdl | 表示模型推理类的接口 |
| OP | op | 表示算子执行类的接口 |
| fv | fv | 表示特征向量检索的接口 |
| Profiling | prof | 表示Profiling配置类接口 |

>[!NOTE]
>
> 表中的子模块通过`acl.<子模块>`访问。功能类别与子模块不一定一一对应，例如AIPP接口和模型推理接口均位于`acl.mdl`，AIPP参数设置接口包括`acl.mdl.set_aipp_by_input_index`。

## 变量命名

本文代码示例中涉及的变量，其中，命名带下划线的变量（例如：\_deviceId\_）表示类的私有变量。
