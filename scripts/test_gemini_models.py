#!/usr/bin/env python3
"""Test script to check available Gemini models."""

import google.generativeai as genai
import os

# Configure API key
api_key = "AIzaSyC0Tnyssy1GK8pgf8Ro94HqwCPl3BuSzls"
genai.configure(api_key=api_key)

print("=" * 60)
print("Available Gemini Models for Content Generation")
print("=" * 60)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"\n✓ {m.name}")
        print(f"  Display Name: {m.display_name}")
        if m.description:
            print(f"  Description: {m.description[:150]}...")
        print(f"  Supported methods: {', '.join(m.supported_generation_methods)}")

print("\n" + "=" * 60)
print("Testing Gemini 2.0 Flash (recommended model):")
print("=" * 60)

try:
    # Test with gemini-2.0-flash-exp (latest experimental)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    response = model.generate_content("Say 'Hello from Gemini!' in one sentence.")
    print(f"✓ Model 'gemini-2.0-flash-exp' works!")
    print(f"  Response: {response.text}")
except Exception as e:
    print(f"✗ Error with gemini-2.0-flash-exp: {e}")

print("\n" + "=" * 60)
