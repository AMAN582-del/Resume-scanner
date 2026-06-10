# Resume-scanner

A lightweight resume scanner for recruiters that compares resumes against a job description.

## Features
- Extracts important keywords from a job description
- Scores each resume by keyword match percentage
- Shows matched and missing keywords per candidate
- Ranks candidates from highest to lowest match score

## Usage

```bash
python resume_scanner.py --job /path/to/job_description.txt --resumes /path/to/resume1.txt /path/to/resume2.txt
```

## Run tests

```bash
python -m unittest discover -s tests
```