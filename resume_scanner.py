import argparse
import re
from collections import Counter


STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "are",
    "you",
    "your",
    "will",
    "this",
    "that",
    "from",
    "have",
    "has",
    "our",
    "their",
    "into",
    "about",
    "job",
    "role",
    "years",
    "year",
    "experience",
    "looking",
    "required",
    "skills",
    "skill",
    "candidate",
    "ability",
}

MIN_TOKEN_LENGTH = 2


def _tokenize(text):
    tokens = []
    for token in re.findall(r"[a-zA-Z0-9+#.]+", text):
        cleaned = token.strip(".").lower()
        if cleaned:
            tokens.append(cleaned)
    return tokens


def extract_keywords(job_description, max_keywords=20):
    tokens = [
        token for token in _tokenize(job_description) if len(token) > MIN_TOKEN_LENGTH and token not in STOPWORDS
    ]
    counts = Counter(tokens)
    return [word for word, _ in counts.most_common(max_keywords)]


def score_resume(job_description, resume_text):
    keywords = extract_keywords(job_description)
    if not keywords:
        return {"score": 0.0, "matched_keywords": [], "missing_keywords": []}

    resume_tokens = set(_tokenize(resume_text))
    matched = [keyword for keyword in keywords if keyword in resume_tokens]
    missing = [keyword for keyword in keywords if keyword not in resume_tokens]
    score = round((len(matched) / len(keywords)) * 100, 2)

    return {"score": score, "matched_keywords": matched, "missing_keywords": missing}


def rank_resumes(job_description, resumes):
    """Return resumes sorted by score descending, then candidate name ascending."""
    ranked = []
    for candidate_name, resume_text in resumes.items():
        result = score_resume(job_description, resume_text)
        ranked.append(
            {
                "candidate": candidate_name,
                "score": result["score"],
                "matched_keywords": result["matched_keywords"],
                "missing_keywords": result["missing_keywords"],
            }
        )
    return sorted(ranked, key=lambda item: (-item["score"], item["candidate"].lower()))


def _read_text(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def main():
    parser = argparse.ArgumentParser(description="Scan resumes against a job description.")
    parser.add_argument("--job", required=True, help="Path to job description text file")
    parser.add_argument("--resumes", required=True, nargs="+", help="Paths to resume text files")
    args = parser.parse_args()

    job_description = _read_text(args.job)
    resumes = {path: _read_text(path) for path in args.resumes}
    ranked = rank_resumes(job_description, resumes)

    print("Resume Match Results")
    print("====================")
    for item in ranked:
        print(f"\nCandidate: {item['candidate']}")
        print(f"Score: {item['score']}%")
        print(f"Matched Keywords: {', '.join(item['matched_keywords']) if item['matched_keywords'] else 'None'}")
        print(f"Missing Keywords: {', '.join(item['missing_keywords']) if item['missing_keywords'] else 'None'}")


if __name__ == "__main__":
    main()
