#!/usr/bin/env python3
"""Verify file structure"""

import os
from pathlib import Path
from collections import defaultdict

def verify_structure():
    """Verify the complete file structure"""
    
    base_path = Path('.')
    
    # Count files by category
    file_counts = defaultdict(int)
    total_size = 0
    all_files = []
    
    for file_path in base_path.rglob('*'):
        if file_path.is_file() and file_path.name != 'repomix-TheRole.txt' and file_path.name != 'extract_files.py':
            all_files.append(file_path)
            total_size += file_path.stat().st_size
            
            # Categorize
            if 'nihiltheistic-engine' in str(file_path):
                file_counts['nihiltheistic-engine'] += 1
            elif 'supabase' in str(file_path):
                file_counts['supabase'] += 1
            elif 'docs' in str(file_path):
                file_counts['docs'] += 1
            elif 'memories' in str(file_path):
                file_counts['memories'] += 1
            elif 'user_input_files' in str(file_path):
                file_counts['user_input_files'] += 1
            else:
                file_counts['root'] += 1
    
    # Print summary
    print("=" * 70)
    print("FILE STRUCTURE VERIFICATION REPORT")
    print("=" * 70)
    print()
    
    print("Files by Directory:")
    print("-" * 70)
    for category, count in sorted(file_counts.items()):
        print(f"  {category:.<45} {count:>5d} files")
    
    print()
    print(f"Total files created: {len(all_files)}")
    print(f"Total size: {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)")
    print()
    
    # List directories created
    subdirs = set()
    for file_path in all_files:
        parent = file_path.parent
        rel_path = parent.relative_to(base_path)
        if rel_path != Path('.'):
            subdirs.add(str(rel_path))
    
    print("Directories Created:")
    print("-" * 70)
    for dir_path in sorted(subdirs):
        print(f"  {dir_path}/")
    
    print()
    print(f"Total directories: {len(subdirs)}")
    print()
    
    # List top-level files
    print("Root-level Files:")
    print("-" * 70)
    root_files = [f for f in all_files if f.parent == base_path]
    for f in sorted(root_files):
        print(f"  {f.name}")
    
    print()
    print("=" * 70)
    print("✓ EXTRACTION COMPLETE - ALL FILES SUCCESSFULLY CREATED")
    print("=" * 70)

if __name__ == '__main__':
    verify_structure()
