#!/usr/bin/env python3
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
Test script to verify Responsibility Futures Analysis integration
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Test data
TEST_TEXT = """
The company faces significant risks from market volatility and regulatory changes. 
Management remains optimistic about future growth prospects despite current challenges.
The board of directors has implemented new risk management protocols.
Investors are concerned about potential losses from the economic downturn.
"""

def test_integration():
    """Test the complete integration workflow"""
    print("🧪 Testing Responsibility Futures Analysis Integration")
    print("=" * 60)
    
    try:
        # Import modules
        print("Step 1: Importing modules...")
        from src.nlp_processor import ModernNLPProcessor
        from src.report_generator import generate_html_report
        from src.responsibility_analyzer import analyze_responsibility
        from src.responsibility_report_generator import generate_responsibility_reports
        print("✅ All modules imported successfully")
        
        # Initialize processor
        print("\nStep 2: Initializing NLP processor...")
        processor = ModernNLPProcessor()
        print("✅ NLP processor initialized")
        
        # Process text
        print("\nStep 3: Processing test text...")
        results = processor.process_text(TEST_TEXT, enrich_wikipedia=False)  # Skip wiki for speed
        print("✅ Text processing completed")
        
        # Create output files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create lingualint_analysis directory structure
        analysis_base_dir = Path("./lingualint_analysis")
        analysis_base_dir.mkdir(exist_ok=True)
        
        # Create timestamped analysis folder
        analysis_dir = analysis_base_dir / f"test_analysis_{timestamp}"
        analysis_dir.mkdir(exist_ok=True)
        
        json_file = analysis_dir / f"test_extraction_{timestamp}.json"
        html_file = analysis_dir / f"test_report_{timestamp}.html"
        
        # Save JSON
        print("\nStep 4: Saving extraction results...")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON saved: {json_file}")
        
        # Generate HTML report
        print("\nStep 5: Generating HTML report...")
        generate_html_report(str(json_file), str(html_file))
        print(f"✅ HTML report generated: {html_file}")
        
        # Test responsibility analysis
        print("\nStep 6: Running responsibility analysis...")
        responsibility_report = analyze_responsibility(str(json_file))
        
        responsibility_json = json_file.with_name(f"test_extraction_{timestamp}_responsibility_analysis.json")
        with open(responsibility_json, 'w', encoding='utf-8') as f:
            json.dump(responsibility_report, f, indent=2, ensure_ascii=False)
        print(f"✅ Responsibility analysis completed: {responsibility_json}")
        
        # Generate responsibility reports
        print("\nStep 7: Generating responsibility visualizations...")
        responsibility_files = generate_responsibility_reports(str(responsibility_json))
        print("✅ Responsibility visualizations generated")
        
        # Print summary
        print("\n" + "=" * 60)
        print("🎉 INTEGRATION TEST SUCCESSFUL!")
        print("=" * 60)
        
        sentences_count = len(results['_source']['sentences'])
        phen_count = len(results['_source']['phen'])
        entities_count = responsibility_report['total_entities']
        events_count = responsibility_report['total_events']
        
        print(f"📊 Processed {sentences_count} sentences")
        print(f"🔍 Identified {phen_count} phenomena")
        print(f"👥 Analyzed {entities_count} entities")
        print(f"📈 Processed {events_count} events")
        
        print(f"\n📄 Generated files:")
        print(f"   • Main JSON: {json_file}")
        print(f"   • Main HTML: {html_file}")
        print(f"   • Responsibility JSON: {responsibility_json}")
        
        for file_type, filename in responsibility_files.items():
            if filename:
                print(f"   • {file_type.replace('_', ' ').title()}: {filename}")
        
        print(f"\n✅ Integration test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install spacy matplotlib seaborn pandas numpy")
        print("   python -m spacy download en_core_web_sm")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_integration()
    sys.exit(0 if success else 1)