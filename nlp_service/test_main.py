import unittest
from parser import parse_cv

class TestNLPParser(unittest.TestCase):
    def test_parse_empty(self):
        data = parse_cv("   \n  ")
        self.assertIsNone(data["name"])
        self.assertIsNone(data["email"])
        self.assertEqual(data["skills"], [])
        self.assertEqual(data["education"], [])
        self.assertEqual(data["experience"], [])

    def test_parse_valid(self):
        sample_cv = """
        John Doe
        Email: john.doe@example.com
        
        Education:
        Bachelor of Science in Computer Science, University of Technology
        
        Experience:
        Software Developer at Tech Corp (2020 - Present)
        
        Skills:
        Python, Node.js, FastAPI, React
        """
        
        data = parse_cv(sample_cv)
        
        # Check email
        self.assertEqual(data["email"], "john.doe@example.com")
        
        # Check name heuristic (first non-empty line)
        self.assertEqual(data["name"], "John Doe")
        
        # Check skills
        extracted_skills = set(data["skills"])
        expected_skills = {"Python", "Node.js", "FastAPI", "React"}
        self.assertTrue(expected_skills.issubset(extracted_skills))
        
        # Check education
        self.assertTrue(len(data["education"]) > 0)
        self.assertTrue(any("Bachelor of Science" in ed for ed in data["education"]))
        
        # Check experience
        self.assertTrue(len(data["experience"]) > 0)
        self.assertTrue(any("Software Developer" in ex for ex in data["experience"]))

if __name__ == '__main__':
    unittest.main()
