#!/usr/bin/env python3
"""Extract all files from repomix archive"""

import re
import os
from pathlib import Path

def extract_files_from_repomix(repomix_path):
    """Extract all files from repomix txt file"""
    
    with open(repomix_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Find all file markers and their positions
    file_pattern = r'================\s*File:\s*([^\n]+)\s*================'
    matches = list(re.finditer(file_pattern, content))
    
    print(f"Found {len(matches)} files in repomix archive")
    
    extracted_files = []
    created_files = []
    failed_files = []
    
    for i, match in enumerate(matches):
        file_path = match.group(1).strip()
        start_pos = match.end() + 1
        
        # Find the end position (start of next file or end of content)
        if i < len(matches) - 1:
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(content)
        
        # Extract file content
        file_content = content[start_pos:end_pos].rstrip('\n')
        
        # Remove trailing markers if present
        if file_content.endswith('================'):
            file_content = file_content[:file_content.rfind('================')].rstrip('\n')
        
        # Create full file path
        full_path = Path(file_path)
        
        # Skip if path seems invalid
        if not file_path or file_path.startswith('==='):
            continue
        
        try:
            # Create parent directories
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            created_files.append(file_path)
            extracted_files.append({
                'path': file_path,
                'size': len(file_content),
                'status': 'created'
            })
            print(f"✓ Created: {file_path}")
            
        except Exception as e:
            failed_files.append({
                'path': file_path,
                'error': str(e)
            })
            print(f"✗ Failed: {file_path} - {e}")
    
    return {
        'total_found': len(matches),
        'created': len(created_files),
        'failed': len(failed_files),
        'created_files': created_files,
        'failed_files': failed_files,
        'extracted_files': extracted_files
    }

if __name__ == '__main__':
    repomix_path = 'repomix-TheRole.txt'
    
    print(f"Extracting files from {repomix_path}...\n")
    results = extract_files_from_repomix(repomix_path)
    
    print(f"\n{'='*60}")
    print(f"EXTRACTION SUMMARY")
    print(f"{'='*60}")
    print(f"Total files found: {results['total_found']}")
    print(f"Successfully created: {results['created']}")
    print(f"Failed: {results['failed']}")
    
    if results['failed_files']:
        print(f"\nFailed files:")
        for f in results['failed_files']:
            print(f"  - {f['path']}: {f['error']}")
    
    print(f"\nCreated files:")
    for f in results['created_files']:
        print(f"  - {f}")
