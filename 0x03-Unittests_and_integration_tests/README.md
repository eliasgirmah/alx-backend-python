# 📦 0x03. Unittests and Integration Tests

This project is part of the **ALX Backend Specialization** and focuses on writing **unit tests**, **integration tests**, and using techniques like **mocking**, **parameterization**, and **memoization** in Python.

---

## 🧰 Technologies Used

- Python 3.12+
- `unittest` – built-in Python test framework
- `parameterized` – for parameterized test cases
- `requests` – for making HTTP requests
- `unittest.mock` – for mocking APIs and internal calls
- `venv` – Python virtual environment

---

## 📁 Project Structure

0x03-Unittests_and_integration_tests/
│
├── utils.py # Utility functions to be tested
├── client.py # GitHubOrgClient class for GitHub API
├── test_utils.py # Unit tests for utils.py
├── test_client.py # Unit & integration tests for client.py
└── README.md # This file

yaml
Copy
Edit

---

## 📚 Concepts Covered

- ✅ Writing unit tests using `unittest.TestCase`
- 🧪 Using `@parameterized.expand` to test with multiple inputs
- 💣 Testing exception cases using `assertRaises`
- 🎭 Mocking API responses using `patch` and `Mock`
- 🔁 Memoization and testing cached results
- 🔍 Differentiating between unit tests and integration tests

---

## ▶️ Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/alx-backend-python.git
cd alx-backend-python/0x03-Unittests_and_integration_tests
2. Create and activate a virtual environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows
3. Install dependencies
bash
Copy
Edit
pip install requests parameterized
4. Run tests
Run all tests:

bash
Copy
Edit
python -m unittest discover
Run a specific test file:

bash
Copy
Edit
python -m unittest test_utils.py
🧪 Example Tests
✅ Unit test with parameterization:
python
Copy
Edit
@parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a",), {"b": 2}),
    ({"a": {"b": 2}}, ("a", "b"), 2),
])
def test_access_nested_map(self, nested_map, path, expected):
    self.assertEqual(access_nested_map(nested_map, path), expected)
💥 Exception test:
python
Copy
Edit
def test_key_error(self):
    with self.assertRaises(KeyError):
        access_nested_map({}, ("a",))