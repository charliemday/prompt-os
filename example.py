#!/usr/bin/env python3
"""
Example usage of PromptOS
"""

import os
from prompt_os import grade_prompt, view_prompt_log


def main():
    """Example usage of the prompt improvement tool"""

    # Example prompt
    original_prompt = "Write a story about a cat"

    print("🐱 PromptOS Example")
    print("=" * 50)

    # Grade the prompt
    print("📊 Grading the prompt...")
    grading = grade_prompt(original_prompt)
    print(f"Original: {grading['original_prompt']}")

    if "error" in grading["grading"]:
        print(f"Error: {grading['grading']['raw_response']}")
    else:
        scores = grading["grading"]["scores"]
        explanations = grading["grading"]["explanations"]

        print("\n📈 SCORES (1-10 scale):")
        print(f"  Ambiguity: {scores['ambiguity']}/10")
        print(f"  Contradictions: {scores['contradictions']}/10")
        print(f"  Context: {scores['context']}/10")

        print("\n📝 EXPLANATIONS:")
        print(f"  Ambiguity: {explanations['ambiguity']}")
        print(f"  Contradictions: {explanations['contradictions']}")
        print(f"  Context: {explanations['context']}")

        print(f"\n🎯 OVERALL: {grading['grading']['overall_assessment']}")
    print()

    # Show recent log entries
    print("📋 Recent prompt log entries:")
    log_content = view_prompt_log(limit=3)
    print(log_content)


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set your OPENAI_API_KEY environment variable")
        print("💡 You can create a .env file with: OPENAI_API_KEY=your_key_here")
        exit(1)

    main()
