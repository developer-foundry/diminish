sphinx-apidoc -o Sphinx-docs . sphinx-apidoc --full -A 'Eric LaForce\nKeith LaForce';
cd Sphinx-docs;
echo "\nimport os
import sys
sys.path.insert(0,os.path.abspath('../'))
def skip(app, what, name, obj,would_skip, options):
    if name in ( '__init__',):
        return False
    return would_skip
def setup(app):
    app.connect('autodoc-skip-member', skip)
" >> conf.py;
make markdown;
cd ..
cat Sphinx-docs/_build/markdown/*.md >> docs/InternalCodeDocumentation.md;
rm -r Sphinx-docs;