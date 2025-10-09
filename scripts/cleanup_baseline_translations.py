#!/usr/bin/env python3
"""
Script to clean up the baseline_translations folder.
Keeps only the latest deduplicated baseline and archives old files.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def cleanup_baseline_translations():
    """Clean up baseline translations folder."""
    
    translations_dir = Path("data/results/baseline_translations")
    
    if not translations_dir.exists():
        logger.error(f"❌ Directory not found: {translations_dir}")
        return
    
    logger.info("="*80)
    logger.info("🧹 BASELINE TRANSLATIONS CLEANUP")
    logger.info("="*80)
    logger.info(f"📁 Directory: {translations_dir}")
    logger.info("")
    
    # List all files
    all_files = list(translations_dir.glob("*"))
    csv_files = [f for f in all_files if f.suffix == '.csv']
    
    logger.info(f"📊 Total files: {len(all_files)}")
    logger.info(f"📊 CSV files: {len(csv_files)}")
    logger.info("")
    
    # Identify files to keep
    KEEP_FILES = [
        "baseline_translations_clean_50proverbs_deduped.csv",  # Latest clean version
    ]
    
    # Identify files to archive (old/duplicate baselines)
    ARCHIVE_PATTERNS = [
        "baseline_translations_clean_50proverbs_20251007_000921.csv",  # Duplicated version
        "baseline_clean_temp_*.csv",  # Temporary incremental saves
        "baseline_translations_clean_2proverbs_*.csv",  # Test runs
        "translation_comparison_*.csv",  # Old comparison files
        "translation_comparison_*.txt",  # Old summary files
    ]
    
    # Create archive directory
    archive_dir = translations_dir / "archive_old_duplicates"
    archive_dir.mkdir(exist_ok=True)
    
    # Categorize files
    keep = []
    archive = []
    unknown = []
    
    for file in csv_files:
        if file.name in KEEP_FILES:
            keep.append(file)
        elif any(file.match(pattern) for pattern in ARCHIVE_PATTERNS):
            archive.append(file)
        else:
            unknown.append(file)
    
    # Display plan
    logger.info("📋 CLEANUP PLAN:")
    logger.info("")
    
    logger.info(f"✅ KEEP ({len(keep)} files):")
    for f in keep:
        logger.info(f"   - {f.name}")
    logger.info("")
    
    logger.info(f"📦 ARCHIVE ({len(archive)} files):")
    for f in archive:
        logger.info(f"   - {f.name}")
    logger.info("")
    
    if unknown:
        logger.info(f"❓ UNKNOWN ({len(unknown)} files) - Manual review needed:")
        for f in unknown:
            logger.info(f"   - {f.name}")
        logger.info("")
    
    # Ask for confirmation
    print("="*80)
    response = input("🤔 Proceed with cleanup? (yes/no): ").strip().lower()
    
    if response != 'yes':
        logger.info("❌ Cleanup cancelled by user")
        return
    
    logger.info("")
    logger.info("="*80)
    logger.info("🔄 EXECUTING CLEANUP...")
    logger.info("")
    
    # Move files to archive
    archived_count = 0
    for file in archive:
        try:
            dest = archive_dir / file.name
            shutil.move(str(file), str(dest))
            logger.info(f"   ✓ Archived: {file.name}")
            archived_count += 1
        except Exception as e:
            logger.error(f"   ✗ Failed to archive {file.name}: {e}")
    
    logger.info("")
    logger.info("="*80)
    logger.info("✅ CLEANUP COMPLETE")
    logger.info("="*80)
    logger.info(f"📦 Archived: {archived_count} files → {archive_dir.name}/")
    logger.info(f"✅ Kept: {len(keep)} files")
    
    if unknown:
        logger.info(f"❓ Review manually: {len(unknown)} files")
    
    logger.info("")
    logger.info("📁 Current structure:")
    remaining = list(translations_dir.glob("*.csv"))
    for f in remaining:
        logger.info(f"   - {f.name}")
    
    logger.info("="*80)


if __name__ == "__main__":
    cleanup_baseline_translations()
