# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a progressive Linux command-line tutorial (TP - "Travaux Pratiques") designed for beginners learning basic Linux commands. The repository provides a self-paced, guided, and automatically-verified learning experience covering file system manipulation, searching, filtering, archiving, links, variables, and process management.

**Language**: French (all instructions and verification messages are in French)

## Architecture

### Core Components

- **setup.sh**: Initialization script that creates the practice environment
  - Recreates `data/` from scratch on every run (lorem.txt, fruits.txt, Fruits_exotiques.txt, sample.csv, logs/app.log, hidden `.bienvenue`, non-executable `salut.sh`)
  - Creates only `workspace/preuves/` and `workspace/.verify/` (SHA-256 of `data/` files); students create the other folders at step 3
  - Keeps existing `workspace/`; `bash setup.sh --reset` wipes it
  - Must be run before starting exercises

- **verify.py**: Automated verification system (Python 3, stdlib only)
  - Checks the concrete result of each task and, on failure, explains what it found plus a hint (never the command itself)
  - Each task is a function (`e1_man`, `e6_uniques`...) returning `OK(message, *remarques)` or `KO(message, *indices)`; `ETAPES` lists the 10 steps and their tasks
  - Observation questions (`question()`) check tasks that leave no file (secret word, PID of the shell...); correct answers are stored in `workspace/.verify/reponses.json`
  - Warns when `data/` differs from the checksums written by setup.sh

- **readme.md**: Landing page of the tutorial: presentation, setup, table of the 10 steps, working method, links to the help pages
  - No quiz: quiz questions are managed in a separate system
  - No `sudo` required; all work happens in user's home directory

- **etapes/NN-*.md**: One page per step (01 to 10), all with the same plan
  - Header (objective, commands, what to produce, help links), then `## Comprendre`, `## À réaliser`, `## Documentation`, `## Valider`, and navigation links (previous / summary / next) at top and bottom
  - Each task (`### Tâche N — ...`) gives its expected result, links to its documentation anchor (`#man-find`), an optional "Pour contrôler" command and an optional `<details>` hint taken from verify.py's hints
  - `## Documentation` has one `### \`man cmd\`` heading per command: real excerpts of `man`/`help` pages (English man, French `help`), kept verbatim
  - The two-digit prefix is used by verify.py (`enonce()`) to print the page of the next step

- **aide/**: Help pages linked from every step: `memo.md` (cheat sheet), `man.md` (man guide), `verification.md` (verify.py output), `depannage.md` (troubleshooting)

- **readme_correction.md** (git-ignored): teacher's solutions, must stay in sync with etapes/

### Directory Structure

```
.
├── data/                    # Source files, recreated by setup.sh, never modified by students
│   ├── .bienvenue          # Hidden file with the secret word (step 2)
│   ├── fruits.txt          # Fruit names with duplicates and mixed case
│   ├── Fruits_exotiques.txt # Capitalized name: find must ignore case (step 5)
│   ├── lorem.txt           # Lorem ipsum text for practice
│   ├── salut.sh            # Script without execute permission (step 8)
│   ├── sample.csv          # CSV file for column extraction practice
│   └── logs/app.log        # Log file for filtering practice
├── workspace/              # Student working directory
│   ├── preuves/            # Outputs saved with > so verify.py can check them
│   └── .verify/            # data.sha256 (setup.sh) and reponses.json (verify.py)
├── etapes/                 # Tutorial instructions, one page per step (01-aide-historique.md ... 10-processus.md)
├── aide/                   # Help pages: memo.md, man.md, verification.md, depannage.md
├── setup.sh                # Environment setup script
├── verify.py               # Automated verification script
└── readme.md               # Landing page: presentation, setup, list of steps
```

## Common Commands

### Setup and Verification

```bash
# Initialize the practice environment (REQUIRED FIRST STEP)
bash setup.sh

# Progress table of all steps (never asks questions)
python3 verify.py

# Detailed check of one step (asks the unanswered observation questions)
python3 verify.py N        # or: python3 verify.py --step N

# Detailed check of all steps
python3 verify.py --all

# Restart the whole TP
bash setup.sh --reset
```

### Verification System Details

- Exit code 0 = validated, 2 = to fix, 1 = environment not ready (setup.sh not run)
- Works from any directory (`BASE` is the script's folder)
- A task never crashes the script: exceptions become a KO line
- Checks tolerate later steps: step 3 still passes after step 4 moved `bonjour.txt` or removed `janvier`, so all 38 tasks can be green at the end
- Answers to questions can be piped (`printf 'a\nb\n' | python3 verify.py 2`), handy for testing

## Tutorial Steps (10 Exercises)

1. **Help/History**: man, man -k, --help, help, history, date
2. **Navigation**: pwd, cd, ls -a -l, cat, absolute/relative paths
3. **File/Directory Creation**: mkdir (-p), touch, echo, redirection (>, >>), cat -n
4. **Copy/Move/Delete**: cp -R, mv, rm -r, rmdir
5. **Search**: find -iname, grep -i -n, which, type
6. **Filters/Pipes**: head, tail, sort, uniq, wc, tr, cut, grep | wc
7. **Archive/Compress**: tar (create, list, extract with gzip)
8. **Symlinks/Permissions**: ln -s, chmod (octal notation), executable script
9. **Environment/Aliases**: export, child processes, alias
10. **Processes**: ps, jobs, pgrep, kill/pkill, df -h, background jobs (&)

## Implementation Notes

### When Modifying verify.py

- A task function must return exactly one `OK(...)` or `KO(...)`: the progress table counts tasks
- Compute expected values from `data/` files (word count, column...), never hard-code them, so setup.sh stays the single source of truth
- `absent(path)` is the standard KO for a missing file: it also looks for a file of the same name elsewhere (wrong current directory)
- Hints point to the relevant option or concept, not to the full command
- When changing tasks, update the step page in etapes/, readme_correction.md and VERIFICATION_COHERENCE.md together; the "Quand tout est juste" block of each step page shows the exact success line printed by `verifier_etape()`

### Expected Student Work Products

- Step 1: `workspace/preuves/historique.txt`; questions: `-S`, weekday of 2030-01-01, `pwd`
- Step 2: questions only (absolute path of the TP, secret word, size of sample.csv, relative path)
- Step 3: `workspace/{docs,data,tmp}/`, `workspace/projets/2026/janvier/`, `workspace/data/todo.txt`, `workspace/tmp/.cache`, `workspace/docs/bonjour.txt` (≥2 lines)
- Step 4: `workspace/backup_data/` (without `logs/`), `workspace/bonjour.renomme.txt`, `janvier/` removed
- Step 5: `workspace/preuves/find_fruits.txt`, `grep_poire.txt`, `which_python3.txt`
- Step 6: `workspace/data/lorem_extrait.txt`, `fruits_uniques.txt`, `lorem_wc.txt`, `fruits_upper.txt`, `col2.txt`, `nb_info.txt`
- Step 7: `workspace/data_archive.tgz`, `workspace/preuves/contenu_archive.txt`, extracted `workspace/tmp/data/`
- Step 8: `workspace/data/link_fruits.txt` (symlink), `fruits_uniques.txt` with mode 640, `workspace/salut.sh` with mode 755
- Step 9: exported `MYVAR` (inherited by verify.py), `workspace/preuves/alias.txt` containing the `verif` alias
- Step 10: question (PID of the shell), `workspace/preuves/sleep.pid` (process terminated), `workspace/preuves/disque.txt` (`df -h`)

### Constraints and Philosophy

- **No sudo**: All operations within user's home directory
- **Discovery-based learning**: Instructions provide hints, not exact commands
- **Man page emphasis**: Students learn to use `man` to find commands
- **Concrete verification**: Checks focus on observable results, not process
- **Progressive difficulty**: Builds from basic navigation to complex pipelines
