import os
import subprocess
from pathlib import Path
from notes_utils import (
    NOTE_EXT, iso_now, sanitize_filename, generate_note_filename,
    read_note_file, write_note_file
)

NOTES_DIR = Path(__file__).parent.parent / "notes_repository"
NOTES_DIR.mkdir(exist_ok=True)
EDITOR = os.environ.get("EDITOR", "nano")

def list_notes(filter_tag=None):
    results = []
    for note_file in NOTES_DIR.glob(f"*{NOTE_EXT}"):
        meta, content = read_note_file(note_file)
        if meta is None:
            continue
        if filter_tag:
            tags = meta.get('tags', [])
            if filter_tag not in tags:
                continue
        results.append((note_file.name, meta))
    return results

def create_note():
    title = input("Enter note title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    tags_raw = input("Enter tags (comma separated, optional): ").strip()
    tags = [t.strip() for t in tags_raw.split(",")] if tags_raw else []
    filename = generate_note_filename(title)
    filepath = NOTES_DIR / filename
    created = iso_now()
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
    content = ""
    write_note_file(filepath, metadata, content)
    subprocess.run([EDITOR, str(filepath)])
    meta, content = read_note_file(filepath)
    if meta:
        meta['modified'] = iso_now()
        write_note_file(filepath, meta, content)
    print(f"Note created as {filename}")

def read_note(note_id):
    filepath = NOTES_DIR / note_id
    if not filepath.exists():
        print(f"Note '{note_id}' not found.")
        return
    meta, content = read_note_file(filepath)
    if meta is None:
        print("Failed to read note metadata.")
        return
    print(f"Title: {meta.get('title', '')}")
    print(f"Created: {meta.get('created', '')}")
    print(f"Modified: {meta.get('modified', '')}")
    print(f"Tags: {', '.join(meta.get('tags', []))}")
    print("\n---\n")
    print(content)

def edit_note(note_id):
    filepath = NOTES_DIR / note_id
    if not filepath.exists():
        print(f"Note '{note_id}' not found.")
        return
    subprocess.run([EDITOR, str(filepath)])
    meta, content = read_note_file(filepath)
    if meta:
        meta['modified'] = iso_now()
        write_note_file(filepath, meta, content)
        print("Note updated.")

def delete_note(note_id):
    filepath = NOTES_DIR / note_id
    if not filepath.exists():
        print(f"Note '{note_id}' not found.")
        return
    try:
        filepath.unlink()
        print(f"Note '{note_id}' deleted.")
    except Exception as e:
        print(f"Failed to delete note: {e}")

def search_notes(query: str):
    results = []
    q = query.lower()
    for note_file in NOTES_DIR.glob(f"*{NOTE_EXT}"):
        meta, content = read_note_file(note_file)
        if meta is None:
            continue
        haystack = ' '.join([
            meta.get('title', '').lower(),
            ' '.join(tag.lower() for tag in meta.get('tags', [])),
            content.lower()
        ])
        if q in haystack:
            results.append((note_file.name, meta))
    return results

def stats():
    notes = list_notes()
    count = len(notes)
    tag_count = {}
    for _, meta in notes:
        for tag in meta.get('tags', []):
            tag_count[tag] = tag_count.get(tag, 0) + 1
    print(f"Total notes: {count}")
    print("Tags summary:")
    if tag_count:
        for tag, c in tag_count.items():
            print(f"  {tag}: {c}")
    else:
        print("  No tags found.")