# Import the argparse module for command-line argument parsing
import argparse
# Import specific functions from the notes_commands module
from notes_commands import (
    create_note, list_notes, read_note, edit_note,
    delete_note, search_notes, stats
)

# Define the main function that will handle command-line interface logic
def main():
    # Create an ArgumentParser object with a description for the CLI tool
    parser = argparse.ArgumentParser(description="Personal Notes Manager - Phase 1 CLI")
    # Create subparsers to handle different commands (create, list, read, etc.)
    subparsers = parser.add_subparsers(dest='command')
    # Add a 'create' subcommand with help text
    subparsers.add_parser('create', help='Create a new note')
    # Add a 'list' subcommand and store its parser object
    list_parser = subparsers.add_parser('list', help='List notes, optionally filtered by tag')
    # Add an optional --tag argument to the list command
    list_parser.add_argument('--tag', help='Filter notes by tag')
    # Add a 'read' subcommand and store its parser object
    read_parser = subparsers.add_parser('read', help='Read/display a note')
    # Add a required positional argument for note_id to the read command
    read_parser.add_argument('note_id', help='Note filename')
    # Add an 'edit' subcommand and store its parser object
    edit_parser = subparsers.add_parser('edit', help='Edit a note')
    # Add a required positional argument for note_id to the edit command
    edit_parser.add_argument('note_id', help='Note filename')
    # Add a 'delete' subcommand and store its parser object
    delete_parser = subparsers.add_parser('delete', help='Delete a note')
    # Add a required positional argument for note_id to the delete command
    delete_parser.add_argument('note_id', help='Note filename')
    # Add a 'search' subcommand and store its parser object
    search_parser = subparsers.add_parser('search', help='Search notes')
    # Add a required positional argument for search query to the search command
    search_parser.add_argument('query', help='Search query')
    # Add a 'stats' subcommand with help text
    subparsers.add_parser('stats', help='Show notes statistics')
    # Parse the command-line arguments and store them in args object
    args = parser.parse_args()
    # Check if the command is 'create'
    if args.command == 'create':
        # Call the create_note function
        create_note()
    # Check if the command is 'list'
    elif args.command == 'list':
        # Call list_notes function with optional tag filter and store results
        notes = list_notes(filter_tag=args.tag)
        # Check if no notes were found
        if not notes:
            # Print message indicating no notes found
            print("No notes found.")
        # If notes were found
        else:
            # Iterate through each note (filename and metadata)
            for filename, meta in notes:
                # Print formatted note information with filename, title, and tags
                print(f"{filename}: {meta.get('title', '')} (tags: {', '.join(meta.get('tags', []))})")
    # Check if the command is 'read'
    elif args.command == 'read':
        # Call read_note function with the provided note_id
        read_note(args.note_id)
    # Check if the command is 'edit'
    elif args.command == 'edit':
        # Call edit_note function with the provided note_id
        edit_note(args.note_id)
    # Check if the command is 'delete'
    elif args.command == 'delete':
        # Call delete_note function with the provided note_id
        delete_note(args.note_id)
    # Check if the command is 'search'
    elif args.command == 'search':
        # Call search_notes function with the query and store results
        results = search_notes(args.query)
        # Check if no search results were found
        if not results:
            # Print message indicating no matching notes found
            print("No matching notes found.")
        # If search results were found
        else:
            # Iterate through each search result (filename and metadata)
            for filename, meta in results:
                # Print formatted search result with filename and title
                print(f"{filename}: {meta.get('title', '')}")
    # Check if the command is 'stats'
    elif args.command == 'stats':
        # Call the stats function to display statistics
        stats()
    # If no valid command was provided
    else:
        # Print the help message showing available commands
        parser.print_help()

# Check if this script is being run directly (not imported)
if __name__ == "__main__":
    # Call the main function to start the CLI application
    main()


# Multi-line comment containing usage instructions for the CLI tool
# Usage instructions:
'''
python python/notes_cli.py create
python python/notes_cli.py list
python python/notes_cli.py read <note_filename>
python python/notes_cli.py edit <note_filename>
python python/notes_cli.py delete <note_filename>
python python/notes_cli.py search <query>
python python/notes_cli.py stats
'''