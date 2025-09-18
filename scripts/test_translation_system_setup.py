#!/usr/bin/env python3
"""
Test script to verify the translation comparison system setup.
Checks dependencies and system integration without running full pipeline.
"""

import sys
from pathlib import Path

def check_basic_imports():
    """Check basic Python imports."""
    try:
        import pandas as pd
        import json
        import asyncio
        import logging
        print("✅ Basic Python packages: OK")
        return True
    except ImportError as e:
        print(f"❌ Basic Python packages: FAILED - {e}")
        return False

def check_llm_clients():
    """Check LLM client availability."""
    clients_status = {}
    
    try:
        import openai
        clients_status['openai'] = "✅ Available"
    except ImportError:
        clients_status['openai'] = "❌ Missing (pip install openai)"
    
    try:
        import google.generativeai as genai
        clients_status['google-generativeai'] = "✅ Available"
    except ImportError:
        clients_status['google-generativeai'] = "❌ Missing (pip install google-generativeai)"
    
    try:
        import anthropic
        clients_status['anthropic'] = "✅ Available"
    except ImportError:
        clients_status['anthropic'] = "❌ Missing (pip install anthropic)"
    
    try:
        import cohere
        clients_status['cohere'] = "✅ Available"
    except ImportError:
        clients_status['cohere'] = "❌ Missing (pip install cohere)"
    
    print("🤖 LLM Client Status:")
    for client, status in clients_status.items():
        print(f"  {client}: {status}")
    
    available_count = sum(1 for status in clients_status.values() if "✅" in status)
    return available_count > 0

def check_evaluation_framework():
    """Check LLM as a Judge evaluation framework."""
    sys.path.append(str(Path(__file__).parent.parent))
    
    try:
        from src.evaluation import LLMJudgeEvaluator, DynamicLLMConfigurator
        print("✅ LLM as a Judge Framework: Available")
        return True
    except ImportError as e:
        print(f"❌ LLM as a Judge Framework: FAILED - {e}")
        return False

def check_translation_comparison():
    """Check translation comparison system."""
    try:
        from scripts.enhanced_translation_comparison import EnhancedTranslationComparisonSystem
        print("✅ Translation Comparison System: Available")
        return True
    except ImportError as e:
        print(f"❌ Translation Comparison System: FAILED - {e}")
        return False

def check_data_directories():
    """Check required data directories."""
    base_dir = Path(__file__).parent.parent
    required_dirs = [
        "data/evaluation/benchmark",
        "data/evaluation/translations",
        "src/evaluation"
    ]
    
    all_exist = True
    print("📁 Directory Structure:")
    for dir_path in required_dirs:
        full_path = base_dir / dir_path
        if full_path.exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} (will be created automatically)")
            all_exist = False
    
    return all_exist

def check_environment_setup():
    """Check environment configuration."""
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        print("✅ Environment file (.env): Found")
        return True
    else:
        print("⚠️ Environment file (.env): Not found")
        print("   Copy .env.example to .env and configure API keys for full functionality")
        return False

def main():
    """Run system setup verification."""
    print("🔍 Translation Comparison System Setup Check")
    print("=" * 60)
    
    checks = [
        ("Basic Imports", check_basic_imports),
        ("LLM Clients", check_llm_clients),
        ("Evaluation Framework", check_evaluation_framework),
        ("Translation Comparison", check_translation_comparison),
        ("Data Directories", check_data_directories),
        ("Environment Setup", check_environment_setup)
    ]
    
    results = {}
    for name, check_func in checks:
        print(f"\\n🔍 Checking {name}...")
        results[name] = check_func()
    
    print("\\n" + "=" * 60)
    print("📊 SETUP VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    print(f"\\n🎯 Overall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\\n🎉 System is ready! You can run:")
        print("   python scripts/run_translation_comparison_demo.py")
    elif passed >= 4:
        print("\\n⚠️ System partially ready. Missing components:")
        for name, result in results.items():
            if not result:
                print(f"   • {name}")
        print("\\n💡 Install missing dependencies:")
        print("   pip install -r requirements.txt")
    else:
        print("\\n❌ System not ready. Please install dependencies:")
        print("   pip install -r requirements.txt")
        print("   Copy .env.example to .env and configure API keys")
    
    return 0 if passed >= 4 else 1

if __name__ == "__main__":
    sys.exit(main())