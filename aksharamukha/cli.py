#! /usr/bin/env/ python3

import argparse
import sys
import warnings
from collections.abc import Generator
from typing import Callable, Optional, TextIO
from zipfile import BadZipFile

from aksharamukha import GeneralMap, transliterate

STDIN_ARG = "-"
DEFAULT_SRC = "autodetect"
DEFAULT_TGT = {
    "default": "IAST",
    "script_code": "Latn-IAST",
    "lang_code": "la",
    "lang_name": "Latin",
}
TABLE_INDENT = 2
DOC_SITE="https://www.aksharamukha.com"
FILE_MODE_SUF = (".txt", ".html", ".docx",)

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=("Askh desck"),
        epilog=(
            "For supported scripts, pre- and post-options visit the page "
            f"{DOC_SITE}/documentation"
        )
    )
    parser.add_argument(
        "FILE",
        type=str,
        nargs="?",
        help=(
            "Plain text file to transliterate, "
            " encoding expected to be default for platform, "
            f"`{STDIN_ARG}` to read stdin (by default)"
        )
    )
    parser.add_argument(
        "-d", "--detect",
        action="store_true",
        help=(
            "Try to autodetect the input script and exit, "
            "respects `FILE` arg only. "
            "Reads all input at once!"
        )
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Write to file instead of stdout",
    )
    parser.add_argument(
        "-s", "--src",
        type=str,
        default=DEFAULT_SRC,
        help=(
            "The script to transliterate from. "
            f"`{DEFAULT_SRC}` by default. "
            "Be carefule, autodetection works for every line."
        )
    )
    parser.add_argument(
        "-t", "--tgt",
        type=str,
        help=(
            "Script to transliterate to. "
            f"`{DEFAULT_TGT['default']}` by default."
        )
    )
    parser.add_argument(
        "-l", "--list-scripts",
        action="store_true",
        help="List known scripts and exit discarding other flags",
    )
    parser.add_argument(
        "-n", "--not-nativize",
        action="store_true",
        help="Do not ask to input, use defaults",
    )
    parser.add_argument(
        "-p", "--param",
        choices=("default", "script_code", "lang_code", "lang_name",),
        default="default",
        help=f"Visit {DOC_SITE}/python for usage",
    )
    parser.add_argument(
        "--pre", "--pre-options",
        nargs="*",
        default=[],
        type=str,
        help="Source script specific parameters. Space separated values.",
    )
    parser.add_argument(
        "--post", "--post-options",
        nargs="*",
        default=[],
        type=str,
        help="Target script specific parameters. Space separated values.",
    )
    parser.add_argument(
        "--file-mode",
        action="store_true",
        help="Convert txt, HTML or docx file rather than write to stdout.",
    )

    return validate_args(parser.parse_args())


def validate_args(args: argparse.Namespace) -> argparse.Namespace:
    if args.FILE is None:
        args.FILE = STDIN_ARG

    if args.tgt is None:
        args.tgt = DEFAULT_TGT[args.param]

    if args.src == "autodetect" and args.pre:
        error("`--pre_options` are ignored with `--src=autodetect`")

    if args.file_mode:
        if not any([args.FILE.endswith(suf) for suf in FILE_MODE_SUF]):
            fmts_str = ", ".join(f"`*.{s}`" for s in FILE_MODE_SUF)
            error(f"`--file-mode` supports {fmts_str} files only")
        if args.output is not None:
            error("`--file-mode` does not support `--output` flag")
        if args.param != "default":
            error("`--file-mode` does not support `--param` options")

    return args


def error(text: str, *, before_line=True) -> None:
    if before_line:
        print(file=sys.stderr)
    print(text, file=sys.stderr)
    print("Exiting on error", file=sys.stderr)
    print(file=sys.stderr)
    sys.exit(1)


def open_file(file: str, mode: str) -> TextIO:
    """ Returns stream which should be closed after reading """
    try:
        return open(file=file, mode=mode)
    except OSError as err:
        error(str(err))

def read_lines(file) -> Generator:
    if file == STDIN_ARG:
        for line in sys.stdin:
            yield line
    else:
        stream = open_file(file=file, mode="r")
        for line in stream:
            yield line
        stream.close()


class Output:
    def __init__(self, file: Optional[str]) -> None:
        self.file = file
        self.stream = sys.stdout

    def __enter__(self) -> "Output":
        if self.file is not None:
            self.stream = open_file(self.file, "w")
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.file is not None:
            self.stream.close()

    def __call__(self, line: str) -> None:
        print(line, end="", file=self.stream)


class WarnDetector:
    """ Wrap showwarning function to check was it any warning """
    def __init__(self, showwarning: Callable) -> None:
        self.orig = showwarning
        self.is_warned = False

    def __call__(self, message, category, filename, lineno, file=None, line=None) -> None:
        self.is_warned = True
        self.orig(
            message=message, category=category,
            filename=filename, lineno=lineno,
            file=file, line=line
        )

    def __bool__(self) -> bool:
        return self.is_warned


def list_scripts(param: str = "") -> None:
    indic_scr = sorted(GeneralMap.IndicScripts)
    non_indic_scr = sorted(GeneralMap.LatinScripts)
    print()
    print("Indic scripts:")
    for s in indic_scr:
        print(f"  - {s}")
    print()
    print("Non-Indic scripts:")
    for s in non_indic_scr:
        print(f"  - {s}")
    print()


def detect(file: str) -> None:
    lines = list(read_lines(file))
    data = "\n".join(lines)
    if not data.strip():
        error("No data to detect")
    res = transliterate.auto_detect(data)
    print()
    print(f"Detected script: {res}")
    print()
    return


def process(args: argparse.Namespace) -> None:
    # warn stop and exit 1
    with Output(args.output) as out:
        for line in read_lines(args.FILE):
            res = transliterate.process(
                src=args.src, tgt=args.tgt,
                txt=line,
                nativize=not args.not_nativize,
                pre_options=args.pre,
                post_options=args.post,
                param=args.param,
            )
            out(res)


def process_file(args: argparse.Namespace) -> None:
    print()
    try:
        from aksharamukha import GeneralMap, transliterate, transliterate_file  # noqa: F401
    except ImportError:
        error("Import error, try to install with group: `pip install aksharamukha[transliterate_file]`")

    try:
        transliterate_file.process(
            src=args.src, tgt=args.tgt,
            file=args.FILE,
            nativize=not args.not_nativize,
            pre_options=args.pre,
            post_options=args.post
        )
    except BadZipFile:
        error("File does not look like a correct docx", before_line=False)
    except OSError as err:
        error(err, before_line=False)
    print()


def main() -> None:
    warned = WarnDetector(warnings.showwarning)
    warnings.showwarning = warned
    args = get_args()
    if args.list_scripts:
        list_scripts()
    elif args.detect:
        detect(args.FILE)
    elif args.file_mode:
        process_file(args)
    else:
        process(args)
    if warned:
        error('Processed with warning(s)')


if __name__ == "__main__":
    main()
