"""LLM Narrative and Behavioral Virtual Population Package for NAOMI."""

from src.llm.prompts import (
    EXECUTIVE_SYSTEM_PROMPT,
    USER_BRIEF_TEMPLATE,
    DISCLAIMER_TEXT,
    build_narrative_prompt,
)
from src.llm.fallback import generate_fallback_narrative
from src.llm.narrator import (
    generate_narrative,
    validate_narrative_numerics,
    extract_numbers_from_text,
    extract_numbers_from_dict,
)
from src.llm.virtual_population import (
    CustomerPersona,
    DEFAULT_PERSONAS,
    elicit_persona_purchase_probability,
    simulate_virtual_population_demand,
)

__all__ = [
    "EXECUTIVE_SYSTEM_PROMPT",
    "USER_BRIEF_TEMPLATE",
    "DISCLAIMER_TEXT",
    "build_narrative_prompt",
    "generate_fallback_narrative",
    "generate_narrative",
    "validate_narrative_numerics",
    "extract_numbers_from_text",
    "extract_numbers_from_dict",
    "CustomerPersona",
    "DEFAULT_PERSONAS",
    "elicit_persona_purchase_probability",
    "simulate_virtual_population_demand",
]

