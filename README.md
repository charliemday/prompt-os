# PromptOS 🚀

A Python tool to grade your prompts in terms of Ambiguity, Contradictions, and Contextual Awareness.

## Features

- **Prompt Grading**: Grade prompts on ambiguity, contradictions, and context (1-10 scale)
- **CLI Interface**: Easy-to-use command-line tool
- **Python API**: Simple import and use in your Python projects

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd prompt-os
   ```

2. **Install dependencies and CLI**:

   ```bash
   poetry install
   poetry run pip install -e .
   ```

3. **Set up your OpenAI API key**:

   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Create the grading prompt file**:
   ```bash
   mkdir -p prompt_os/prompts
   # Create prompt_os/prompts/prompt_grader.txt with your grading instructions
   ```

## Usage

### Command Line Interface

**Grade a prompt**:

```bash
prompt-os "Write a story about a cat"
```

**Grade with explicit flag**:

```bash
prompt-os "Write a story about a cat" --grade
```

**Use different model**:

```bash
prompt-os "Write a story about a cat" --model gpt-4
```

**Available options**:

- `--model` / `-m`: OpenAI model to use (default: `gpt-5`)
- `--grade` / `-g`: Grade the prompt on ambiguity, contradictions, and context (default action)

- `--verbose` / `-v`: Show additional information

### Python API

```python
from prompt_os import grade_prompt

# Grade a prompt
grading = grade_prompt("Write a story about a cat")  # Uses GPT-5 by default
print(f"Ambiguity: {grading['ambiguity']['score']}/10")
print(f"Contradictions: {grading['contradictions']['score']}/10")
print(f"Context: {grading['context']['score']}/10")
```

### Example Script

Run the included example:

```bash
python example.py
```

## Grading Criteria

- **Ambiguity** (1-10): How unclear or open to interpretation is the prompt?
- **Contradictions** (1-10): How many internal contradictions or conflicting instructions does the prompt contain?
- **Context** (1-10): How much context and background information does the prompt provide?

**Note**: The grading system uses an external prompt file (`prompt_os/prompts/prompt_grader.txt`) that must be created before using the grading functionality. If the file is not found, the system will throw an error.

## Requirements

- Python 3.11+
- OpenAI API key
- Poetry (for dependency management)

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Development

1. **Install development dependencies**:

   ```bash
   poetry install
   ```

2. **Run tests** (when available):

   ```bash
   poetry run pytest
   ```

3. **Format code**:
   ```bash
   poetry run black prompt_os/
   ```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
