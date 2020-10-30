![](https://img.shields.io/github/workflow/status/samayer12/Interleave/CI) 
![](https://img.shields.io/github/languages/count/samayer12/Interleave) ![](https://img.shields.io/github/last-commit/samayer12/Interleave) 
[![codecov](https://codecov.io/gh/wemake-services/wemake-python-styleguide/branch/master/graph/badge.svg)](https://codecov.io/gh/wemake-services/wemake-python-styleguide)
[![Python Version](https://img.shields.io/pypi/pyversions/wemake-python-styleguide.svg)](https://pypi.org/project/wemake-python-styleguide/)

Messing around with Github CI and PDF processing.

This program will take two PDF files and match all paragraphs (which SHOULD be numbered) and store the matched pairs in a .csv. file.

**Example usage**
`python interleave.py file1.pdf file2.pdf output.csv`

**Example output**
```
Document1,Document2
1. First Entry.,1. First Entry
2. Second Entry.,2. Second Entry
3. Third Entry,3. Third Entry
```
