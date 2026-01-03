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
Modern LinguaLint HTML Report Generator

Generates self-contained HTML report with D3.js force-directed graph
from extracted JSON data.
"""

import json
from pathlib import Path

def generate_html_report(json_file, output_file="index.html"):
    """Generate self-contained HTML report with D3.js visualization"""
    
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract data from the nested structure
    source_data = data.get('_source', {})
    sentences = source_data.get('sentences', [])
    subjects = source_data.get('subjects', [])
    phen = source_data.get('phen', [])
    wiki_data = source_data.get('wiki', [])
    
    # Build graph links with better connectivity
    links = []
    nodes_set = set()
    
    # Create hierarchical structure: Sentences -> Subjects -> Phenomena -> Wikipedia
    for i, sentence in enumerate(sentences):
        sentence_node = f"S{i}: {sentence['sentence'][:40]}..."
        nodes_set.add(sentence_node)
        
        # Link sentences to their subjects
        sentence_subjects = [subj for subj in subjects if subj.lower() in sentence['sentence'].lower()]
        for subj in sentence_subjects[:3]:  # Limit to 3 subjects per sentence
            subj_node = f"SUBJ: {subj}"
            nodes_set.add(subj_node)
            links.append({
                "source": sentence_node,
                "target": subj_node,
                "color": "#2E8B57"  # Sea green for sentence-subject links
            })
            
            # Link subjects to related phenomena
            related_phen = [p for p in phen if any(word in p.lower() for word in subj.lower().split())]
            for phenomenon in related_phen[:2]:  # Limit to 2 phenomena per subject
                phen_node = f"PHEN: {phenomenon}"
                nodes_set.add(phen_node)
                links.append({
                    "source": subj_node,
                    "target": phen_node,
                    "color": "#4169E1"  # Royal blue for subject-phenomena links
                })
    
    # Link phenomena to Wikipedia entries
    for i, wiki in enumerate(wiki_data):
        wiki_concept = wiki.get('wiki_search_content', '')
        wiki_node = f"WIKI: {wiki_concept}"
        nodes_set.add(wiki_node)
        
        # Find matching phenomena for this wiki entry
        matching_phen = [p for p in phen if wiki_concept.lower() in p.lower() or p.lower() in wiki_concept.lower()]
        for phenomenon in matching_phen[:1]:  # One wiki per phenomenon
            phen_node = f"PHEN: {phenomenon}"
            if phen_node in nodes_set:
                links.append({
                    "source": phen_node,
                    "target": wiki_node,
                    "color": "#FF6347"  # Tomato red for phenomena-wiki links
                })
    
    # Convert to JSON strings for embedding
    links_json = json.dumps(links, indent=2)
    
    # Generate HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinguaLint Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ margin-bottom: 30px; }}
        .header a {{ margin-right: 15px; color: #0066cc; }}
        .node {{ stroke: #fff; stroke-width: 2px; }}
        .link {{ stroke: #777; stroke-width: 1px; }}
        .controls {{ margin: 20px 0; }}
        .data-tables {{ margin-top: 30px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .phenomenon {{ color: blue; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>LinguaLint Analysis Report</h1>
        <a href="https://lingualint.com" target="_blank">LinguaLint Website</a>
        <a href="https://riskrunners.com" target="_blank">Public Company Risk Factors</a>
        <a href="https://jefferson.cloud" target="_blank">Jefferson.Cloud</a>
        <a href="https://richards.systems" target="_blank">Richards.Systems</a>
        <a href="https://richards.plus" target="_blank">Richards.Plus</a>
    </div>
    
    <div class="controls">
        <button onclick="restartSimulation()">Restart Simulation</button>
        <button onclick="toggleLabels()">Toggle Labels</button>
    </div>
    
    <div id="visualization"></div>
    
    <div class="data-tables">
        <h2>Core Subjects (Capitalized Entities)</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px; margin: 20px 0;">
            {''.join(f'<div style="background: #e6f3ff; padding: 8px; border-radius: 4px; border-left: 3px solid #0066cc;"><span class="phenomenon">{subj}</span></div>' for subj in subjects)}
        </div>
        
        <h2>Phenomena (Non-capitalized Concepts)</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px; margin: 20px 0;">
            {''.join(f'<div style="background: #f0f8e6; padding: 8px; border-radius: 4px; border-left: 3px solid #66cc00;"><span>{concept}</span></div>' for concept in phen)}
        </div>
        
        <h2>Wikipedia Candidates</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px; margin: 20px 0;">
            {''.join(f'<div style="background: #fff0f5; padding: 8px; border-radius: 4px; border-left: 3px solid #ff69b4;"><span>{candidate}</span></div>' for candidate in source_data.get("wiki_blues", []))}
        </div>
        
        <h2>Extracted Sentences</h2>
        <table>
            <thead>
                <tr><th>Sentence</th><th>Warm Vector<br><small>(Positivity, Engagement, Optimism)</small></th><th>Cold Vector<br><small>(Negativity, Risk, Uncertainty)</small></th></tr>
            </thead>
            <tbody>
                {"".join(f'<tr><td>{highlight_phenomena(s["sentence"], phen)}</td><td>{format_vector(s.get("warm_vector", [0,0,0]), "warm")}</td><td>{format_vector(s.get("cold_vector", [0,0,0]), "cold")}</td></tr>' for s in sentences)}
            </tbody>
        </table>
        
        <h2>Wikipedia Enrichment</h2>
        <table>
            <thead>
                <tr><th>Concept</th><th>Summary</th><th>URL</th></tr>
            </thead>
            <tbody>
                {"".join(f'<tr><td>{w.get("wiki_search_content", "")}</td><td>{w.get("wiki_summary", "")[:200]}...</td><td><a href="{w.get("wiki_url", "")}" target="_blank">{w.get("wiki_url", "").split("/")[-1].replace("_", " ")}</a></td></tr>' for w in wiki_data)}
            </tbody>
        </table>
    </div>

    <script src="https://d3js.org/d3.v3.min.js"></script>
    <script>
        // Embedded data
        var graphData = {links_json};
        
        // Visualization setup
        var width = 1200, height = 800;
        var showLabels = true;
        
        var svg = d3.select("#visualization")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .call(d3.behavior.zoom().on("zoom", function () {{
                svg.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")");
            }}))
            .append("g");
        
        // Create nodes from links
        var nodes = {{}};
        graphData.forEach(function(link) {{
            link.source = nodes[link.source] || (nodes[link.source] = {{name: link.source}});
            link.target = nodes[link.target] || (nodes[link.target] = {{name: link.target}});
        }});
        
        // Force layout with better spacing
        var force = d3.layout.force()
            .charge(-800)
            .linkDistance(function(d) {{
                // Different distances for different link types
                if (d.color === "#2E8B57") return 80;  // Sentence-Subject
                if (d.color === "#4169E1") return 60;  // Subject-Phenomena  
                if (d.color === "#FF6347") return 100; // Phenomena-Wiki
                return 80;
            }})
            .size([width, height])
            .nodes(d3.values(nodes))
            .links(graphData)
            .start();
        
        // Links
        var link = svg.selectAll(".link")
            .data(graphData)
            .enter().append("line")
            .attr("class", "link")
            .style("stroke", function(d) {{ return d.color; }});
        
        // Nodes with different sizes and colors by type
        var node = svg.selectAll(".node")
            .data(force.nodes())
            .enter().append("circle")
            .attr("class", "node")
            .attr("r", function(d) {{
                if (d.name.startsWith("S")) return 12;      // Sentences - largest
                if (d.name.startsWith("SUBJ:")) return 10;  // Subjects - medium
                if (d.name.startsWith("PHEN:")) return 8;   // Phenomena - small
                if (d.name.startsWith("WIKI:")) return 6;   // Wikipedia - smallest
                return 8;
            }})
            .style("fill", function(d) {{
                if (d.name.startsWith("S")) return "#FF4500";      // Orange for sentences
                if (d.name.startsWith("SUBJ:")) return "#32CD32";  // Lime green for subjects
                if (d.name.startsWith("PHEN:")) return "#4169E1";  // Royal blue for phenomena
                if (d.name.startsWith("WIKI:")) return "#FF1493";  // Deep pink for wikipedia
                return "#666";
            }})
            .call(force.drag);
        
        // Labels
        var label = svg.selectAll(".label")
            .data(force.nodes())
            .enter().append("text")
            .attr("class", "label")
            .text(function(d) {{ return d.name.length > 30 ? d.name.substring(0, 30) + "..." : d.name; }})
            .style("font-size", "10px")
            .style("fill", "#333");
        
        // Update positions
        force.on("tick", function() {{
            link.attr("x1", function(d) {{ return d.source.x; }})
                .attr("y1", function(d) {{ return d.source.y; }})
                .attr("x2", function(d) {{ return d.target.x; }})
                .attr("y2", function(d) {{ return d.target.y; }});
            
            node.attr("cx", function(d) {{ return d.x; }})
                .attr("cy", function(d) {{ return d.y; }});
            
            label.attr("x", function(d) {{ return d.x + 10; }})
                 .attr("y", function(d) {{ return d.y + 3; }});
        }});
        
        // Control functions
        function restartSimulation() {{
            force.start();
        }}
        
        function toggleLabels() {{
            showLabels = !showLabels;
            label.style("display", showLabels ? "block" : "none");
        }}
    </script>
</body>
</html>"""
    
    # Write HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML report generated: {output_file}")
    
    # Generate project plan at the end of processing
    try:
        from src.project_planner import generate_project_plan
        plan_results = generate_project_plan(str(json_file), str(Path(output_file).parent))
        print(f"📊 Project plan: {plan_results['csv']}")
        print(f"🌐 Interactive Gantt: {plan_results['html']}")
    except Exception as e:
        print(f"Project plan generation failed: {e}")

def format_vector(vector, vector_type=""):
    """Format vector values to 2 decimal places with conditional highlighting"""
    if not vector or vector == "N/A":
        return "N/A"
    
    formatted = f"[{', '.join(f'{v:.2f}' if v is not None else '0.00' for v in vector)}]"
    vector_sum = sum(v for v in vector if v is not None)
    
    if vector_sum > 0.009:
        if vector_type == "warm":
            return f'<span style="background-color: #ffcccc;">{formatted}</span>'
        elif vector_type == "cold":
            return f'<span style="background-color: #ccddff;">{formatted}</span>'
    
    return formatted

def highlight_phenomena(text, phenomena):
    """Highlight phenomena in text with blue color"""
    for phen in phenomena:
        if phen in text:
            text = text.replace(phen, f'<span class="phenomenon">{phen}</span>')
    return text

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate LinguaLint HTML Report")
    parser.add_argument("json_file", help="Input JSON file from NLP processing")
    parser.add_argument("-o", "--output", default="index.html", help="Output HTML file")
    
    args = parser.parse_args()
    
    if not Path(args.json_file).exists():
        print(f"Error: {args.json_file} not found")
        return 1
    
    generate_html_report(args.json_file, args.output)
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())