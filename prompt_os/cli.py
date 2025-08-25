"""
Command-line interface for PromptOS
"""

import argparse
import sys
from .prompt_grader import grade_prompt
from yaspin import yaspin


@yaspin(text="Grading prompt...")
def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="PromptOS - Grade your prompts using PromptOS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  prompt-os "Write a story about a cat"
  prompt-os "Write a story about a cat" --grade
  prompt-os "Write a story about a cat" --model gpt-4
        """,
    )

    parser.add_argument(
        "prompt",
        help="The prompt to grade",
    )

    parser.add_argument(
        "--model",
        "-m",
        default="gpt-5",
        help="OpenAI model to use (default: gpt-5)",
    )

    parser.add_argument(
        "--grade",
        "-g",
        action="store_true",
        help="Grade the prompt on ambiguity, contradictions, and context",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show additional information"
    )

    args = parser.parse_args()

    try:
        if not args.prompt:
            print("❌ Error: Please provide a prompt to grade")
            sys.exit(1)

        else:
            # Default action: grade the prompt
            if args.verbose:
                print("📊 Grading prompt...")

            result = grade_prompt(args.prompt, args.model)

            if result is None:
                print("❌ Error: No result received from the grading")
                sys.exit(1)

            print("\n" + "=" * 50)
            print("📊 PROMPT GRADING")
            print("=" * 50)
            print(f"Original prompt: {result['original_prompt']}")
            print()

            print("📈 SCORES (1-10 scale):")
            print(
                f"  Ambiguity (10 is high amount of ambiguity): {result['ambiguity']['score']}/10"
            )
            print(
                f"  Contradictions (10 is high number contradictions): {result['contradictions']['score']}/10"
            )
            print(
                f"  Lack of Context (10 is a complete lack of context): {result['context']['score']}/10"
            )
            print(
                f"  Grammar (10 is very poor grammar): {result['grammar']['score']}/10"
            )
            print()

            print("📝 EXPLANATIONS:")
            print(f"  Ambiguity: {result['ambiguity']['explanation']}")
            print(f"  Contradictions: {result['contradictions']['explanation']}")
            print(f"  Context: {result['context']['explanation']}")
            print(f"  Grammar: {result['grammar']['explanation']}")
            print()

            print(f"  Overall score: {result['overall_score']}/10")
            print("🎯 OVERALL ASSESSMENT:")
            print(f"  {result['overall_assessment']}")
            print()

    except ValueError as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure to set your OPENAI_API_KEY environment variable")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
