from aksharamukha.transliterate import convert
import io
from lxml import etree
from zipfile import ZipFile

MS_WORD_TEXT_SCHEMA = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"


def convert_docx(src, tgt, file, nativize=True, pre_options=[], post_options=[], is_api_mode=False):
    conversion_data = {
        'source': src,
        'target': tgt,
        'nativize': nativize,
        'pre_options': pre_options,
        'post_options': post_options
    }

    new_zip = io.BytesIO()

    with ZipFile(file, 'r') as old_archive:
        with ZipFile(new_zip, 'w') as new_archive:
            parse_content(conversion_data, old_archive, new_archive)

    file = flush_zip_to_file(file, new_zip, is_api_mode)

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


def flush_zip_to_file(file, zip, is_api_mode):
    if is_api_mode:
        # in-memory stream
        file = io.BytesIO(zip.getvalue())
        return file
    else:
        # path
        with open(file, 'wb') as f:
            f.write(zip.getvalue())