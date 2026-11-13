# 绘图规范

## 修订记录

| 时间 | 变更说明 |
| -------- | --------------------------- |
| 2026-11-12 | 新增绘图规范，涵盖字体、绘图色彩、线条与箭头、图形节点以及层级嵌套等绘图要求。 |

## 概述

本文档针对CANN组织下开源项目的**技术绘图**制定了统一的绘图规范，涵盖了字体、色彩、线条与箭头、图形节点以及层级嵌套等要求，旨在确保所有配图风格一致、清晰美观、易于理解。

开发者在为CANN文档绘制配图前，请务必阅读并遵循本规范。配色、节点、线条与箭头等绘图元素可参考[绘图模板](../writing_template/drawing_template.xml)（以draw.io绘图工具为例）。欢迎随时提出改进建议。

> [!NOTE]说明
> 绘图模板仅用于展示符合本规范的图形示例，模板中的图例仅供参考，不保证与当前业务实现完全一致，请以实际业务场景为准。

## 字体规范

- 字体字号

  中、英文统一使用HarmonyOS Sans字体，[《HarmonyOS Sans字体》下载地址](https://developer.huawei.com/consumer/cn/doc/doccenter-ux-design/font-0000001828772001)。  
  一般文本，如注释文本、框图中的文本等，14px。  
  突出文本，如网络结构图中需要突出的内容，16px。  
  字号下限，需要缩小字号才能放下的情况，不能小于10px。

- 文字方向

  图形中的文字方向应符合读者的阅读习惯，包括：

  字头朝上。水平方向、垂直方向或斜向的文字标注，文字均应沿水平方向、从左到右书写。某些特殊情况下（如文本区域宽度很窄）的文字标注，文字应沿垂直方向写，自上至下。英文单词在页面竖排版时，在线条以左的文字，文字方向自下向上，线条以右的文字，文字方向自上向下。

- 文本换行

  同一组阿拉伯数字应在同一行，不能跨两行，各行的文本长度必须尽量接近。

  英文单词不能换行。

## 绘图色彩规范

- 一张图中建议不超过3种颜色（不包含文字、箭头、线条、边框、流程中开始和结束等中性色）。

- 如果图中内容需要区分主次：使用的颜色为2种时，主要内容使用<span style="display:inline-block;width:14px;height:14px;background:#C2D5FE;vertical-align:-2px"></span> #C2D5FE，次要内容使用<span style="display:inline-block;width:14px;height:14px;background:#E0E2E6;vertical-align:-2px"></span> #E0E2E6；使用的颜色超过2种时，主要内容使用高亮色，次要内容按优先级顺序取用默认色值。

- 非必要不使用高亮色，当图形中内容需要特别强调或突出的时候，可以考虑使用，但要避免大面积出现高亮。

- 存在层级嵌套场景
  - 一个层级框默认使用无填充边框，边框颜色<span style="display:inline-block;width:14px;height:14px;background:#686D75;vertical-align:-2px"></span> #686D75。
  - 多于一个层级则最小层级使用填充色<span style="display:inline-block;width:14px;height:14px;background:#EDEFF2;vertical-align:-2px"></span> #EDEFF2，无边框；其他层级使用无填充边框，边框颜色<span style="display:inline-block;width:14px;height:14px;background:#686D75;vertical-align:-2px"></span> #686D75。

![绘图色板](figures/color_palette.png)

## 线条与箭头规范

- 线、边框等使用规范：推荐参数如下（以draw.io中配置为例），线条宽度0.75pt，线条与边框颜色统一使用<span style="display:inline-block;width:14px;height:14px;background:#686D75;vertical-align:-2px"></span> #686D75。

- 箭头使用规范：线条宽度0.75pt，色值选择、箭头类型、箭头大小请参考[绘图模板](../writing_template/drawing_template.xml)中的配置。

## 图形节点规范

- 节点文字字号为14px，居中对齐于色块。默认节点文字色值为<span style="display:inline-block;width:14px;height:14px;background:#202329;vertical-align:-2px"></span> #202329，突出节点文字色值为<span style="display:inline-block;width:14px;height:14px;background:#FFFFFF;border:1px solid #E0E2E6;vertical-align:-2px"></span> #FFFFFF（白色），节点高度32px，默认宽度140px，宽度可随实际场景设定，建议按照40px的数值梯度递增，例如60（最小尺寸）、100、140、180、220……节点间距建议使用8的倍数，例如8px、16px、24px、32px等，特殊情况最小可以选用4px，具体根据实际场景而定，原则上保证节点宽度和节点间距的整体和谐。

- 流程色块均采用4px圆角，判断和返回以及数据类型流程色块对应不同色值，具体色值参考[绘图模板](../writing_template/drawing_template.xml)。

- 组件容器采用自适应宽度与高度，一般不超过1000px的宽度，如有需要可根据自身业务场景做变动。保持内容主体的同时，可以增加四周的留白空间，比如左右增加80px，上下增加40px。

- 组件图片容器宽度分为大、中、小三种尺寸，分别为920px、600px和300px。

![图形节点示例](figures/graph_node_example.png)


