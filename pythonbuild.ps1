(Get-Content .\setup.py).replace('@@@', $args[0]) | Set-Content .\setup.py

python setup.py sdist bdist_wheel

python -m twine upload -u $args[1] -p $args[2] dist/*

(Get-Content .\setup.py).replace( $args[0], '@@@') | Set-Content .\setup.py

python setup.py clean --all

### How to Run
### ./pythonbuild.ps1 versionnumber pip-username pip-password