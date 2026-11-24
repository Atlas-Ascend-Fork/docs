# Glossary Contribution Guide

This document guides you in contributing new terms and abbreviations to the Ascend glossary or revising existing terms and abbreviations.

## 1. Purpose of This Guide

Terms and abbreviations run through the entire lifecycle of product development. In phases such as requirements analysis, solution design, and development implementation, new terms and abbreviations are often proposed and accumulated. In the phase of product documentation development (such as development guides and API references), the main task is to apply the defined terms and abbreviations to documents accurately and consistently.

This guide helps you correctly contribute new terms and abbreviations to, or revise existing terms and abbreviations in, the common glossary ([`glossary.md`](https://gitcode.com/cann/docs/blob/master/docs/en/common-ref/glossary.md), that is, the Ascend Glossary) during the phases described above, ensuring consistent formatting, standardized sorting, and easy retrieval and maintenance of the glossary.

## 2. Basic Concepts of Terms and Abbreviations

### 2.1 Definition of a Term

A term refers to a word or phrase used to denote a professional concept in a specific professional field. In technical documentation, a term specifically refers to the technical vocabulary involved in describing or using a product.

**Terms include:**

- Words that were originally common and are introduced into the technical field to denote technical concepts, such as Backend, Batch, and Batch size.
- Technical words in the communications field, including computer terms, programming terms, protocols, and standards, such as ARP, TCP, and UDP.
- Product modules, functions, and features, such as AI Core, AIPP, and AVI.
- Names of tools and structural components, such as ATC and AMCT.
- A term can be a noun, a verb, or a modifier (an adjective or an adverb).

**Terms do not include:**

- Command names, parameter names, and document names
- Product names, board names, version names, and brand names

### 2.2 Composition of a Term Definition

A definition is a verbal description of the concept represented by a term.

Definition = superordinate concept + distinguishing feature (differentia, used to distinguish the defined concept from other parallel concepts)

**Example:**

<table style="font-size:14px">
<thead align="left">
<tr>
<th class="cellrowborder" valign="top" width="25%"><strong>Term</strong></th>
<th class="cellrowborder" valign="top" width="25%"><strong>Definition</strong></th>
<th class="cellrowborder" valign="top" width="25%"><strong>Superordinate concept</strong></th>
<th class="cellrowborder" valign="top" width="25%"><strong>Distinguishing feature (differentia)</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td class="cellrowborder" valign="top" width="25%">single-operator comparison</td>
<td class="cellrowborder" valign="top" width="25%">A type of tensor comparison in the accuracy comparison tool. It selects one or more operators involved in computation in a network model for accuracy comparison.</td>
<td class="cellrowborder" valign="top" width="25%">accuracy comparison method</td>
<td class="cellrowborder" valign="top" width="25%">Selects some operators for comparison</td>
</tr>
<tr>
<td class="cellrowborder" valign="top" width="25%">network-wide comparison</td>
<td class="cellrowborder" valign="top" width="25%">A type of tensor comparison in the accuracy comparison tool. It compares the accuracy of all operators involved in computation in a network model.</td>
<td class="cellrowborder" valign="top" width="25%">accuracy comparison method</td>
<td class="cellrowborder" valign="top" width="25%">Compares all operators</td>
</tr>
</tbody>
</table>

### 2.3 Classification of Abbreviations

**Abbreviation:**

A term that omits some components of longer words in its English full name but still refers to the same concept.

- Example: Use E-Keying to represent Electronic Keying, that is, an electronic key.

**Acronym:**

An abbreviation composed of the initial letters of each component or complete syllables in the English full name, and pronounced by syllables.

- Example: Use MAC to represent Medium Access Control, that is, media access control; use EULA to represent End User License Agreement, that is, the end-user license agreement.

**Initialism:**

An abbreviation composed of the initial letters of each component in the English full name, and pronounced by initial letters.

- Example: Use NPU to represent Neural-Network Processing Unit, that is, a neural-network processing unit; use ARP to represent Address Resolution Protocol, that is, the address resolution protocol.

## 3. Contribution Scope and Applicable Scenarios

### 3.1 When to Contribute

Contribute terms or abbreviations to the glossary in the following situations:

- A product, module, function, or feature is referenced for the first time in documentation, and target users are unfamiliar with the concept.
- New technical vocabulary that is not yet included in the glossary is generated during development.
- An abbreviation that is not explained in the body glossary appears in documentation.
- The meaning, English full name, or Chinese translation of an existing term needs to be revised or corrected.

### 3.2 When Not to Contribute

The situations in which contribution is not required are consistent with Section 2.1 "Terms do not include" and Rule 2 "Define as needed" in Section 5, including:

- Concepts familiar to target users do not need to be defined.
- Command names, parameter names, document names, product names, board names, version names, and brand names are not included as terms.

### 3.3 Terms Common to Multiple Products

If a term applies to multiple products, define it as a general concept rather than for a specific product (see Rule 3 "Prefer general concepts" in Section 5).

## 4. Glossary Structure and Format Requirements

The glossary ([`glossary.md`](https://gitcode.com/cann/docs/blob/master/docs/en/common-ref/glossary.md)) uses a structure in which terms are grouped into sections by the initial letter and presented in tables, with each term occupying one row in a table. Strictly follow the following format requirements when contributing.

### 4.1 Overall Structure

1. Group entries into sections by the first letter of the term, with section headings in the format `## A`, `## B`, `## C` ... `## Z`, covering all letters from A to Z.
2. Place a table under each section, containing the following header columns:
   - **Term/Abbreviation** (first column)
   - **Meaning** (second column)
   - **Field** (third column)

### 4.2 Meaning of Header Columns

<table style="font-size:14px">
<thead align="left">
<tr>
<th class="cellrowborder" valign="top" width="20%"><strong>Column Name</strong></th>
<th class="cellrowborder" valign="top" width="80%"><strong>Description</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td class="cellrowborder" valign="top" width="20%">Term/Abbreviation</td>
<td class="cellrowborder" valign="top" width="80%">The name of the term or abbreviation, which <strong>must be bold</strong>. An English abbreviation, a Chinese term, or an English full name can serve as the entry name.</td>
</tr>
<tr>
<td class="cellrowborder" valign="top" width="20%">Meaning</td>
<td class="cellrowborder" valign="top" width="80%">The meaning of the entry. For an English abbreviation, the format is "English full name, corresponding Chinese name", followed by a line break and the Chinese meaning (detailed explanation). For a Chinese term, provide the Chinese meaning directly.</td>
</tr>
<tr>
<td class="cellrowborder" valign="top" width="20%">Field</td>
<td class="cellrowborder" valign="top" width="80%">The field/component the term relates to, such as CANN, MindStudio, HDK, MindIE, and MindCluster. If the term relates to multiple fields, list them separated by <code>/</code>.</td>
</tr>
</tbody>
</table>

### 4.3 Writing Requirements for the Term/Abbreviation, Meaning, and Field Columns

#### English Abbreviation Entries

<table style="font-size:14px">
<thead align="left">
<tr>
<th class="cellrowborder" valign="top" width="20%"><strong>Term/Abbreviation</strong></th>
<th class="cellrowborder" valign="top" width="50%"><strong>Meaning</strong></th>
<th class="cellrowborder" valign="top" width="30%"><strong>Field</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td class="cellrowborder" valign="top" width="20%">English abbreviation</td>
<td class="cellrowborder" valign="top" width="50%">English full name and corresponding Chinese name. Provide the Chinese meaning after a line break (a detailed description of the concept).</td>
<td class="cellrowborder" valign="top" width="30%">The field/component the term relates to, such as CANN and MindStudio. If it relates to multiple fields, separate them with <code>/</code>.</td>
</tr>
<tr>
<td class="cellrowborder" valign="top" width="20%">English full-name entry (not an abbreviation)</td>
<td class="cellrowborder" valign="top" width="50%">Use the full English name as the entry (such as Accumulated Relative Error and Batch size). The Meaning column follows the same "English full name, corresponding Chinese name" + detailed description format.</td>
<td class="cellrowborder" valign="top" width="30%">The field/component the term relates to. If it relates to multiple fields, separate them with <code>/</code>.</td>
</tr>
</tbody>
</table>

Example:

<table style="font-size:14px">
<thead align="left">
<tr>
<th class="cellrowborder" valign="top" width="20%"><strong>Term/Abbreviation</strong></th>
<th class="cellrowborder" valign="top" width="50%"><strong>Meaning</strong></th>
<th class="cellrowborder" valign="top" width="30%"><strong>Field</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td class="cellrowborder" valign="top" width="20%"><strong>AscendCL</strong></td>
<td class="cellrowborder" valign="top" width="50%">Ascend Computing Language, the Ascend programming language.<br/>It provides C-language API libraries for Device management, Context management, Stream management, memory management, model loading and execution, operator loading and execution, and media data processing for you to develop deep neural network applications, implementing functions such as target recognition and image classification.</td>
<td class="cellrowborder" valign="top" width="30%">CANN</td>
</tr>
</tbody>
</table>

#### Chinese Term Entries

<table style="font-size:14px">
<thead align="left">
<tr>
<th class="cellrowborder" valign="top" width="20%"><strong>Term/Abbreviation</strong></th>
<th class="cellrowborder" valign="top" width="50%"><strong>Meaning</strong></th>
<th class="cellrowborder" valign="top" width="30%"><strong>Field</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td class="cellrowborder" valign="top" width="20%">Chinese term</td>
<td class="cellrowborder" valign="top" width="50%">The Chinese meaning, with a line break to provide additional details when necessary.</td>
<td class="cellrowborder" valign="top" width="30%">The field/component the term relates to, such as CANN and MindStudio. If it relates to multiple fields, separate them with <code>/</code>.</td>
</tr>
</tbody>
</table>

See Section 2.2 (definition composition examples) and Section 9 (entry examples) for examples.

### 4.4 Sorting Rules

- Sort entries in **alphabetical order**, in dictionary format, **with English entries first and Chinese entries last**.
- Place English entries into sections by their first letter (A–Z); place Chinese entries into sections by the **first letter of their pinyin** (for example, the Chinese term for single-operator comparison (pinyin starts with D) goes into Section D, network-wide comparison (pinyin starts with Z) into Section Z, and service plane (pinyin starts with Y) into Section Y).
- Within the same section, place English entries before Chinese entries, all in dictionary order.
- When an abbreviation corresponds to multiple English full names and meanings, it may appear **multiple times** in the table (one row for each), with different meanings provided separately.

See Section 9.3 for an example of an abbreviation appearing multiple times.

## 5. Term Contribution Rules

Follow the following rules when contributing or revising terms:

1. **Keep consistent with standards**: The term name must be consistent with the name used in international, national, and industry standards.
2. **Define as needed**: Whether a term in documentation needs a definition depends on the needs of target users. Concepts familiar to users do not need to be defined; concepts unfamiliar to users need to be defined (usually provided in the form of a glossary).
3. **Prefer general concepts**: If a term applies to multiple products, define it as a general concept rather than for a specific product.
4. **Use one term for one meaning**: Do not use multiple terms to refer to the same concept.
5. **Keep definitions appropriate**: The definition of a term must be appropriate, neither too broad nor too narrow.
6. **Specialize common words**: When using a common word to represent an unfamiliar concept, if the common word has a special meaning in a specific field, include it as a term and provide a definition.
7. **Define unfamiliar words**: When using an unfamiliar word to represent an unfamiliar concept, include it as a term and provide a definition.
8. **Use simple words in definitions**: When defining a term, do not use more complex or unfamiliar words in the definition.
9. **Avoid circular references**: When defining a term, avoid repeatedly referencing the term or its variants (common in English terms).
10. **Explain at first occurrence**: Provide an explanation of the meaning at the first occurrence of a term in the document body (except in titles and headers). For documents published on the [CANN Document Center](https://www.hiascend.com/en-sg/document/detail/en/CANNCommunityEdition/latest/index/index.html), when the term appears again, it can be configured in bubble form (wrap it with the `<term>term</term>` tag so that the community frontend can display it in bubble form). On the same page, it is recommended to configure the term at its first occurrence.

## 6. Abbreviation Contribution Rules

Follow the following rules when contributing or revising abbreviations:

1. **Keep consistent with standards**: The name and English full name of an abbreviation must be consistent with international, national, or industry standards. Abbreviations are usually uppercase (such as CPU and API), and capitalization follows the official writing. Do not use variant expressions (for example, the official glossary uses AI Core; do not write aicore).
2. **Expand the full name**: Expand the full name of an abbreviation, and avoid directly reusing part of the abbreviation in the English full name.
3. **Explain in the glossary**: All abbreviations that appear in the document body must be explained in the glossary.
4. **Handle multiple meanings**: When an abbreviation may correspond to multiple English full names and meanings, it is usually recommended to use the full name in all cases, or use the abbreviation for one meaning and the full names for the other meanings.
5. **Unit abbreviations**: The capitalization of unit abbreviations follows international conventions.
6. **Determine by frequency of use**:
   - For words that appear frequently or are lengthy in the documentation, you can use the abbreviation after the abbreviation is clearly explained.
   - For words that appear infrequently or are short, avoid using abbreviations to prevent confusion for readers.
   - For abbreviations that are very familiar to readers, you can directly use the abbreviation at the first occurrence without providing the English full name.
7. **Provide the full name at first occurrence**: Provide the full name at the first occurrence of an abbreviation in the document body (except in titles and headers), in the format: abbreviation (English full name, Chinese full name), with content words in the full name capitalized, using full-width parentheses, for example, CRC（Cyclic Redundancy Check，cyclic redundancy check）. For documents published on the [CANN Document Center](https://www.hiascend.com/en-sg/document/detail/en/CANNCommunityEdition/latest/index/index.html), when the abbreviation appears again, it can be configured in bubble form (wrap it with the `<term>abbreviation</term>` tag so that the community frontend can display it in bubble form). On the same page, it is recommended to configure the abbreviation at its first occurrence.
8. **Scenarios exempt from providing the full name**:
   - **Software and hardware environment requirements areas**: Tables following headings such as environment requirements, hardware requirements, software requirements, and OS and software requirements (including abbreviations in CPU, memory, hard disk, RAID card, NIC, codec card, GPU card, OS, operating system, software package names, and software package URL paths)
   - **Image names and image reference URLs**: Abbreviations in the alt (image name) and URL of the image syntax `![alt](url)`
   - **Node names or examples**: Node names containing NODE/HOST/SERVER (such as INDEX_NODE/QUERY_NODE/NODE0) and example node names
   - **Abbreviations with numeric suffixes**: Known abbreviations followed by a number (such as CPU0/NUMA0/NODE0/GPU0/PF0/VF0/DIMM0)
   - **Programming language keywords**: TRUE/FALSE/NULL/VOID/INT/RETURN/CLASS/IF/ELSE/FOR/WHILE/NEW/DELETE/TEMPLATE/NAMESPACE, and so on
   - **File format extensions**: PNG/JPG/PDF/JSON/XML/YAML/TOML, and so on
   - **Code and comment areas**: Inside fenced code blocks (wrapped by ` ``` ` or ` ~~~ `), inline code (wrapped by backticks), YAML frontmatter (wrapped by `---`), HTML comments (`<!-- -->`), and inside `<script>`/`<style>` blocks

## 7. Review and Integration Process

Term contributions take effect only after the following review and integration process:

### 7.1 Review

1. The contributor reviews the terms/abbreviations within their field.
   - Check whether the name is consistent with industry standards.
   - Check whether the format and sorting comply with the requirements of this guide.

### 7.2 Integration

1. Integrate the approved term entries into the corresponding sections of [`glossary.md`](https://gitcode.com/cann/docs/blob/master/docs/en/common-ref/glossary.md), inserting them in the correct position in alphabetical order.
2. After integration, update the documents that reference these terms, ensuring that the first occurrence in the document body provides the English full name and Chinese full name in the format defined in Rule 7 of Section 6.

## 8. Contribution Steps (Practical Guide)

1. Query the glossary [`glossary.md`](https://gitcode.com/cann/docs/blob/master/docs/en/common-ref/glossary.md): Search for the term/abbreviation in the glossary. If it is not included, confirm whether it is consistent with international, national, and industry standards.

2. Determine the need for contribution: Refer to Section 3 to confirm that the entry falls within the inclusion scope and that target users actually need a definition.

3. Draft the entry: Write the content for the new term/abbreviation according to the requirements in Sections 4, 5, and 6, ensuring that the Meaning column format is correct and the definition meets the structural requirements.

4. Submit for review: Have the new term/abbreviation reviewed and confirmed within the field (see Section 7.1 for review content and acceptance criteria).

5. Integrate to the repository: Integrate the entry into the corresponding section of [`glossary.md`](https://gitcode.com/cann/docs/blob/master/docs/en/common-ref/glossary.md) in alphabetical order, and update the first occurrence in the document body accordingly (see Section 7.2).

## 9. Entry Examples

### 9.1 English Abbreviation Entries

<table style="font-size:14px">
<thead align="left">
<tr>
<th class="cellrowborder" valign="top" width="20%"><strong>Term/Abbreviation</strong></th>
<th class="cellrowborder" valign="top" width="50%"><strong>Meaning</strong></th>
<th class="cellrowborder" valign="top" width="30%"><strong>Field</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td class="cellrowborder" valign="top" width="20%"><strong>AOE</strong></td>
<td class="cellrowborder" valign="top" width="50%">Ascend Optimization Engine, the Ascend tuning engine. It encapsulates the ATC compilation and AscendCL runtime service APIs in the tuning process, providing parallel tuning capabilities.</td>
<td class="cellrowborder" valign="top" width="30%">CANN</td>
</tr>
</tbody>
</table>

### 9.2 Chinese Term Entries

<table style="font-size:14px">
<thead align="left">
<tr>
<th class="cellrowborder" valign="top" width="20%"><strong>Term/Abbreviation</strong></th>
<th class="cellrowborder" valign="top" width="50%"><strong>Meaning</strong></th>
<th class="cellrowborder" valign="top" width="30%"><strong>Field</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td class="cellrowborder" valign="top" width="20%"><strong>single-operator comparison</strong></td>
<td class="cellrowborder" valign="top" width="50%">A type of tensor comparison in the accuracy comparison tool. It selects one or more operators involved in computation in a network model for accuracy comparison.</td>
<td class="cellrowborder" valign="top" width="30%">CANN</td>
</tr>
</tbody>
</table>

### 9.3 Entries with Multiple Meanings (an Abbreviation Appearing Multiple Times)

<table style="font-size:14px">
<thead align="left">
<tr>
<th class="cellrowborder" valign="top" width="20%"><strong>Term/Abbreviation</strong></th>
<th class="cellrowborder" valign="top" width="50%"><strong>Meaning</strong></th>
<th class="cellrowborder" valign="top" width="30%"><strong>Field</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td class="cellrowborder" valign="top" width="20%"><strong>AMP</strong></td>
<td class="cellrowborder" valign="top" width="50%">Asymmetric multiprocessing. A type of multiprocessing architecture...</td>
<td class="cellrowborder" valign="top" width="30%">General</td>
</tr>
<tr>
<td class="cellrowborder" valign="top" width="20%"><strong>AMP</strong></td>
<td class="cellrowborder" valign="top" width="50%">Automatic Mixed Precision. Mixed-precision training is a technique in deep learning that improves training speed and efficiency...</td>
<td class="cellrowborder" valign="top" width="30%">CANN</td>
</tr>
</tbody>
</table>

## 10. Self-check Checklist for Contribution

Before submission, verify each item. The checklist is grouped into "content, format, and process":

**Content quality**

- [ ] The term name is consistent with international, national, or industry standards, and the English full name and Chinese name are accurate.
- [ ] A one-sentence definition states "what it is", and the detailed definition supplements the scenarios and boundaries.
- [ ] The definition does not use more complex or unfamiliar words.
- [ ] The definition does not repeatedly reference the term or its variants.
- [ ] No subjective evaluations such as "powerful" or "efficient" are used.

**Format and structure**

- [ ] The term name is bold, and all three columns (Term/Abbreviation, Meaning, and Field) are present.
- [ ] The English abbreviation format is "English full name, corresponding Chinese name", and the in-text explanation format is "abbreviation (English full name, Chinese full name)", without mixing the two.
- [ ] Abbreviations are all uppercase, capitalization follows official writing, and no variant expressions are used.
- [ ] Terms/abbreviations configured as tooltips in the document body are wrapped with the `<term>...</term>` tag.
- [ ] When an abbreviation corresponds to multiple meanings, each meaning is listed separately or distinguished using the full name.
- [ ] The full name of the abbreviation is fully expanded and does not reuse the abbreviation itself.
- [ ] Entries are inserted into the correct sections in alphabetical order (English first, then Chinese).
- [ ] All aliases (abbreviated/full/former names) can be searched.

**Process and submission**

- [ ] Duplicate check has been performed in [`glossary.md`](https://gitcode.com/cann/docs/blob/master/docs/en/common-ref/glossary.md), confirming that the entry is not a duplicate.
- [ ] After the review passes, integrate the entry into the corresponding section of [`glossary.md`](https://gitcode.com/cann/docs/blob/master/docs/en/common-ref/glossary.md) in alphabetical order, and update the first occurrence in the document body accordingly.
