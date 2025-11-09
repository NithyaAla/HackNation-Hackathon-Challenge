from skill_extraction import get_skill_embedding
import numpy as np

def generate_recommendations(db, user_id):
    # Step 1: Get recommended skills
    rec_skills = db.get_recommendations(user_id)  # list of skill names

    # Step 2: Get existing user skills
    user_skill_data = db.get_user_skills(user_id)  # returns [(skill, conf), ...]
    user_skill_embeddings = [
        get_skill_embedding(skill)
        for skill, _ in user_skill_data
        if get_skill_embedding(skill) is not None
    ]

    results = []

    for rec_skill in rec_skills:
        rec_emb = get_skill_embedding(rec_skill)
        if rec_emb is None:
            results.append((rec_skill, ""))  # fallback
            db.log_interaction(user_id, "VIEWED_RECOMMENDATION", skill=rec_skill)
            continue

        # Compute similarity to user's best skill
        sims = [np.dot(rec_emb, emb) for emb in user_skill_embeddings] if user_skill_embeddings else []
        max_sim = float(max(sims)) if sims else 0.40

        # Scale & normalize confidence
        conf_score = min(round(max_sim * 1.2, 2), 0.98)

        results.append((rec_skill, conf_score))

        # Log
        db.log_interaction(user_id, "VIEWED_RECOMMENDATION", skill=rec_skill)

    return sorted(results, key=lambda x: x[1], reverse=True)
