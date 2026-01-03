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
Wikipedia Integration for Modern NLP Processor
Enriches extracted concepts with Wikipedia summaries
"""

import wikipedia
from typing import List, Dict, Any
from urllib.parse import quote

def integrate_wikipedia_sync(nlp_result: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous Wikipedia enrichment using wikipedia library"""
    wiki_candidates = nlp_result['_source']['wiki_blues']
    wiki_data = []
    
    for concept in wiki_candidates[:10]:  # Limit to 10 to avoid rate limits
        try:
            # Search for the concept
            search_results = wikipedia.search(concept, results=1)
            if search_results:
                page_title = search_results[0]
                summary = wikipedia.summary(page_title, sentences=2)
                wiki_data.append({
                    "wiki_search_content": concept,
                    "wiki_url": f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}",
                    "wiki_summary": summary
                })
            else:
                wiki_data.append({
                    "wiki_search_content": concept,
                    "wiki_url": f"https://en.wikipedia.org/wiki/{concept.replace(' ', '_')}",
                    "wiki_summary": ""
                })
        except Exception:
            wiki_data.append({
                "wiki_search_content": concept,
                "wiki_url": f"https://en.wikipedia.org/wiki/{concept.replace(' ', '_')}",
                "wiki_summary": ""
            })
    
    nlp_result['_source']['wiki'] = wiki_data
    return nlp_result