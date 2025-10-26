#!/usr/bin/env python3
"""
Create Tier 2 Diverse Sample for Generalization Testing
Samples 75 proverbs from diverse themes (excluding wealth/prosperity)
"""

import pandas as pd
import random
from typing import List, Dict
from datetime import datetime

# Theme keywords for classification (excluding wealth/prosperity)
THEME_KEYWORDS = {
    'wisdom': ['wisdom', 'knowledge', 'learn', 'teach', 'understand', 'know', 'clever', 'smart', 'wise', 'fool'],
    'family': ['wife', 'husband', 'child', 'son', 'daughter', 'mother', 'father', 'family', 'home', 'parent', 'brother', 'sister'],
    'social': ['friend', 'neighbor', 'community', 'people', 'guest', 'visitor', 'stranger', 'together', 'help', 'share'],
    'nature': ['tree', 'bird', 'animal', 'water', 'rain', 'sun', 'goat', 'cow', 'ox', 'sheep', 'forest', 'river', 'leopard', 'hyena'],
    'conflict': ['war', 'fight', 'enemy', 'quarrel', 'dispute', 'anger', 'hate', 'revenge', 'kill', 'weapon', 'thief', 'steal'],
    'work': ['work', 'labor', 'till', 'field', 'cultivate', 'harvest', 'plant', 'lazy', 'effort', 'task'],
    'morality': ['truth', 'lie', 'honest', 'cheat', 'good', 'bad', 'evil', 'virtue', 'sin', 'guilt', 'shame'],
    'life': ['life', 'death', 'old', 'young', 'age', 'time', 'day', 'night', 'born', 'die'],
}

# Wealth-related keywords to EXCLUDE
WEALTH_KEYWORDS = ['rich', 'poor', 'wealth', 'money', 'poverty', 'prosper', 'fortune', 'abundance', 
                   'cattle', 'property', 'possession', 'treasure', 'gold', 'trade', 'sell', 'buy', 'price']


def classify_proverb_themes(text: str) -> List[str]:
    """
    Classify a proverb into themes based on keywords
    Returns list of themes (can be multiple)
    """
    text_lower = text.lower()
    themes = []
    
    # Check each theme
    for theme, keywords in THEME_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            themes.append(theme)
    
    return themes if themes else ['general']


def is_wealth_related(text: str) -> bool:
    """
    Check if proverb is wealth/prosperity related (to exclude)
    """
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in WEALTH_KEYWORDS)


def create_diverse_sample(df: pd.DataFrame, target_count: int = 75, min_per_theme: int = 8) -> pd.DataFrame:
    """
    Create stratified diverse sample
    
    Args:
        df: Full proverb dataframe
        target_count: Total proverbs to sample (default 75)
        min_per_theme: Minimum proverbs per theme (default 8)
    
    Returns:
        Dataframe with diverse sample
    """
    
    print(f"\n🎯 Creating diverse sample of {target_count} proverbs...")
    
    # Filter out wealth-related proverbs
    print(f"   Filtering out wealth-related proverbs...")
    df['is_wealth'] = df['english_translation'].apply(is_wealth_related)
    non_wealth_df = df[~df['is_wealth']].copy()
    
    print(f"   Total proverbs: {len(df)}")
    print(f"   Non-wealth proverbs: {len(non_wealth_df)}")
    print(f"   Excluded: {len(df) - len(non_wealth_df)}")
    
    # Classify proverbs by theme
    print(f"\n   Classifying proverbs by theme...")
    non_wealth_df['themes'] = non_wealth_df['english_translation'].apply(classify_proverb_themes)
    
    # Expand themes (one row per theme for stratified sampling)
    theme_rows = []
    for _, row in non_wealth_df.iterrows():
        for theme in row['themes']:
            theme_row = row.copy()
            theme_row['primary_theme'] = theme
            theme_rows.append(theme_row)
    
    theme_df = pd.DataFrame(theme_rows)
    
    # Print theme distribution
    theme_counts = theme_df['primary_theme'].value_counts()
    print(f"\n   Theme distribution:")
    for theme, count in theme_counts.items():
        print(f"      {theme:12s}: {count:4d} proverbs")
    
    # Stratified sampling
    print(f"\n   Performing stratified sampling...")
    samples = []
    themes_list = list(THEME_KEYWORDS.keys()) + ['general']
    
    # Calculate samples per theme
    available_themes = [t for t in themes_list if t in theme_counts.index and theme_counts[t] >= min_per_theme]
    samples_per_theme = target_count // len(available_themes)
    remainder = target_count % len(available_themes)
    
    print(f"   Target: {samples_per_theme} per theme (from {len(available_themes)} themes)")
    
    sampled_ids = set()
    
    for i, theme in enumerate(available_themes):
        theme_proverbs = theme_df[theme_df['primary_theme'] == theme]
        
        # Add extra sample to first themes to use remainder
        n_samples = samples_per_theme + (1 if i < remainder else 0)
        n_samples = min(n_samples, len(theme_proverbs))
        
        # Sample without replacement
        theme_sample = theme_proverbs.sample(n=n_samples, random_state=42)
        
        for _, row in theme_sample.iterrows():
            if row['proverb_id'] not in sampled_ids:
                samples.append(row)
                sampled_ids.add(row['proverb_id'])
        
        print(f"      {theme:12s}: sampled {len([s for s in samples[-n_samples:]])} proverbs")
    
    # Create final sample dataframe
    sample_df = pd.DataFrame(samples)
    sample_df = sample_df.drop_duplicates(subset=['proverb_id'])
    
    # Select only needed columns
    result_df = sample_df[[
        'proverb_id', 'proverb_number', 'kikuyu_text', 'english_translation',
        'cultural_meaning', 'english_equivalent', 'source', 'page_number',
        'primary_theme', 'extraction_date'
    ]].copy()
    
    result_df = result_df.sort_values('proverb_number')
    
    return result_df


def generate_statistics(sample_df: pd.DataFrame) -> Dict:
    """Generate statistics for the sample"""
    
    stats = {
        'total': len(sample_df),
        'avg_kikuyu_length': sample_df['kikuyu_text'].str.len().mean(),
        'avg_english_length': sample_df['english_translation'].str.len().mean(),
        'themes': sample_df['primary_theme'].value_counts().to_dict(),
        'with_cultural_meaning': sample_df['cultural_meaning'].notna().sum(),
        'with_english_equivalent': sample_df['english_equivalent'].notna().sum(),
    }
    
    return stats


def main():
    """Main pipeline for Tier 2 sample creation"""
    
    print("=" * 70)
    print("TIER 2 DIVERSE SAMPLE CREATION")
    print("=" * 70)
    print("\n📋 Purpose: Create diverse sample for generalization testing")
    print("   Target: 75 proverbs across multiple themes (non-wealth)")
    print("   Strategy: Stratified sampling for thematic diversity")
    
    # Load extracted proverbs
    input_path = "data/raw/gbarra_1000_proverbs_extracted.csv"
    output_path = "data/evaluation/tier2_diverse_sample.csv"
    
    print(f"\n📖 Loading proverbs from: {input_path}")
    df = pd.read_csv(input_path)
    print(f"   Loaded: {len(df)} proverbs")
    
    # Create diverse sample
    sample_df = create_diverse_sample(df, target_count=75, min_per_theme=8)
    
    # Generate statistics
    stats = generate_statistics(sample_df)
    
    # Save sample
    sample_df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\n💾 Sample saved to: {output_path}")
    
    # Print final statistics
    print(f"\n📊 Final Sample Statistics:")
    print(f"   Total proverbs: {stats['total']}")
    print(f"   Avg Kikuyu length: {stats['avg_kikuyu_length']:.1f} chars")
    print(f"   Avg English length: {stats['avg_english_length']:.1f} chars")
    print(f"   With cultural meaning: {stats['with_cultural_meaning']}")
    print(f"   With English equivalent: {stats['with_english_equivalent']}")
    
    print(f"\n   Theme distribution in sample:")
    for theme, count in sorted(stats['themes'].items(), key=lambda x: -x[1]):
        percentage = (count / stats['total']) * 100
        print(f"      {theme:12s}: {count:2d} ({percentage:5.1f}%)")
    
    # Show first 5
    print(f"\n✨ First 5 sampled proverbs:")
    print(sample_df[['proverb_id', 'primary_theme', 'kikuyu_text', 'english_translation']].head().to_string(index=False))
    
    print("\n" + "=" * 70)
    print("✅ TIER 2 SAMPLE CREATION COMPLETE!")
    print("=" * 70)
    print("\n📝 Next steps:")
    print("   1. Review sample for quality and diversity")
    print("   2. Proceed to Day 1: Neo4j setup and ontology population")
    print("   3. Use this sample for Tier 2 generalization testing")


if __name__ == "__main__":
    main()
