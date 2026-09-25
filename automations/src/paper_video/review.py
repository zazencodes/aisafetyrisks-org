"""Independent science review of the storyboard and the web page."""

from paper_video.context import as_yaml, paper_header, paper_text, system
from paper_video.llm import Provider, generate
from paper_video.models import Notes, PaperRecord, ScienceReview


def science_review(provider: Provider, record: PaperRecord, pages: list[str], notes: Notes,
                   subject: str, content: str) -> ScienceReview:
    prompt = (
        f"{paper_header(record)}\n\n# Full paper text\n\n{paper_text(pages)}\n\n"
        f"# Reading notes the explainer was built from\n\n{as_yaml(notes)}\n\n"
        f"# The {subject} to review\n\n{content}"
    )
    return generate(provider, system("science_review"), prompt, ScienceReview)


def blocking(review: ScienceReview) -> list:
    return [i for i in review.issues if i.severity in ("blocker", "major")]


def issues_text(review: ScienceReview) -> str:
    return "\n".join(
        f"- [{i.severity}/{i.category}] {i.location}: {i.problem} Fix: {i.suggested_fix}" for i in blocking(review)
    )
