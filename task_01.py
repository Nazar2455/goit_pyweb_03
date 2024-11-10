import os
import shutil
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

def copy_file(file_path: Path, target_dir: Path):
    extension = file_path.suffix[1:].lower()
    if not extension:
        extension = "unknown"
    
    destination = target_dir / extension
    destination.mkdir(parents=True, exist_ok=True)
    
    shutil.copy2(file_path, destination / file_path.name)

def process_directory(source_dir: Path, target_dir: Path, file_executor: ThreadPoolExecutor):
    futures = []
    
    for item in source_dir.iterdir():
        if item.is_file():
            future = file_executor.submit(copy_file, item, target_dir)
            futures.append(future)
        elif item.is_dir():
            process_directory(item, target_dir, file_executor)

    for future in as_completed(futures):
        future.result()

def main(source_path: str, target_path: Optional[str] = "dist"):
    source_dir = Path(source_path)
    target_dir = Path(target_path)

    if not source_dir.is_dir():
        print("The specified input directory path is invalid.")
        sys.exit(1)

    target_dir.mkdir(parents=True, exist_ok=True)

    with ThreadPoolExecutor() as file_executor:
        process_directory(source_dir, target_dir, file_executor)

    print("Processing complete!")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="File sorting by extension.")
    parser.add_argument("source", type=str, help="Path to the directory for processing.")
    parser.add_argument("target", type=str, nargs="?", default="dist", help="Path to the target directory (default 'dist').")
    args = parser.parse_args()

    main(args.source, args.target)