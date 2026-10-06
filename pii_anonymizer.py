import spacy
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def anonymize_text(text):
    doc = nlp(text)
    replacements = []

    # -------------------------------
    # spaCy NER detection
    # -------------------------------
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            replacements.append(
                (ent.start_char, ent.end_char, "[PERSON]")
            )

        elif ent.label_ == "ORG":
            replacements.append(
                (ent.start_char, ent.end_char, "[ORGANIZATION]")
            )

        elif ent.label_ in ["GPE", "LOC"]:
            replacements.append(
                (ent.start_char, ent.end_char, "[LOCATION]")
            )

    # -------------------------------
    # Email
    # -------------------------------
    for match in re.finditer(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        text
    ):
        replacements.append(
            (match.start(), match.end(), "[EMAIL]")
        )

    # -------------------------------
    # Indian phone number
    # -------------------------------
    for match in re.finditer(
        r'\b(?:\+91[-\s]?)?[6-9]\d{9}\b',
        text
    ):
        replacements.append(
            (match.start(), match.end(), "[PHONE]")
        )

    # -------------------------------
    # Date
    # -------------------------------

    # Numeric dates:
    # 12/09/2026
    # 12-09-2026
    # 12.09.2026
    for match in re.finditer(
        r'\b\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4}\b',
        text
    ):
        replacements.append(
            (match.start(), match.end(), "[DATE]")
        )


    # Dates containing month names:
    # 12 September 2026
    # 12 Sep 2026
    # September 12, 2026
    # Sep 12, 2026
    for match in re.finditer(
        r'\b(?:'
        r'\d{1,2}\s+'
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December|'
        r'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
        r'\s+\d{4}'
        r'|'
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December|'
        r'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
        r'\s+\d{1,2},?\s+\d{4}'
        r')\b',
        text,
        re.IGNORECASE
    ):
        replacements.append(
            (match.start(), match.end(), "[DATE]")
    )

    # -------------------------------
    # Age
    # -------------------------------
    for match in re.finditer(
        r'\b(?:age[d]?\s*)?(\d{1,3})\s*'
        r'(?:years?\s*old|yrs?\s*old|years?)\b',
        text,
        re.IGNORECASE
    ):
        replacements.append(
            (match.start(), match.end(), "[AGE]")
        )

    # -------------------------------
    # Patient ID
    # -------------------------------
    for match in re.finditer(
        r'\b(?:patient\s*id|patient\s*no|patient\s*number)'
        r'\s*[:#-]?\s*[A-Za-z0-9-]+\b',
        text,
        re.IGNORECASE
    ):
        replacements.append(
            (match.start(), match.end(), "[PATIENT_ID]")
        )

    # -------------------------------
    # Remove overlapping replacements
    # -------------------------------
    replacements.sort(key=lambda x: x[0])

    filtered = []
    last_end = -1

    for start, end, replacement in replacements:
        if start >= last_end:
            filtered.append((start, end, replacement))
            last_end = end

    # -------------------------------
    # Replace PII
    # -------------------------------
    result = text

    for start, end, replacement in reversed(filtered):
        result = result[:start] + replacement + result[end:]

    return result, len(filtered)