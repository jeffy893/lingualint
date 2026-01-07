#!/usr/bin/env node
/*
 * LinguaLint - AI-powered project planning and analysis platform
 * Copyright (C) 2026 Jefferson Richards
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

import express from 'express';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const app = express();
const port = 3001;

app.use(express.json());

app.get('/', (req, res) => {
  res.send(`
<!DOCTYPE html>
<html>
<head>
    <title>LinguaLint Event Code Extractor</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        textarea { width: 100%; height: 200px; margin: 10px 0; }
        button { background: #007cba; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        .result { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>LinguaLint Event Code Extractor</h1>
    <textarea id="textInput" placeholder="Paste your risk factor text here...">The COVID-19 pandemic has materially adversely affected our business operations.</textarea>
    <br>
    <button onclick="extractRiskFactors()">Extract Risk Factors</button>
    <div id="result"></div>
    
    <script>
        function extractRiskFactors() {
            const text = document.getElementById('textInput').value;
            const resultDiv = document.getElementById('result');
            
            if (!text.trim()) {
                alert('Please enter text');
                return;
            }
            
            resultDiv.innerHTML = '<div>Processing...</div>';
            
            fetch('/extract', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text_content: text })
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    resultDiv.innerHTML = '<div class="result"><h3>Success!</h3><pre>' + result.output + '</pre></div>';
                } else {
                    resultDiv.innerHTML = '<div class="result"><h3>Error</h3><pre>' + result.error + '</pre></div>';
                }
            })
            .catch(error => {
                resultDiv.innerHTML = '<div class="result"><h3>Error</h3><p>' + error.message + '</p></div>';
            });
        }
    </script>
</body>
</html>
  `);
});

app.post('/extract', (req, res) => {
  const { text_content } = req.body;
  
  const python = spawn('python3.10', ['-c', `
from src.nlp_processor import ModernNLPProcessor
from src.report_generator import generate_html_report
from src.responsibility_analyzer import analyze_responsibility
from src.responsibility_report_generator import generate_responsibility_reports
from src.pdf_generator import generate_comprehensive_pdf
import json
from pathlib import Path
from datetime import datetime

try:
    processor = ModernNLPProcessor()
    text = """${text_content.replace(/"/g, '\\"')}"""
    
    results = processor.process_text(text, enrich_wikipedia=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create lingualint_analysis directory structure
    analysis_base_dir = Path("./lingualint_analysis")
    analysis_base_dir.mkdir(exist_ok=True)
    
    # Create timestamped analysis folder
    analysis_dir = analysis_base_dir / f"analysis_{timestamp}"
    analysis_dir.mkdir(exist_ok=True)
    
    json_file = analysis_dir / f"extraction_{timestamp}.json"
    html_file = analysis_dir / f"report_{timestamp}.html"
    
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    generate_html_report(str(json_file), str(html_file))
    
    # Generate Responsibility Futures Analysis
    responsibility_status = "SKIPPED"
    try:
        responsibility_report = analyze_responsibility(str(json_file))
        responsibility_json = json_file.with_name(f"extraction_{timestamp}_responsibility_analysis.json")
        with open(responsibility_json, 'w') as f:
            json.dump(responsibility_report, f, indent=2)
        
        responsibility_files = generate_responsibility_reports(str(responsibility_json))
        responsibility_status = f"COMPLETED - {responsibility_report['total_entities']} entities analyzed"
    except Exception as resp_e:
        responsibility_status = f"FAILED - {str(resp_e)}"
    
    # Generate Comprehensive PDF
    pdf_status = "SKIPPED"
    try:
        pdf_file = generate_comprehensive_pdf(timestamp, analysis_dir)
        if pdf_file:
            pdf_status = f"COMPLETED - {pdf_file.name}"
        else:
            pdf_status = "FAILED - See logs"
    except Exception as pdf_e:
        pdf_status = f"FAILED - {str(pdf_e)}"
    
    sentences_count = len(results.get('_source', {}).get('sentences', []))
    phen_count = len(results.get('_source', {}).get('phen', []))
    wiki_count = len(results.get('_source', {}).get('wiki', []))
    
    print(f"Processed {sentences_count} sentences, {phen_count} phenomena, {wiki_count} wiki entries")
    print(f"Responsibility Analysis: {responsibility_status}")
    print(f"PDF Generation: {pdf_status}")
    print(f"Main Report: {html_file}")
    print(f"Analysis Directory: {analysis_dir}")
    
except Exception as e:
    print(f"Error: {str(e)}")
    exit(1)
  `], { cwd: __dirname });
  
  let output = '';
  let error = '';
  
  python.stdout.on('data', (data) => {
    output += data.toString();
  });
  
  python.stderr.on('data', (data) => {
    error += data.toString();
  });
  
  python.on('close', (code) => {
    if (code === 0) {
      res.json({ success: true, output });
    } else {
      res.json({ success: false, error: error || 'Unknown error' });
    }
  });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});