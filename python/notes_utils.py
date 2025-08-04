# Import yaml module for YAML parsing and dumping
import yaml
# Import datetime module for timestamp operations
import datetime
# Import uuid module for generating unique identifiers
import uuid
# Import Path class from pathlib for cross-platform path handling
from pathlib import Path

# Define constant for note file extension
NOTE_EXT = ".note"

# Define function to get current timestamp in ISO format
def iso_now():
    # Get current UTC time, remove microseconds, convert to ISO format and add Z suffix
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

# Define function to sanitize filename by removing invalid characters
def sanitize_filename(name: str) -> str:
    # Define string of valid characters for filenames
    valid_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    # Replace invalid characters with underscore and spaces with underscore
    return ''.join(c if c in valid_chars else '_' for c in name).replace(' ', '_')

# Define function to generate unique filename from title
def generate_note_filename(title: str) -> str:
    # Sanitize the title to make it filename-safe
    sanitized = sanitize_filename(title)
    # Generate 2-character unique ID from UUID hex string
    unique_id = uuid.uuid4().hex[:2]  # Only 2 characters for uniqueness
    # Combine sanitized title, unique ID, and file extension
    return f"{sanitized}_{unique_id}{NOTE_EXT}"

# Define function to read note file and parse metadata and content
def read_note_file(filepath: Path):
    # Try to read and parse the file
    try:
        # Open file in read mode with UTF-8 encoding
        with open(filepath, 'r', encoding='utf-8') as f:
            # Read all lines from the file
            lines = f.readlines()
        # Check if file is empty or doesn't start with YAML header marker
        if not lines or lines[0].strip() != "---":
            # Raise error for missing YAML header
            raise ValueError("Missing YAML header")
        # Try to find the closing YAML header marker
        try:
            # Find index of closing "---" line in remaining lines
            yaml_end = lines[1:].index("---\n") + 1
        # Handle case where closing marker is not found
        except ValueError:
            # Raise error for malformed YAML header
            raise ValueError("Malformed YAML header (missing closing ---)")
        # Extract YAML content between the markers
        yaml_str = ''.join(lines[1:yaml_end])
        # Parse YAML string into metadata dictionary
        metadata = yaml.safe_load(yaml_str)
        # Extract content after the closing YAML marker
        content = ''.join(lines[yaml_end + 1:])
        # Return parsed metadata and content
        return metadata, content
    # Handle any exceptions during file reading or parsing
    except Exception as e:
        # Print error message with filename and exception details
        print(f"Error reading note {filepath.name}: {e}")
        # Return None values to indicate failure
        return None, None

# Define function to write note file with metadata and content
def write_note_file(filepath: Path, metadata: dict, content: str):
    # Open file in write mode with UTF-8 encoding
    with open(filepath, 'w', encoding='utf-8') as f:
        # Write opening YAML header marker
        f.write("---\n")
        # Dump metadata dictionary as YAML without sorting keys
        yaml.dump(metadata, f, sort_keys=False)
        # Write closing YAML header marker
        f.write("---\n")
        # Write the note content after the YAML front matter
        f.write(content)