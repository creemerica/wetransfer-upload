# wetransfer-upload
[![PyPI version](https://badge.fury.io/py/wetransfer-upload.svg)](https://badge.fury.io/py/wetransfer-upload)
[![PyPI license](https://img.shields.io/pypi/l/wetransfer-upload.svg)](https://img.shields.io/pypi/l/wetransfer-upload.svg)

Upload files or directories to WeTransfer. Tie into your Bitly account to create custom short urls for your downloads. Inspired by [upload-wetransfer](https://github.com/kraynel/upload-wetransfer) by [kraynel](https://github.com/kraynel).

## Feautures

- Upload files or directories of files
- Create custom bitly link for upload
- Show progress of upload

## Installation

`$ pip install wetransfer-upload`

## Usage

```python
from wetransfer import WeTransfer

wt = WeTransfer()
upload = wt.start('file.txt')
print upload
```
