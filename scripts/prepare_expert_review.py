#!/usr/bin/env python3
"""Prepare expert review materials for creating AI translation evaluation benchmark."""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExpertReviewPreparator:
    """Prepare materials for creating gold standard AI translation evaluation benchmark."""
    
    def __init__(self, csv_file: str):
        """Load extracted proverbs from CSV."""
        self.csv_file = Path(csv_file)
        if not self.csv_file.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_file}")
        
        self.df = pd.read_csv(csv_file)
        logger.info(f"Loaded {len(self.df)} proverbs from {csv_file}")
        
        # Filter out non-proverb entries (those that look like English text or document fragments)
        self.df = self._filter_authentic_proverbs()
        logger.info(f"Filtered to {len(self.df)} potential authentic proverbs")
    
    def _filter_authentic_proverbs(self):
        """Filter to keep only entries that appear to be actual Kikuyu proverbs."""
        # Remove entries that are clearly English text or document fragments
        filtered_df = self.df.copy()
        
        # Remove entries that start with common English words or phrases
        english_patterns = [
            'My greatest thanks', 'The Gikuyu', 'TABLE OF CONTENTS', 
            'English:', 'dialect.', 'several continuous', 'daughters got married',
            'The elders cautioned', 'The use of proverbs', 'use of them',
            'and can therefore'
        ]
        
        for pattern in english_patterns:
            filtered_df = filtered_df[~filtered_df['kikuyu_text'].str.contains(pattern, na=False)]
        
        # Keep entries that have numbered proverb format (e.g., "1. ", "2. ", etc.)
        # or contain common Kikuyu words/patterns
        kikuyu_patterns = [
            r'^\d+\.\s+[A-Za-z]',  # Numbered proverbs
            r'Gutiri|Gukiaga|Andu|mburi|gitonga|muthenya|ngia|mbura',  # Common Kikuyu words
        ]
        
        # Keep entries that match Kikuyu patterns OR are marked with higher domain relevance
        mask = (
            filtered_df['kikuyu_text'].str.contains('|'.join(kikuyu_patterns), na=False, regex=True) |
            filtered_df['domain_relevance'].str.contains('High|Medium', na=False)
        )
        
        return filtered_df[mask]
    
    def create_expert_review_spreadsheet(self, output_file: str = "data/processed/expert_evaluation_benchmark.xlsx"):
        """Create expert review spreadsheet for AI translation evaluation benchmark creation."""
        
        # Ensure output directory exists
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare review columns
        review_data = []
        
        for idx, row in self.df.iterrows():
            # Clean up the Kikuyu text (remove numbering and references)
            kikuyu_text = row['kikuyu_text']
            if pd.notna(kikuyu_text):
                # Remove pattern like "1. " or "13. " from the beginning
                import re
                kikuyu_text = re.sub(r'^\d+\.\s*', '', kikuyu_text)
                # Remove reference patterns like "(GJW A 5, Ba 4) M"
                kikuyu_text = re.sub(r'\([^)]*\)\s*[A-Z]*\s*$', '', kikuyu_text).strip()
            
            review_row = {
                # Original extracted data (for AI system reference)
                'Proverb_ID': row.get('id', f'prov_{idx:03d}'),
                'Kikuyu_Text': kikuyu_text,
                'Auto_Literal_Translation': row.get('literal_translation', '[AI SYSTEM WILL TRANSLATE]'),
                'Auto_Cultural_Meaning': row.get('cultural_meaning', '[AI SYSTEM WILL INTERPRET]'),
                'Suggested_Themes': row.get('themes', ''),
                'Domain_Relevance': row.get('domain_relevance', ''),
                'Complexity_Level': row.get('complexity_level', 'unknown'),
                'Source_Notes': row.get('usage_notes', ''),
                'Extraction_Confidence': self._extract_confidence(row.get('usage_notes', '')),
                
                # GOLD STANDARD BENCHMARK FIELDS (for AI comparison evaluation)
                'Gold_Standard_Translation': '',  # Expert reference translation for comparison
                'Gold_Standard_Cultural_Meaning': '',  # Expert cultural interpretation baseline
                'Traditional_Usage_Context': '',  # Authentic usage context for evaluation
                'Cultural_Concepts_To_Preserve': '',  # Key concepts AI must maintain
                'Translation_Quality_Criteria': '',  # What makes translation good/bad
                'Business_Relevance_Score': '',  # 1-5 scale for domain evaluation
                'Cultural_Authenticity_Score': '',  # 1-5 scale for cultural accuracy
                'Translation_Difficulty_Level': '',  # Easy/Medium/Hard for AI systems
                'Common_AI_Translation_Errors': '',  # Typical mistakes to watch for
                'Evaluation_Notes': '',  # Additional assessment criteria
                'Benchmark_Status': 'Pending Expert Evaluation'
            }
            review_data.append(review_row)
        
        # Create DataFrame and save to Excel
        review_df = pd.DataFrame(review_data)
        
        # Create multiple sheets for evaluation benchmark
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Main evaluation benchmark sheet
            review_df.to_excel(writer, sheet_name='Evaluation_Benchmark', index=False)
            
            # Instructions for creating evaluation benchmark
            instructions_df = pd.DataFrame([
                {'Section': 'RESEARCH PURPOSE', 'Instructions': 'Create gold standard evaluation benchmark to compare AI translation systems'},
                {'Section': 'PROJECT GOAL', 'Instructions': 'We will test: Does cultural knowledge (ontology) improve AI translation quality?'},
                {'Section': 'YOUR ROLE', 'Instructions': 'Provide reference standards to evaluate AI system performance against'},
                {'Section': 'Gold_Standard_Translation', 'Instructions': 'THE BEST possible English translation - our reference baseline'},
                {'Section': 'Gold_Standard_Cultural_Meaning', 'Instructions': 'Authoritative cultural interpretation - what AI systems should achieve'},
                {'Section': 'Cultural_Concepts_To_Preserve', 'Instructions': 'Key cultural elements that good AI translation MUST maintain'},
                {'Section': 'Translation_Quality_Criteria', 'Instructions': 'What makes a translation excellent vs poor for this proverb?'},
                {'Section': 'Business_Relevance_Score', 'Instructions': '1-5 scale: Relevance to wealth/entrepreneurship domain'},
                {'Section': 'Cultural_Authenticity_Score', 'Instructions': '1-5 scale: How culturally authentic is this proverb?'},
                {'Section': 'Translation_Difficulty_Level', 'Instructions': 'Easy/Medium/Hard - how challenging for AI systems?'},
                {'Section': 'Common_AI_Translation_Errors', 'Instructions': 'What mistakes do you expect AI systems to make?'},
                {'Section': 'EVALUATION FOCUS', 'Instructions': 'Focus on creating standards to measure AI translation quality'},
            ])
            instructions_df.to_excel(writer, sheet_name='Evaluation_Instructions', index=False)
            
            # Benchmark summary statistics
            summary_df = pd.DataFrame([
                {'Metric': 'Total Proverbs in Benchmark', 'Value': len(review_df)},
                {'Metric': 'High Domain Relevance', 'Value': len(review_df[review_df['Domain_Relevance'].str.contains('High', na=False)])},
                {'Metric': 'Medium Domain Relevance', 'Value': len(review_df[review_df['Domain_Relevance'].str.contains('Medium', na=False)])},
                {'Metric': 'Complex Translation Cases', 'Value': len(review_df[review_df['Complexity_Level'] == 'complex'])},
                {'Metric': 'High Confidence Extractions', 'Value': len(review_df[review_df['Extraction_Confidence'] > 0.7])},
                {'Metric': 'Research Purpose', 'Value': 'AI Translation Quality Evaluation'},
                {'Metric': 'Comparison Method', 'Value': 'Ontology-Grounded RAG vs Raw LLM vs Expert Gold Standard'},
            ])
            summary_df.to_excel(writer, sheet_name='Benchmark_Summary', index=False)
        
        logger.info(f"Created AI translation evaluation benchmark: {output_file}")
        return output_file
    
    def _extract_confidence(self, usage_notes: str) -> float:
        """Extract confidence score from usage notes."""
        if pd.isna(usage_notes):
            return 0.0
        
        import re
        confidence_match = re.search(r'confidence:\s*([\d.]+)', usage_notes)
        if confidence_match:
            return float(confidence_match.group(1))
        return 0.0
    
    def create_expert_instructions_document(self, output_file: str = "data/processed/expert_validation_instructions.md"):
        """Create detailed instructions for cultural experts."""
        
        instructions = f"""# Kikuyu Proverb Cultural Expert Validation
## Instructions for Cultural Review and Translation

**Date**: {datetime.now().strftime('%Y-%m-%d')}  
**Total Proverbs for Review**: {len(self.df)}  
**Focus Domain**: Wealth, Business, and Entrepreneurship  
**Project**: OPIT RAI9001 Research Project

---

## Overview

You are being asked to validate and enhance a collection of Kikuyu proverbs that have been automatically extracted from research documents. Your cultural expertise is essential for ensuring accurate translations and authentic cultural interpretations, particularly as they relate to wealth, business practices, and entrepreneurial wisdom.

## Project Context

This expert validation is part of the OPIT RAI9001 research project focusing on "Traditional Kikuyu Proverbs for Modern Wealth and Entrepreneurship." The goal is to create a culturally authentic knowledge base that bridges traditional wisdom with contemporary business practices.

## Review Process

### 1. **Cultural Authenticity Verification**
For each proverb, please verify:
- Is this an authentic Kikuyu proverb?
- Is the Kikuyu text correctly written?
- Are there any spelling or grammatical errors?
- Rate authenticity from 1-5 (5 = completely authentic)

### 2. **Expert Translation**
- Provide an accurate English translation
- Prioritize cultural meaning over literal word-for-word translation
- Consider the business/entrepreneurship context where relevant
- Note if direct translation is impossible without cultural explanation

### 3. **Cultural Meaning Analysis**
- Explain the deeper cultural wisdom embedded in the proverb
- Describe the traditional context and significance
- Note any business or wealth-related interpretations
- Explain metaphorical or symbolic meanings

### 4. **Usage Context Documentation**
- When is this proverb traditionally used?
- Who typically uses it (elders, peers, business people)?
- What situations call for this proverb?
- Are there specific ceremonial or social contexts?

### 5. **Theme Classification**
Classify each proverb with relevant themes:
- **business_wisdom**: Trade, commerce, business practices
- **work_ethic**: Hard work, diligence, persistence
- **wealth_management**: Saving, investment, financial planning
- **entrepreneurship**: Innovation, opportunity, risk-taking
- **partnership**: Cooperation, trust, collaboration
- **financial_wisdom**: Money management, debt, lending
- **success_failure**: Achievement, setbacks, recovery
- **community_wealth**: Collective prosperity, sharing resources
- **generational_wisdom**: Passing knowledge about wealth

### 6. **Business Relevance Rating**
Rate from 1-5 how relevant each proverb is to modern business and entrepreneurship:
- **1**: No business relevance
- **2**: Minimal business application
- **3**: Some business relevance
- **4**: High business relevance
- **5**: Directly applicable to business/entrepreneurship

### 7. **Translation Difficulty Assessment**
Rate translation difficulty:
- **Easy**: Direct equivalent exists in English
- **Medium**: Requires cultural explanation but translatable
- **Hard**: Culturally specific, very difficult to translate

### 8. **Modern Business Application**
For proverbs with business relevance, describe:
- How this wisdom applies to modern business
- Specific business scenarios where it's relevant
- Contemporary examples of this principle

## Guidelines for Cultural Preservation

1. **Maintain Cultural Integrity**: Preserve the cultural wisdom even if it requires explanation
2. **Context Matters**: Consider traditional usage contexts
3. **Regional Variations**: Note any regional differences you're aware of
4. **Modern Relevance**: Comment on contemporary applicability
5. **Respectful Interpretation**: Ensure interpretations honor Kikuyu cultural values

## Examples of Good Practice

**Proverb**: "Gukiaga na gutonga ititiganaga"
- **Expert Translation**: "Poverty and wealth do not separate"
- **Cultural Meaning**: "This proverb reflects the Kikuyu understanding that wealth and poverty are interconnected states that can change. It emphasizes that wealthy individuals should not look down on the poor, as circumstances can change."
- **Usage Context**: "Traditionally used by elders when teaching about humility and the temporary nature of material wealth. Often shared in community gatherings when discussing social responsibility."
- **Business Application**: "In modern business, this applies to maintaining humility in success and treating all stakeholders with respect regardless of their economic status."

## Quality Indicators

High-quality expert validation includes:
- Accurate cultural context
- Clear business relevance explanation
- Thoughtful modern applications
- Preservation of traditional meaning
- Regional or dialectical notes where relevant

## Technical Notes

- Complete all fields for each proverb
- Use "N/A" if a field doesn't apply
- Flag any proverbs you believe are inauthentic or incorrectly extracted
- Feel free to add additional comments in the Expert_Comments field
- If you recognize alternative versions, please note them

## Contact Information

For questions or clarifications regarding this validation process, please contact:
[Research Team Contact Information]

**Thank you for your invaluable cultural expertise in preserving and interpreting Kikuyu wisdom for contemporary applications!**

---

*This document is part of the OPIT RAI9001 research project on Traditional Kikuyu Proverbs for Modern Wealth and Entrepreneurship.*
"""
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        logger.info(f"Created expert instructions: {output_file}")
        return output_file
    
    def create_validation_summary_report(self, output_file: str = "data/processed/validation_preparation_report.md"):
        """Create a summary report of the validation preparation process."""
        
        # Analyze the data for the report
        total_proverbs = len(self.df)
        high_confidence = len(self.df[self.df['usage_notes'].str.contains('confidence: 0.[7-9]', na=False)])
        high_domain_relevance = len(self.df[self.df['domain_relevance'].str.contains('High', na=False)])
        medium_domain_relevance = len(self.df[self.df['domain_relevance'].str.contains('Medium', na=False)])
        
        # Theme distribution
        all_themes = self.df['themes'].str.split(',').explode().str.strip()
        theme_counts = all_themes.value_counts().head(10)
        
        report = f"""# Expert Validation Preparation Report
**Date**: {datetime.now().strftime('%Y-%m-%d')}  
**Project**: OPIT RAI9001 - Traditional Kikuyu Proverbs for Modern Wealth and Entrepreneurship

## Summary Statistics

- **Total Proverbs Prepared for Review**: {total_proverbs}
- **High Confidence Extractions**: {high_confidence}
- **High Domain Relevance**: {high_domain_relevance}
- **Medium Domain Relevance**: {medium_domain_relevance}
- **General Cultural Proverbs**: {total_proverbs - high_domain_relevance - medium_domain_relevance}

## Data Quality Assessment

### Extraction Confidence Distribution
The proverbs have been filtered to remove obvious non-proverb content such as:
- English acknowledgments and document text
- Table of contents entries
- Descriptive text about Kikuyu culture

### Theme Distribution (Top 10)
"""
        
        for theme, count in theme_counts.items():
            if pd.notna(theme) and theme.strip():
                report += f"- **{theme}**: {count} proverbs\n"
        
        report += f"""

## Validation Process

### Materials Created
1. **Expert Review Spreadsheet**: Comprehensive Excel file with validation fields
2. **Expert Instructions Document**: Detailed guidelines for cultural experts
3. **Validation Summary Report**: This document

### Next Steps
1. **Expert Recruitment**: Identify and contact Kikuyu cultural experts
2. **Review Session Planning**: Schedule validation sessions
3. **Quality Assurance**: Implement review quality checks
4. **Data Integration**: Process validated results back into the system

## Expert Review Requirements

### Recommended Expert Profile
- Native Kikuyu speaker
- Deep knowledge of traditional culture
- Understanding of business/entrepreneurship concepts
- Academic or community leadership background

### Review Timeline
- **Estimated time per proverb**: 5-10 minutes
- **Total estimated review time**: {total_proverbs * 7 // 60} hours
- **Recommended session length**: 2-3 hours
- **Suggested number of sessions**: {(total_proverbs * 7 // 60) // 2 + 1}

## Quality Assurance Measures

1. **Multiple Expert Review**: Consider having 2-3 experts review high-priority proverbs
2. **Consistency Checks**: Compare expert translations for consistency
3. **Cultural Validation**: Verify authenticity with multiple sources
4. **Business Relevance Verification**: Ensure business applications are culturally appropriate

## Success Metrics

- **Authenticity Verification**: >95% of proverbs confirmed as authentic
- **Translation Quality**: Expert translations for >90% of proverbs
- **Business Relevance**: Clear business applications for >60% of proverbs
- **Cultural Preservation**: Detailed cultural context for >80% of proverbs

---

*Generated by Expert Review Preparation System*
*OPIT RAI9001 Research Project*
"""
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Created validation summary report: {output_file}")
        return output_file

def main():
    """Prepare expert review materials from CSV."""
    
    # Use the actual CSV file path from the project
    csv_file = "data/proverbs/extracted_proverbs.csv"
    
    if not Path(csv_file).exists():
        print(f"CSV file not found: {csv_file}")
        print("Please ensure the extracted proverbs CSV file exists.")
        return
    
    try:
        preparator = ExpertReviewPreparator(csv_file)
        
        # Create review materials
        excel_file = preparator.create_expert_review_spreadsheet()
        instructions_file = preparator.create_expert_instructions_document()
        report_file = preparator.create_validation_summary_report()
        
        print(f"\\n🎯 Expert review materials created successfully!")
        print(f"📊 Review spreadsheet: {excel_file}")
        print(f"📋 Instructions document: {instructions_file}")
        print(f"📈 Preparation report: {report_file}")
        print(f"\\n📊 Statistics:")
        print(f"   - Total proverbs for review: {len(preparator.df)}")
        print(f"   - Original extractions: {len(pd.read_csv(csv_file))}")
        print(f"   - Filtered authentic proverbs: {len(preparator.df)}")
        print(f"\\n🔄 Next steps:")
        print(f"   1. Review the preparation report")
        print(f"   2. Recruit qualified Kikuyu cultural experts")
        print(f"   3. Schedule expert validation sessions")
        print(f"   4. Distribute materials to experts")
        print(f"   5. Collect and process expert feedback")
        
    except Exception as e:
        logger.error(f"Error creating review materials: {e}")
        print(f"❌ Error creating review materials: {e}")

if __name__ == "__main__":
    main()