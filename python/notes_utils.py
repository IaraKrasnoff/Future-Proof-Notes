import yaml
import datetime
import uuid
from pathlib import Path

NOTE_EXT = ".note"

def iso_now():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def sanitize_filename(name: str) -> str:
    valid_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(c if c in valid_chars else '_' for c in name).replace(' ', '_')

def generate_note_filename(title: str) -> str:
    sanitized = sanitize_filename(title)
    unique_id = uuid.uuid4().hex[:2]  # Only 2 characters for uniqueness
    return f"{sanitized}_{unique_id}{NOTE_EXT}"

def read_note_file(filepath: Path):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        if not lines or lines[0].strip() != "---":
            raise ValueError("Missing YAML header")
        try:
            yaml_end = lines[1:].index("---\n") + 1
        except ValueError:
            raise ValueError("Malformed YAML header (missing closing ---)")
        yaml_str = ''.join(lines[1:yaml_end])
        metadata = yaml.safe_load(yaml_str)
        content = ''.join(lines[yaml_end + 1:])
        return metadata, content
    except Exception as e:
        print(f"Error reading note {filepath.name}: {e}")
        return None, None

def write_note_file(filepath: Path, metadata: dict, content: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("---\n")
        yaml.dump(metadata, f, sort_keys=False)
        f.write("---\n")
        f.write(content)