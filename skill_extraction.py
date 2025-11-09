# skill_extraction.py

import json
import spacy
import numpy as np
from sentence_transformers import SentenceTransformer
from spacy.cli import download

# Ensure spaCy model is available
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load skills from JSON
with open("skills_vocab.json", "r", encoding="utf-8") as f:
    SKILL_VOCAB = json.load(f)["skills"]

# Precompute embeddings
skill_embeddings = model.encode(SKILL_VOCAB, convert_to_numpy=True, normalize_embeddings=True)

# Map skill -> embedding for quick lookup
SKILL_TO_EMB = {skill: emb for skill, emb in zip(SKILL_VOCAB, skill_embeddings)}

def extract_skills(text, threshold=0.50):
    """
    Extract skills from text.
    Returns list of (skill, confidence, evidence_sentences)
    """
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    if not sentences:
        return []

    sentence_embeddings = model.encode(sentences, convert_to_numpy=True, normalize_embeddings=True)
    skill_confidences = {}
    skill_evidence = {}

    # Iterate skill-by-skill
    for j, skill_emb in enumerate(skill_embeddings):
        sims = np.dot(sentence_embeddings, skill_emb)  # similarity across sentences
        max_sim_idx = int(np.argmax(sims))
        max_sim = float(sims[max_sim_idx])

        if max_sim >= threshold:
            skill = SKILL_VOCAB[j]
            skill_confidences[skill] = round(max_sim, 2)
            # Take the sentence with highest similarity as evidence
            skill_evidence[skill] = sentences[max_sim_idx]

    # Return sorted list of (skill, confidence, evidence)
    results = [(skill, skill_confidences[skill], skill_evidence[skill]) for skill in skill_confidences]
    results.sort(key=lambda x: x[1], reverse=True)
    return results


# --- NEW FUNCTION ---
def get_skill_embedding(skill_name):
    """Return the embedding vector for a skill, or None if not in vocab"""
    return SKILL_TO_EMB.get(skill_name)
