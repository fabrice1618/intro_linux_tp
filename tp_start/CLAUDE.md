# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a progressive Linux command-line tutorial (TP - "Travaux Pratiques") designed for beginners learning basic Linux commands. The repository provides a self-paced, guided, and automatically-verified learning experience covering file system manipulation, searching, filtering, archiving, links, variables, and process management.

**Language**: French (all instructions and verification messages are in French)

## Architecture

### Core Components

- **setup.sh**: Initialization script that creates the practice environment
  - Creates `data/` directory with sample files (lorem.txt, fruits.txt, sample.csv, logs/app.log)
  - Creates `workspace/` directory structure (docs/, data/, tmp/) for student work
  - Must be run before starting exercises

- **verify.py**: Automated verification system (Python 3)
  - Validates each step's completion by checking expected files/directories/states
  - Includes QCM (multiple choice quiz) questions to reinforce learning
  - 10 verification functions (`step1()` through `step10()`) corresponding to exercises
  - Uses colored terminal output (GREEN/RED/YELLOW/CYAN) for feedback

- **readme.md**: Complete tutorial with 10 progressive exercises
  - Each step includes: concept introduction, tasks, hints for finding commands via `man`, validation instructions, and 5 QCM questions
  - No `sudo` required; all work happens in user's home directory

### Directory Structure

```
.
├── data/                    # Initial data files (read-only source material)
│   ├── fruits.txt          # Sample text file with fruit names
│   ├── lorem.txt           # Lorem ipsum text for practice
│   ├── sample.csv          # CSV file for column extraction practice
│   └── logs/app.log        # Log file for filtering practice
├── workspace/              # Student working directory (created by setup.sh)
│   ├── docs/               # For document creation exercises
│   ├── data/               # For data manipulation exercises
│   └── tmp/                # For temporary files and extraction
├── setup.sh                # Environment setup script
├── verify.py               # Automated verification and quiz system
└── readme.md               # Complete tutorial instructions
```

## Common Commands

### Setup and Verification

```bash
# Initialize the practice environment (REQUIRED FIRST STEP)
bash setup.sh

# Verify a specific step (with quiz)
python3 verify.py --step N

# Verify without quiz questions
python3 verify.py --step N --no-quiz

# Verify all steps (1-10)
python3 verify.py --all

# Auto-answer quiz with specific choice
python3 verify.py --step N --answer B
```

### Verification System Details

- Exit code 0 = success, 2 = failure
- QCM questions are randomly selected from a bank for each step
- Step 8 verification is tolerant (environment variables/aliases are shell-specific)
- Verification checks concrete results (files, permissions, symlinks) not command history

## Tutorial Steps (10 Exercises)

1. **Navigation**: pwd, ls, $HOME, $PWD
2. **File/Directory Creation**: mkdir, touch, echo, redirection (>, >>)
3. **Copy/Move/Delete**: cp -R, mv, rm, rmdir
4. **Search**: find, grep, which, type
5. **Filters/Pipes**: head, tail, sort, uniq, wc, tr, cut
6. **Archive/Compress**: tar (create, list, extract with gzip)
7. **Symlinks/Permissions**: ln -s, chmod (octal notation)
8. **Environment/Aliases**: export, alias, $MYVAR
9. **Processes**: ps, pgrep, pkill, df, background jobs (&)
10. **Help/History**: man, --help, history, date, cal

## Implementation Notes

### When Modifying verify.py

- Each step function must return `True` (passed) or `False` (failed)
- File existence checks use `Path` objects from `pathlib`
- `run()` helper executes shell commands with captured output
- `file_has_lines(path, min_lines)` validates minimum line count
- QCM bank in `QCM` dictionary maps step number to list of (question, options, correct_answer)

### Expected Student Work Products

Verification looks for specific files created by students:

- Step 2: `workspace/data/todo.txt`, `workspace/tmp/.cache`, `workspace/docs/bonjour.txt` (≥2 lines)
- Step 3: `workspace/backup_data/` (recursive copy), `workspace/bonjour.renomme.txt`, `workspace/docs/bonjour.txt` (deleted)
- Step 5: `workspace/data/fruits_uniques.txt`, `lorem_wc.txt`, `fruits_upper.txt`, `col2.txt`
- Step 6: `workspace/data_archive.tgz`, extracted `workspace/tmp/data/fruits.txt`
- Step 7: `workspace/data/link_fruits.txt` (symlink), `fruits_uniques.txt` with mode 640

### Constraints and Philosophy

- **No sudo**: All operations within user's home directory
- **Discovery-based learning**: Instructions provide hints, not exact commands
- **Man page emphasis**: Students learn to use `man` to find commands
- **Concrete verification**: Checks focus on observable results, not process
- **Progressive difficulty**: Builds from basic navigation to complex pipelines
