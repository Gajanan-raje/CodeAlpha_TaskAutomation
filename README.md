
# CodeAlpha_TaskAutomation

A Python-based **Task Automation Toolkit** built as part of the CodeAlpha Python Programming Internship (Task 3). This single script combines **6 real-world automation tools** in one menu-driven program.

## About
Repetitive manual tasks like sorting files, cleaning up folders, or checking a webpage can be automated with a few lines of Python. This toolkit demonstrates practical automation using core Python modules — no external setup needed except one optional library for web scraping.

## Features / Tools Included

### 1. Move .jpg Files
Moves all `.jpg`/`.jpeg` files from a source folder into a destination folder. Automatically renames files to avoid overwriting if a duplicate name exists.

### 2. Extract Email Addresses
Reads a `.txt` file, scans it using regular expressions, and extracts every valid email address found. Removes duplicates and saves the clean list to a new file.

### 3. Scrape Webpage Title
Given any URL, fetches the page and extracts the content inside its `<title>` tag, then saves the URL and title to a text file. Handles connection errors and timeouts gracefully.

### 4. Bulk Rename Files
Renames every file in a folder (optionally filtered by extension) using a common prefix and sequential numbering — e.g. `photo_1.jpg`, `photo_2.jpg`, etc.

### 5. Find & Delete Duplicate Files
Scans a folder and calculates an MD5 hash for every file to detect exact duplicates (based on content, not just filename). Reports how much space is wasted and optionally deletes the duplicate copies.

### 6. Backup (Zip) a Folder
Compresses an entire folder — including all subfolders — into a single timestamped `.zip` file for quick backup.

## Extra Touches
- 🎨 Color-coded terminal output (green = success, red = error, yellow = warning)
- 📊 Live progress bar for file operations
- 🛡 Full error handling — invalid paths, missing files, no internet, and interrupted operations (Ctrl+C) are all handled without crashing
- 📝 Clear before/after summaries for every operation

## How to Run
```bash
python task_automation.py
```
A menu appears — enter a number (1–7) to choose a tool, or 7 to exit.

## Requirements
- Python 3
- `requests` library (only needed for Option 3 — Scrape Webpage Title)
  ```bash
  pip install requests
  ```

## Concepts Used
`os`, `shutil`, `re`, `requests`, `hashlib`, `zipfile`, file handling, exception handling

## Tech Stack
- Python 3 (standard library + `requests`)

## Author
Gajanan Harinarayan Raje — CodeAlpha Python Programming Intern
