"""
Streamlit app for PromptOS - Interactive Prompt Grading Interface
"""

import streamlit as st
import os
from prompt_os.prompt_grader import grade_prompt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="PromptOS - Prompt Grading Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for minimalistic light mode styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f2937;
        letter-spacing: -0.025em;
    }
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 1.25rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        transition: all 0.2s ease;
    }
    .metric-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }
    .score-display {
        font-size: 1.75rem;
        font-weight: 600;
        text-align: center;
        color: #1f2937;
    }
    .metric-label {
        font-size: 0.875rem;
        font-weight: 500;
        text-align: center;
        color: #6b7280;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .explanation-box {
        background-color: #f9fafb;
        border: 1px solid #e5e7eb;
        padding: 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        color: black;
    }
    .overall-assessment {
        background-color: #f0f9ff;
        border: 1px solid #bae6fd;
        padding: 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: white;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #f3f4f6;
    }
    .success-box {
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        color: #166534;
        padding: 0.75rem;
        border-radius: 6px;
        margin: 0.5rem 0;
    }
    .warning-box {
        background-color: #fffbeb;
        border: 1px solid #fcd34d;
        color: #92400e;
        padding: 0.75rem;
        border-radius: 6px;
        margin: 0.5rem 0;
    }
    .info-box {
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1e40af;
        padding: 0.75rem;
        border-radius: 6px;
        margin: 0.5rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)


def main():
    # Initialize session state for API key
    if "api_key" not in st.session_state:
        st.session_state.api_key = os.getenv("OPENAI_API_KEY", "")

    # Header
    st.markdown(
        '<h1 class="main-header">📊 PromptOS Grading Engine</h1>',
        unsafe_allow_html=True,
    )

    # API Key Configuration Section
    if not os.getenv("OPENAI_API_KEY") and not st.session_state.api_key:
        st.markdown(
            '<div class="warning-box">🔑 **OpenAI API Key Required**</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="info-box">To use the grading engine, you need to provide your OpenAI API key.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
        **Don't have an API key?** 
        - Get one for free at [OpenAI Platform](https://platform.openai.com/api-keys)
        - Or set it as an environment variable: `export OPENAI_API_KEY="your-key-here"`
        """
        )

        col1, col2 = st.columns([3, 1])
        with col1:
            api_key = st.text_input(
                "Enter your OpenAI API Key",
                type="password",
                placeholder="sk-...",
                value=st.session_state.api_key,
                help="Your OpenAI API key is required to grade prompts. You can get one from https://platform.openai.com/api-keys",
            )
        with col2:
            st.markdown("")
            st.markdown("")
            if st.button("🔑 Set API Key", type="primary"):
                if api_key and api_key.startswith("sk-"):
                    st.session_state.api_key = api_key
                    os.environ["OPENAI_API_KEY"] = api_key
                    st.success("✅ API key set successfully!")
                    st.rerun()
                else:
                    st.error("Please enter a valid API key (should start with 'sk-')")

        st.markdown("---")
    else:
        st.markdown(
            '<div class="success-box">✅ OpenAI API Key configured</div>',
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🔑 Change API Key"):
                del os.environ["OPENAI_API_KEY"]
                st.session_state.api_key = ""
                st.rerun()
        with col2:
            st.markdown("")
        st.markdown("---")

    # Model selection (moved to main area)
    model = "gpt-4o"  # Default model

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            '<div class="section-header">📝 Enter Your Prompt</div>',
            unsafe_allow_html=True,
        )

        # Quick examples
        st.markdown("**Quick examples:**")
        example_prompts = [
            "Write a story about a cat",
            "Create a Python function that sorts a list",
            "Write an essay about climate change in exactly 500 words, but make it 1000 words",
        ]

        cols = st.columns(3)
        for i, example in enumerate(example_prompts):
            with cols[i]:
                if st.button(
                    f"Example {i+1}", key=f"example_{i}", use_container_width=True
                ):
                    st.session_state.prompt_text = example
                    st.rerun()

        # Prompt input
        prompt_text = st.text_area(
            "Prompt to grade",
            value=st.session_state.get("prompt_text", ""),
            height=200,
            placeholder="Enter your prompt here to get detailed grading feedback...",
        )

        # Grade button
        if st.button("🚀 Grade Prompt", type="primary", use_container_width=True):
            if not prompt_text.strip():
                st.error("Please enter a prompt to grade!")
            elif not os.getenv("OPENAI_API_KEY") and not st.session_state.api_key:
                st.error("Please provide your OpenAI API key above!")
            else:
                with st.spinner("🔍 Analyzing your prompt..."):
                    try:
                        result = grade_prompt(prompt_text, model)

                        if result:
                            st.session_state.grading_result = result
                            st.success("✅ Grading completed!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to grade the prompt. Please try again.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

    with col2:
        st.markdown(
            '<div class="section-header">📊 Quick Stats</div>', unsafe_allow_html=True
        )

        # Grading criteria info
        st.markdown(
            """
        **Grading Criteria:**
        - **Ambiguity** (1-10): Lower is better
        - **Contradictions** (1-10): Lower is better  
        - **Lack of Context** (1-10): Lower is better
        - **Grammar** (1-10): Lower is better
        """
        )

        if "grading_result" in st.session_state:
            result = st.session_state.grading_result

            # Display scores in cards
            col_a, col_b, col_c = st.columns(3)

            with col_a:
                st.markdown(
                    f"""
                <div class="metric-card">
                    <div class="metric-label">🎯 Ambiguity</div>
                    <div class="score-display">{result['ambiguity']['score']}/10</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                <div class="metric-card">
                    <div class="metric-label">⚠️ Contradictions</div>
                    <div class="score-display">{result['contradictions']['score']}/10</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col_b:
                st.markdown(
                    f"""
                <div class="metric-card">
                    <div class="metric-label">🔄 Context</div>
                    <div class="score-display">{result['context']['score']}/10</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                <div class="metric-card">
                    <div class="metric-label">📝 Grammar</div>
                    <div class="score-display">{result['grammar']['score']}/10</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col_c:
                # Calculate overall score (weighted average)
                overall_score = result["overall_score"]

                st.markdown(
                    f"""
                <div class="metric-card">
                    <div class="metric-label">⭐ Overall</div>
                    <div class="score-display">{overall_score:.1f}/10</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("Enter a prompt and click 'Grade Prompt' to see results!")

    # Display detailed results
    if "grading_result" in st.session_state:
        result = st.session_state.grading_result

        st.markdown("---")
        st.markdown(
            '<div class="section-header">📋 Detailed Analysis</div>',
            unsafe_allow_html=True,
        )

        # Overall assessment
        st.markdown(
            f"""
        <div class="overall-assessment">
            <div class="section-header">🎯 Overall Assessment</div>
            <p style="margin: 0; color: #1f2937;">{result['overall_assessment']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Detailed explanations
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("🎯 Ambiguity Analysis")
            st.markdown(
                f"""
            <div class="explanation-box">
                <strong>Score: {result['ambiguity']['score']}/10</strong><br>
                {result['ambiguity']['explanation']}
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.subheader("⚠️ Contradictions Analysis")
            st.markdown(
                f"""
            <div class="explanation-box">
                <strong>Score: {result['contradictions']['score']}/10</strong><br>
                {result['contradictions']['explanation']}
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col3:
            st.subheader("🔄 Context Analysis")
            st.markdown(
                f"""
            <div class="explanation-box">
                <strong>Score: {result['context']['score']}/10</strong><br>
                {result['context']['explanation']}
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col4:
            st.subheader("📝 Grammar Analysis")
            st.markdown(
                f"""
            <div class="explanation-box">
                <strong>Score: {result['grammar']['score']}/10</strong><br>
                {result['grammar']['explanation']}
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Original prompt display
        st.markdown("---")
        st.markdown(
            '<div class="section-header">📝 Original Prompt</div>',
            unsafe_allow_html=True,
        )
        st.code(result["original_prompt"], language="text")

        # Clear results button
        if st.button("🗑️ Clear Results"):
            if "grading_result" in st.session_state:
                del st.session_state.grading_result
            st.rerun()


if __name__ == "__main__":
    main()
