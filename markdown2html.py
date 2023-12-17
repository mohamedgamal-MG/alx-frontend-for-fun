#!/usr/bin/python3
import sys
import pathlib
import re
import hashlib

def convert_md_to_html(input_file, output_file):
    with open(input_file, encoding='utf-8') as f:
        md_content = f.readlines()

    html_content = []
    in_list = False

    for line in md_content:
        # Check if the line is a heading
        heading_match = re.match(r'^\s*#{1,6}\s+(.*)', line)
        if heading_match:
            h_level = min(6, len(heading_match.group(0).strip()))
            h_content = heading_match.group(1).strip()
            html_content.append(f'<h{h_level}>{h_content}</h{h_level}>\n')
        elif line.startswith('- '):
            if not in_list:
                in_list = True
                html_content.append('<ul>\n')
            html_content.append(f'<li>{line[2:].strip()}</li>\n')
        elif line.startswith('* '):
            if not in_list:
                in_list = True
                html_content.append('<ol>\n')
            html_content.append(f'<li>{line[2:].strip()}</li>\n')
        elif re.match(r'^\s*$', line):
            if in_list:
                in_list = False
                html_content.append('</ul>\n' if line.startswith('- ') else '</ol>\n')
            else:
                html_content.append('<p>\n')
        else:
            # Check for bold and emphasis
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)

            # Check for custom syntax
            line = re.sub(r'\[\[(.*?)\]\]', lambda x: hashlib.md5(x.group(1).encode('utf-8')).hexdigest(), line)
            line = re.sub(r'\(\((.*?)\)\)', lambda x: x.group(1).replace('c', ''), line)

            html_content.append(f'{line.rstrip()}<br/>\n')

    # Write the HTML content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(html_content)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py [input_file] [output_file]", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not pathlib.Path(input_file).is_file():
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    convert_md_to_html(input_file, output_file)
    sys.exit(0)
