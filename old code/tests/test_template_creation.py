# tests/test_template_creation.py
import unittest
import os
from old.utils.convert_lines import load_verb_conjugations

class TestTemplateCreation(unittest.TestCase):

    def test_load_verb_conjugations(self):
        verb_file = 'app/utils/verb_conjugations.txt'
        # Ensure the verb conjugations file exists
        self.assertTrue(os.path.exists(verb_file))

        verbs_1ps, verbs_1pp, verbs_2ps, verbs_3ps = load_verb_conjugations(verb_file)
        self.assertIsInstance(verbs_1ps, dict)
        self.assertIsInstance(verbs_3ps, dict)
        self.assertIn('am', verbs_1ps)
        self.assertIn('is', verbs_3ps)

if __name__ == '__main__':
    unittest.main()
