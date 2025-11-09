# SkillSense - Graph-based Skill Recommendation System

SkillSense is a graph-based skill recommendation system designed to help individuals understand their current skill landscape and identify what to learn next based on what skills their peers possess. Today, learners struggle to know which skills matter for specific roles, and how to prioritize their learning path. At the same time, many recommendation systems need large datasets to work effectively. I built SkillSense to solve both challenges.

The system extracts skills from resumes, professional summaries, portfolios, or even LinkedIn exports(pdf, docx), using semantic language models to ensure accuracy and context. Each skill is returned with evidence pulled directly from the user's documents, along with a confidence score, so the results remain transparent and trustworthy. The extracted skills are then stored in a Neo4j graph along with interaction history.

What makes SkillSense powerful is its recommendation engine. By analyzing users with similar skill profiles and career interests, the system identifies meaningful skill gaps and proposes new skills to learn—again, with confidence scores. Because the graph grows as more users interact, recommendations continuously improve without requiring a large initial dataset.

In short, SkillSense provides not only personalized but also explainable recommendations that support informed career growth and lifelong learning.

Challenge Tackled: Structured skill profile generation with evidence and confidence scores ✅ Recommendation of skills based on users who share similar interests (this enables skill-gap analysis) ✅ Limited training data: user interactions, interested roles, skills stored in a graph to improve future recommendations ✅Mutli-source support- system takes pdf, docx format of resume, professional summaries, portfolio or linked pages as pdf, docx ✅ Scalability- graph expands as more users interact with the system, improving the quality of recommendations ✅ 

Interact with the app (Caution: Free tier DB used, limited users):  https://huggingface.co/spaces/NithyaAla/RecSys_Skills

Setup & Deployment (Developer Instructions)

The application can be run locally or deployed on Hugging Face Spaces. Below are the steps for both workflows.

1. Clone the Repository
git clone <your-repo-url>
cd <repo-folder-name>

2. Create and Activate a Virtual Environment (Recommended)
python3 -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

3. Install Dependencies
pip install -r requirements.txt

**The json file has the skill vocabulary used. It is a sample skill set and can be extended. Make sure to use the same json format as skills_vocab.json if adding more skills. 

4. Configure Secrets

The application uses environment variables for API keys (Neo4j credentials).

Local Development:

Create a .env file:

NEO4J_URI=<your-uri>
NEO4J_USER=<your-user>
NEO4J_PASSWORD=<your-password>


Hugging Face Deployment:

On your Space page:

Settings → Variables and Secrets → Add Secrets


Add each key exactly as referenced in app.py.

5. Run Locally
python app.py


The UI will open in your browser (typically at http://127.0.0.1:7860).

Deploying to Hugging Face Spaces

Go to: https://huggingface.co/spaces

Click Create New Space

Choose:

Space SDK: Gradio

Visibility: Public or Private

Either:

Upload your project files, or

Select “Repository → Add Files → Upload directory”

Or push from local:

git remote add origin https://huggingface.co/spaces/<user>/<space-name>
git push --set-upstream origin main


As soon as the repository contains app.py (or main.py) and requirements.txt, the Space will auto-build and launch.
