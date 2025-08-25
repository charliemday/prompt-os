"""
Prompt improvement functionality using LangChain
"""

import os
from typing import Optional
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
    grammar_score: int = Field(
        description="Grammar score (1-10 scale, 1=perfect grammar, 10=very poor grammar)",
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
    grammar_explanation: str = Field(
        description="Detailed explanation for the grammar score",
    )

    overall_assessment: str = Field(
        description="Brief overall assessment of the prompt quality",
        examples=["This is a well-structured prompt with good clarity and context"],
    )


def calculate_overall_score(result: GradingResult) -> int:
    """Calculate the overall score based on the scores of the individual categories"""

    try:
        # Take the reverse as we want low values to indicate a poor prompt
        ambiguity_score = result.ambiguity_score
        contradictions_score = result.contradictions_score
        context_score = result.context_score
        grammar_score = result.grammar_score

        # Reverse the scores: high = good, low = bad, with 1 as the worst possible score
        # Subtract from 11 so that a score of 10 (worst) becomes 1, and a score of 1 (best) becomes 10
        reversed_ambiguity = 11 - ambiguity_score
        reversed_contradictions = 11 - contradictions_score
        reversed_context = 11 - context_score
        reversed_grammar = 11 - grammar_score

        return int(
            (
                reversed_ambiguity
                + reversed_contradictions
                + reversed_context
                + reversed_grammar
            )
            // 4
        )
    except:
        print("Error calculating overall score")
        return 0


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
            "grammar": {
                "score": grading_result.grammar_score,
                "explanation": grading_result.grammar_explanation,
            },
            "overall_score": calculate_overall_score(grading_result),
            "overall_assessment": grading_result.overall_assessment,
            "original_prompt": prompt,
        }

        # Log the prompt and grading summary
        return result
    else:
        return None
