import unittest
import tempfile
import shutil
from pathlib import Path



# Import functions and modules from your split files
import notes_utils
import notes_commands

class TestPersonalNotesCLI(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for notes to isolate tests
        self.test_dir = tempfile.mkdtemp()
        notes_commands.NOTES_DIR = Path(self.test_dir)

    def tearDown(self):
        # Remove temp notes directory after each test
        shutil.rmtree(self.test_dir)

    def test_create_note_file(self):
        # Simulate creating a note and writing to file without user prompts
        title = "Test Note"
        tags = ['test', 'sample']
        created = notes_utils.iso_now()
        metadata = {
            'title': title,
            'created': created,
            'modified': created,
            'tags': tags,
        }
        content = "This is a test note content."
        filename = notes_utils.generate_note_filename(title)
        filepath = notes_commands.NOTES_DIR / filename

        notes_utils.write_note_file(filepath, metadata, content)

        self.assertTrue(filepath.exists())

        # Read it back
        meta, cont = notes_utils.read_note_file(filepath)
        self.assertIsNotNone(meta)
        self.assertEqual(meta['title'], title)
        self.assertEqual(cont, content)

    def test_list_notes_filter_tag(self):
        # Create two notes, one with a tag, one without
        meta1 = {
            'title': 'Note One',
            'created': notes_utils.iso_now(),
            'modified': notes_utils.iso_now(),
            'tags': ['work']
        }
        content1 = "Content 1"
        file1 = notes_commands.NOTES_DIR / notes_utils.generate_note_filename(meta1['title'])
        notes_utils.write_note_file(file1, meta1, content1)

        meta2 = {
            'title': 'Note Two',
            'created': notes_utils.iso_now(),
            'modified': notes_utils.iso_now(),
            'tags': ['personal']
        }
        content2 = "Content 2"
        file2 = notes_commands.NOTES_DIR / notes_utils.generate_note_filename(meta2['title'])
        notes_utils.write_note_file(file2, meta2, content2)

        all_notes = notes_commands.list_notes()
        self.assertEqual(len(all_notes), 2)
        
        filtered_notes = notes_commands.list_notes(filter_tag='work')
        self.assertEqual(len(filtered_notes), 1)
        self.assertEqual(filtered_notes[0][1]['title'], 'Note One')

    def test_search_notes(self):
        meta = {
            'title': 'Shopping list',
            'created': notes_utils.iso_now(),
            'modified': notes_utils.iso_now(),
            'tags': ['errands']
        }
        content = "Buy milk, eggs, and bread."
        file = notes_commands.NOTES_DIR / notes_utils.generate_note_filename(meta['title'])
        notes_utils.write_note_file(file, meta, content)

        results = notes_commands.search_notes("milk")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1]['title'], meta['title'])

        results_empty = notes_commands.search_notes("nothingfound")
        self.assertEqual(len(results_empty), 0)

    def test_delete_note(self):
        meta = {
            'title': 'Delete test',
            'created': notes_utils.iso_now(),
            'modified': notes_utils.iso_now(),
            'tags': []
        }
        content = "This note will be deleted."
        filename = notes_utils.generate_note_filename(meta['title'])
        filepath = notes_commands.NOTES_DIR / filename
        notes_utils.write_note_file(filepath, meta, content)
        self.assertTrue(filepath.exists())

        # Delete the note
        notes_commands.delete_note(filename)
        self.assertFalse(filepath.exists())

    def test_read_note_nonexistent(self):
        # Should print warning, here we just test that no exception is thrown
        try:
            notes_commands.read_note("nonexistent.note")
        except Exception as e:
            self.fail(f"read_note raised an exception unexpectedly: {e}")

    def test_sanitize_filename(self):
        dirty_name = "My *Invalid: Note? Title/Name"
        clean_name = notes_utils.sanitize_filename(dirty_name)
        self.assertNotIn("*", clean_name)
        self.assertNotIn(":", clean_name)
        self.assertNotIn("?", clean_name)
        self.assertNotIn("/", clean_name)
        self.assertTrue(len(clean_name) > 0)

if __name__ == '__main__':
    unittest.main()
