#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os
import sys
import argparse


def create_arg_parser():
    parser = argparse.ArgumentParser(
        description='删除 Markdown 中特定 NPU 的条件内容块',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python remove_npu_content.py D:\\docs\\user_guides
  python remove_npu_content.py /path/to/docs --npu 310p
  python remove_npu_content.py /path/to/docs --npu A3
"""
    )
    parser.add_argument('target_dir', help='要处理的目录路径')
    parser.add_argument('--npu', default='IPV350', help='要删除的 NPU 名称（默认: IPV350）')
    return parser


OPENER = re.compile(r'<!--\s*npu="([^"]*)"\s+(id\d+)\s*-->')
CLOSER = re.compile(r'<!--\s*end\s+(id\d+)\s*-->')


def process_file(filepath, content, use_crlf, target_npu):
    lines = content.replace('\r\n', '\n').split('\n')
    original_lines = list(lines)

    for _ in range(20):
        prev = list(lines)
        lines = remove_inner_target_only(lines, target_npu)
        lines = remove_target_from_mixed(lines, target_npu)
        lines = remove_standalone_target_only(lines, target_npu)
        if lines == prev:
            break

    lines = collapse_blank_lines(lines)
    if lines == original_lines:
        return False

    new_content = '\n'.join(lines)
    if use_crlf:
        new_content = new_content.replace('\n', '\r\n')
    try:
        with open(filepath, 'wb') as f:
            f.write(new_content.encode('utf-8'))
    except OSError:
        return None
    return True


def remove_inner_target_only(lines, target_npu):
    result = []
    depth = 0
    target_open_depth = 0
    target_skip = False
    for line in lines:
        stripped = line.strip()
        m_open = OPENER.match(stripped)
        m_close = CLOSER.match(stripped)

        if m_open:
            npus = [n.strip() for n in m_open.group(1).split(',')]
            if depth > 0 and not target_skip and npus == [target_npu]:
                target_open_depth = depth
                target_skip = True
                depth += 1
                continue
            result.append(line)
            depth += 1
        elif m_close:
            if target_skip and depth == target_open_depth + 1:
                target_skip = False
                target_open_depth = 0
                depth -= 1
                continue
            depth -= 1
            result.append(line)
        else:
            if target_skip:
                continue
            result.append(line)
    return result


def remove_target_from_mixed(lines, target_npu):
    result = []
    for line in lines:
        m = OPENER.match(line.strip())
        if m:
            npus = [n.strip() for n in m.group(1).split(',')]
            if target_npu in npus and len(npus) > 1:
                npus.remove(target_npu)
                new_npus = ','.join(npus)
                line = re.sub(r'npu="[^"]*"', f'npu="{new_npus}"', line, count=1)
        result.append(line)
    return result


def remove_standalone_target_only(lines, target_npu):
    result = []
    i = 0
    while i < len(lines):
        m_open = OPENER.match(lines[i].strip())
        if m_open and [n.strip() for n in m_open.group(1).split(',')] == [target_npu]:
            block_id = m_open.group(2)
            j = i + 1
            depth = 1
            while j < len(lines):
                sj = lines[j].strip()
                if OPENER.match(sj) and OPENER.match(sj).group(2) == block_id:
                    depth += 1
                elif CLOSER.match(sj) and CLOSER.match(sj).group(1) == block_id:
                    depth -= 1
                    if depth == 0:
                        i = j + 1
                        break
                j += 1
            else:
                result.append(lines[i])
                i += 1
            continue
        result.append(lines[i])
        i += 1
    return result


def collapse_blank_lines(lines):
    result = []
    for line in lines:
        if line.strip() == '' and result and result[-1].strip() == '':
            continue
        result.append(line)
    while result and result[-1].strip() == '':
        result.pop()
    result.append('')
    return result


if __name__ == '__main__':
    parser = create_arg_parser()
    args = parser.parse_args()

    base_dir = args.target_dir
    target_npu = args.npu

    if not os.path.isdir(base_dir):
        print(f"错误：目录不存在: {base_dir}")
        sys.exit(1)

    print(f"目标目录: {base_dir}")
    print(f"目标 NPU: {target_npu}")
    print()

    modified_count = 0
    skipped_count = 0
    for dirpath, dirnames, filenames in os.walk(base_dir):
        for filename in sorted(filenames):
            if not filename.endswith('.md'):
                continue
            filepath = os.path.join(dirpath, filename)
            relpath = os.path.relpath(filepath, base_dir)
            try:
                with open(filepath, 'rb') as f:
                    raw = f.read()
            except OSError as e:
                print(f"  SKIPPED (读取失败: {e}): {relpath}")
                skipped_count += 1
                continue
            if target_npu.encode() not in raw:
                continue
            try:
                content = raw.decode('utf-8')
            except UnicodeDecodeError:
                print(f"  SKIPPED (非 UTF-8 编码): {relpath}")
                skipped_count += 1
                continue
            result = process_file(filepath, content, b'\r\n' in raw, target_npu)
            if result is None:
                print(f"  SKIPPED (写入失败): {relpath}")
                skipped_count += 1
            elif result:
                print(f"  MODIFIED: {relpath}")
                modified_count += 1
            else:
                print(f"  no change:  {relpath}")

    summary = f"\n{modified_count} files modified"
    if skipped_count:
        summary += f", {skipped_count} files skipped"
    print(summary)
