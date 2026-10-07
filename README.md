# CV Extraction Service

A full-stack application that intelligently extracts and parses candidate information (Name, Email, Skills, Education, and Experience) from uploaded CVs (PDF and DOCX).

## 🚀 Features

- **CV Upload & Text Extraction**: Built with Node.js and Express. It extracts raw text from PDF and DOCX files using `pdf-parse` and `mammoth`.
- **Intelligent NLP Parsing**: A completely dependency-free Python backend service that heuristically analyzes the extracted CV text to categorize information into structured data.
- **Premium User Interface**: A modern, glassmorphism-themed frontend that lets users upload a CV, review the parsed data in an editable format, and save it to the candidate profile database.
- **Automated Testing**: Fully tested backend routes using `Jest` and `Supertest`.

## 🛠️ Tech Stack

- **Frontend**: HTML5, Vanilla CSS (Glassmorphism design), Vanilla JavaScript
- **Backend (Extraction & API)**: Node.js, Express, Multer
- **Backend (NLP Service)**: Python 3 (Standard Library: `http.server`, `re`, `json`)

## 📦 Installation

### 1. Clone the repository
Ensure you are in the root directory `CV Extraction`.

### 2. Install Node.js Dependencies
```bash
npm install
```
*(This installs Express, Multer, pdf-parse, mammoth, and Jest).*

### 3. Python Dependencies
The NLP service is intentionally built using Python's standard library, meaning **no `pip install` is required**!

## 🏃‍♂️ Running the Services

To run the application, you need to start both the Node.js server and the Python NLP server.

### Start the Python NLP Server (Port 8000)
Open a terminal and run:
```bash
cd nlp_service
python main.py
```

### Start the Node.js Application (Port 3000)
Open a second terminal and run:
```bash
node server.js
```

## 🌐 Usage

1. Open your web browser and navigate to `http://localhost:3000`.
2. Drag and drop (or browse for) a `.pdf` or `.docx` CV file.
3. The system will automatically:
   - Extract the text in Node.js.
   - Send the text to the Python NLP service.
   - Return the structured data and populate the UI fields.
4. Review the extracted data and click **Apply to Profile** to save the candidate to the system.

## 📂 Project Structure

```text
d:\CV Extraction\
├── app.js                 # Main Express application (Routes & Extraction)
├── server.js              # Entry point for the Node.js server
├── app.test.js            # Jest test suite for the Node APIs
├── package.json           # Node.js dependencies
│
├── public/                # Frontend UI
│   ├── index.html         # User Interface structure
│   ├── style.css          # Premium Glassmorphism styling
│   └── script.js          # File upload & profile population logic
│
└── nlp_service/           # Python NLP Microservice
    ├── main.py            # HTTP Server exposing the /parse endpoint
    ├── parser.py          # Regex & heuristic text parsing logic
    └── test_main.py       # Unittest suite for the parser
```
