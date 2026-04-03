# Code to Text File Converter

A Python tool that scans a project folder, reads all supported text/code files, and combines them into one clean output file.

This is useful when you want to give an AI tool your full codebase in one readable export instead of uploading many individual files.

---

## What it does

This tool:

- scans a folder and its subfolders
- reads supported source/text files
- skips binary files and junk folders
- combines everything into one output file
- preserves file paths and separators so the structure stays readable

The final output is a single `.txt` file that can be used for:

- AI code review
- bug analysis
- project summarization
- documentation generation
- architecture explanations
- refactor planning
- codebase archiving

---

## Why this exists

AI tools work much better when they can see:

- multiple related files together
- shared context across the project
- frontend, backend, config, and utility files in one place
- file boundaries and file names clearly marked

Instead of manually copying dozens of files, this tool turns an entire codebase into one readable export.

---

## Main use cases

- review a full codebase with ChatGPT, Claude, Gemini, Copilot, or another AI tool
- generate a README or documentation from existing code
- summarize a project for onboarding or handoff
- scan for bugs or inconsistent logic across files
- create a context pack for AI coding assistants
- archive a project in a human-readable format

---

## Features

- combines many files into one output file
- supports recursive folder scanning
- preserves file paths in the export
- skips common junk folders like `node_modules`, `.git`, `dist`, and `build`
- skips binary files
- supports GUI versions with folder/file selection
- can be packaged into a standalone Windows `.exe`
- useful as a base for AI-agent workflows

---

## Requirements

- Python 3.9 or newer recommended

Most versions of this project only use Python standard library modules.

Common modules used:

- `os`
- `sys`
- `pathlib`
- `datetime`
- `tkinter` for GUI versions

If your version supports drag-and-drop, it may also require:

- `tkinterdnd2`

---

## Installation

### 1. Clone or download the project

```bash
git clone https://github.com/aadiossikka/Code-to-Text.git
cd 
