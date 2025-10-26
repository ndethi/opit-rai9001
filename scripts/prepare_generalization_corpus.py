#!/usr/bin/env python3
"""
Prepare Tier 2 Generalization Corpus
Extract 75 diverse proverbs from extracted_proverbs.csv
Ensure no overlap with Ireri wealth corpus
Stratify by theme for diversity
"""

import pandas as pd
import numpy as np
import re

# Load source corpus
print("Loading extracted proverbs...")
df = pd.read_csv('data/proverbs/extracted_proverbs.csv')
print(f"Total proverbs available: {len(df)}")

# Load Ireri corpus to check for overlap
ireri_df = pd.read_csv('data/evaluation/gold_standard_ireri_deduplicated.csv')
ireri_texts = set(ireri_df['kikuyu_text'].str.lower().str.strip())
print(f"Ireri corpus size: {len(ireri_texts)}")

# Filter out:
# 1. Non-proverb content (PDF artifacts)
# 2. Overlap with Ireri
# 3. Low-quality extractions

def is_valid_proverb(row):
    """Check if row contains a valid proverb"""
    text = str(row['kikuyu_text']).lower()
    
    # Filter PDF artifacts
    artifacts = ['thank', 'page', 'bible', 'english:', 'kiswahili:', 
                 'pdf', 'vol.', 'pg', 'greatest thanks']
    if any(artifact in text for artifact in artifacts):
        return False
    
    # Must have some length
    if len(text.strip()) < 10:
        return False
    
    # Check overlap with Ireri
    if text.strip() in ireri_texts:
        return False
    
    # Check if has actual Kikuyu text (not just placeholders)
    if '[NEEDS EXPERT TRANSLATION' in str(row['literal_translation']):
        # Only keep if has confidence > 0.65
        usage_notes = str(row.get('usage_notes', ''))
        conf_match = re.search(r'confidence: (0\.\d+)', usage_notes)
        if conf_match:
            confidence = float(conf_match.group(1))
            return confidence > 0.65
        return False
    
    return True

# Filter valid proverbs
print("\nFiltering valid proverbs...")
valid_df = df[df.apply(is_valid_proverb, axis=1)].copy()
print(f"Valid proverbs after filtering: {len(valid_df)}")

# Categorize by theme (infer from themes column or content)
def categorize_theme(row):
    """Categorize proverb into broad themes"""
    themes = str(row.get('themes', 'general')).lower()
    text = str(row['kikuyu_text']).lower()
    
    # Social relationships
    if any(word in themes or word in text 
           for word in ['family', 'friend', 'neighbor', 'social', 'community', 
                       'marriage', 'kinship']):
        return 'social_relationships'
    
    # Agriculture/Nature
    if any(word in themes or word in text
           for word in ['farm', 'crop', 'plant', 'rain', 'harvest', 'land',
                       'animal', 'nature', 'agricultural']):
        return 'agriculture_nature'
    
    # Wisdom/Education
    if any(word in themes or word in text
           for word in ['wisdom', 'learn', 'teach', 'knowledge', 'education',
                       'elder', 'advice']):
        return 'wisdom_education'
    
    # Family/Marriage (more specific)
    if any(word in themes or word in text
           for word in ['wife', 'husband', 'child', 'parent', 'mother', 'father']):
        return 'family_marriage'
    
    # Conflict/Resolution
    if any(word in themes or word in text
           for word in ['fight', 'war', 'peace', 'reconcile', 'conflict', 
                       'dispute', 'quarrel']):
        return 'conflict_resolution'
    
    # Work/Effort
    if any(word in themes or word in text
           for word in ['work', 'labor', 'effort', 'diligence', 'lazy', 'busy']):
        return 'work_effort'
    
    return 'general_wisdom'

valid_df['inferred_theme'] = valid_df.apply(categorize_theme, axis=1)

print("\nThematic distribution:")
print(valid_df['inferred_theme'].value_counts())

# Stratified sampling: 75 total
# Aim for diversity across themes
sample_size = 75
theme_samples = {
    'social_relationships': 15,
    'agriculture_nature': 15,
    'wisdom_education': 15,
    'family_marriage': 10,
    'conflict_resolution': 10,
    'work_effort': 5,
    'general_wisdom': 5
}

sampled_dfs = []
for theme, size in theme_samples.items():
    theme_df = valid_df[valid_df['inferred_theme'] == theme]
    if len(theme_df) >= size:
        sample = theme_df.sample(n=size, random_state=42)
    else:
        # Take all available + sample from general
        sample = theme_df
        remaining = size - len(theme_df)
        if remaining > 0:
            general_df = valid_df[valid_df['inferred_theme'] == 'general_wisdom']
            extra = general_df.sample(n=min(remaining, len(general_df)), 
                                     random_state=42)
            sample = pd.concat([sample, extra])
    
    sampled_dfs.append(sample)

tier2_corpus = pd.concat(sampled_dfs).drop_duplicates(subset=['kikuyu_text'])

# Ensure exactly 75
if len(tier2_corpus) > 75:
    tier2_corpus = tier2_corpus.sample(n=75, random_state=42)
elif len(tier2_corpus) < 75:
    # Fill with general wisdom
    needed = 75 - len(tier2_corpus)
    remaining_df = valid_df[~valid_df.index.isin(tier2_corpus.index)]
    extra = remaining_df.sample(n=min(needed, len(remaining_df)), random_state=42)
    tier2_corpus = pd.concat([tier2_corpus, extra])

print(f"\n✅ Final Tier 2 corpus size: {len(tier2_corpus)}")
print("\nFinal thematic distribution:")
print(tier2_corpus['inferred_theme'].value_counts())

# Create clean output
output_df = tier2_corpus[[
    'kikuyu_text', 'literal_translation', 'cultural_meaning', 
    'themes', 'inferred_theme'
]].copy()

output_df = output_df.rename(columns={'inferred_theme': 'theme'})

# Save
output_path = 'data/evaluation/tier2_generalization_corpus.csv'
output_df.to_csv(output_path, index=False)
print(f"\n✅ Tier 2 corpus saved to: {output_path}")

# Verification: no overlap check
overlap_check = set(output_df['kikuyu_text'].str.lower().str.strip()) & ireri_texts
if len(overlap_check) > 0:
    print(f"\n⚠️ WARNING: Found {len(overlap_check)} overlapping proverbs!")
    print("Overlaps:", overlap_check)
else:
    print("\n✅ Verification passed: No overlap with Ireri corpus")

print("\n" + "="*60)
print("CORPUS PREPARATION COMPLETE")
print("="*60)
print(f"Tier 1 (Ireri - Wealth): {len(ireri_texts)} proverbs")
print(f"Tier 2 (Diverse domains): {len(output_df)} proverbs")
print(f"Total evaluation corpus: {len(ireri_texts) + len(output_df)} proverbs")
