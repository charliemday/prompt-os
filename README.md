# PromptOS 🚀

A Python tool to grade your prompts in terms of Ambiguity, Contradictions, and Contextual Awareness.

## Features

- **Prompt Grading**: Grade prompts on ambiguity, contradictions, and context (1-10 scale)
- **CLI Interface**: Easy-to-use command-line tool
- **Streamlit Web Interface**: Interactive web app for prompt grading
- **Python API**: Simple import and use in your Python projects

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd prompt-os
   ```

2. **Install dependencies and CLI**:

   **Using Poetry (recommended)**:

   ```bash
   poetry install
   poetry run pip install -e .
   ```

   **Using pip**:

   ```bash
   pip install -r requirements.txt
   pip install -e .
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

### Streamlit Web Interface

Launch the interactive web app for a beautiful, user-friendly interface:

```bash
# Method 1: Using the provided script
python run_streamlit.py

# Method 2: Direct streamlit command
streamlit run streamlit_app.py
```

The Streamlit app provides:

- **Interactive prompt input** with real-time grading
- **Visual score cards** for easy interpretation
- **Detailed explanations** for each grading criterion
- **Model selection** (GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo)
- **Quick example prompts** to test the system
- **Overall assessment** with weighted scoring
- **Enhanced API key management** with validation and session state
- **Responsive design** that works on desktop and mobile

### Example Script

Run the included example:

```bash
python example.py
```

### API Key Management

The Streamlit app includes enhanced API key management:

- **Prominent Input**: API key input is displayed at the top of the page when not configured
- **Session State**: Your API key is remembered across interactions
- **Validation**: Checks for valid API key format (starts with 'sk-')
- **Multiple Sources**: Accepts key from environment variable or manual input
- **Easy Management**: Change or remove your API key with one click
- **Security**: API key is masked in the interface

**Getting an API Key**:

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key (starts with 'sk-')
4. Enter it in the Streamlit app or set as environment variable:
   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```

## Grading Criteria

- **Ambiguity** (1-10): How unclear or open to interpretation is the prompt?
- **Contradictions** (1-10): How many internal contradictions or conflicting instructions does the prompt contain?
- **Context** (1-10): How much context and background information does the prompt provide?

**Note**: The grading system uses an external prompt file (`prompt_os/prompts/prompt_grader.txt`) that must be created before using the grading functionality. If the file is not found, the system will throw an error.

## Requirements

- Python 3.11+
- OpenAI API key
- Poetry (for dependency management) or pip
- Streamlit (for web interface)

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
