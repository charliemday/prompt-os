#!/usr/bin/env python3
"""
Demo script to show the Streamlit app with API key functionality
"""

import os
import sys


def main():
    print("🚀 PromptOS Streamlit Demo")
    print("=" * 50)
    print()
    print("This demo will launch the Streamlit app with enhanced API key management.")
    print()
    print("Features:")
    print("✅ Prominent API key input at the top of the page")
    print("✅ Session state management (remembers your key)")
    print("✅ Validation (checks for 'sk-' prefix)")
    print("✅ Easy key change/removal")
    print("✅ Fallback to environment variable")
    print("✅ Alternative input in sidebar")
    print()

    # Check if API key is already set
    if os.getenv("OPENAI_API_KEY"):
        print("🔑 Found OPENAI_API_KEY in environment variables")
        print("   You can still change it in the app if needed")
    else:
        print("🔑 No OPENAI_API_KEY found in environment")
        print("   You'll need to enter it in the app")

    print()
    print("📊 The app will open in your browser at http://localhost:8501")
    print("   Press Ctrl+C to stop the app")
    print()

    try:
        import streamlit

        print("✅ Starting Streamlit app...")

        # Run the app
        import subprocess

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
        print("❌ Streamlit not installed. Installing...")
        os.system("pip install streamlit")
        print("✅ Streamlit installed. Please run this script again.")
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
