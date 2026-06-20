import logging
from langchain_openai import ChatOpenAI
from backend.schemas.models import StartupState, ProcessedIdea
from backend.config import settings

logger = logging.getLogger(__name__)

_llm = ChatOpenAI(
    model=settings.model_name,
    api_key=settings.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
    max_tokens=1024,
    max_retries=3,
).with_structured_output(ProcessedIdea)

_SYSTEM = """You are a business analyst. Extract and structure the startup idea provided by the user.
Return ONLY the structured fields. Be concise and specific. If geography is not mentioned, default to "India"."""


async def run_input_processor(state: StartupState) -> dict:
    new_events = [{"type": "agent_start", "agent": "input_processor"}]

    try:
        result: ProcessedIdea = await _llm.ainvoke([
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": state["raw_idea"]},
        ])
        new_events.append({"type": "agent_complete", "agent": "input_processor", "data": result.model_dump()})
        return {"processed_idea": result, "stream_events": new_events, "agent_errors": []}

    except Exception as e:
        logger.error(f"input_processor FAILED: {type(e).__name__}: {e}", exc_info=True)
        new_events.append({"type": "error", "agent": "input_processor", "message": str(e)})
        return {"processed_idea": None, "stream_events": new_events, "agent_errors": [f"input_processor: {e}"]}
