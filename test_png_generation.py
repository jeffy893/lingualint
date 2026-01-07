#!/usr/bin/env python3.10
"""
LinguaLint - AI-powered project planning and analysis platform
Copyright (C) 2026 Jefferson Richards

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

"""
Test PNG generation in the responsibility analysis workflow
"""

import json
from pathlib import Path
from datetime import datetime

# Test with existing responsibility analysis data
# Look for the most recent analysis in lingualint_analysis folder
analysis_base = Path("lingualint_analysis")
test_file = None

if analysis_base.exists():
    # Find the most recent analysis folder
    analysis_folders = [d for d in analysis_base.iterdir() if d.is_dir() and d.name.startswith("analysis_")]
    if analysis_folders:
        latest_folder = max(analysis_folders, key=lambda x: x.name)
        # Look for responsibility analysis JSON
        responsibility_files = list(latest_folder.glob("*_responsibility_analysis.json"))
        if responsibility_files:
            test_file = str(responsibility_files[0])

# Fallback to old reports folder if nothing found in new structure
if not test_file:
    old_test_file = "reports/extraction_20260101_092551_responsibility_analysis.json"
    if Path(old_test_file).exists():
        test_file = old_test_file

if test_file and Path(test_file).exists():
    print(f"🧪 Testing PNG generation with: {test_file}")
    
    try:
        from src.responsibility_report_generator import generate_responsibility_reports
        
        print("📊 Generating responsibility reports...")
        result = generate_responsibility_reports(test_file)
        
        print("\n✅ PNG Generation Test Results:")
        for file_type, filename in result.items():
            if filename:
                file_path = Path(test_file).parent / filename
                if file_path.exists():
                    size = file_path.stat().st_size
                    print(f"   ✅ {file_type}: {filename} ({size:,} bytes)")
                else:
                    print(f"   ❌ {file_type}: {filename} (FILE NOT FOUND)")
            else:
                print(f"   ⚠️  {file_type}: None (not generated)")
        
        # Check if PNG files specifically exist
        output_dir = Path(test_file).parent
        png_files = list(output_dir.glob("*responsibility*.png"))
        print(f"\n📈 Total PNG files found: {len(png_files)}")
        for png_file in sorted(png_files):
            print(f"   📊 {png_file.name}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        
else:
    print(f"❌ Test file not found")
    print("Available files in lingualint_analysis:")
    if analysis_base.exists():
        for analysis_folder in analysis_base.iterdir():
            if analysis_folder.is_dir():
                print(f"   📁 {analysis_folder.name}/")
                for f in analysis_folder.glob("*responsibility_analysis.json"):
                    print(f"      📄 {f.name}")
    else:
        print("   No lingualint_analysis folder found")
    
    print("Available files in reports folder:")
    reports_folder = Path("reports")
    if reports_folder.exists():
        for f in reports_folder.glob("*responsibility_analysis.json"):
            print(f"   📄 {f}")
    else:
        print("   No reports folder found")