# 术语贡献指南

本文档用于指导开发者向昇腾术语表贡献新的术语和缩略语，或修订已有的术语和缩略语。

## 1. 指南目的

术语和缩略语贯穿产品研发的全生命周期：在需求分析、方案设计、开发实现等阶段，往往会提出并沉淀新的术语和缩略语。产品文档开发（如开发指南、API参考等）阶段，主要是将已定义的术语和缩略语准确、一致地应用到文档中。

本指南用于指导开发者在上述各阶段正确地向公共术语表（[`glossary.md`](https://gitcode.com/cann/docs/blob/master/docs/zh/common-ref/glossary.md)，即《昇腾术语表》）贡献新的术语和缩略语，或修订已有的术语和缩略语，确保术语表格式统一、排序规范、易于检索和维护。

## 2. 术语与缩略语的基本概念

### 2.1 术语的定义

术语指用于一定专业领域内指代专业概念的词语或词组。在技术资料领域，术语特指描述或使用产品时涉及的技术词汇。

**术语包括：**

- 原来为通用词汇，引入技术领域并指代技术概念的词汇，如 Backend、Batch、Batch size。
- 通信领域技术词汇，包括计算机术语、编程术语、协议、标准等，如 ARP、TCP、UDP。
- 产品模块、功能、特性等，如 AI Core、AIPP、AVI。
- 工具、结构件名称，如 ATC、AMCT。
- 术语可以是名词、动词、修饰词（形容词或副词）。

**术语不包括：**

- 命令名称、参数名称、文档名称
- 产品名称、单板名称、版本名称、品牌名称

### 2.2 术语定义的构成

定义是对术语所表示的概念的语言描述。

定义 = 上位概念 + 区别特征（种差，用于区分所定义概念同其他并列概念）

**示例：**

<table style="font-size:14px">
<thead align="left">
<tr>
<th class="cellrowborder" valign="top" width="25%"><strong>术语</strong></th>
<th class="cellrowborder" valign="top" width="25%"><strong>定义</strong></th>
<th class="cellrowborder" valign="top" width="25%"><strong>上位概念</strong></th>
<th class="cellrowborder" valign="top" width="25%"><strong>区别特征（种差）</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td class="cellrowborder" valign="top" width="25%">单算子比对</td>
<td class="cellrowborder" valign="top" width="25%">精度比对工具里Tensor比对的一种方式。选择网络模型中一个或多个参与计算的算子进行精度比对。</td>
<td class="cellrowborder" valign="top" width="25%">精度比对方式</td>
<td class="cellrowborder" valign="top" width="25%">选择部分算子进行比对</td>
</tr>
<tr>
<td class="cellrowborder" valign="top" width="25%">整网比对</td>
<td class="cellrowborder" valign="top" width="25%">精度比对工具里Tensor比对的一种方式。对网络模型中参与计算的所有算子进行精度比对。</td>
<td class="cellrowborder" valign="top" width="25%">精度比对方式</td>
<td class="cellrowborder" valign="top" width="25%">对所有算子进行比对</td>
</tr>
</tbody>
</table>

### 2.3 缩略语的分类

**缩写词（abbreviation）：**

省略英文全称中较长词语的某些成分，但仍指同一概念的术语。

- 示例：用 E-Keying 表示 Electronic Keying，即电子键。

**缩合词（acronym）：**

由英文全称中各成分的首字母或其中完整的音节组成，并按音节发音的缩写词。

- 示例：用 MAC 表示 Medium Access Control，即媒体接入控制；用 EULA 表示 End User License Agreement，即最终用户许可协议。

**首字母缩写词（initialism）：**

由英文全称中各成分的首字母组成，并按首字母发音的缩写词。

- 示例：用 NPU 表示 Neural-Network Processing Unit，即神经网络处理器单元；用 ARP 表示 Address Resolution Protocol，即地址解析协议。

## 3. 贡献范围与适用场景

### 3.1 需要贡献的情形

出现以下情形时，应向术语表贡献术语或缩略语：

- 产品、模块、功能、特性在文档中首次被引用，且目标用户不熟悉该概念。
- 开发过程中产生了新的、未被术语表收录的技术词汇。
- 文档中出现了正文术语表中未解释的缩略语。
- 已有术语的含义、英文全称、中文译名需要修订或纠错。

### 3.2 无需贡献的情形

无需贡献的情形与 2.1 节“术语不包括”、第5节规则2“按需定义”一致，包括：

- 目标用户熟悉的概念，可不定义。
- 命令名称、参数名称、文档名称、产品名称、单板名称、版本名称、品牌名称，不作为术语收录。

### 3.3 多产品通用术语

如果某个术语适用于多个产品，则需作为通用概念定义，不可针对具体产品（详见第5节规则3“通用概念优先”）。

## 4. 术语表结构与格式要求

术语表（[`glossary.md`](https://gitcode.com/cann/docs/blob/master/docs/zh/common-ref/glossary.md)）采用“按首字母分节 + 表格”的结构，每条术语占表格中的一行。贡献时须严格遵守以下格式要求。

### 4.1 总体结构

1. 按术语首字母分节，节标题格式为 `## A`、`## B`、`## C` …… `## Z`，覆盖 A–Z 全部字母。
2. 每个分节下放置一个表格，包含以下表头列：
   - **术语/缩略语**（第一列）
   - **含义**（第二列）
   - **领域**（第三列）

### 4.2 表头列含义

<table style="font-size:14px">
<thead align="left">
<tr>
<th class="cellrowborder" valign="top" width="20%"><strong>列名</strong></th>
<th class="cellrowborder" valign="top" width="80%"><strong>说明</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td class="cellrowborder" valign="top" width="20%">术语/缩略语</td>
<td class="cellrowborder" valign="top" width="80%">术语或缩略语的名称，<strong>必须加粗</strong>。英文缩略语、中文术语、英文全称均可作为词条名称。</td>
</tr>
<tr>
<td class="cellrowborder" valign="top" width="20%">含义</td>
<td class="cellrowborder" valign="top" width="80%">词条含义。英文缩略语格式为“英文全称，对应的中文名称”，换行后提供中文含义（详细解释）。中文术语直接给出中文含义。</td>
</tr>
<tr>
<td class="cellrowborder" valign="top" width="20%">领域</td>
<td class="cellrowborder" valign="top" width="80%">该术语涉及的领域/所属组件，如 CANN、MindStudio、HDK、MindIE、MindCluster等。跨领域时可填写多个，用 <code>/</code> 分隔。</td>
</tr>
</tbody>
</table>

### 4.3 术语/缩略语、含义、领域列编写要求

#### 英文缩略语词条

<table style="font-size:14px">
<thead align="left">
<tr>
<th class="cellrowborder" valign="top" width="20%"><strong>术语/缩略语</strong></th>
<th class="cellrowborder" valign="top" width="50%"><strong>含义</strong></th>
<th class="cellrowborder" valign="top" width="30%"><strong>领域</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td class="cellrowborder" valign="top" width="20%">英文缩略语</td>
<td class="cellrowborder" valign="top" width="50%">英文全称，对应的中文名称。换行后提供中文含义（对概念做详细说明）。</td>
<td class="cellrowborder" valign="top" width="30%">该术语涉及的领域/所属组件，如 CANN、MindStudio等，跨领域用 <code>/</code> 分隔。</td>
</tr>
<tr>
<td class="cellrowborder" valign="top" width="20%">英文全称词条（非缩略语）</td>
<td class="cellrowborder" valign="top" width="50%">以完整英文名称作为词条（如 Accumulated Relative Error、Batch size），含义列同样遵循“英文全称，对应的中文名称”+ 详细说明的格式。</td>
<td class="cellrowborder" valign="top" width="30%">该术语涉及的领域/所属组件，跨领域用 <code>/</code> 分隔。</td>
</tr>
</tbody>
</table>

示例：

<table style="font-size:14px">
<thead align="left">
<tr>
<th class="cellrowborder" valign="top" width="20%"><strong>术语/缩略语</strong></th>
<th class="cellrowborder" valign="top" width="50%"><strong>含义</strong></th>
<th class="cellrowborder" valign="top" width="30%"><strong>领域</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td class="cellrowborder" valign="top" width="20%"><strong>AscendCL</strong></td>
<td class="cellrowborder" valign="top" width="50%">Ascend Computing Language，昇腾编程语言。<br/>提供Device管理、Context管理、Stream管理、内存管理、模型加载与执行、算子加载与执行、媒体数据处理等C语言的API库供用户开发深度神经网络应用，用于实现目标识别、图像分类等功能。</td>
<td class="cellrowborder" valign="top" width="30%">CANN</td>
</tr>
</tbody>
</table>

#### 中文术语词条

<table style="font-size:14px">
<thead align="left">
<tr>
<th class="cellrowborder" valign="top" width="20%"><strong>术语/缩略语</strong></th>
<th class="cellrowborder" valign="top" width="50%"><strong>含义</strong></th>
<th class="cellrowborder" valign="top" width="30%"><strong>领域</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td class="cellrowborder" valign="top" width="20%">中文术语</td>
<td class="cellrowborder" valign="top" width="50%">中文含义，必要时换行补充详细说明。</td>
<td class="cellrowborder" valign="top" width="30%">该术语涉及的领域/所属组件，如 CANN、MindStudio等，跨领域用 <code>/</code> 分隔。</td>
</tr>
</tbody>
</table>

示例见 2.2 节（定义构成示例）及第9节（词条示例）。

### 4.4 排序规则

- 排序请务必按照**字母序列**排列，以字典的格式，**先英文，后中文**。
- 英文词条按首字母（A–Z）归入对应分节；中文词条按其**拼音首字母**归入对应分节（如“单算子比对”归入 D 节、“整网比对”归入 Z 节、“业务面”归入 Y 节）。
- 同一分节内，英文词条在前、中文词条在后，均按字典序排列。
- 同一个缩略语对应多个英文全称和含义时，允许在表中**多次出现**（各占一行），分别给出不同含义。

同一缩略语多次出现的示例见 9.3 节。

## 5. 术语贡献规则

贡献或修订术语时，须遵循以下规则：

1. **与标准保持一致**：术语名称要与国际、国家、行业标准中的名称保持一致。
2. **按需定义**：资料中的术语是否需要提供定义取决于目标用户的需求；用户熟悉的概念可以不定义；用户不熟悉的概念需要定义（一般以术语表的形式提供）。
3. **通用概念优先**：如果某个术语适用于多个产品，则需作为通用概念定义，不可针对具体产品。
4. **一词一义**：不使用多个术语指代同一个概念。
5. **定义适度**：术语的定义要适度，不可过宽或过窄。
6. **常用词汇特殊化**：使用常用词汇来表示陌生概念时，如果该常用词汇在某个领域具有特殊含义，则需要将其作为术语并给出定义。
7. **陌生词汇须定义**：使用陌生词汇来表示陌生概念时，需要将其作为术语并给出定义。
8. **定义用词要简单**：在定义一个术语时，定义中不应使用更复杂、陌生的词汇。
9. **避免循环引用**：在定义某个术语时，不建议重复引用该术语或者该术语的变体（英文术语中较为常见）。
10. **首次出现给出解释**：文档正文中术语首次出现的位置要给出含义解释（标题/表头除外）。对于发布在 [CANN文档中心](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/latest/index/index.html) 的文档，术语之后再次出现时，可配置为气泡形式（配置时须使用 `<term>术语</term>` 标签包裹，便于社区前端以冒泡形式呈现）。在同一页面上，建议为首次出现的术语进行配置。

## 6. 缩略语贡献规则

贡献或修订缩略语时，须遵循以下规则：

1. **与标准保持一致**：缩略语的名称和英文全称要与国际、国家或行业标准保持一致，缩写词通常大写（如 CPU、API），大小写遵循官方写法，禁止使用变体表达（如官方术语表为 AI Core，禁止写作 aicore）。
2. **全称要展开**：缩略语的全称要展开，避免缩略语的部分内容在英文全称中直接沿用。
3. **必须在术语表中解释**：文档正文中出现的所有缩略语都必须在术语表中给予解释。
4. **一词多义处理**：当一个缩略语可能对应多个英文全称和含义时，通常建议均使用全称，或者其中一个含义使用缩略语，其他含义使用全称。
5. **单位缩略语**：单位缩略语的大小写遵循国际惯例。
6. **使用频率判断**：
   - 对于在文档中出现次数频繁或冗长的词语，在对缩略语解释清楚后，可以使用缩略语。
   - 对于在文档中出现次数较少或长度较短的词语，避免使用缩略语，以免读者产生误解。
   - 当某些缩略语为读者非常熟悉时，首次出现的位置可以不给英文全称，直接使用缩略语。
7. **首次出现给出全称**：正文缩略语首次出现（标题/表头除外）给出全称，格式：缩略语（英文全称，中文全称），全称实词首字母大写，使用全角括号，如 CRC（Cyclic Redundancy Check，循环冗余校验）。对于发布在 [CANN文档中心](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/latest/index/index.html) 的文档，缩略语之后再次出现时，可配置为气泡形式（配置时须使用 `<term>缩略语</term>` 标签包裹，便于社区前端以冒泡形式呈现）。在同一页面上，建议为首次出现的缩略语进行配置。
8. **无需给出全称的豁免场景**：
   - **软硬件环境要求区域**：环境要求/硬件要求/软件要求/操作系统和软件要求等标题后的表格（含CPU/内存/硬盘/RAID卡/网卡/编解码卡/GPU卡/OS/操作系统/软件包名/软件包URL路径中的缩略语）
   - **图片名称与图片引用URL**：图片语法 `![alt](url)` 中 alt（图片名）与 URL 内的缩略语
   - **节点名称或示例**：含 NODE/HOST/SERVER 的节点名（如 INDEX_NODE/QUERY_NODE/NODE0）及示例节点名
   - **缩略语带数字序号**：已知缩略语+数字（如 CPU0/NUMA0/NODE0/GPU0/PF0/VF0/DIMM0）
   - **编程语言关键字**：TRUE/FALSE/NULL/VOID/INT/RETURN/CLASS/IF/ELSE/FOR/WHILE/NEW/DELETE/TEMPLATE/NAMESPACE 等
   - **文件格式扩展名**：PNG/JPG/PDF/JSON/XML/YAML/TOML 等
   - **代码/注释区域**：围栏代码块（` ``` ` 或 ` ~~~ ` 包裹）内部、行内代码（反引号包裹）、YAML frontmatter（`---` 包裹）、HTML注释（`<!-- -->`）、`<script>`/`<style>` 块内部

## 7. 评审与合入流程

术语贡献需经过以下评审与合入流程后方可生效：

### 7.1 评审

1. 贡献者在其领域内进行术语/缩略语评审。
   - 名称是否与行业标准一致。
   - 格式、排序是否符合本指南要求。

### 7.2 合入

1. 将评审通过的术语条目合入 [`glossary.md`](https://gitcode.com/cann/docs/blob/master/docs/zh/common-ref/glossary.md) 对应分节，按字母序插入正确位置。
2. 合入后同步更新引用这些术语的文档，保证正文首现处按第6节规则7的格式给出英文全称和中文全称。

## 8. 贡献操作步骤（实操指引）

1. 查询术语表[`glossary.md`](https://gitcode.com/cann/docs/blob/master/docs/zh/common-ref/glossary.md)：在术语表中检索该术语/缩略语，若无收录，确认是否与国际、国家、行业标准一致。

2. 判断贡献必要性：对照第3节，确认该词条符合收录范围、目标用户确实需要定义。

3. 撰写初稿：按照第4、5、6节要求撰写新增术语/缩略语相关内容，确保含义列格式正确、定义满足结构要求。

4. 提交评审：将新增术语/缩略语在领域内进行评审确认（评审内容及通过标准见 7.1 节）。

5. 上库与合入：按字母序合入 [`glossary.md`](https://gitcode.com/cann/docs/blob/master/docs/zh/common-ref/glossary.md) 对应分节，并同步更新正文首现（见 7.2 节）。

## 9. 词条示例

### 9.1 英文缩略语词条

<table style="font-size:14px">
<thead align="left">
<tr>
<th class="cellrowborder" valign="top" width="20%"><strong>术语/缩略语</strong></th>
<th class="cellrowborder" valign="top" width="50%"><strong>含义</strong></th>
<th class="cellrowborder" valign="top" width="30%"><strong>领域</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td class="cellrowborder" valign="top" width="20%"><strong>AOE</strong></td>
<td class="cellrowborder" valign="top" width="50%">Ascend Optimization Engine，昇腾调优引擎。用于封装调优过程中的ATC编译及AscendCL运行服务接口，提供并行调优功能。</td>
<td class="cellrowborder" valign="top" width="30%">CANN</td>
</tr>
</tbody>
</table>

### 9.2 中文术语词条

<table style="font-size:14px">
<thead align="left">
<tr>
<th class="cellrowborder" valign="top" width="20%"><strong>术语/缩略语</strong></th>
<th class="cellrowborder" valign="top" width="50%"><strong>含义</strong></th>
<th class="cellrowborder" valign="top" width="30%"><strong>领域</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td class="cellrowborder" valign="top" width="20%"><strong>单算子比对</strong></td>
<td class="cellrowborder" valign="top" width="50%">精度比对工具里Tensor比对的一种方式。选择网络模型中一个或多个参与计算的算子进行精度比对。</td>
<td class="cellrowborder" valign="top" width="30%">CANN</td>
</tr>
</tbody>
</table>

### 9.3 一词多义词条（同一缩略语多次出现）

<table style="font-size:14px">
<thead align="left">
<tr>
<th class="cellrowborder" valign="top" width="20%"><strong>术语/缩略语</strong></th>
<th class="cellrowborder" valign="top" width="50%"><strong>含义</strong></th>
<th class="cellrowborder" valign="top" width="30%"><strong>领域</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td class="cellrowborder" valign="top" width="20%"><strong>AMP</strong></td>
<td class="cellrowborder" valign="top" width="50%">Asymmetric multiprocessing，非对称多处理。一种多处理的架构……</td>
<td class="cellrowborder" valign="top" width="30%">通用</td>
</tr>
<tr>
<td class="cellrowborder" valign="top" width="20%"><strong>AMP</strong></td>
<td class="cellrowborder" valign="top" width="50%">Automatic Mixed Precision，自动混合精度。混合精度训练是深度学习中一种提高训练速度和效率的技术……</td>
<td class="cellrowborder" valign="top" width="30%">CANN</td>
</tr>
</tbody>
</table>

## 10. 贡献自检清单

提交前请逐项核对，按“内容—格式—流程”分组：

**内容质量**

- [ ] 术语名称与国际/国家/行业标准一致，英文全称与中文名称准确。
- [ ] 一句话定义说明“是什么”，详细定义补充场景与边界。
- [ ] 定义中未使用更复杂、陌生的词汇。
- [ ] 定义中未重复引用该术语或其变体。
- [ ] 未使用“强大”“高效”等主观评价。

**格式与结构**

- [ ] 术语名称已加粗，三列（术语/缩略语、含义、领域）齐全。
- [ ] 英文缩略语格式为“英文全称，对应的中文名称”；正文解释格式为“缩略语（英文全称，中文全称）”，两者未混用。
- [ ] 缩略语全大写、大小写遵循官方写法，未使用变体表达。
- [ ] 正文中配置气泡的术语/缩略语已使用 `<term>…</term>` 标签包裹。
- [ ] 一个缩略语对应多个含义时已分别列出或使用全称区分。
- [ ] 缩略语全称已完整展开，未沿用缩略语本身。
- [ ] 词条已按字母序（先英文、后中文）插入正确分节。
- [ ] 别名（缩写/全称/旧称）均可被检索到。

**流程与提交**

- [ ] 已在 [`glossary.md`](https://gitcode.com/cann/docs/blob/master/docs/zh/common-ref/glossary.md) 查重，确认非重复词条。
- [ ] 评审通过后，按字母序合入 [`glossary.md`](https://gitcode.com/cann/docs/blob/master/docs/zh/common-ref/glossary.md) 对应分节，并同步更新正文首现。
