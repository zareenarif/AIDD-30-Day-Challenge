
from config.sdk_client import model, config  # Assume SDK config for Gemini
from agents import Agent, Runner
from tools import extract_pdf_text, load_pdf_text, store_pdf_text

study_agent = Agent(
    name="StudyNotesAgent",
    instructions="""
    You are a Study Assistant Agent.
    When asked for summary, read the PDF text and create clear structured study notes.
    When asked to create quizzes, use ONLY the original PDF text. Do NOT use the summary.
    Generate MCQs or mixed quiz formats depending on user request.
    """,
    model=model,
    tools=[extract_pdf_text, load_pdf_text, store_pdf_text]
)

async def generate_agent_response(prompt: str):
    return await Runner.run(study_agent, prompt, run_config=config)
