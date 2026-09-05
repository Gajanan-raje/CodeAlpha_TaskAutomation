"""
CodeAlpha_TaskAutomation
Task 3: Task Automation with Python Scripts (Advanced Version 2)
Concepts: os, shutil, re, requests, file handling, exception handling, zipfile

Automation tools (menu-driven):
  1. Move all .jpg files from a folder to a new folder
  2. Extract all email addresses from a .txt file and save them
  3. Scrape the title of a fixed webpage and save it
  4. Bulk rename files in a folder
  5. Find and delete duplicate files in a folder
  6. Backup (zip) a folder                                    [NEW]
"""

import os
import shutil
import re
import hashlib
import zipfile
from datetime import datetime

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


# ---------- Colors ----------
class C:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"


def success(msg):
    print(f"{C.GREEN}[OK] {msg}{C.END}")


def error(msg):
    print(f"{C.RED}[ERROR] {msg}{C.END}")


def warn(msg):
    print(f"{C.YELLOW}[!] {msg}{C.END}")


def info(msg):
    print(f"{C.CYAN}{msg}{C.END}")


def section(title):
    print(f"\n{C.HEADER}{C.BOLD}--- {title} ---{C.END}")


def progress_bar(current, total, width=30):
    """Print a simple inline progress bar."""
    filled = int(width * current / total) if total else width
    bar = "#" * filled + "-" * (width - filled)
    pct = (current / total * 100) if total else 100
    print(f"\r  [{bar}] {pct:5.1f}% ({current}/{total})", end="", flush=True)
    if current == total:
        print()


# ---------- Task 1: Move .jpg files ----------
def move_jpg_files():
    section("Move .jpg Files")
    source = input("Enter source folder path: ").strip()

    if not os.path.isdir(source):
        error(f"'{source}' is not a valid folder.")
        return

    dest = input("Enter destination folder path (created if missing): ").strip()
    if not dest:
        error("Destination folder cannot be empty.")
        return

    try:
        os.makedirs(dest, exist_ok=True)
    except OSError as e:
        error(f"Could not create destination folder: {e}")
        return

    jpg_files = [f for f in os.listdir(source)
                 if f.lower().endswith((".jpg", ".jpeg"))]

    if not jpg_files:
        warn("No .jpg files found in the source folder.")
        return

    moved_count = 0
    total = len(jpg_files)
    for i, filename in enumerate(jpg_files, start=1):
        src_path = os.path.join(source, filename)
        dest_path = os.path.join(dest, filename)
        try:
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(dest, f"{base}_{counter}{ext}")
                    counter += 1
            shutil.move(src_path, dest_path)
            moved_count += 1
        except (OSError, shutil.Error) as e:
            print()
            error(f"Failed to move {filename}: {e}")
        progress_bar(i, total)

    print(f"\n{C.BOLD}Summary:{C.END} {moved_count} of {total} .jpg file(s) moved to '{dest}'.")
    success("Task complete.")


# ---------- Task 2: Extract emails ----------
def extract_emails():
    section("Extract Email Addresses")
    source_file = input("Enter path to .txt file: ").strip()

    if not os.path.isfile(source_file):
        error(f"'{source_file}' does not exist.")
        return

    try:
        with open(source_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except (IOError, OSError) as e:
        error(f"Could not read file: {e}")
        return

    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    emails_found = re.findall(email_pattern, content)

    if not emails_found:
        warn("No email addresses found in the file.")
        return

    unique_emails = sorted(set(emails_found))
    info(f"\nFound {len(unique_emails)} unique email address(es):")
    for email in unique_emails:
        print(f"  {email}")

    output_file = input("\nEnter output filename to save (default: extracted_emails.txt): ").strip()
    if not output_file:
        output_file = "extracted_emails.txt"
    if not output_file.endswith(".txt"):
        output_file += ".txt"

    try:
        with open(output_file, "w") as f:
            for email in unique_emails:
                f.write(email + "\n")
        success(f"Saved {len(unique_emails)} email(s) to: {os.path.abspath(output_file)}")
    except (IOError, OSError) as e:
        error(f"Could not save file: {e}")


# ---------- Task 3: Scrape webpage title ----------
def scrape_webpage_title():
    section("Scrape Webpage Title")

    if not REQUESTS_AVAILABLE:
        error("'requests' library is not installed.")
        info("Install it with: pip install requests")
        return

    url = input("Enter webpage URL (e.g. https://example.com): ").strip()

    if not url:
        error("URL cannot be empty.")
        return

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except requests.exceptions.Timeout:
        error("Request timed out.")
        return
    except requests.exceptions.ConnectionError:
        error("Could not connect. Check the URL or your internet connection.")
        return
    except requests.exceptions.HTTPError as e:
        error(f"HTTP error occurred - {e}")
        return
    except requests.exceptions.RequestException as e:
        error(str(e))
        return

    title_match = re.search(r"<title[^>]*>(.*?)</title>", response.text, re.IGNORECASE | re.DOTALL)

    if not title_match:
        warn("No <title> tag found on this page.")
        return

    title = re.sub(r"\s+", " ", title_match.group(1).strip())
    info(f"\nPage Title: {title}")

    output_file = input("\nEnter filename to save title (default: page_title.txt): ").strip()
    if not output_file:
        output_file = "page_title.txt"
    if not output_file.endswith(".txt"):
        output_file += ".txt"

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"URL: {url}\nTitle: {title}\n")
        success(f"Saved to: {os.path.abspath(output_file)}")
    except (IOError, OSError) as e:
        error(f"Could not save file: {e}")


# ---------- Task 4: Bulk rename files ----------
def bulk_rename_files():
    section("Bulk Rename Files")
    folder = input("Enter folder path: ").strip()

    if not os.path.isdir(folder):
        error(f"'{folder}' is not a valid folder.")
        return

    ext_filter = input("Only rename files with extension (e.g. jpg, txt) or leave blank for all: ").strip().lstrip(".")
    prefix = input("Enter new name prefix (e.g. 'photo'): ").strip()

    if not prefix:
        error("Prefix cannot be empty.")
        return

    files = sorted(os.listdir(folder))
    if ext_filter:
        files = [f for f in files if f.lower().endswith("." + ext_filter.lower())]

    files = [f for f in files if os.path.isfile(os.path.join(folder, f))]

    if not files:
        warn("No matching files found.")
        return

    print(f"\n{len(files)} file(s) will be renamed like: {prefix}_1{os.path.splitext(files[0])[1]}, "
          f"{prefix}_2{os.path.splitext(files[0])[1]} ...")
    if not get_yes_no("Proceed? (y/n): "):
        warn("Cancelled.")
        return

    renamed_count = 0
    total = len(files)
    for i, filename in enumerate(files, start=1):
        ext = os.path.splitext(filename)[1]
        new_name = f"{prefix}_{i}{ext}"
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)

        if os.path.exists(new_path) and new_path != old_path:
            print()
            warn(f"Skipped {filename}: '{new_name}' already exists.")
        else:
            try:
                os.rename(old_path, new_path)
                renamed_count += 1
            except OSError as e:
                print()
                error(f"Could not rename {filename}: {e}")
        progress_bar(i, total)

    print(f"\n{C.BOLD}Summary:{C.END} {renamed_count} of {total} file(s) renamed.")
    success("Task complete.")


# ---------- Task 5: Find & delete duplicate files ----------
def file_hash(path, chunk_size=8192):
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def find_duplicate_files():
    section("Find Duplicate Files")
    folder = input("Enter folder path to scan: ").strip()

    if not os.path.isdir(folder):
        error(f"'{folder}' is not a valid folder.")
        return

    hashes = {}
    duplicates = []

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not files:
        warn("No files found in this folder.")
        return

    info(f"Scanning {len(files)} file(s)...")
    total = len(files)
    total_size_saved = 0

    for i, filename in enumerate(files, start=1):
        path = os.path.join(folder, filename)
        try:
            h = file_hash(path)
        except (OSError, IOError) as e:
            print()
            error(f"Could not read {filename}: {e}")
            progress_bar(i, total)
            continue

        if h in hashes:
            duplicates.append((filename, hashes[h]))
            total_size_saved += os.path.getsize(path)
        else:
            hashes[h] = filename
        progress_bar(i, total)

    if not duplicates:
        success("No duplicate files found.")
        return

    warn(f"\nFound {len(duplicates)} duplicate file(s) (~{total_size_saved / 1024:.1f} KB wasted):")
    for dup, original in duplicates:
        print(f"  '{dup}' is a duplicate of '{original}'")

    if get_yes_no("\nDelete duplicate copies? (y/n): "):
        deleted = 0
        for dup, _ in duplicates:
            try:
                os.remove(os.path.join(folder, dup))
                print(f"  Deleted: {dup}")
                deleted += 1
            except OSError as e:
                error(f"Could not delete {dup}: {e}")
        success(f"Deleted {deleted} duplicate file(s), freed ~{total_size_saved / 1024:.1f} KB.")
    else:
        info("No files were deleted.")


# ---------- Task 6 (NEW): Backup (zip) a folder ----------
def backup_folder():
    section("Backup (Zip) a Folder")
    folder = input("Enter folder path to back up: ").strip()

    if not os.path.isdir(folder):
        error(f"'{folder}' is not a valid folder.")
        return

    dest_dir = input("Enter destination folder for the backup (blank = current folder): ").strip()
    if dest_dir and not os.path.isdir(dest_dir):
        try:
            os.makedirs(dest_dir, exist_ok=True)
        except OSError as e:
            error(f"Could not create destination folder: {e}")
            return
    if not dest_dir:
        dest_dir = "."

    folder_name = os.path.basename(os.path.normpath(folder))
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_name = f"{folder_name}_backup_{timestamp}.zip"
    zip_path = os.path.join(dest_dir, zip_name)

    all_files = []
    for root, _, files in os.walk(folder):
        for f in files:
            all_files.append(os.path.join(root, f))

    if not all_files:
        warn("The folder is empty. Nothing to back up.")
        return

    info(f"Backing up {len(all_files)} file(s)...")
    total = len(all_files)

    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for i, file_path in enumerate(all_files, start=1):
                arcname = os.path.relpath(file_path, os.path.dirname(folder))
                zipf.write(file_path, arcname)
                progress_bar(i, total)
    except (OSError, zipfile.BadZipFile) as e:
        print()
        error(f"Backup failed: {e}")
        return

    zip_size = os.path.getsize(zip_path) / 1024
    print()
    success(f"Backup created: {os.path.abspath(zip_path)} ({zip_size:.1f} KB)")


# ---------- Helpers ----------
def get_yes_no(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        warn("Please answer 'y' or 'n'.")


def main_menu():
    print(f"{C.BOLD}{C.HEADER}" + "=" * 55 + f"{C.END}")
    print(f"{C.BOLD}{C.HEADER}" + " " * 12 + "TASK AUTOMATION TOOLKIT" + f"{C.END}")
    print(f"{C.BOLD}{C.HEADER}" + "=" * 55 + f"{C.END}")

    options = {
        "1": ("Move all .jpg files from a folder", move_jpg_files),
        "2": ("Extract emails from a .txt file", extract_emails),
        "3": ("Scrape the title of a webpage", scrape_webpage_title),
        "4": ("Bulk rename files in a folder", bulk_rename_files),
        "5": ("Find & delete duplicate files", find_duplicate_files),
        "6": ("Backup (zip) a folder", backup_folder),
        "7": ("Exit", None),
    }

    while True:
        print(f"\n{C.BOLD}Choose an automation task:{C.END}")
        for key, (desc, _) in options.items():
            print(f"  {C.CYAN}{key}.{C.END} {desc}")

        choice = input(f"\n{C.BOLD}Enter choice (1-7): {C.END}").strip()

        if choice not in options:
            warn("Invalid choice. Please enter a number from 1 to 7.")
            continue

        if choice == "7":
            info("Goodbye!")
            break

        _, func = options[choice]
        try:
            func()
        except KeyboardInterrupt:
            warn("\nOperation cancelled by user.")
        except Exception as e:
            error(f"Unexpected error: {e}")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{C.YELLOW}Program interrupted. Goodbye!{C.END}")
