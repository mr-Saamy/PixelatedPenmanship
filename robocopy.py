import os
import re
import subprocess
import sys
from pathlib import Path
import shutil

def sanitize_folder_name(name):
    """
    Convert filename to a valid folder name.
    """
    # Replace invalid characters
    sanitized = re.sub(r'[\\/*?:"<>|]', '', name)
    # Replace spaces with hyphens
    sanitized = re.sub(r'\s+', '-', sanitized)
    # Remove leading/trailing hyphens
    sanitized = sanitized.strip('-')
    # Ensure we have a valid folder name
    if not sanitized:
        return "untitled"
    return sanitized

def prepare_hugo_structure(source_dir, destination_dir):
    """
    Prepare the Hugo directory structure based on markdown filenames.
    Only copies files that don't already exist in the destination.
    """
    try:
        # Ensure source directory exists
        source_path = Path(source_dir)
        destination_path = Path(destination_dir)
        
        if not source_path.exists():
            print(f"Error: Source directory '{source_dir}' does not exist.")
            return False
        
        if not destination_path.exists():
            print(f"Creating destination directory '{destination_dir}'")
            destination_path.mkdir(parents=True, exist_ok=True)
        
        # Find all markdown files in source directory
        markdown_files = list(source_path.glob('**/*.md'))
        
        if not markdown_files:
            print(f"No markdown files found in '{source_dir}'.")
            return False
        
        print(f"Found {len(markdown_files)} markdown files to process.")
        
        # Create temporary directory structure
        temp_dir = Path(os.environ.get('TEMP', '/tmp')) / 'hugo_temp'
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(parents=True)
        
        # Track statistics
        new_files = 0
        skipped_files = 0
        
        # Process each markdown file
        for md_file in markdown_files:
            try:
                # Get filename without extension to use as folder name
                file_stem = md_file.stem
                folder_name = sanitize_folder_name(file_stem)
                
                # Check if this file already exists in destination
                dest_folder = destination_path / folder_name
                dest_file = dest_folder / "index.md"
                
                if dest_file.exists():
                    print(f"Skipping (already exists): {folder_name}/index.md")
                    skipped_files += 1
                    continue
                
                # This is a new file, create folder in temp directory
                article_folder = temp_dir / folder_name
                article_folder.mkdir(exist_ok=True)
                
                # Copy file to temp directory as index.md
                shutil.copy2(md_file, article_folder / "index.md")
                print(f"Processed: {md_file} -> {folder_name}/index.md")
                new_files += 1
            except Exception as e:
                print(f"Error processing file {md_file}: {e}")
        
        # Summary before copying
        print(f"\nSummary:")
        print(f"  New files to copy: {new_files}")
        print(f"  Files skipped (already exist): {skipped_files}")
        
        if new_files == 0:
            print("No new files to copy. Operation complete.")
            shutil.rmtree(temp_dir)
            return True
        
        # Use robocopy to copy new files to the destination (without /MIR flag)
        robocopy_cmd = f'robocopy "{temp_dir}" "{destination_dir}" /E'
        print(f"\nExecuting: {robocopy_cmd}")
        result = subprocess.run(robocopy_cmd, shell=True)
        
        # Check robocopy exit code (codes 0-7 are success with various conditions)
        if result.returncode >= 8:
            print(f"Robocopy failed with exit code {result.returncode}.")
            return False
        
        # Clean up
        shutil.rmtree(temp_dir)
        print(f"\nSuccessfully copied {new_files} new files.")
        
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def main():
    """
    Main function to run the script.
    """
    # Parse command line arguments
    # if len(sys.argv) < 3:
    #     print("Usage: python script.py <source_directory> <destination_directory>")
    #     return
    
    source_dir =  r"D:\Obsidian Notes\Obsidian Notes\Obsidian Notes\Personl Notes"
    destination_dir = r"D:\InksAndTech\content\posts"
    
    print(f"Source directory: {source_dir}")
    print(f"Destination directory: {destination_dir}")
    
    if prepare_hugo_structure(source_dir, destination_dir):
        print("Process completed successfully.")
    else:
        print("Process failed.")

if __name__ == "__main__":
    main()