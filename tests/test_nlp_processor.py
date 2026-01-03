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
Test suite for LinguaLint NLP Processor
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.nlp_processor import ModernNLPProcessor

class TestModernNLPProcessor:
    
    def setup_method(self):
        """Setup test fixtures"""
        self.processor = ModernNLPProcessor()
        self.sample_text = """
        The COVID-19 pandemic has materially adversely affected our business operations.
        Apple Inc. reported strong quarterly earnings despite market volatility.
        Interest rates may increase due to inflationary pressures.
        """
    
    def test_processor_initialization(self):
        """Test that processor initializes correctly"""
        assert self.processor is not None
        assert self.processor.nlp is not None
        assert len(self.processor.semantic_primes) > 0
    
    def test_process_text_basic(self):
        """Test basic text processing functionality"""
        result = self.processor.process_text(self.sample_text, enrich_wikipedia=False)
        
        assert '_source' in result
        assert 'sentences' in result['_source']
        assert 'subjects' in result['_source']
        assert 'phen' in result['_source']
        assert len(result['_source']['sentences']) > 0
    
    def test_subject_extraction(self):
        """Test that subjects are properly extracted"""
        result = self.processor.process_text(self.sample_text, enrich_wikipedia=False)
        subjects = result['_source']['subjects']
        
        # Should extract proper nouns and organizations
        assert any('Apple' in subj for subj in subjects)
        assert any('COVID' in subj or 'pandemic' in subj for subj in subjects)
    
    def test_phenomena_extraction(self):
        """Test that phenomena are extracted"""
        result = self.processor.process_text(self.sample_text, enrich_wikipedia=False)
        phen = result['_source']['phen']
        
        assert len(phen) > 0
        # Should contain both subjects and concepts
        assert any(item for item in phen if len(item) > 3)
    
    def test_sentiment_vectors(self):
        """Test that sentiment vectors are calculated"""
        result = self.processor.process_text(self.sample_text, enrich_wikipedia=False)
        sentences = result['_source']['sentences']
        
        for sentence in sentences:
            assert 'warm_vector' in sentence
            assert 'cold_vector' in sentence
            assert len(sentence['warm_vector']) == 3
            assert len(sentence['cold_vector']) == 3
    
    def test_empty_text(self):
        """Test handling of empty text"""
        result = self.processor.process_text("", enrich_wikipedia=False)
        
        assert '_source' in result
        assert len(result['_source']['sentences']) == 0
        assert len(result['_source']['subjects']) == 0
    
    def test_wiki_candidates(self):
        """Test Wikipedia candidate extraction"""
        result = self.processor.process_text(self.sample_text, enrich_wikipedia=False)
        wiki_blues = result['_source']['wiki_blues']
        
        assert len(wiki_blues) > 0
        # Should prioritize proper nouns and financial terms
        assert any('Apple' in candidate for candidate in wiki_blues)

if __name__ == "__main__":
    pytest.main([__file__])