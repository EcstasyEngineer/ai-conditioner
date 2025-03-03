# tests/test_utils.py
import unittest
from old.utils.convert_lines import process_file_to_template
import os

class TestUtils(unittest.TestCase):

    def test_template_creation(self):
        input_file = 'data/preconverted/test_input.txt'
        output_file = 'data/converted/test_output.txt'
        dominant_name = 'Master'
        subject_name = 'Slave'

        # Create a sample input file
        with open(input_file, 'w') as f:
            f.write('I obey {dominant_name}.\n')

        # Run the template creation
        process_file_to_template(input_file, output_file, dominant_name, subject_name)

        # Check if output file is created
        self.assertTrue(os.path.exists(output_file))

        # Read the output file and check contents
        with open(output_file, 'r') as f:
            content = f.read()
            self.assertIn('{subject_subjective} obey {dominant_name}.', content)

        # Clean up
        os.remove(input_file)
        os.remove(output_file)

if __name__ == '__main__':
    unittest.main()
