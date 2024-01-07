from aksharamukha.transliterate import convert
import io
import os
from lxml import etree
from zipfile import ZipFile
from bs4 import BeautifulSoup
import warnings

MS_WORD_TEXT_SCHEMA = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"

def process(src, tgt, file, nativize=True, pre_options=[], post_options=[], is_api_mode=False):
    if os.path.isfile(file):
        if '.txt' in file:
            convert_txt(src, tgt, file, nativize, pre_options, post_options, is_api_mode)
        elif '.docx' in file:
            convert_docx(src, tgt, file, nativize, pre_options, post_options, is_api_mode)
        elif '.htm' in file:
            convert_html(src, tgt, file, nativize, pre_options, post_options, is_api_mode)
        else:
            warnings.warn('Only .txt, .html, .docx formats are supported for file conversion. Input file not processed.')
    else:
        warnings.warn('Not a file. Please pass a file as an argument')

def convert_txt(src, tgt, file, nativize=True, pre_options=[], post_options=[], is_api_mode=False):
    with open(file, 'r', encoding='utf8') as f:
        txt = f.read()

    file_parts = os.path.splitext(file)
    new_file = file_parts[0] + '_' + src + tgt + file_parts[1]

    with open(new_file, 'w', encoding='utf8') as f:
        f.write(convert(src, tgt, txt, nativize, pre_options, post_options))

    print('The following file has been created: ' + new_file)

def convert_html(src, tgt, file, nativize=True, pre_options=[], post_options=[], is_api_mode=False):
    if is_api_mode:
        html = file
    else:
        with open(file, 'r', encoding='utf8') as f:
            html = f.read()

    soup = BeautifulSoup(html)

    for node in soup.findAll(text=True):
        new_node = node.replace(node.string, convert(src, tgt, node.string, nativize, pre_options, post_options))
        node.replace_with(new_node)

    if is_api_mode:
        return soup.prettify()
    else:
        file_parts = os.path.splitext(file)
        new_file = file_parts[0] + '_' + src + tgt + file_parts[1]

        with open(new_file, 'w', encoding='utf8') as f:
            f.write(soup.prettify())

        print('The following file has been created: ' + new_file)

def convert_docx(src, tgt, file, nativize=True, pre_options=[], post_options=[], is_api_mode=False):
    conversion_data = {
        'source': src,
        'target': tgt,
        'nativize': nativize,
        'pre_options': pre_options,
        'post_options': post_options
    }

    new_zip = io.BytesIO()

    if is_api_mode:
        import re
        from io import BytesIO
        from base64 import b64decode
        file = BytesIO(b64decode(file))

    with ZipFile(file, 'r') as old_archive:
        with ZipFile(new_zip, 'w') as new_archive:
            parse_content(conversion_data, old_archive, new_archive)

    file = flush_zip_to_file(file, new_zip, is_api_mode, src, tgt)

    return file


def parse_content(data, old_archive, new_archive):
    for item in old_archive.filelist:
        if item.filename.startswith('word/') and item.filename.endswith('.xml'):
            xml_file_to_convert(data, old_archive, new_archive, item)
        else:
            new_archive.writestr(item, old_archive.read(item.filename))


def xml_file_to_convert(data, old_archive, new_archive, item):
    with old_archive.open(item, 'r') as xml_file:
        tree = etree.parse(xml_file)
        for element in tree.getroot().iter():
            if element.tag == MS_WORD_TEXT_SCHEMA:
                element.text = convert(data['source'],
                                       data['target'],
                                       element.text,
                                       data['nativize'],
                                       data['post_options'],
                                       data['pre_options'])

        string = etree.tostring(tree.getroot(),
                                xml_declaration=True,
                                encoding="UTF-8",
                                standalone=True)

        new_archive.writestr(item, string)


def flush_zip_to_file(file, zip, is_api_mode, src, tgt):
    if is_api_mode:
        # in-memory stream
        file = io.BytesIO(zip.getvalue())
        return file
    else:
        # path
        file_parts = os.path.splitext(file)
        new_file = file_parts[0] + '_' + src + '_' + tgt + file_parts[1]

        with open(new_file, 'wb') as f:
            f.write(zip.getvalue())

        print('The following file has been created: ' + new_file)
