"""Rebuilds pyodide/fonttools-4.51.0-py3-none-any.whl as a trimmed wheel.

The real PyPI fonttools wheel is ~4.1MB (ttLib, varLib, feaLib, subset,
pens, ...). This project only ever does `from fontTools import unicodedata
as ucd` (in aksharamukha/gimeltra.py, for Semitic-script handling) - none
of the font-file-parsing machinery is imported anywhere. This script keeps
only that submodule's actual transitive closure - fontTools/__init__.py,
fontTools/misc/__init__.py, fontTools/misc/loggingTools.py,
fontTools/misc/textTools.py, and fontTools/unicodedata/* - shrinking the
wheel to ~108KB. Verified byte-identical conversion output against the
full wheel for Hebrew/Arabic/Devanagari round trips before this was first
adopted (see README.md's "Size optimizations" section).

Re-run this if fonttools is upgraded or if gimeltra.py's fontTools usage
ever grows beyond `unicodedata` - it will need `keep` extended to match.

Usage: python build_trimmed_fonttools.py [version]
"""

import sys
import os
import json
import zipfile
import hashlib
import base64
import urllib.request

VERSION = sys.argv[1] if len(sys.argv) > 1 else '4.51.0'
WHEEL_NAME = f'fonttools-{VERSION}-py3-none-any.whl'
DIST_INFO = f'fonttools-{VERSION}.dist-info'
OUT_PATH = os.path.join('pyodide', WHEEL_NAME)


def _download_url():
    # Looked up via PyPI's JSON API rather than guessed - file URLs are
    # content-hash-based paths that can't be constructed from the wheel
    # name alone.
    with urllib.request.urlopen(f'https://pypi.org/pypi/fonttools/{VERSION}/json') as resp:
        info = json.load(resp)
    for f in info['urls']:
        if f['filename'] == WHEEL_NAME:
            return f['url']
    raise SystemExit(f'{WHEEL_NAME} not found in PyPI release {VERSION}')

KEEP = [
    'fontTools/__init__.py',
    'fontTools/misc/__init__.py',
    'fontTools/misc/loggingTools.py',
    'fontTools/misc/textTools.py',
    'fontTools/unicodedata/__init__.py',
    'fontTools/unicodedata/Blocks.py',
    'fontTools/unicodedata/OTTags.py',
    'fontTools/unicodedata/ScriptExtensions.py',
    'fontTools/unicodedata/Scripts.py',
]


def digest(data):
    h = hashlib.sha256(data).digest()
    return 'sha256=' + base64.urlsafe_b64encode(h).decode().rstrip('=')


def main():
    src_path = 'fonttools-full.whl.tmp'
    print(f'Fetching original {WHEEL_NAME} from PyPI...')
    urllib.request.urlretrieve(_download_url(), src_path)

    src = zipfile.ZipFile(src_path)
    orig_metadata = src.read(f'{DIST_INFO}/METADATA').decode()

    record_lines = []
    with zipfile.ZipFile(OUT_PATH, 'w', zipfile.ZIP_DEFLATED) as out:
        for name in KEEP:
            data = src.read(name)
            out.writestr(name, data)
            record_lines.append(f'{name},{digest(data)},{len(data)}')

        wheel_meta = (
            'Wheel-Version: 1.0\n'
            'Generator: trimmed-for-aksharamukha-wasm\n'
            'Root-Is-Purelib: true\n'
            'Tag: py3-none-any\n'
        )
        out.writestr(f'{DIST_INFO}/WHEEL', wheel_meta)
        record_lines.append(f'{DIST_INFO}/WHEEL,{digest(wheel_meta.encode())},{len(wheel_meta)}')

        out.writestr(f'{DIST_INFO}/METADATA', orig_metadata)
        record_lines.append(f'{DIST_INFO}/METADATA,{digest(orig_metadata.encode())},{len(orig_metadata.encode())}')

        record_lines.append(f'{DIST_INFO}/RECORD,,')
        out.writestr(f'{DIST_INFO}/RECORD', '\n'.join(record_lines) + '\n')

    src.close()
    os.remove(src_path)

    print(f'Wrote {OUT_PATH}: {os.path.getsize(OUT_PATH)} bytes')


if __name__ == '__main__':
    main()
