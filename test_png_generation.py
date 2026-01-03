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
test_file = "reports/extraction_20260101_092551_responsibility_analysis.json"

if Path(test_file).exists():
    print(f"🧪 Testing PNG generation with: {test_file}")
    
    try:
        from src.responsibility_report_generator import generate_responsibility_reports
        
        print("📊 Generating responsibility reports...")
        result = generate_responsibility_reports(test_file)
        
        print("\n✅ PNG Generation Test Results:")
        for file_type, filename in result.items():
            if filename:
                file_path = Path("reports") / filename
                if file_path.exists():
                    size = file_path.stat().st_size
                    print(f"   ✅ {file_type}: {filename} ({size:,} bytes)")
                else:
                    print(f"   ❌ {file_type}: {filename} (FILE NOT FOUND)")
            else:
                print(f"   ⚠️  {file_type}: None (not generated)")
        
        # Check if PNG files specifically exist
        png_files = list(Path("reports").glob("*20260101_*.png"))
        print(f"\n📈 Total PNG files found: {len(png_files)}")
        for png_file in sorted(png_files):
            print(f"   📊 {png_file.name}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        
else:
    print(f"❌ Test file not found: {test_file}")
    print("Available files:")
    for f in Path("reports").glob("*responsibility_analysis.json"):
        print(f"   📄 {f}")