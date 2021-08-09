# LC3_asm

[![CodeFactor](https://www.codefactor.io/repository/github/d0rj/lc3_asm/badge)](https://www.codefactor.io/repository/github/d0rj/lc3_asm)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/de6a83d6b5d347bc8bb4b1aab31dab32)](https://app.codacy.com/gh/d0rj/LC3_asm?utm_source=github.com&utm_medium=referral&utm_content=d0rj/LC3_asm&utm_campaign=Badge_Grade_Settings)
[![DeepSource](https://deepsource.io/gh/d0rj/LC3_asm.svg/?label=active+issues&show_trend=true&token=3t4Dx4wWstyjQ9XcNnJOS_s6)](https://deepsource.io/gh/d0rj/LC3_asm/?ref=repository-badge)

[![Pytest](https://github.com/d0rj/LC3_asm/actions/workflows/pytest.yaml/badge.svg)](https://github.com/d0rj/LC3_asm/actions/workflows/pytest.yaml)
[![PyPI Upload](https://github.com/d0rj/LC3_asm/actions/workflows/pypi-publish.yml/badge.svg)](https://pypi.org/project/lc3asm/)

## Overview

⚠ WIP - it has some 🪲🪲 ⚠

Simple asssembler for LC3 virtual machine. You can see my own realization of VM [there](https://github.com/d0rj/LC3_vm) or try good [online simulator](https://wchargin.com/lc3web/).

## How to use

### Copy

```bash
git clone https://github.com/d0rj/LC3_asm.git
cd LC3_asm
```

### Install dependencies

```bash
python -m pip install --upgrade pip
pip install . --use-feature=in-tree-build
```

### Run tests

```bash
pip install pytest
python -m pytest
```

### Start assembler

```bash
python main.py -p "./examples/hello_world.asm" -o "./output/my_assambled_programm.bin"
```

**\-p / --path** - path to assembly programm source file.

**\-o / --out** - path for output binary file.

## Currently not supported

- **.BLKW** pseudo-operation
- **BR\*** operation and sub-operations (*bug*)
- Advanced label declaration with address etc.

## Resources

- [Some example of assembly language (Jupyter notebook)](https://jupyter.brynmawr.edu/services/public/dblank/CS240%20Computer%20Organization/2015-Fall/Notes/LC3%20Assembly%20Language.ipynb)
- [Doc file](http://people.cs.georgetown.edu/~squier/Teaching/HardwareFundamentals/LC3-trunk/docs/LC3-AssemblyManualAndExamples.pdf)
