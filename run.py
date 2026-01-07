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
Simple CLI runner for LinguaLint processing with Responsibility Futures Analysis
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from src.nlp_processor import ModernNLPProcessor
from src.report_generator import generate_html_report
from src.responsibility_analyzer import analyze_responsibility
from src.responsibility_report_generator import generate_responsibility_reports
from src.pdf_generator import generate_comprehensive_pdf

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py 'Your text here'")
        print("   or: python run.py --file input.txt")
        return 1
    
    # Initialize processor
    processor = ModernNLPProcessor()
    
    # Get input text
    if sys.argv[1] == '--file':
        if len(sys.argv) < 3:
            print("Error: Please specify input file")
            return 1
        with open(sys.argv[2], 'r') as f:
            text = f.read()
    else:
        text = sys.argv[1]
    
    # Process text
    print("Processing text...")
    results = processor.process_text(text, enrich_wikipedia=True)
    
    # Generate output files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create lingualint_analysis directory structure
    analysis_base_dir = Path("./lingualint_analysis")
    analysis_base_dir.mkdir(exist_ok=True)
    
    # Create timestamped analysis folder
    analysis_dir = analysis_base_dir / f"analysis_{timestamp}"
    analysis_dir.mkdir(exist_ok=True)
    
    json_file = analysis_dir / f"extraction_{timestamp}.json"
    html_file = analysis_dir / f"report_{timestamp}.html"
    
    # Save JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Generate HTML report
    generate_html_report(str(json_file), str(html_file))
    
    # Generate Responsibility Futures Analysis (ALWAYS RUN AT END)
    print("\n" + "="*60)
    print("🔬 GENERATING RESPONSIBILITY FUTURES ANALYSIS")
    print("="*60)
    
    responsibility_success = False
    try:
        # Step 1: Analyze responsibility from extraction data
        print("Step 1: Analyzing entity responsibility ratios...")
        responsibility_report = analyze_responsibility(str(json_file))
        
        # Step 2: Save responsibility analysis JSON
        responsibility_json = json_file.with_name(f"extraction_{timestamp}_responsibility_analysis.json")
        with open(responsibility_json, 'w', encoding='utf-8') as f:
            json.dump(responsibility_report, f, indent=2, ensure_ascii=False)
        print(f"✅ Responsibility analysis JSON saved: {responsibility_json.name}")
        
        # Step 3: Generate responsibility visualizations and HTML report
        print("Step 2: Generating responsibility visualizations...")
        responsibility_files = generate_responsibility_reports(str(responsibility_json))
        
        # Step 4: Report results
        print(f"\n🎉 RESPONSIBILITY ANALYSIS COMPLETE!")
        print(f"📊 Analyzed {responsibility_report['total_entities']} entities across {responsibility_report['total_events']} events")
        
        # List all generated files
        if responsibility_files.get('html_report'):
            responsibility_html = analysis_dir / responsibility_files['html_report']
            print(f"📄 Main Report: {responsibility_html}")
        
        for file_type, filename in responsibility_files.items():
            if filename and file_type != 'html_report':
                print(f"📈 {file_type.replace('_', ' ').title()}: {filename}")
        
        responsibility_success = True
        
    except ImportError as e:
        print(f"⚠️  Missing dependencies for responsibility analysis: {e}")
        print("💡 Install with: pip install matplotlib seaborn pandas numpy")
        print("📝 Responsibility analysis skipped, but extraction completed successfully.")
        
    except Exception as e:
        print(f"❌ Responsibility analysis failed with error: {e}")
        print("📝 This is not critical - your main extraction completed successfully.")
        import traceback
        print("🔍 Debug info:")
        traceback.print_exc()
    
    # Always show final summary
    print("\n" + "="*60)
    print("📋 FINAL PROCESSING SUMMARY")
    print("="*60)
    
    # Print summary
    sentences_count = len(results['_source']['sentences'])
    phen_count = len(results['_source']['phen'])
    wiki_count = len(results['_source']['wiki'])
    
    print(f"✅ LinguaLint PROCESSING COMPLETE!")
    print(f"📊 Processed {sentences_count} sentences")
    print(f"🔍 Identified {phen_count} phenomena")
    print(f"📚 Enriched with {wiki_count} Wikipedia entries")
    print(f"📄 Main JSON: {json_file}")
    print(f"🌐 Main HTML: {html_file}")
    
    if responsibility_success:
        print(f"🎯 Responsibility analysis: COMPLETED")
        if responsibility_files.get('html_report'):
            print(f"📊 Responsibility report: {analysis_dir / responsibility_files['html_report']}")
    else:
        print(f"⚠️  Responsibility analysis: SKIPPED (see details above)")
    
    print(f"\n🌐 Open {html_file} in your browser to view the interactive visualization.")
    if responsibility_success and responsibility_files.get('html_report'):
        print(f"📊 Open {analysis_dir / responsibility_files['html_report']} for responsibility analysis.")
    
    # Generate Comprehensive PDF (FINAL STEP)
    print("\n" + "="*60)
    print("📄 GENERATING COMPREHENSIVE PDF REPORT")
    print("="*60)
    
    try:
        pdf_file = generate_comprehensive_pdf(timestamp, analysis_dir)
        
        if pdf_file:
            print(f"🎉 COMPREHENSIVE PDF GENERATED!")
            print(f"📄 PDF Report: {pdf_file}")
            print(f"📁 Analysis Package: {pdf_file.parent}")
            print(f"📄 Open {pdf_file} for the comprehensive PDF report.")
        else:
            print(f"⚠️  PDF generation failed (see details above)")
            print(f"📝 All other reports completed successfully")
            
    except Exception as e:
        print(f"❌ PDF generation failed with error: {e}")
        print(f"📝 This is not critical - all other reports completed successfully")
        import traceback
        print("🔍 Debug info:")
        traceback.print_exc()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())