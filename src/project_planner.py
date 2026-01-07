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
LinguaLint Project Plan Generator

Generates MS Project CSV and Gantt chart visualizations from risk factor analysis results.
Creates actionable project plans based on extracted subjects, phenomena, and Wikipedia data.
"""

import json
import csv
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path

class LinguaLintProjectPlanner:
    def __init__(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.source = self.data.get('_source', {})
        self.project_start = datetime.fromisoformat(self.source.get('@timestamp', datetime.now().isoformat()))
        self.tasks = []
        self.task_id = 1
    
    def add_task(self, name, duration_days, start_date, predecessors="", resources="", notes=""):
        """Add a task to the project plan"""
        finish_date = start_date + timedelta(days=duration_days)
        task = {
            'ID': self.task_id,
            'Task_Name': name,
            'Duration': f"{duration_days} days",
            'Start_Date': start_date.strftime("%Y-%m-%d"),
            'Finish_Date': finish_date.strftime("%Y-%m-%d"),
            'Predecessors': predecessors,
            'Resource_Names': resources,
            'Notes': notes
        }
        self.tasks.append(task)
        current_id = self.task_id
        self.task_id += 1
        return current_id, finish_date
    
    def generate_project_plan(self):
        """Generate comprehensive project plan from LinguaLint analysis"""
        
        # Phase 1: Risk Assessment & Research
        phase1_start = self.project_start
        p1_id, p1_end = self.add_task(
            "Phase 1: Risk Assessment & Research", 
            0, phase1_start, "", "", "Initial analysis phase"
        )
        
        # Research tasks for core subjects
        subjects = self.source.get('subjects', [])
        subject_ids = []
        for i, subject in enumerate(subjects[:5]):  # Top 5 subjects
            note = f"Research regulatory and market implications of {subject}"
            s_id, s_end = self.add_task(
                f"Research Subject: {subject}", 
                2, phase1_start, str(p1_id), "Risk Analyst", note
            )
            subject_ids.append(s_id)
        
        # Wikipedia research tasks
        wiki_data = self.source.get('wiki', [])
        wiki_ids = []
        for item in wiki_data[:3]:  # Top 3 wiki entries
            if item.get('wiki_summary'):
                note = f"Background research: {item['wiki_url']}"
                w_id, w_end = self.add_task(
                    f"Wiki Research: {item['wiki_search_content']}", 
                    1, phase1_start, str(p1_id), "Researcher", note
                )
                wiki_ids.append(w_id)
        
        # Phase 2: Risk Mitigation Planning
        phase2_start = p1_end + timedelta(days=1)
        p2_pred = ",".join(map(str, subject_ids + wiki_ids))
        p2_id, p2_end = self.add_task(
            "Phase 2: Risk Mitigation Planning", 
            0, phase2_start, p2_pred, "", "Develop mitigation strategies"
        )
        
        # Analyze high-risk sentences for action items
        sentences = self.source.get('sentences', [])
        action_ids = []
        
        for i, sent in enumerate(sentences):
            warm_vector = sent.get('warm_vector', [0, 0, 0])
            cold_vector = sent.get('cold_vector', [0, 0, 0])
            
            warm_score = sum(v for v in warm_vector if v is not None)
            cold_score = sum(v for v in cold_vector if v is not None)
            
            # High-risk items need immediate attention
            if cold_score > 0.1:
                task_name = f"Mitigate High Risk Item #{i+1}"
                duration = 3
                resource = "Risk Manager"
                note = f"Address: {sent['sentence'][:150]}..."
                
                a_id, a_end = self.add_task(
                    task_name, duration, phase2_start, str(p2_id), resource, note
                )
                action_ids.append(a_id)
            
            # Positive opportunities
            elif warm_score > 0.1:
                task_name = f"Leverage Opportunity #{i+1}"
                duration = 2
                resource = "Strategy Lead"
                note = f"Opportunity: {sent['sentence'][:150]}..."
                
                a_id, a_end = self.add_task(
                    task_name, duration, phase2_start, str(p2_id), resource, note
                )
                action_ids.append(a_id)
        
        # Phase 3: Implementation & Monitoring
        phase3_start = p2_end + timedelta(days=1)
        p3_pred = ",".join(map(str, action_ids)) if action_ids else str(p2_id)
        p3_id, p3_end = self.add_task(
            "Phase 3: Implementation & Monitoring", 
            0, phase3_start, p3_pred, "", "Execute and track progress"
        )
        
        # Implementation tasks
        phenomena = self.source.get('phen', [])
        for i, phen in enumerate(phenomena[:3]):  # Top 3 phenomena
            task_name = f"Monitor: {phen}"
            note = f"Ongoing monitoring and assessment of {phen}"
            self.add_task(
                task_name, 5, phase3_start, str(p3_id), "Operations Team", note
            )
        
        # Final review
        self.add_task(
            "Project Review & Documentation", 
            2, p3_end, str(p3_id), "Project Manager", 
            "Compile results and lessons learned"
        )
    
    def save_ms_project_csv(self, filename="lingualint_project_plan.csv"):
        """Save project plan as MS Project compatible CSV"""
        headers = ['ID', 'Task_Name', 'Duration', 'Start_Date', 'Finish_Date', 
                  'Predecessors', 'Resource_Names', 'Notes']
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(self.tasks)
        
        return filename
    
    def create_html_gantt(self, output_file="lingualint_gantt_chart.html"):
        """Create interactive HTML Gantt chart"""
        if not self.tasks:
            return None
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>LinguaLint Project Plan - Gantt Chart</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .gantt-container {{ overflow-x: auto; }}
        .gantt-table {{ border-collapse: collapse; width: 100%; min-width: 800px; }}
        .gantt-table th, .gantt-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        .gantt-table th {{ background-color: #f2f2f2; }}
        .task-bar {{ height: 20px; border-radius: 3px; margin: 2px 0; }}
        .risk-analyst {{ background-color: #FF6B6B; }}
        .researcher {{ background-color: #4ECDC4; }}
        .risk-manager {{ background-color: #45B7D1; }}
        .strategy-lead {{ background-color: #96CEB4; }}
        .operations-team {{ background-color: #FFEAA7; }}
        .project-manager {{ background-color: #DDA0DD; }}
        .milestone {{ background-color: #D3D3D3; }}
    </style>
</head>
<body>
    <h1>LinguaLint Risk Factor Analysis - Project Plan</h1>
    <p>Generated from risk factor extraction on {self.project_start.strftime('%Y-%m-%d %H:%M')}</p>
    
    <div class="gantt-container">
        <table class="gantt-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Task Name</th>
                    <th>Duration</th>
                    <th>Start Date</th>
                    <th>Finish Date</th>
                    <th>Resource</th>
                    <th>Visual Timeline</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for task in self.tasks:
            resource_class = task['Resource_Names'].lower().replace(' ', '-') or 'milestone'
            html_content += f"""
                <tr>
                    <td>{task['ID']}</td>
                    <td>{task['Task_Name']}</td>
                    <td>{task['Duration']}</td>
                    <td>{task['Start_Date']}</td>
                    <td>{task['Finish_Date']}</td>
                    <td>{task['Resource_Names']}</td>
                    <td><div class="task-bar {resource_class}" title="{task['Notes'][:100]}"></div></td>
                </tr>
            """
        
        html_content += """
            </tbody>
        </table>
    </div>
    
    <h2>Legend</h2>
    <div style="display: flex; flex-wrap: wrap; gap: 15px; margin: 20px 0;">
        <div><span class="task-bar risk-analyst" style="display: inline-block; width: 20px;"></span> Risk Analyst</div>
        <div><span class="task-bar researcher" style="display: inline-block; width: 20px;"></span> Researcher</div>
        <div><span class="task-bar risk-manager" style="display: inline-block; width: 20px;"></span> Risk Manager</div>
        <div><span class="task-bar strategy-lead" style="display: inline-block; width: 20px;"></span> Strategy Lead</div>
        <div><span class="task-bar operations-team" style="display: inline-block; width: 20px;"></span> Operations Team</div>
        <div><span class="task-bar project-manager" style="display: inline-block; width: 20px;"></span> Project Manager</div>
    </div>
</body>
</html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_file

def generate_project_plan(json_file, output_dir=None):
    """Generate complete project plan from LinguaLint analysis"""
    if output_dir is None:
        # Default to the same directory as the JSON file
        output_dir = Path(json_file).parent
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Initialize planner
    planner = LinguaLintProjectPlanner(json_file)
    planner.generate_project_plan()
    
    # Generate outputs
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    csv_file = output_path / f"project_plan_{timestamp}.csv"
    html_file = output_path / f"gantt_chart_{timestamp}.html"
    
    # Save files
    planner.save_ms_project_csv(csv_file)
    planner.create_html_gantt(html_file)
    
    return {
        'csv': csv_file,
        'html': html_file,
        'task_count': len(planner.tasks)
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python project_planner.py <json_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    results = generate_project_plan(json_file)
    
    print(f"✅ Project Plan Generated:")
    print(f"  📊 MS Project CSV: {results['csv']}")
    print(f"  🌐 Interactive HTML: {results['html']}")
    print(f"  📋 Total Tasks: {results['task_count']}")