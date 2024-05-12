(Get-Content .\setup.py).replace('@@@', $args[0]) | Set-Content .\setup.py

python setup.py sdist bdist_wheel

python -m twine upload -u __token__ -p replace_token_here dist/*

python setup.py clean --all

### How to Run
### ./pythonbuild.ps1 versionnumber