#!/usr/bin/env python3
"""
ArXiv Citation Verifier
Checks which arXiv citations in the bibliography actually exist
"""

import urllib.request
import urllib.error
import time
import sys

# ArXiv citations from bibliography with their metadata
ARXIV_CITATIONS = [
    {
        'key': 'bai2024hipporag',
        'arxiv_id': '2405.14831',
        'expected_year': 2024,
        'expected_title': 'HippoRAG'
    },
    {
        'key': 'edge2024graphrag',
        'arxiv_id': '2404.16130',
        'expected_year': 2024,
        'expected_title': 'From Local to Global'
    },
    {
        'key': 'guo2024lazygraphrag',
        'arxiv_id': '2408.12741',
        'expected_year': 2024,
        'expected_title': 'LazyGraphRAG'
    },
    {
        'key': 'zhang2024triplex',
        'arxiv_id': '2406.02911',
        'expected_year': 2024,
        'expected_title': 'Triplex'
    },
    {
        'key': 'guo2024lightrag',
        'arxiv_id': '2410.05779',
        'expected_year': 2024,
        'expected_title': 'LightRAG'
    },
    {
        'key': 'agarwal2024llm',
        'arxiv_id': '2211.10511',
        'expected_year': 2024,  # MISMATCH: arXiv says 2022
        'expected_title': 'Knowledge Graph Generation'
    },
    {
        'key': 'wang2024pandalm',
        'arxiv_id': '2306.05087',
        'expected_year': 2024,  # MISMATCH: arXiv says 2023
        'expected_title': 'PandaLM'
    },
    {
        'key': 'zhou2024collaborative',
        'arxiv_id': '2406.09917',
        'expected_year': 2024,
        'expected_title': 'Collaborative Knowledge Base'
    },
    {
        'key': 'chen2024multilingual',
        'arxiv_id': '2404.10405',
        'expected_year': 2024,
        'expected_title': 'MultiLingual Knowledge Graph'
    },
    {
        'key': 'chenOmniRAGComprehensiveRetrievalAugmented2025',
        'arxiv_id': '2501.02460',
        'expected_year': 2025,
        'expected_title': 'Omni-RAG'
    },
    {
        'key': 'fengOntologyRAGBetterFaster2025',
        'arxiv_id': '2502.18992',
        'expected_year': 2025,  # CRITICAL: Feb 2025 - impossible
        'expected_title': 'OntologyRAG'
    },
    {
        'key': 'sharmaOGRAGOntologyGroundedRetrievalAugmented2024',
        'arxiv_id': '2412.15235',
        'expected_year': 2024,
        'expected_title': 'OG-RAG'
    },
    {
        'key': 'zhang2023siren',
        'arxiv_id': '2309.01219',
        'expected_year': 2023,
        'expected_title': 'Siren'
    }
]

def check_arxiv_exists(arxiv_id):
    """
    Check if an arXiv paper exists by trying to access its abstract page.
    Returns (exists: bool, status_code: int)
    """
    url = f"https://arxiv.org/abs/{arxiv_id}"
    try:
        response = urllib.request.urlopen(url, timeout=10)
        return (True, response.getcode())
    except urllib.error.HTTPError as e:
        return (False, e.code)
    except urllib.error.URLError:
        return (None, 0)  # Network error
    except Exception as e:
        return (None, -1)  # Other error

def extract_arxiv_year(arxiv_id):
    """
    Extract publication year from arXiv ID.
    Format: YYMM.NNNNN (e.g., 2405.14831 = May 2024)
    """
    year_code = arxiv_id[:2]
    month_code = arxiv_id[2:4]
    
    # arXiv switched to 4-digit years in 2015 (1501.xxxxx)
    year = int("20" + year_code)
    month = int(month_code)
    
    return year, month

def main():
    print("=" * 70)
    print("ArXiv Citation Verification Report")
    print("=" * 70)
    print(f"Checking {len(ARXIV_CITATIONS)} arXiv citations...\n")
    
    results = {
        'verified': [],
        'not_found': [],
        'year_mismatch': [],
        'network_error': []
    }
    
    for i, citation in enumerate(ARXIV_CITATIONS, 1):
        print(f"[{i}/{len(ARXIV_CITATIONS)}] Checking {citation['key']}...", end=" ")
        sys.stdout.flush()
        
        exists, status = check_arxiv_exists(citation['arxiv_id'])
        arxiv_year, arxiv_month = extract_arxiv_year(citation['arxiv_id'])
        
        if exists is None:
            print("⚠️  NETWORK ERROR")
            results['network_error'].append(citation)
        elif not exists:
            print(f"❌ NOT FOUND (HTTP {status})")
            results['not_found'].append(citation)
        elif arxiv_year != citation['expected_year']:
            print(f"⚠️  YEAR MISMATCH (arXiv: {arxiv_year}, cited: {citation['expected_year']})")
            results['year_mismatch'].append({
                **citation,
                'arxiv_year': arxiv_year,
                'arxiv_month': arxiv_month
            })
        else:
            print(f"✅ VERIFIED ({arxiv_year})")
            results['verified'].append(citation)
        
        # Be nice to arXiv servers
        time.sleep(1)
    
    # Print summary report
    print("\n" + "=" * 70)
    print("SUMMARY REPORT")
    print("=" * 70)
    
    print(f"\n✅ VERIFIED ({len(results['verified'])} citations):")
    for citation in results['verified']:
        print(f"   - {citation['key']} (arXiv:{citation['arxiv_id']})")
    
    if results['year_mismatch']:
        print(f"\n⚠️  YEAR MISMATCHES ({len(results['year_mismatch'])} citations):")
        for citation in results['year_mismatch']:
            print(f"   - {citation['key']}")
            print(f"     arXiv ID: {citation['arxiv_id']} → {citation['arxiv_year']}-{citation['arxiv_month']:02d}")
            print(f"     Cited as: {citation['expected_year']}")
            print(f"     ACTION: Change year to {citation['arxiv_year']}\n")
    
    if results['not_found']:
        print(f"\n❌ NOT FOUND ({len(results['not_found'])} citations):")
        for citation in results['not_found']:
            print(f"   - {citation['key']} (arXiv:{citation['arxiv_id']})")
            print(f"     VERDICT: HALLUCINATION - DELETE FROM BIBLIOGRAPHY\n")
    
    if results['network_error']:
        print(f"\n⚠️  NETWORK ERRORS ({len(results['network_error'])} citations):")
        print("   Could not verify due to network issues. Try again later.")
    
    print("\n" + "=" * 70)
    print("RECOMMENDATIONS")
    print("=" * 70)
    
    if results['not_found']:
        print("\n🚨 IMMEDIATE ACTION REQUIRED:")
        print("   Delete these citations - they don't exist on arXiv:")
        for citation in results['not_found']:
            print(f"   - {citation['key']}")
    
    if results['year_mismatch']:
        print("\n⚠️  FIX YEAR MISMATCHES:")
        print("   Update BibTeX year field for:")
        for citation in results['year_mismatch']:
            print(f"   - {citation['key']}: year = {{{citation['arxiv_year']}}}")
    
    if results['verified']:
        print(f"\n✅ {len(results['verified'])} citations are VERIFIED and correct")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
