# Import os module for operating system interface functions
import os
# Import subprocess module for running external commands
import subprocess
# Import Path class from pathlib for cross-platform path handling
from pathlib import Path
# Import utility functions from notes_utils module
from notes_utils import (
    NOTE_EXT, iso_now, generate_note_filename,
    read_note_file, write_note_file
)

# Define the notes directory path relative to this file's parent directory
NOTES_DIR = Path(__file__).parent.parent / "notes_repository"
# Create the notes directory if it doesn't exist
NOTES_DIR.mkdir(exist_ok=True)
# Get the editor command from environment variable, default to "nano"
EDITOR = os.environ.get("EDITOR", "nano")

# Define function to list notes with optional tag filtering
def list_notes(filter_tag=None):
    # Initialize empty list to store results
    results = []
    # Iterate through all files in notes directory with NOTE_EXT extension
    for note_file in NOTES_DIR.glob(f"*{NOTE_EXT}"):
        # Read metadata and content from the note file
        meta, content = read_note_file(note_file)
        # Skip this file if metadata couldn't be read
        if meta is None:
            continue
        # If tag filtering is requested
        if filter_tag:
            # Get the tags list from metadata, default to empty list
            tags = meta.get('tags', [])
            # Skip this note if the filter tag is not in its tags
            if filter_tag not in tags:
                continue
        # Add filename and metadata tuple to results
        results.append((note_file.name, meta))
    # Return the list of matching notes
    return results

# Define function to create a new note
def create_note():
    # Prompt user for note title and remove whitespace
    title = input("Enter note title: ").strip()
    # Check if title is empty
    if not title:
        # Print error message and exit function
        print("Title cannot be empty.")
        return
    # Prompt user for tags and remove whitespace
    tags_raw = input("Enter tags (comma separated, optional): ").strip()
    # Split tags by comma and strip whitespace, or empty list if no tags
    tags = [t.strip() for t in tags_raw.split(",")] if tags_raw else []
    # Generate filename from title using utility function
    filename = generate_note_filename(title)
    # Create full file path by joining directory and filename
    filepath = NOTES_DIR / filename
    # Get current timestamp in ISO format
    created = iso_now()
    # Create metadata dictionary with note information
    metadata = {
        'note_id': filename[:-len(NOTE_EXT)],  # Use filename without extension as ID
        'filename': filename,
        'path': str(filepath),
        'created': created,
        'modified': created,
        'tags': tags,   
        'title': title,
        'content': '',
        'editor': EDITOR    
    }
    # Initialize empty content string
    content = ""
    # Write the note file with metadata and empty content
    write_note_file(filepath, metadata, content)
    # Open the note file in the configured editor
    subprocess.run([EDITOR, str(filepath)])
    # Re-read the note file after editing
    meta, content = read_note_file(filepath)
    # If metadata was successfully read
    if meta:
        # Update the modified timestamp
        meta['modified'] = iso_now()
        # Write the updated note file
        write_note_file(filepath, meta, content)
    # Print confirmation message with filename
    print(f"Note created as {filename}")

# Define function to read and display a note
def read_note(note_id):
    # Create file path from notes directory and note_id
    filepath = NOTES_DIR / note_id
    # Check if the file exists
    if not filepath.exists():
        # Print error message and exit function
        print(f"Note '{note_id}' not found.")
        return
    # Read metadata and content from the note file
    meta, content = read_note_file(filepath)
    # Check if metadata was successfully read
    if meta is None:
        # Print error message and exit function
        print("Failed to read note metadata.")
        return
    # Print the note title from metadata
    print(f"Title: {meta.get('title', '')}")
    # Print the creation timestamp from metadata
    print(f"Created: {meta.get('created', '')}")
    # Print the modification timestamp from metadata
    print(f"Modified: {meta.get('modified', '')}")
    # Print the tags joined by commas from metadata
    print(f"Tags: {', '.join(meta.get('tags', []))}")
    # Print separator line
    print("\n---\n")
    # Print the note content
    print(content)

# Define function to edit an existing note
def edit_note(note_id):
    # Create file path from notes directory and note_id
    filepath = NOTES_DIR / note_id
    # Check if the file exists
    if not filepath.exists():
        # Print error message and exit function
        print(f"Note '{note_id}' not found.")
        return
    # Open the note file in the configured editor
    subprocess.run([EDITOR, str(filepath)])
    # Re-read the note file after editing
    meta, content = read_note_file(filepath)
    # If metadata was successfully read
    if meta:
        # Update the modified timestamp
        meta['modified'] = iso_now()
        # Write the updated note file
        write_note_file(filepath, meta, content)
        # Print confirmation message
        print("Note updated.")

# Define function to delete a note
def delete_note(note_id):
    # Create file path from notes directory and note_id
    filepath = NOTES_DIR / note_id
    # Check if the file exists
    if not filepath.exists():
        # Print error message and exit function
        print(f"Note '{note_id}' not found.")
        return
    # Try to delete the file
    try:
        # Remove the file from filesystem
        filepath.unlink()
        # Print confirmation message
        print(f"Note '{note_id}' deleted.")
    # Handle any exceptions during deletion
    except Exception as e:
        # Print error message with exception details
        print(f"Failed to delete note: {e}")

# Define function to search notes by query string
def search_notes(query: str):
    # Initialize empty list to store search results
    results = []
    # Convert query to lowercase for case-insensitive search
    q = query.lower()
    # Track corrupted files
    corrupted_files = []
    
    # Iterate through all files in notes directory with NOTE_EXT extension
    for note_file in NOTES_DIR.glob(f"*{NOTE_EXT}"):
        # Read metadata and content from the note file
        meta, content = read_note_file(note_file)
        # Skip this file if metadata couldn't be read (corrupted)
        if meta is None:
            corrupted_files.append(note_file.name)
            continue
        
        # Create searchable text by combining title, tags, and content (all lowercase)
        haystack = ' '.join([
            meta.get('title', '').lower(),
            ' '.join(tag.lower() for tag in meta.get('tags', [])),
            content.lower()
        ])
        # Check if query is found in the searchable text
        if q in haystack:
            # Add filename and metadata tuple to results
            results.append((note_file.name, meta))
    
    # Warn about corrupted files if any were found
    if corrupted_files:
        print(f"Warning: Skipped {len(corrupted_files)} corrupted file(s): {', '.join(corrupted_files)}")
    
    # Return the list of matching notes
    return results

# Define function to display notes statistics
def stats():
    # Get all notes using list_notes function
    notes = list_notes()
    # Count total number of notes
    count = len(notes)
    # Initialize empty dictionary to count tags
    tag_count = {}
    # Iterate through each note and its metadata
    for _, meta in notes:
        # Iterate through each tag in the note's tags
        for tag in meta.get('tags', []):
            # Increment tag count, defaulting to 0 if tag not seen before
            tag_count[tag] = tag_count.get(tag, 0) + 1
    # Print total notes count
    print(f"Total notes: {count}")
    # Print tags summary header
    print("Tags summary:")
    # Check if any tags were found
    if tag_count:
        # Iterate through each tag and its count
        for tag, c in tag_count.items():
            # Print tag name and count with indentation
            print(f"  {tag}: {c}")
    # If no tags were found
    else:
        # Print message indicating no tags
        print("  No tags found.")