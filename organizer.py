import shutil
from pathlib import Path

# Mapping of file extensions to category subfolders
# Extensions are stored in lowercase for reliable matching
EXTENSION_MAP = {
    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".webp": "Images",
    # Documents
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    # Spreadsheets
    ".xls": "Spreadsheets",
    ".xlsx": "Spreadsheets",
    ".csv": "Spreadsheets",
    # Audio
    ".mp3": "Audio",
    ".wav": "Audio",
    ".flac": "Audio",
    # Videos
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".avi": "Videos",
    # Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    # Python
    ".py": "Python",
}


def get_category(file_path: Path) -> str:
    """Determine the category folder name based on the file extension."""
    # Obtain extension in lowercase (e.g., '.jpg')
    extension = file_path.suffix.lower()
    # Return matched category or 'Other' if not in the mapping dictionary
    return EXTENSION_MAP.get(extension, "Other")


def get_unique_destination(target_dir: Path, original_filename: str) -> Path:
    """
    Generate a unique destination path to avoid overwriting existing files.
    If 'photo.jpg' exists in the category folder, this will return 'photo_1.jpg'.
    """
    destination = target_dir / original_filename
    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix
    counter = 1

    # Keep incrementing counter until a non-conflicting filename is found
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_destination = target_dir / new_name
        if not new_destination.exists():
            return new_destination
        counter += 1


def organize_folder(folder_path_str: str) -> None:
    """
    Scans the specified folder and moves files into subfolders based on extension.
    """
    # Convert input string into a pathlib Path object
    target_folder = Path(folder_path_str.strip('"\''))

    # Basic error handling: check if path exists and is a directory
    if not target_folder.exists():
        print(f"Error: The path '{target_folder}' does not exist.")
        return

    if not target_folder.is_dir():
        print(f"Error: The path '{target_folder}' is not a directory.")
        return

    print(f"\nScanning folder: {target_folder.resolve()}")
    print("-" * 50)

    # Dictionary to keep track of how many files are moved into each category
    summary = {}
    total_moved = 0

    try:
        # Iterate over all items in the target directory
        for item in target_folder.iterdir():
            # Skip directories; process only files
            if not item.is_file():
                continue

            # Determine the appropriate category folder name
            category = get_category(item)

            # Create destination category directory if it doesn't already exist
            category_dir = target_folder / category
            category_dir.mkdir(exist_ok=True)

            # Generate safe destination path avoiding file overwrites
            dest_path = get_unique_destination(category_dir, item.name)

            # Move the file to the category folder
            try:
                shutil.move(str(item), str(dest_path))
                print(f"Moved: {item.name} -> {category}/{dest_path.name}")

                # Update count summary
                summary[category] = summary.get(category, 0) + 1
                total_moved += 1

            except PermissionError:
                print(f"Permission Error: Skipped '{item.name}' (file is in use or access denied).")
            except Exception as e:
                print(f"Failed to move '{item.name}': {e}")

    except PermissionError:
        print(f"Permission Error: Access denied when reading directory '{target_folder}'.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    # Print summary of moved files
    print("\n" + "=" * 50)
    print("ORGANIZATION SUMMARY")
    print("=" * 50)
    if total_moved == 0:
        print("No files were moved.")
    else:
        print(f"Total files moved: {total_moved}")
        for cat, count in sorted(summary.items()):
            print(f"  - {cat}: {count} file(s)")
    print("=" * 50)


def main():
    print("=" * 50)
    print("                FILE ORGANIZER                   ")
    print("=" * 50)
    print("This utility categorizes files in a folder into subfolders")
    print("based on file extensions (Images, Documents, Audio, etc.).")
    print("Existing subfolders and directories will be untouched.")
    print("=" * 50 + "\n")

    user_input = input("Enter the path of the folder you want to organize: ").strip()

    if not user_input:
        print("No path entered. Exiting.")
        return

    organize_folder(user_input)


if __name__ == "__main__":
    main()
