# Code to Text File Converter

A simple Python tool that reads all code files inside a project folder
and combines them into one clean text file. This makes it easier to feed
your codebase into AI agents for review, debugging, planning,
documentation, or refactoring.

## What this tool does

This script:

-   scans a folder and its subfolders
-   reads supported code/text files
-   combines their contents into a single output text file
-   keeps file names and structure clear so an AI agent can understand
    where each piece of code came from

It is useful when you want to give an AI a full codebase in one file
instead of uploading many separate files.

## Why use it

AI tools often work better when they can see:

-   the full project structure
-   multiple related files together
-   context across frontend, backend, config, and utility files

## Requirements

-   Python 3.9+

## How to run

``` bash
python anycode_to_textfile.py
```

## Convert to EXE

``` bash
pip install pyinstaller
pyinstaller --onefile anycode_to_textfile.py
```

Executable will be inside the dist folder.

## Disclaimer

Remove sensitive data before sharing with AI tools.
