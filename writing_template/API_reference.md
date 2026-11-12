# API参考写作模板

当前API参考模板包含三部分内容：

- 接口简介
  
  概述本文档中接口的主要功能、使用场景、接口分类、头文件和库文件等内容。

- 接口介绍

  介绍每个接口的产品支持情况、功能、函数原型、参数、返回值等内容。

  - 若一个接口对应一个md文件，则md文件的一级标题是接口名，二级标题是产品支持情况、功能说明、函数原型、参数说明等部分。接口多的情况下，可以增加一个父级目录，目录名可以是功能名、模块名等。示例如下：
    
    ```text
    目录名
      # 接口名1
        ## 产品支持情况
        ## 功能说明
        ## 函数原型
        ## 参数说明
        ......
      # 接口名2
      ......
    ```

  - 若多个接口合并成一个md文件，则md文件的一级标题是功能名或模块名等，二级标题是接口名，三级标题是产品支持情况、功能说明、函数原型、参数说明等部分。示例如下：
    
    ```text
    # 功能名
      ## 接口名1
         ### 产品支持情况
         ### 功能说明
         ### 函数原型
         ### 参数说明
      ## 接口名2
      ......
    ```
   - 若涉及类，还需在介绍接口前，增加一节介绍类的作用、使用场景、继承/派生关系、涉及的头文件以及Public成员函数等。其中，继承/派生关系为可选内容，存在继承关系时需要列出继承关系图，图中应包含基类及其所有派生类，继承关系通过箭头表示（子类指向父类），当前类用主题色突出显示。可参考[简介](https://gitcode.com/cann/metadef/blob/master/docs/zh/api/gert_namespace/extendedkernelcontext/introduction.md)。

- 自定义数据类型介绍
  
  介绍除C/C++、Python标准库之外的自定义数据类型，包括返回值、枚举、结构体等内容。

下文介绍接口简介、接口介绍、自定义数据类型部分的写作要求。

## 接口简介

概述本文档中接口的主要功能、使用场景、接口分类、头文件和库文件等信息。可参考[《Runtime API参考》](https://gitcode.com/cann/runtime/blob/master/docs/zh/api_ref/01_overview.md)中的描述。该章节的标题可按需调整。

## 接口介绍

以接口名命名接口介绍章节的标题，建议按如下顺序介绍接口。该顺序非强制要求，各组件可按需调整。
1. 产品支持情况
2. 功能说明
3. 函数原型
4. 参数说明
5. 返回值说明
6. 约束说明
7. 调用示例
  
该建议顺序主要考虑以下要点：
- 参考案例及各组件现有文档的实际情况。
- 往期问题反馈显示，读者需先确认当前使用的产品是否支持该接口，再决定是否继续阅读，因此将产品支持情况置于最前。
- 部分接口有约束说明，部分没有；此外，有些接口的约束说明内容较长、条目较多，甚至占据整屏。因此，建议将约束说明后置，以便读者先在一屏内了解接口的整体情况，再看使用约束。

### 产品支持情况

- **写作示例：**

    ```text
    ### 产品支持情况

    <!-- npu="950" id295 -->
    - Ascend 950PR&950DT系列产品：支持
    <!-- end id295 -->
    <!-- npu="A3" id296 -->
    - Atlas A3系列产品：支持
    <!-- end id296 -->
    <!-- npu="910b" id297 -->
    - Atlas A2系列产品：支持
    <!-- end id297 -->
    <!-- npu="310b" id298 -->
    - Atlas 200I/500 A2推理产品：支持
    <!-- end id298 -->
    <!-- npu="310p" id2756 -->
    - Atlas推理系列产品：支持
    <!-- end id2756 -->
    <!-- npu="910" id2757 -->
    - Atlas训练系列产品：支持
    <!-- end id2757 -->
    <!-- npu="IPV350" id2758 -->
    - IPV350：不支持
    <!-- end id2758 -->
    <!-- npu="5162A" id5002 -->
    - Hisilicon5162A：不支持
    <!-- end id5002 -->
    ```

- **效果展示：**

  ![](figures/api_ref_image_0000002779844914.png)

- **写作要求：**
    1. 小节标题为“产品支持情况”，各产品的支持情况以列表形式呈现。

        备注：对于部分系列产品，若API只支持该系列产品中的部分产品，则需要区分说明。

    2. 列表自上而下按产品发布先后顺序排列，最新的产品置于最上方。
    3. 产品所在行需添加产品标签。
    4. 当该API参考对所有产品通用、无需区分支持情况时，接口文档中可不添加“产品支持情况”小节。
    5. 部分版本的手册（如硬件接口文档）不按系列产品维度描述接口支持度，而是每种硬件产品独立成一本API参考，此类文档的接口中无需添加“产品支持情况”小节。
    6. 若接口为非商用特性，需要在文档中添加说明，可参考以下写法：“**须知：本接口为试验特性，后续版本可能会存在变更，不支持应用于生产环境中。**”建议将其置于“产品支持情况”之前。
    7. 对于暂不支持、后续会放开的接口，可以在文档中备注为预留接口，可参考以下写法：“**须知：本接口为预留接口，暂不支持。**”若接口为预留接口，则无需说明“产品支持情况”。

### 功能说明

- **写作示例：**

    此处以Runtime的aclrtSetDevice接口为例。

    ```text
    ### 功能说明

    指定当前线程中用于运算的Device。支持在不同线程中调用aclrtSetDevice接口指定同一个Device用于运算。

    多Device场景下，可在进程中通过aclrtSetDevice接口切换到其他Device。

    调用本接口会隐式创建默认Context，该默认Context中包含一个默认Stream。在同一个进程的多个线程中，如果调用aclrtSetDevice接口并指定相同的Device用于计算，那么这些线程将共享同一个默认Context。
    ```

- **效果展示：**

  ![](figures/api_ref_image_0000002780241006.png)

- **写作要求：**
    1. 介绍接口功能，若存在使用场景限制，需说明清楚。
    2. 多款产品在一份文档中同时发布时，若各产品支持的功能不同，需区分并说明清楚。
    3. 同一版本内，若新增接口与原有接口功能类似或是其扩展接口，需在新接口中写清楚功能差异。

        举例如下：

        - aclrtCreateEvent接口功能：创建一个Event，创建出来的Event可用于统计两个Event之间的耗时、多Stream场景下的同步等待等场景。
        - aclrtCreateEventWithFlag接口功能：创建一个带flag的Event，不同flag的Event用于不同的功能。支持创建Event时携带多个flag（按位进行或操作），从而同时使能对应flag的功能。

    4. 同一版本内，若新增接口将替代老接口且老接口后续废弃，需在老接口中增加须知“**须知：xxx接口在CANN x.x.x版本标记为废弃，将在xxxx年xx月xx日之后的版本删除，替换为：xxx接口。**”同时，需集中说明当前组件的所有废弃项。可参考《Runtime API参考》的[aclrtQueryEvent](https://gitcode.com/cann/runtime/blob/master/docs/zh/api_ref/07_event_management.md#aclrtQueryEvent_deprecated)、[废弃项列表](https://gitcode.com/cann/runtime/blob/master/docs/zh/api_ref/01_overview.md)。

    5. 若该接口需与其他多个接口配合使用，需在“功能说明”处介绍配合接口的调用关系。可参考《Runtime API参考》的[aclrtMemExportToShareableHandle](https://gitcode.com/cann/runtime/blob/master/docs/zh/api_ref/11-04_virtual_memory_management.md#aclrtMemExportToShareableHandle)。

    6. （可选）不同接口所在的头文件、库文件可能不同，可在“功能说明”处介绍该接口所在的头文件与库文件。
    7. 功能说明中若涉及术语或其缩写，需给出解释，或参见术语解释章节。

### 函数原型

- **写作示例：**

    此处以Ascend C的接口为例。

    ```cpp
    template <typename T>
    __aicore__ inline void DataCopyPad(const GlobalTensor<T> &dstGlobal, const LocalTensor<T> &srcLocal, const DataCopyExtParams &dataCopyParams)
    ```

- **效果展示：**

  ![](figures/api_ref_image_0000002809655687.png)

- **写作要求：**
    1. 函数原型使用代码块样式并设置语言类型，使函数原型中的字符串高亮显示；数据类型、枚举值、返回值不跳转，需在参数说明处提供跳转。
    2. 函数原型不加粗，且结尾不加分号。
    3. 若有多个函数原型，需以列表形式呈现并说明区别。可参考《Ascend C API参考》中的[asc_copy](https://gitcode.com/cann/asc-devkit/blob/9.2.0/docs/zh/api/SIMD-API/c_api/vector_datamove/asc_copy.md)。

### 参数说明

- **写作示例：**

  ![](figures/api_ref_image_0000002780694058.png)

- **效果展示：**

  ![](figures/api_ref_image_0000002780858146.png)

- **写作要求：**
  - 参数名：与函数原型中的参数名保持一致。
  - 输入/输出：与头文件中接口注释中的说明保持一致。
  - 说明：该列包括但不限于参数含义、单位、数据类型、取值范围、默认值及其他约束信息，不涉及的内容可删除。
    - 若参数取值的支持情况需区分产品，应移到“约束说明”中呈现，因为表格中无法添加产品标签。

      说明时可列举所有产品的支持情况，也可按归类方式说明，例如：

      - 以下产品型号支持XX取值：

        XX

        XX

      - 以下产品型号支持XX取值：

        XX

        XX

    - Python接口的函数原型中无数据类型，需在参数说明中体现各参数的数据类型。
    - C/C++接口的函数原型已展示各参数的数据类型，参数说明中无需重复；但除C/C++基本数据类型外，自定义数据类型需提供跳转至其详细解释。
    - 若参数为自定义的枚举或结构体，需说明枚举的定义以及各枚举项的含义、结构体的定义以及各成员变量的含义与用法；枚举和结构体的定义要与软件保持一致。

### 返回值说明

- **写作示例：**

    此处以Runtime接口为例。

    ```text
    ### 返回值说明

    返回0表示成功，返回其他值表示失败，请参见aclError。
    ```

- **效果展示：**

  ![](figures/api_ref_image_0000002780894462.png)

- **写作要求：**
  - 无返回值时注明“无”，结尾不加句号。
  - 有返回值时，需说明返回值的具体含义。

### 约束说明（可选）

本节主要描述接口维度的使用约束，或接口中多个参数配合使用的约束。注意：单个参数的使用约束应写到“参数说明”中。

若存在多条约束，以无序列表形式展示。

若某条约束仅适用部分产品，需在约束中区分说明。可以参考以下写法，既便于维护又简洁：

![](figures/api_ref_image_0000002810271647.png)

### 调用示例（可选）

- 使用代码块包裹示例代码，并设置语言类型。
- 若调用示例为伪码，无法直接编译运行，需注明，例如：“调用接口后，需增加异常处理的分支，并记录报错日志、提示日志，此处不一一列举。以下是关键步骤的代码示例，不可以直接拷贝编译运行，仅供参考。”
- （可选）关键代码处可辅以注释说明；注意不同语言的注释风格不同，注释符号与文字之间需留空格，例如：

    // xxxxxxxxxxxx

    /\* xxxxxxxxxxx  \*/

    \# xxxxxxxxx

## 自定义数据类型介绍

### 返回码

介绍接口返回码的定义规则，每个返回码的定义、可能原因以及解决方法。可参考《Runtime API参考》的[aclError](https://gitcode.com/cann/runtime/blob/master/docs/zh/api_ref/25-01_aclError.md)。

### Enumerations

介绍每个枚举的定义、每个枚举项的含义以及使用说明。可参考《Runtime API参考》的[Enumerations](https://gitcode.com/cann/runtime/blob/master/docs/zh/api_ref/25-02_Enumerations.md)。

### Structs

介绍结构体的定义、每个成员变量的含义以及使用说明。可参考《Runtime API参考》的[Structs](https://gitcode.com/cann/runtime/blob/master/docs/zh/api_ref/25-04_Structs.md)。

### Typedefs

介绍每个Typedef的定义。如有特殊注意事项，也需说明。可参考《Runtime API参考》的[Typedefs](https://gitcode.com/cann/runtime/blob/master/docs/zh/api_ref/25-05_Typedefs.md)。
