import re
from .ml import Vectorizer

def extract_keywords(required_skills, soft_skills, jd_text):
    if not hasattr(Vectorizer, "vocabulary_"):
        return []
    required_skills_lc = {s.lower() for s in required_skills}
    soft_skills_lc = {s.lower() for s in soft_skills}


    generic_verbs = {
        "develop", "maintain", "design", "build", "create",
        "implement", "integrate", "write", "work",
        "ensure", "participate", "collaborate"
    }
    custom_stop_phrases = {
        "looking for", "responsible for", "experience in",
        "knowledge of", "ability to", "strong understanding",
        "hands on", "hands-on", "good knowledge","graduate", "pg", "postgraduate", "ug",
        "degree", "education", "any graduate", "industry", "department", "role category",
        "employment type", "services", "consulting", "experience", "knowledge", "understanding", "ability","responsibility", "responsibilities", "skills", "developer"
    }

    vect = Vectorizer.transform([jd_text])
    terms = Vectorizer.get_feature_names_out()
    scores = vect.toarray()[0]

    ranked_terms = sorted(
        zip(terms, scores),
        key=lambda x:(len(x[0].split()),x[1]),
        reverse=True
    )

    final_keywords = []

    for term, score in ranked_terms:
        term_lc = term.lower()

        if score == 0:
            continue
        if len(term_lc) <= 3:
            continue
        if term_lc in required_skills_lc:
            continue
        if term_lc in soft_skills_lc:
            continue
        if term_lc.split()[0] in generic_verbs:
            continue
        if any(p in term_lc for p in custom_stop_phrases):
            continue
        if not re.search(r"[a-zA-Z]", term_lc):
            continue

        final_keywords.append(term.title())

        if len(final_keywords) == 10:
            break

    return final_keywords
