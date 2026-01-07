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
PDF Report Generator for LinguaLint

Combines all HTML reports from a single run into a comprehensive PDF
stored in an appropriately named folder in the root directory.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import subprocess
import tempfile
import shutil

# Try to import PDF generation libraries
try:
    import weasyprint
    PDF_WEASYPRINT_AVAILABLE = True
except ImportError:
    PDF_WEASYPRINT_AVAILABLE = False

try:
    import pdfkit
    PDF_PDFKIT_AVAILABLE = True
except ImportError:
    PDF_PDFKIT_AVAILABLE = False

class LinguaLintPDFGenerator:
    """
    Generates comprehensive PDF reports from LinguaLint HTML outputs
    """
    
    def __init__(self, timestamp: str, analysis_dir: Path = None):
        self.timestamp = timestamp
        self.analysis_dir = analysis_dir
        self.root_dir = Path(".")
        
        if analysis_dir:
            # Use provided analysis directory
            self.output_dir = analysis_dir
            print(f"📁 Using existing analysis directory: {self.output_dir}")
        else:
            # Create lingualint_analysis directory structure (legacy mode)
            self.super_dir = self.root_dir / "lingualint_analysis"
            self.super_dir.mkdir(exist_ok=True)
            
            # Create specific analysis folder within super folder
            self.output_dir = self.super_dir / f"analysis_{timestamp}"
            self.output_dir.mkdir(exist_ok=True)
            
            print(f"📁 PDF super directory: {self.super_dir}")
            print(f"📁 Analysis output directory: {self.output_dir}")
    
    def find_html_reports(self) -> Dict[str, Optional[Path]]:
        """Find all HTML reports for the given timestamp"""
        reports = {
            'main_report': None,
            'responsibility_report': None,
            'gantt_chart': None
        }
        
        # Look for main report in the analysis directory
        main_report = self.output_dir / f"report_{self.timestamp}.html"
        if main_report.exists():
            reports['main_report'] = main_report
        
        # Look for responsibility report in the analysis directory
        responsibility_report = self.output_dir / f"responsibility_report_{self.timestamp}.html"
        if responsibility_report.exists():
            reports['responsibility_report'] = responsibility_report
        
        # Look for gantt chart in the analysis directory
        gantt_chart = self.output_dir / f"gantt_chart_{self.timestamp}.html"
        if gantt_chart.exists():
            reports['gantt_chart'] = gantt_chart
        
        return reports
    
    def copy_assets_to_output(self) -> None:
        """Assets are already in the output directory, so this is a no-op"""
        print("📋 Assets already in analysis directory - no copying needed")
        
        # List existing assets
        png_files = list(self.output_dir.glob(f"*{self.timestamp}*.png"))
        json_files = list(self.output_dir.glob(f"*{self.timestamp}*.json"))
        csv_files = list(self.output_dir.glob(f"*{self.timestamp}*.csv"))
        
        for png_file in png_files:
            print(f"   📊 Found: {png_file.name}")
        for json_file in json_files:
            print(f"   📄 Found: {json_file.name}")
        for csv_file in csv_files:
            print(f"   📈 Found: {csv_file.name}")
    
    def create_combined_html(self, reports: Dict[str, Optional[Path]]) -> Path:
        """Create a combined HTML document with all reports"""
        print("📄 Creating combined HTML document...")
        
        combined_html = self.output_dir / f"combined_report_{self.timestamp}.html"
        
        # Read the main report to extract metadata
        main_content = ""
        responsibility_content = ""
        gantt_content = ""
        
        if reports['main_report']:
            with open(reports['main_report'], 'r', encoding='utf-8') as f:
                main_content = f.read()
        
        if reports['responsibility_report']:
            with open(reports['responsibility_report'], 'r', encoding='utf-8') as f:
                responsibility_content = f.read()
        
        if reports['gantt_chart']:
            with open(reports['gantt_chart'], 'r', encoding='utf-8') as f:
                gantt_content = f.read()
        
        # Create combined HTML
        combined_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinguaLint Comprehensive Analysis Report - {self.timestamp}</title>
    <style>
        @page {{
            size: A4;
            margin: 0.75in;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.4;
            margin: 0;
            padding: 0;
            background: white;
            color: #333;
            font-size: 11pt;
        }}
        
        .cover-page {{
            text-align: center;
            padding: 2in 0.5in;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin-bottom: 0.5in;
            border-radius: 8px;
            page-break-after: always;
        }}
        
        .cover-page h1 {{
            font-size: 2.5em;
            margin-bottom: 0.5in;
            font-weight: 300;
        }}
        
        .cover-page .subtitle {{
            font-size: 1.3em;
            opacity: 0.9;
            margin-bottom: 0.5in;
        }}
        
        .cover-page .timestamp {{
            font-size: 1em;
            opacity: 0.8;
        }}
        
        .section-divider {{
            page-break-before: always;
            margin: 0.5in 0;
            text-align: center;
            padding: 0.5in;
            background: #f8f9fa;
            border-radius: 8px;
            page-break-after: avoid;
        }}
        
        .section-divider h2 {{
            color: #2c3e50;
            font-size: 1.8em;
            margin: 0;
        }}
        
        .report-section {{
            margin-bottom: 0.5in;
            page-break-inside: avoid;
        }}
        
        .toc {{
            background: #f8f9fa;
            padding: 0.5in;
            border-radius: 8px;
            margin: 0.5in 0;
            page-break-after: always;
        }}
        
        .toc h2 {{
            color: #2c3e50;
            margin-top: 0;
            font-size: 1.5em;
        }}
        
        .toc ul {{
            list-style: none;
            padding: 0;
        }}
        
        .toc li {{
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }}
        
        .toc a {{
            color: #3498db;
            text-decoration: none;
            font-size: 1em;
        }}
        
        /* Image sizing for PDF */
        img {{
            max-width: 100% !important;
            height: auto !important;
            display: block;
            margin: 0.25in auto;
            page-break-inside: avoid;
        }}
        
        /* Visualization containers */
        .visualization {{
            text-align: center;
            margin: 0.25in 0;
            padding: 0.25in;
            background: #f8f9fa;
            border-radius: 8px;
            page-break-inside: avoid;
        }}
        
        .visualization img {{
            max-width: 95% !important;
            max-height: 6in !important;
            width: auto !important;
            height: auto !important;
        }}
        
        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 0.25in 0;
            font-size: 9pt;
            page-break-inside: avoid;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 6px;
            text-align: left;
            word-wrap: break-word;
        }}
        
        th {{
            background: #f2f2f2;
            font-weight: bold;
        }}
        
        /* Headers */
        h1 {{ font-size: 1.8em; margin: 0.5in 0 0.25in 0; page-break-after: avoid; }}
        h2 {{ font-size: 1.5em; margin: 0.4in 0 0.2in 0; page-break-after: avoid; }}
        h3 {{ font-size: 1.3em; margin: 0.3in 0 0.15in 0; page-break-after: avoid; }}
        h4 {{ font-size: 1.1em; margin: 0.25in 0 0.1in 0; page-break-after: avoid; }}
        
        /* Paragraphs */
        p {{
            margin: 0.15in 0;
            text-align: justify;
        }}
        
        /* Lists */
        ul, ol {{
            margin: 0.15in 0;
            padding-left: 0.5in;
        }}
        
        li {{
            margin: 0.05in 0;
        }}
        
        /* Stats grid - make it PDF friendly */
        .stats-grid {{
            display: block !important;
            margin: 0.25in 0;
        }}
        
        .stat-card {{
            display: inline-block;
            width: 30%;
            margin: 0.1in 1%;
            padding: 0.15in;
            background: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            text-align: center;
            vertical-align: top;
        }}
        
        .stat-number {{
            font-size: 1.5em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 0.05in;
        }}
        
        .stat-label {{
            color: #7f8c8d;
            font-size: 0.8em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        /* Grid sections for Core Subjects, Phenomena, Wikipedia - make PDF friendly */
        .data-tables div[style*="display: grid"] {{
            display: block !important;
            margin: 0.25in 0;
        }}
        
        .data-tables div[style*="display: grid"] > div {{
            display: inline-block;
            width: 30%;
            margin: 0.1in 1%;
            padding: 0.15in;
            border-radius: 4px;
            vertical-align: top;
            box-sizing: border-box;
            font-size: 0.9em;
        }}
        
        /* PDF grid container for converted grid sections */
        .pdf-grid-container {{
            display: block !important;
            margin: 0.25in 0;
        }}
        
        .pdf-grid-container > div {{
            display: inline-block;
            width: 30%;
            margin: 0.1in 1%;
            padding: 0.15in;
            border-radius: 4px;
            vertical-align: top;
            box-sizing: border-box;
            font-size: 0.9em;
            page-break-inside: avoid;
        }}
        
        /* Ensure grid items don't break across pages */
        .data-tables div[style*="display: grid"] > div {{
            page-break-inside: avoid;
        }}
        
        /* Risk badges */
        .risk-badge {{
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.7em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        
        .risk-very-low {{ background: #2ecc71; color: white; }}
        .risk-low {{ background: #27ae60; color: white; }}
        .risk-moderate {{ background: #f39c12; color: white; }}
        .risk-high {{ background: #e74c3c; color: white; }}
        .risk-very-high {{ background: #c0392b; color: white; }}
        
        /* Entity table - make it more compact for PDF */
        .entity-table {{
            font-size: 8pt;
            margin: 0.25in 0;
        }}
        
        .entity-table th {{
            background: #34495e;
            color: white;
            padding: 8px 4px;
            font-size: 8pt;
        }}
        
        .entity-table td {{
            padding: 6px 4px;
            border-bottom: 1px solid #ecf0f1;
        }}
        
        /* Methodology section */
        .methodology {{
            background: #ecf0f1;
            padding: 0.25in;
            border-radius: 8px;
            margin: 0.25in 0;
            page-break-inside: avoid;
        }}
        
        .methodology h3 {{
            color: #2c3e50;
            margin-top: 0;
        }}
        
        .methodology ul {{
            margin: 0.1in 0;
        }}
        
        /* Force page breaks */
        .page-break {{
            page-break-before: always;
        }}
        
        /* Avoid page breaks */
        .no-break {{
            page-break-inside: avoid;
        }}
        
        /* Hide interactive elements in PDF */
        script, .interactive-only {{
            display: none !important;
        }}
        
        /* Ensure content fits in margins */
        .container {{
            max-width: 100%;
            margin: 0;
            padding: 0;
        }}
        
        /* D3.js visualization containers - make them PDF friendly */
        #visualization, .d3-container {{
            display: none !important;
        }}
        
        /* Replace D3 with static message */
        .d3-replacement {{
            text-align: center;
            padding: 0.5in;
            background: #f8f9fa;
            border: 2px dashed #ccc;
            border-radius: 8px;
            margin: 0.25in 0;
        }}
    </style>
</head>
<body>
    <!-- Cover Page -->
    <div class="cover-page">
        <h1>LinguaLint</h1>
        <div class="subtitle">Comprehensive Analysis Report</div>
        <div class="timestamp">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        <div class="timestamp">Analysis ID: {self.timestamp}</div>
    </div>
    
    <!-- Table of Contents -->
    <div class="toc">
        <h2>📋 Table of Contents</h2>
        <ul>
            <li><a href="#main-analysis">1. Main Event Code Analysis</a></li>
            <li><a href="#responsibility-analysis">2. Responsibility Futures Analysis</a></li>
            <li><a href="#project-management">3. Project Management & Timeline</a></li>
            <li><a href="#appendix">4. Appendix - Raw Data & Assets</a></li>
        </ul>
    </div>
    
    <!-- Main Analysis Section -->
    <div class="section-divider" id="main-analysis">
        <h2>📊 Main Event Code Analysis</h2>
    </div>
    
    <div class="report-section">
        {self._extract_body_content(main_content) if main_content else '<p>Main analysis report not available.</p>'}
    </div>
    
    <!-- Responsibility Analysis Section -->
    <div class="section-divider" id="responsibility-analysis">
        <h2>🎯 Responsibility Futures Analysis</h2>
    </div>
    
    <div class="report-section">
        {self._extract_body_content(responsibility_content) if responsibility_content else '<p>Responsibility analysis report not available.</p>'}
    </div>
    
    <!-- Project Management Section -->
    <div class="section-divider" id="project-management">
        <h2>📈 Project Management & Timeline</h2>
    </div>
    
    <div class="report-section">
        {self._extract_body_content(gantt_content) if gantt_content else '<p>Project timeline not available.</p>'}
    </div>
    
    <!-- Appendix -->
    <div class="section-divider" id="appendix">
        <h2>📎 Appendix</h2>
    </div>
    
    <div class="report-section">
        <h3>Generated Files</h3>
        <ul>
            <li>📄 Raw extraction data: extraction_{self.timestamp}.json</li>
            <li>📊 Responsibility analysis: extraction_{self.timestamp}_responsibility_analysis.json</li>
            <li>📈 Project plan: project_plan_{self.timestamp}.csv</li>
            <li>🎨 Visualizations: Multiple PNG files with analysis charts</li>
        </ul>
        
        <h3>Analysis Metadata</h3>
        <p><strong>Timestamp:</strong> {self.timestamp}</p>
        <p><strong>Generated:</strong> {datetime.now().isoformat()}</p>
        <p><strong>System:</strong> LinguaLint Event Code Extractor with Responsibility Futures Analysis</p>
    </div>
</body>
</html>
"""
        
        with open(combined_html, 'w', encoding='utf-8') as f:
            f.write(combined_content)
        
        print(f"✅ Combined HTML created: {combined_html}")
        return combined_html
    
    def _extract_body_content(self, html_content: str) -> str:
        """Extract content from HTML body, removing head and script tags, and optimizing for PDF"""
        import re
        
        # Extract body content
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL | re.IGNORECASE)
        if body_match:
            body_content = body_match.group(1)
        else:
            # If no body tag, take everything after head
            head_end = re.search(r'</head>', html_content, re.IGNORECASE)
            if head_end:
                body_content = html_content[head_end.end():]
            else:
                body_content = html_content
        
        # Remove script tags and interactive elements
        body_content = re.sub(r'<script[^>]*>.*?</script>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
        body_content = re.sub(r'<button[^>]*>.*?</button>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove D3.js visualization divs and replace with static message
        body_content = re.sub(
            r'<div[^>]*id="visualization"[^>]*>.*?</div>',
            '<div class="d3-replacement"><p><strong>Interactive D3.js Visualization</strong><br/>This section contains an interactive network graph that is available in the HTML version of this report.</p></div>',
            body_content,
            flags=re.DOTALL | re.IGNORECASE
        )
        
        # Update image paths to be relative and add PDF-friendly sizing
        body_content = re.sub(r'<img([^>]*?)src="([^"]*\.png)"([^>]*?)>', r'<img\1src="\2"\3 style="max-width: 95% !important; max-height: 6in !important; height: auto !important; display: block; margin: 0.25in auto;">', body_content)
        
        # Fix stats grid for PDF
        body_content = re.sub(
            r'<div[^>]*class="stats-grid"[^>]*>',
            '<div class="stats-grid">',
            body_content
        )
        
        # Fix CSS grid sections for PDF (Core Subjects, Phenomena, Wikipedia)
        body_content = re.sub(
            r'<div style="display: grid; grid-template-columns: repeat\(auto-fill, minmax\(200px, 1fr\)\); gap: 10px; margin: 20px 0;">',
            '<div class="pdf-grid-container">',
            body_content
        )
        
        # Make tables more PDF-friendly
        body_content = re.sub(r'<table([^>]*?)>', r'<table\1 style="font-size: 9pt; page-break-inside: avoid;">', body_content)
        
        # Add page break avoidance to visualization containers
        body_content = re.sub(
            r'<div[^>]*class="visualization"[^>]*>',
            '<div class="visualization no-break">',
            body_content
        )
        
        # Remove any remaining interactive controls
        body_content = re.sub(r'<div[^>]*class="controls"[^>]*>.*?</div>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Clean up excessive whitespace
        body_content = re.sub(r'\n\s*\n\s*\n', '\n\n', body_content)
        
        return body_content
    
    def generate_pdf_weasyprint(self, html_file: Path) -> Optional[Path]:
        """Generate PDF using WeasyPrint"""
        if not PDF_WEASYPRINT_AVAILABLE:
            return None
        
        try:
            pdf_file = self.output_dir / f"lingualint_analysis_{self.timestamp}.pdf"
            
            print("🔄 Generating PDF with WeasyPrint...")
            weasyprint.HTML(filename=str(html_file)).write_pdf(str(pdf_file))
            
            print(f"✅ PDF generated: {pdf_file}")
            return pdf_file
            
        except Exception as e:
            print(f"❌ WeasyPrint PDF generation failed: {e}")
            return None
    
    def generate_pdf_pdfkit(self, html_file: Path) -> Optional[Path]:
        """Generate PDF using pdfkit (wkhtmltopdf)"""
        if not PDF_PDFKIT_AVAILABLE:
            return None
        
        try:
            pdf_file = self.output_dir / f"lingualint_analysis_{self.timestamp}.pdf"
            
            print("🔄 Generating PDF with pdfkit...")
            
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'no-outline': None,
                'enable-local-file-access': None
            }
            
            pdfkit.from_file(str(html_file), str(pdf_file), options=options)
            
            print(f"✅ PDF generated: {pdf_file}")
            return pdf_file
            
        except Exception as e:
            print(f"❌ pdfkit PDF generation failed: {e}")
            return None
    
    def generate_pdf_chrome(self, html_file: Path) -> Optional[Path]:
        """Generate PDF using Chrome/Chromium headless"""
        try:
            pdf_file = self.output_dir / f"lingualint_analysis_{self.timestamp}.pdf"
            
            print("🔄 Generating PDF with Chrome headless...")
            
            # Try different Chrome/Chromium executables
            chrome_commands = [
                'google-chrome',
                'chromium',
                'chromium-browser',
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '/usr/bin/google-chrome',
                '/usr/bin/chromium'
            ]
            
            chrome_cmd = None
            for cmd in chrome_commands:
                if shutil.which(cmd) or Path(cmd).exists():
                    chrome_cmd = cmd
                    break
            
            if not chrome_cmd:
                print("❌ Chrome/Chromium not found")
                return None
            
            cmd = [
                chrome_cmd,
                '--headless',
                '--disable-gpu',
                '--print-to-pdf=' + str(pdf_file),
                '--print-to-pdf-no-header',
                '--run-all-compositor-stages-before-draw',
                '--virtual-time-budget=10000',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--print-to-pdf-no-header',
                '--no-margins',
                'file://' + str(html_file.absolute())
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and pdf_file.exists():
                print(f"✅ PDF generated: {pdf_file}")
                return pdf_file
            else:
                print(f"❌ Chrome PDF generation failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Chrome PDF generation failed: {e}")
            return None
    
    def generate_comprehensive_pdf(self) -> Optional[Path]:
        """Generate comprehensive PDF report using available methods"""
        print("\n" + "="*60)
        print("📄 GENERATING COMPREHENSIVE PDF REPORT")
        print("="*60)
        
        # Find HTML reports
        reports = self.find_html_reports()
        found_reports = [k for k, v in reports.items() if v is not None]
        
        print(f"📋 Found {len(found_reports)} HTML reports:")
        for report_type, report_path in reports.items():
            if report_path:
                print(f"   ✅ {report_type}: {report_path.name}")
            else:
                print(f"   ❌ {report_type}: Not found")
        
        if not found_reports:
            print("❌ No HTML reports found for PDF generation")
            return None
        
        # Copy assets to output directory
        self.copy_assets_to_output()
        
        # Create combined HTML
        combined_html = self.create_combined_html(reports)
        
        # Try different PDF generation methods
        pdf_file = None
        
        # Method 1: WeasyPrint (best for complex CSS)
        if PDF_WEASYPRINT_AVAILABLE:
            pdf_file = self.generate_pdf_weasyprint(combined_html)
        
        # Method 2: pdfkit (wkhtmltopdf)
        if not pdf_file and PDF_PDFKIT_AVAILABLE:
            pdf_file = self.generate_pdf_pdfkit(combined_html)
        
        # Method 3: Chrome headless (fallback)
        if not pdf_file:
            pdf_file = self.generate_pdf_chrome(combined_html)
        
        if pdf_file:
            file_size = pdf_file.stat().st_size
            print(f"\n🎉 PDF GENERATION SUCCESSFUL!")
            print(f"📄 File: {pdf_file}")
            print(f"📊 Size: {file_size:,} bytes")
            print(f"📁 Directory: {self.output_dir}")
            
            # List all files in output directory
            print(f"\n📋 Complete analysis package:")
            for file in sorted(self.output_dir.iterdir()):
                if file.is_file():
                    size = file.stat().st_size
                    print(f"   📄 {file.name} ({size:,} bytes)")
        else:
            print(f"\n❌ PDF generation failed with all methods")
            print(f"💡 Install PDF dependencies:")
            print(f"   pip install weasyprint")
            print(f"   pip install pdfkit")
            print(f"   # or ensure Chrome/Chromium is installed")
        
        return pdf_file

def generate_comprehensive_pdf(timestamp: str, analysis_dir: Path = None) -> Optional[Path]:
    """
    Main function to generate comprehensive PDF from LinguaLint reports
    """
    generator = LinguaLintPDFGenerator(timestamp, analysis_dir)
    return generator.generate_comprehensive_pdf()

def main():
    """Main execution function"""
    if len(sys.argv) != 2:
        print("Usage: python pdf_generator.py <timestamp>")
        print("Example: python pdf_generator.py 20260101_093621")
        sys.exit(1)
    
    timestamp = sys.argv[1]
    
    try:
        pdf_file = generate_comprehensive_pdf(timestamp)
        
        if pdf_file:
            print(f"\n✅ Success! PDF generated: {pdf_file}")
            sys.exit(0)
        else:
            print(f"\n❌ Failed to generate PDF")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()