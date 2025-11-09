# SkillSense - Graph-based Skill Recommendation System

SkillSense provides not only personalized but also explainable recommendations that support informed career growth.

Challenge Tackled: Structured skill profile generation with evidence and confidence scores ✅ Recommendation of skills based on users who share similar interests (this enables skill-gap analysis) ✅ Limited training data: user interactions, interested roles, skills stored in a graph to improve future recommendations ✅Mutli-source support- system takes pdf, docx format of resume, professional summaries, portfolio or linked pages as pdf, docx ✅ Scalability- graph expands as more users interact with the system, improving the quality of recommendations ✅ 

Interact with the app (Caution: Free tier DB used, limited users):  

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
