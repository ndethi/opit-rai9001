#!/usr/bin/env python3
"""
Monitor LLM-as-a-Judge Evaluation Progress

Checks the evaluation progress by monitoring output files and providing status updates.
"""

import os
import time
from pathlib import Path
import json

def monitor_evaluation():
    """Monitor the evaluation progress."""
    
    results_dir = Path("outputs/evaluation/comparative/results")
    
    print("=" * 70)
    print("LLM-as-a-Judge Evaluation Progress Monitor")
    print("=" * 70)
    print(f"Model: Gemini 2.5 Pro")
    print(f"Dataset: 100 Kikuyu proverbs (3 systems)")
    print(f"Estimated time: 40-50 minutes")
    print("=" * 70)
    print()
    
    start_time = time.time()
    
    while True:
        print(f"\n[{time.strftime('%H:%M:%S')}] Checking progress...")
        
        # Check if results directory exists
        if results_dir.exists():
            files = list(results_dir.glob("*.json"))
            if files:
                print(f"  ✓ Found {len(files)} result file(s)")
                
                # Try to read evaluation metadata
                for file in files:
                    if 'metadata' in file.name or 'summary' in file.name:
                        try:
                            with open(file) as f:
                                data = json.load(f)
                                if 'evaluation_metadata' in data:
                                    total = data['evaluation_metadata'].get('total_evaluations', 0)
                                    print(f"  ✓ Evaluations completed: {total}")
                                elif 'sample_size' in data:
                                    print(f"  ✓ Sample size: {data['sample_size']}")
                        except:
                            pass
            else:
                print("  ⏳ No results yet...")
        else:
            print("  ⏳ Results directory not created yet...")
        
        # Show elapsed time
        elapsed = time.time() - start_time
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        print(f"  ⏱  Elapsed time: {mins}m {secs}s")
        
        # Check if process is still running
        import subprocess
        result = subprocess.run(['pgrep', '-f', 'run_llm_evaluation'], 
                              capture_output=True, text=True)
        if not result.stdout.strip():
            print("\n" + "=" * 70)
            print("Evaluation process has completed!")
            print("=" * 70)
            break
            
        # Wait before next check
        time.sleep(30)

if __name__ == "__main__":
    try:
        monitor_evaluation()
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")
