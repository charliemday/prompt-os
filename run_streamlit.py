#!/usr/bin/env python3
"""
Script to run the PromptOS Streamlit app
"""

import subprocess
import sys
import os


def main():
    """Run the Streamlit app"""
    try:
        # Check if streamlit is installed
        import streamlit

        print("🚀 Starting PromptOS Streamlit app...")
        print("📊 The app will open in your default browser")
        print(
            "🔑 Make sure to set your OPENAI_API_KEY environment variable or enter it in the app"
        )
        print("=" * 50)

        # Run streamlit
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "streamlit_app.py",
                "--server.port",
                "8501",
                "--server.address",
                "localhost",
            ]
        )

    except ImportError:
        print("❌ Streamlit is not installed. Please install it first:")
        print("   pip install streamlit")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped by user")
    except Exception as e:
        print(f"❌ Error running Streamlit app: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
