# -*- coding: utf-8 -*-
"""
Forcing function for documentation coverage: every Fix/pre-option/
post-option function in ConvertFix.py, PreProcess.py, PostProcess.py, and
every ScriptProcessing/<Script>.py file must carry a one-line docstring.
Add a new option or a new per-script Fix function without documenting it,
and this test fails - that's the point (see aksharamukha/DOCS_NEEDING_REVIEW.md
for how the initial pass of 753 docstrings was sourced/drafted).
"""
import ast
import io
import os

AKSHARAMUKHA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def _files_requiring_docstrings():
    files = [
        os.path.join(AKSHARAMUKHA_DIR, 'ConvertFix.py'),
        os.path.join(AKSHARAMUKHA_DIR, 'PreProcess.py'),
        os.path.join(AKSHARAMUKHA_DIR, 'PostProcess.py'),
    ]
    sp_dir = os.path.join(AKSHARAMUKHA_DIR, 'ScriptProcessing')
    for fname in sorted(os.listdir(sp_dir)):
        if fname.endswith('.py') and fname != '__init__.py':
            files.append(os.path.join(sp_dir, fname))
    return files


def _undocumented_functions():
    missing = []
    for path in _files_requiring_docstrings():
        with io.open(path, encoding='utf-8') as f:
            src = f.read()
        tree = ast.parse(src)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and ast.get_docstring(node) is None:
                rel = os.path.relpath(path, AKSHARAMUKHA_DIR)
                missing.append('%s::%s (line %d)' % (rel, node.name, node.lineno))
    return missing


def test_all_fix_and_option_functions_have_docstrings():
    missing = _undocumented_functions()
    assert not missing, (
        "%d function(s) are missing a docstring. Every Fix/pre-option/"
        "post-option function in ConvertFix.py, PreProcess.py, PostProcess.py, "
        "and ScriptProcessing/*.py must have a one-line docstring:\n%s"
        % (len(missing), '\n'.join(missing))
    )
