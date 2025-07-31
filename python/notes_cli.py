import argparse
from notes_commands import (
    create_note, list_notes, read_note, edit_note,
    delete_note, search_notes, stats
)

def main():
    parser = argparse.ArgumentParser(description="Personal Notes Manager - Phase 1 CLI")
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('create', help='Create a new note')
    list_parser = subparsers.add_parser('list', help='List notes, optionally filtered by tag')
    list_parser.add_argument('--tag', help='Filter notes by tag')
    read_parser = subparsers.add_parser('read', help='Read/display a note')
    read_parser.add_argument('note_id', help='Note filename')
    edit_parser = subparsers.add_parser('edit', help='Edit a note')
    edit_parser.add_argument('note_id', help='Note filename')
    delete_parser = subparsers.add_parser('delete', help='Delete a note')
    delete_parser.add_argument('note_id', help='Note filename')
    search_parser = subparsers.add_parser('search', help='Search notes')
    search_parser.add_argument('query', help='Search query')
    subparsers.add_parser('stats', help='Show notes statistics')
    args = parser.parse_args()
    if args.command == 'create':
        create_note()
    elif args.command == 'list':
        notes = list_notes(filter_tag=args.tag)
        if not notes:
            print("No notes found.")
        else:
            for filename, meta in notes:
                print(f"{filename}: {meta.get('title', '')} (tags: {', '.join(meta.get('tags', []))})")
    elif args.command == 'read':
        read_note(args.note_id)
    elif args.command == 'edit':
        edit_note(args.note_id)
    elif args.command == 'delete':
        delete_note(args.note_id)
    elif args.command == 'search':
        results = search_notes(args.query)
        if not results:
            print("No matching notes found.")
        else:
            for filename, meta in results:
                print(f"{filename}: {meta.get('title', '')}")
    elif args.command == 'stats':
        stats()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()


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