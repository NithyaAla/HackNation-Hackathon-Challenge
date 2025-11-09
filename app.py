import gradio as gr
from neo4j_connectors import GraphDB
from skill_extraction import extract_skills
from recommender import generate_recommendations
import uuid
from pypdf import PdfReader
import docx

db = GraphDB()

EDUCATION_OPTIONS = ["High School", "Undergraduate", "Graduate"]
STATUS_OPTIONS = ["Student", "Employed", "Continuous Learning"]

def read_file(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file.name)
        return "\n".join(page.extract_text() for page in reader.pages)
    elif file.name.endswith(".docx"):
        doc = docx.Document(file.name)
        return "\n".join(p.text for p in doc.paragraphs)
    return ""

def run_pipeline(education, status, role, file):
    user_id = str(uuid.uuid4())
    db.create_or_update_user(user_id, education, status, role)
    db.log_interaction(user_id, type_="PROFILE_CREATED", details=role, role=role)

    text = read_file(file)
    extracted = extract_skills(text, threshold=0.50)

    # Store extracted skills + evidence trail
    for skill, conf, evidence in extracted:
        db.add_skill(user_id, skill, conf)
        db.log_interaction(user_id, type_="SKILL_ADDED", skill=skill, details=evidence)

    # Format extracted skills into collapsible HTML
    extracted_html = "<h2 style='font-weight:bold;'>Extracted Skills</h2>\n<p><i>Tap the triangle to see evidence for each skill.</i></p>\n"
    for skill, conf, evidence in extracted:
        extracted_html += f"""
        <details>
            <summary><b>{skill}</b> — confidence {conf}</summary>
            <p style="margin-left:10px;">Evidence: {evidence}</p>
        </details>
        """

    # Generate recommendations (no evidence)
    recommendations = generate_recommendations(db, user_id)
    recommended_df = [[r[0], r[1]] for r in recommendations]

    # Recommended skills heading HTML
    recommended_html = "<h2 style='font-weight:bold;'>Recommended Skills</h2>\n<p><i>Skills recommended based on similar users in the system.</i></p>"

    return extracted_html, recommended_html, recommended_df

# ---------------- Gradio UI ----------------
interface = gr.Interface(
    fn=run_pipeline,
    inputs=[
        gr.Radio(EDUCATION_OPTIONS, label="Education"),
        gr.Radio(STATUS_OPTIONS, label="Professional Status"),
        gr.Textbox(label="Desired Role", placeholder="Enter the role you are interested in"),
        gr.File(label="Upload professional document (.pdf or .docx)", file_types=[".pdf", ".docx"], type="filepath")
    ],
    outputs=[
        gr.HTML(
            value="""
            <h2 style='font-weight:bold;'>Extracted Skills</h2>
            <p><i>Tap the triangle to see evidence for each skill.</i></p>
            """,
            label="Extracted Skills + Evidence Trails"
        ),
        gr.HTML(
            value="""
            <h2 style='font-weight:bold;'>Recommended Skills</h2>
            <p><i>Skills recommended based on similar users in the system.</i></p>
            """,
            label="Recommended Skills Header"
        ),
        gr.Dataframe(
            headers=["Skill", "Confidence"],
            value=[],  # empty dataframe skeleton
            label="Recommended Skills"
        )
    ],
    title="SkillSense",
    description="""
    Upload your professional document (resume, CV, professional summary, or pdf/docx of portfolio, linkedin, etc.) 
    and get a structured skill profile. Get skill recommendations based on other users' skills with similar interests. 
(Currently resume,CV uploads render high-quality recommendations, uploaded documents are stored securely in a graph database for improving recommendation quality)
    """
)

interface.launch()
