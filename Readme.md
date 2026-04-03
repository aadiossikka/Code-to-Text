# Code to Text File Converter

A simple Python tool that reads all code files inside a project folder and combines them into one clean text file. This makes it easier to feed your codebase into AI agents for review, debugging, planning, documentation, or refactoring.

## What this tool does

This script:

- scans a folder and its subfolders
- reads supported code/text files
- combines their contents into a single output text file
- keeps file names and structure clear so an AI agent can understand where each piece of code came from

It is useful when you want to give an AI a full codebase in one file instead of uploading many separate files.

## Why use it

AI tools often work better when they can see:

- the full project structure
- multiple related files together
- context across frontend, backend, config, and utility files

This tool helps turn a whole codebase into one readable text file that can be pasted into ChatGPT, Claude, Gemini, Copilot, or other AI tools.

## Example use cases

- ask an AI to review your whole codebase
- generate documentation from existing code
- summarize a project
- find bugs across multiple files
- prepare a context file for Copilot or another coding assistant
- archive code into a human-readable text format

## Requirements

You need Python installed.

Recommended version:

- Python 3.9 or newer

## Python modules needed

Most versions of this tool only need Python standard library modules, such as:

- `os`
- `pathlib`
- `tkinter` (only if using a GUI version)
- `fnmatch`
- `sys`

If your version uses a graphical file picker, then `tkinter` is required.

## Important note about tkinter

If you are using a GUI version with folder/file selection and see an error like:

`ModuleNotFoundError: No module named '_tkinter'`

that means your Python installation does not include Tkinter.

### On Windows

Tkinter usually comes with the normal Python installer from the official Python website.

### On macOS

If you installed Python with Homebrew, Tkinter may not be included by default. You may need a Python version that includes Tcl/Tk support.

## How to run it

Open Command Prompt or PowerShell in the project folder and run:

```bash
python your_script_name.py
