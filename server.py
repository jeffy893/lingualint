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
LinguaLint MCP Server

Model Context Protocol server that exposes LinguaLint risk factor extraction
as tools for MCP clients. Uses FastMCP for simple server implementation.
"""

import json
import tempfile
import smtplib
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from mcp.server.fastmcp import FastMCP
from src.nlp_processor import ModernNLPProcessor
from src.report_generator import generate_html_report
from src.responsibility_analyzer import analyze_responsibility
from src.responsibility_report_generator import generate_responsibility_reports
from src.pdf_generator import generate_comprehensive_pdf

# Initialize MCP server
mcp = FastMCP("LinguaLint Event Code Extractor")

# Global processor instance
processor = ModernNLPProcessor()

# Output directory for reports
REPORTS_DIR = Path("./reports")
REPORTS_DIR.mkdir(exist_ok=True)

@mcp.tool()
def extract_risk_factors(text_content: str) -> str:
    """
    Extract risk factors and generate interactive D3.js report from text content.
    
    Args:
        text_content: Input text to analyze for risk factors
        
    Returns:
        Summary of extraction results and path to generated HTML report
    """
    
    if not text_content.strip():
        return "Error: Empty text content provided"

    try:
        # Process text through NLP pipeline
        results = processor.process_text(text_content, enrich_wikipedia=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = REPORTS_DIR / f"extraction_{timestamp}.json"
        html_file = REPORTS_DIR / f"report_{timestamp}.html"
        
        # Save JSON results
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Generate HTML report
        generate_html_report(str(json_file), str(html_file))
        
        # Generate Responsibility Futures Analysis
        responsibility_summary = ""
        try:
            # Analyze responsibility
            responsibility_report = analyze_responsibility(str(json_file))
            
            # Save responsibility analysis JSON
            responsibility_json = json_file.with_name(f"extraction_{timestamp}_responsibility_analysis.json")
            with open(responsibility_json, 'w', encoding='utf-8') as f:
                json.dump(responsibility_report, f, indent=2, ensure_ascii=False)
            
            # Generate responsibility visualizations and HTML report
            responsibility_files = generate_responsibility_reports(str(responsibility_json))
            
            # Add to summary
            responsibility_summary = f"""
- Responsibility Analysis: COMPLETED
- Analyzed {responsibility_report['total_entities']} entities across {responsibility_report['total_events']} events
- Responsibility report: {responsibility_files.get('html_report', 'N/A')}
- Generated visualizations: {len([f for f in responsibility_files.values() if f])} files"""
            
        except Exception as e:
            responsibility_summary = f"\n- Responsibility Analysis: FAILED ({str(e)})"
        
        # Generate Comprehensive PDF
        pdf_summary = ""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_file = generate_comprehensive_pdf(timestamp, REPORTS_DIR)
            
            if pdf_file:
                pdf_summary = f"\n- Comprehensive PDF: GENERATED ({pdf_file.name})"
            else:
                pdf_summary = f"\n- Comprehensive PDF: FAILED (see logs)"
                
        except Exception as e:
            pdf_summary = f"\n- Comprehensive PDF: FAILED ({str(e)})"
        
        # Create summary
        sentences_count = len(results.get('_source', {}).get('sentences', []))
        phen_count = len(results.get('_source', {}).get('phen', []))
        wiki_count = len(results.get('_source', {}).get('wiki', []))
        
        summary = f"""Risk Factor Extraction Complete:
- Processed {sentences_count} sentences
- Identified {phen_count} key phenomena
- Enriched with {wiki_count} Wikipedia entries{responsibility_summary}{pdf_summary}
- Interactive report: {html_file.absolute()}
- Raw data: {json_file.absolute()}

Open the HTML file in your browser to view the interactive D3.js visualization."""
        
        return summary
        
    except Exception as e:
        return f"Error during extraction: {str(e)}"

if __name__ == "__main__":
    mcp.run()