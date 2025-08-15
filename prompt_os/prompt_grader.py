"""
Prompt improvement functionality using LangChain
"""

import os
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import json
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()


class GradingResult(BaseModel):
    """Schema for prompt grading results"""

    ambiguity_score: int = Field(
        description="Ambiguity score (1-10 scale, 1=no ambiguity, 10=high ambiguity)",
        ge=1,
        le=10,
    )
    contradictions_score: int = Field(
        description="Contradictions score (1-10 scale, 1=no contradictions, 10=high contradictions)",
        ge=1,
        le=10,
    )
    context_score: int = Field(
        description="Context score (1-10 scale, 1=no context, 10=lots of context)",
        ge=1,
        le=10,
    )
    ambiguity_explanation: str = Field(
        description="Detailed explanation for the ambiguity score",
    )
    contradictions_explanation: str = Field(
        description="Detailed explanation for the contradictions score",
    )
    context_explanation: str = Field(
        description="Detailed explanation for the context score",
    )

    overall_assessment: str = Field(
        description="Brief overall assessment of the prompt quality",
        examples=["This is a well-structured prompt with good clarity and context"],
    )


def grade_prompt(prompt: str, model: str = "gpt-5") -> Optional[dict]:
    """
    Grade a prompt based on ambiguity, contradictions, and context.

    Args:
        prompt: The prompt to grade
        model: OpenAI model to use

    Returns:
        Dictionary with grading results including scores and explanations
    """

    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is required")

    llm = ChatOpenAI(
        model=model, temperature=0, api_key=os.getenv("OPENAI_API_KEY")
    ).bind_tools([GradingResult])

    # Read system prompt from file
    prompt_file = "prompt_os/prompts/prompt_grader.txt"
    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            system_prompt = f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

    # Create the grading message
    messages = [HumanMessage(content=f"{system_prompt}\n\nPrompt to grade: {prompt}")]

    response = llm.invoke(messages)

    # Extract the tool call result
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        grading_result = GradingResult.model_validate_json(
            json.dumps(tool_call["args"])
        )

        result = {
            "ambiguity": {
                "score": grading_result.ambiguity_score,
                "explanation": grading_result.ambiguity_explanation,
            },
            "contradictions": {
                "score": grading_result.contradictions_score,
                "explanation": grading_result.contradictions_explanation,
            },
            "context": {
                "score": grading_result.context_score,
                "explanation": grading_result.context_explanation,
            },
            "overall_assessment": grading_result.overall_assessment,
            "original_prompt": prompt,
        }

        # Log the prompt and grading summary
        return result
    else:
        return None
