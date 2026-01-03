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
Enhanced HTML Report and PNG Visualization Generator
for Responsibility Futures Analysis integrated with LinguaLint

Generates enriched visual reports from responsibility analysis JSON data.
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Try to import visualization libraries, but make them optional
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend for PNG generation
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import seaborn as sns
    import pandas as pd
    import numpy as np
    plt.ioff()  # Turn off interactive mode
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("Warning: Visualization libraries not available. Install matplotlib, seaborn, pandas, numpy for full functionality.")

class ResponsibilityReportGenerator:
    """
    Generates enriched HTML reports and PNG visualizations
    from responsibility analysis JSON data
    """
    
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path
        self.data = self.load_data()
        self.output_dir = Path(json_file_path).parent
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Set up matplotlib style if available
        if VISUALIZATION_AVAILABLE:
            plt.style.use('seaborn-v0_8')
            sns.set_palette("husl")
    
    def load_data(self) -> Dict[str, Any]:
        """Load responsibility analysis JSON data"""
        with open(self.json_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def create_responsibility_matrix_plot(self) -> Optional[str]:
        """
        Create a comprehensive responsibility matrix visualization
        Returns the filename of the generated PNG
        """
        if not VISUALIZATION_AVAILABLE:
            return None
            
        assessments = self.data.get('entity_assessments', [])
        if not assessments:
            return None
        
        # Prepare data for visualization
        df = pd.DataFrame(assessments)
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Responsibility Futures Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Responsibility Ratio vs Risk Level (Scatter Plot)
        risk_colors = {
            'Very Low': '#2E8B57',    # Sea Green
            'Low': '#32CD32',         # Lime Green  
            'Moderate': '#FFD700',    # Gold
            'High': '#FF6347',        # Tomato
            'Very High': '#DC143C'    # Crimson
        }
        
        for risk_level in risk_colors:
            mask = df['risk_level'] == risk_level
            if mask.any():
                ax1.scatter(df[mask]['intention_score'], df[mask]['negligence_score'], 
                           c=risk_colors[risk_level], label=risk_level, alpha=0.7, s=60)
        
        ax1.set_xlabel('Intention Score')
        ax1.set_ylabel('Negligence Score')
        ax1.set_title('Risk Assessment Matrix')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Add diagonal lines for R ratios
        x_range = np.linspace(0, df['intention_score'].max() * 1.1, 100)
        for r_val in [1, 2, 5, 10]:
            y_range = x_range / r_val
            ax1.plot(x_range, y_range, '--', alpha=0.5, label=f'R={r_val}')
        
        # 2. Top 15 Entities by Responsibility Ratio (Horizontal Bar Chart)
        top_entities = df.nlargest(15, 'responsibility_ratio')
        bars = ax2.barh(range(len(top_entities)), top_entities['responsibility_ratio'])
        ax2.set_yticks(range(len(top_entities)))
        ax2.set_yticklabels([name[:25] + '...' if len(name) > 25 else name 
                            for name in top_entities['entity']], fontsize=8)
        ax2.set_xlabel('Responsibility Ratio (R = I/N)')
        ax2.set_title('Top 15 Entities by Responsibility Ratio')
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Color bars by risk level
        for i, (_, row) in enumerate(top_entities.iterrows()):
            bars[i].set_color(risk_colors.get(row['risk_level'], '#808080'))
        
        # 3. Risk Level Distribution (Pie Chart)
        risk_counts = df['risk_level'].value_counts()
        colors = [risk_colors.get(level, '#808080') for level in risk_counts.index]
        wedges, texts, autotexts = ax3.pie(risk_counts.values, labels=risk_counts.index, 
                                          autopct='%1.1f%%', colors=colors, startangle=90)
        ax3.set_title('Risk Level Distribution')
        
        # 4. Mention Count vs Responsibility Ratio (Bubble Chart)
        scatter = ax4.scatter(df['mentions'], df['responsibility_ratio'], 
                             s=df['intention_score']*2, alpha=0.6, 
                             c=df['negligence_score'], cmap='RdYlBu_r')
        ax4.set_xlabel('Number of Mentions')
        ax4.set_ylabel('Responsibility Ratio')
        ax4.set_title('Entity Visibility vs Responsibility\\n(Bubble size = Intention Score)')
        ax4.grid(True, alpha=0.3)
        
        # Add colorbar for negligence score
        cbar = plt.colorbar(scatter, ax=ax4)
        cbar.set_label('Negligence Score')
        
        plt.tight_layout()
        
        # Save the plot
        filename = f"responsibility_matrix_{self.timestamp}.png"
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def create_vector_analysis_plot(self) -> Optional[str]:
        """
        Create warm/cold vector analysis visualization
        Returns the filename of the generated PNG
        """
        if not VISUALIZATION_AVAILABLE:
            return None
            
        assessments = self.data.get('entity_assessments', [])
        if not assessments:
            return None
        
        # Prepare vector data
        entities = []
        warm_vectors = []
        cold_vectors = []
        
        for assessment in assessments[:20]:  # Top 20 entities
            entities.append(assessment['entity'][:20])  # Truncate long names
            warm_vectors.append(assessment['avg_warm_vector'])
            cold_vectors.append(assessment['avg_cold_vector'])
        
        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        fig.suptitle('Warm/Cold Vector Analysis - Top 20 Entities', fontsize=14, fontweight='bold')
        
        # Warm vectors heatmap
        warm_df = pd.DataFrame(warm_vectors, 
                              columns=['Positivity', 'Engagement', 'Optimism'],
                              index=entities)
        sns.heatmap(warm_df, annot=True, fmt='.3f', cmap='Reds', ax=ax1)
        ax1.set_title('Warm Vectors (Intention Indicators)')
        ax1.set_ylabel('Entities')
        
        # Cold vectors heatmap
        cold_df = pd.DataFrame(cold_vectors,
                              columns=['Negativity', 'Risk', 'Uncertainty'], 
                              index=entities)
        sns.heatmap(cold_df, annot=True, fmt='.3f', cmap='Blues', ax=ax2)
        ax2.set_title('Cold Vectors (Negligence Indicators)')
        ax2.set_ylabel('')
        
        plt.tight_layout()
        
        # Save the plot
        filename = f"vector_analysis_{self.timestamp}.png"
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def create_statistical_summary_plot(self) -> Optional[str]:
        """
        Create a statistical summary visualization
        Returns the filename of the generated PNG
        """
        if not VISUALIZATION_AVAILABLE:
            return None
            
        assessments = self.data.get('entity_assessments', [])
        if not assessments:
            return None
        
        df = pd.DataFrame(assessments)
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Statistical Analysis Summary', fontsize=14, fontweight='bold')
        
        # 1. Responsibility Ratio Distribution
        ax1.hist(df['responsibility_ratio'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.axvline(df['responsibility_ratio'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {df["responsibility_ratio"].mean():.2f}')
        ax1.axvline(df['responsibility_ratio'].median(), color='green', linestyle='--',
                   label=f'Median: {df["responsibility_ratio"].median():.2f}')
        ax1.set_xlabel('Responsibility Ratio')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Distribution of Responsibility Ratios')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Intention vs Negligence Correlation
        ax2.scatter(df['intention_score'], df['negligence_score'], alpha=0.6)
        ax2.set_xlabel('Intention Score')
        ax2.set_ylabel('Negligence Score')
        ax2.set_title('Intention vs Negligence Correlation')
        
        # Add correlation coefficient
        corr = df['intention_score'].corr(df['negligence_score'])
        ax2.text(0.05, 0.95, f'Correlation: {corr:.3f}', transform=ax2.transAxes,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        ax2.grid(True, alpha=0.3)
        
        # 3. Mentions Distribution
        ax3.hist(df['mentions'], bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
        ax3.set_xlabel('Number of Mentions')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Entity Mention Distribution')
        ax3.grid(True, alpha=0.3)
        
        # 4. Box plot of scores by risk level
        risk_order = ['Very High', 'High', 'Moderate', 'Low', 'Very Low']
        df_melted = pd.melt(df, id_vars=['risk_level'], 
                           value_vars=['intention_score', 'negligence_score'],
                           var_name='Score Type', value_name='Score')
        
        sns.boxplot(data=df_melted, x='risk_level', y='Score', hue='Score Type', ax=ax4,
                   order=risk_order)
        ax4.set_xlabel('Risk Level')
        ax4.set_ylabel('Score')
        ax4.set_title('Score Distribution by Risk Level')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Save the plot
        filename = f"statistical_summary_{self.timestamp}.png"
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def generate_html_report(self, matrix_plot: Optional[str], vector_plot: Optional[str], stats_plot: Optional[str]) -> str:
        """
        Generate comprehensive HTML report with embedded visualizations
        """
        assessments = self.data.get('entity_assessments', [])
        total_entities = self.data.get('total_entities', 0)
        total_events = self.data.get('total_events', 0)
        analysis_timestamp = self.data.get('timestamp', 'Unknown')
        
        # Calculate summary statistics
        df = pd.DataFrame(assessments) if assessments and VISUALIZATION_AVAILABLE else None
        
        if df is not None and not df.empty:
            avg_responsibility = df['responsibility_ratio'].mean()
            median_responsibility = df['responsibility_ratio'].median()
            high_risk_count = len(df[df['risk_level'].isin(['High', 'Very High'])])
            low_risk_count = len(df[df['risk_level'].isin(['Low', 'Very Low'])])
        else:
            avg_responsibility = median_responsibility = high_risk_count = low_risk_count = 0
        
        # Generate visualization sections
        viz_sections = ""
        if matrix_plot:
            viz_sections += f"""
            <div class="section">
                <h2>📊 Responsibility Matrix Dashboard</h2>
                <p>Comprehensive visualization of responsibility ratios, risk assessments, and entity relationships.</p>
                <div class="visualization">
                    <img src="{matrix_plot}" alt="Responsibility Matrix Dashboard">
                </div>
            </div>
            """
        
        if vector_plot:
            viz_sections += f"""
            <div class="section">
                <h2>🌡️ Vector Analysis</h2>
                <p>Warm and cold vector analysis showing intention and negligence indicators for top entities.</p>
                <div class="visualization">
                    <img src="{vector_plot}" alt="Vector Analysis">
                </div>
            </div>
            """
        
        if stats_plot:
            viz_sections += f"""
            <div class="section">
                <h2>📈 Statistical Summary</h2>
                <p>Distribution analysis and correlation patterns in the responsibility data.</p>
                <div class="visualization">
                    <img src="{stats_plot}" alt="Statistical Summary">
                </div>
            </div>
            """
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsibility Futures Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.8;
            margin-top: 10px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            color: #7f8c8d;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section h2 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        
        .visualization {{
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        
        .visualization img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .entity-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }}
        
        .entity-table th {{
            background: #34495e;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        .entity-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ecf0f1;
        }}
        
        .entity-table tr:hover {{
            background: #f8f9fa;
        }}
        
        .risk-badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        
        .risk-very-low {{ background: #2ecc71; color: white; }}
        .risk-low {{ background: #27ae60; color: white; }}
        .risk-moderate {{ background: #f39c12; color: white; }}
        .risk-high {{ background: #e74c3c; color: white; }}
        .risk-very-high {{ background: #c0392b; color: white; }}
        
        .methodology {{
            background: #ecf0f1;
            padding: 30px;
            border-radius: 10px;
            margin-top: 40px;
        }}
        
        .methodology h3 {{
            color: #2c3e50;
            margin-top: 0;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 30px;
            margin-top: 50px;
        }}
        
        .timestamp {{
            font-size: 0.9em;
            opacity: 0.7;
        }}
        
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .content {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Responsibility Futures Analysis</h1>
            <div class="subtitle">Powered by LinguaLint Event Code Extractor</div>
            <div class="timestamp">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_entities}</div>
                <div class="stat-label">Total Entities</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_events}</div>
                <div class="stat-label">Total Events</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{avg_responsibility:.2f}</div>
                <div class="stat-label">Avg Responsibility Ratio</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{high_risk_count}</div>
                <div class="stat-label">High Risk Entities</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{low_risk_count}</div>
                <div class="stat-label">Low Risk Entities</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{median_responsibility:.2f}</div>
                <div class="stat-label">Median R-Ratio</div>
            </div>
        </div>
        
        <div class="content">
            {viz_sections}
            
            <div class="section">
                <h2>🏆 Top Performing Entities</h2>
                <p>Entities with the highest responsibility ratios (R = Intention / Negligence).</p>
                <table class="entity-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Entity</th>
                            <th>R-Ratio</th>
                            <th>Risk Level</th>
                            <th>Mentions</th>
                            <th>Intention</th>
                            <th>Negligence</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        
        # Add top 20 entities to the table
        for i, assessment in enumerate(assessments[:20], 1):
            risk_class = assessment['risk_level'].lower().replace(' ', '-')
            html_content += f"""
                        <tr>
                            <td><strong>{i}</strong></td>
                            <td>{assessment['entity']}</td>
                            <td><strong>{assessment['responsibility_ratio']:.2f}</strong></td>
                            <td><span class="risk-badge risk-{risk_class}">{assessment['risk_level']}</span></td>
                            <td>{assessment['mentions']}</td>
                            <td>{assessment['intention_score']:.2f}</td>
                            <td>{assessment['negligence_score']:.2f}</td>
                        </tr>
"""
        
        html_content += f"""
                    </tbody>
                </table>
            </div>
            
            <div class="methodology">
                <h3>🔬 Methodology</h3>
                <p><strong>Responsibility Ratio (R):</strong> Calculated as R = Intention Score / Negligence Score</p>
                <p><strong>Intention Score:</strong> Derived from warm vectors (Positivity × 0.4 + Engagement × 0.4 + Optimism × 0.2) × 100</p>
                <p><strong>Negligence Score:</strong> Derived from cold vectors (Negativity × 0.5 + Risk × 0.3 + Uncertainty × 0.2) × 100</p>
                <p><strong>Risk Levels:</strong></p>
                <ul>
                    <li><strong>Very Low:</strong> R > 10 (Highly responsible, minimal risk)</li>
                    <li><strong>Low:</strong> 5 < R ≤ 10 (Generally responsible)</li>
                    <li><strong>Moderate:</strong> 2 < R ≤ 5 (Balanced responsibility)</li>
                    <li><strong>High:</strong> 1 < R ≤ 2 (Concerning responsibility levels)</li>
                    <li><strong>Very High:</strong> R ≤ 1 (High risk, negligence exceeds intention)</li>
                </ul>
                <p><strong>Data Source:</strong> Analysis based on {total_events} events extracted from LinguaLint processing, covering {total_entities} unique entities.</p>
                <p><strong>Original Analysis:</strong> {analysis_timestamp}</p>
            </div>
        </div>
        
        <div class="footer">
            <p>Responsibility Futures Engine v2.0 | LinguaLint Integration</p>
            <p>Report generated from: {os.path.basename(self.json_file_path)}</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Save HTML report
        html_filename = f"responsibility_report_{self.timestamp}.html"
        html_filepath = self.output_dir / html_filename
        
        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_filename
    
    def generate_all_reports(self) -> Dict[str, Optional[str]]:
        """
        Generate all reports and visualizations
        Returns dictionary with filenames of generated files
        """
        print("🎨 Generating responsibility matrix visualization...")
        matrix_plot = self.create_responsibility_matrix_plot()
        
        print("🌡️ Generating vector analysis visualization...")
        vector_plot = self.create_vector_analysis_plot()
        
        print("📈 Generating statistical summary...")
        stats_plot = self.create_statistical_summary_plot()
        
        print("📄 Generating HTML report...")
        html_report = self.generate_html_report(matrix_plot, vector_plot, stats_plot)
        
        return {
            'html_report': html_report,
            'matrix_plot': matrix_plot,
            'vector_plot': vector_plot,
            'stats_plot': stats_plot
        }

def generate_responsibility_reports(json_file_path: str) -> Dict[str, Optional[str]]:
    """
    Main function to generate responsibility reports from JSON file
    """
    generator = ResponsibilityReportGenerator(json_file_path)
    return generator.generate_all_reports()

def main():
    """Main execution function"""
    if len(sys.argv) != 2:
        print("Usage: python responsibility_report_generator.py <responsibility_analysis.json>")
        print("Example: python responsibility_report_generator.py extraction_20251230_082034_responsibility_analysis.json")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    if not os.path.exists(json_file):
        print(f"Error: File '{json_file}' not found.")
        sys.exit(1)
    
    try:
        print("🚀 Starting Responsibility Futures Report Generation...")
        print(f"📁 Input file: {json_file}")
        
        generated_files = generate_responsibility_reports(json_file)
        
        print("\\n✅ Report generation completed successfully!")
        print("📋 Generated files:")
        for file_type, filename in generated_files.items():
            if filename:
                print(f"   • {file_type}: {filename}")
        
        if generated_files.get('html_report'):
            output_dir = Path(json_file).parent
            html_path = output_dir / generated_files['html_report']
            print(f"\\n🌐 Open the HTML report to view the complete analysis:")
            print(f"   file://{html_path.absolute()}")
        
    except Exception as e:
        print(f"❌ Error generating reports: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()