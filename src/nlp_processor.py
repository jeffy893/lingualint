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
Modern NLP Processor using SpaCy and Wierzbicka's Semantic Primes
Replaces legacy Java/Talend extraction logic
"""

import spacy
import json
from datetime import datetime
from typing import List, Dict, Any, Tuple
import hashlib
import time
from .wikipedia_enricher import integrate_wikipedia_sync

class ModernNLPProcessor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise RuntimeError("Please install: python -m spacy download en_core_web_sm")
        
        # Wierzbicka's 65 Semantic Primes (NSM)
        self.semantic_primes = {
            # Substantives
            'I', 'YOU', 'SOMEONE', 'SOMETHING', 'PEOPLE', 'BODY',
            # Relational substantives  
            'KIND', 'PART',
            # Determiners
            'THIS', 'THE SAME', 'OTHER', 'ELSE',
            # Quantifiers
            'ONE', 'TWO', 'SOME', 'ALL', 'MUCH', 'MANY', 'LITTLE', 'FEW',
            # Evaluators
            'GOOD', 'BAD',
            # Descriptors
            'BIG', 'SMALL',
            # Mental predicates
            'THINK', 'KNOW', 'WANT', "DON'T WANT", 'FEEL', 'SEE', 'HEAR',
            # Speech
            'SAY', 'WORDS', 'TRUE',
            # Actions, events, movement
            'DO', 'HAPPEN', 'MOVE',
            # Location, existence, specification
            'BE', 'THERE IS', 'HAVE', 'BE SOMEONE/SOMETHING',
            # Life and death
            'LIVE', 'DIE',
            # Time
            'WHEN', 'NOW', 'BEFORE', 'AFTER', 'A LONG TIME', 'A SHORT TIME', 'FOR SOME TIME', 'MOMENT',
            # Space
            'WHERE', 'HERE', 'ABOVE', 'BELOW', 'FAR', 'NEAR', 'SIDE', 'INSIDE', 'TOUCH',
            # Logical concepts
            'NOT', 'MAYBE', 'CAN', 'BECAUSE', 'IF',
            # Intensifier, augmentor
            'VERY', 'MORE',
            # Similarity
            'LIKE'
        }
        
        # Convert to lowercase for matching
        self.prime_words = [prime.lower().split() for prime in self.semantic_primes]
        self.prime_singles = {word for prime in self.prime_words for word in prime if len(prime) == 1}
        self.prime_phrases = {' '.join(prime): prime for prime in self.prime_words if len(prime) > 1}

    def process_text(self, text: str, tag: str = "", email: str = "", enrich_wikipedia: bool = True) -> Dict[str, Any]:
        """Process text using modern NLP techniques"""
        doc = self.nlp(text)
        sentences = list(doc.sents)
        
        processed_sentences = []
        all_subjects = []
        all_concepts = []
        all_relations = []
        
        for sent_idx, sent in enumerate(sentences):
            sent_data = self._process_sentence(sent, sent_idx)
            processed_sentences.append(sent_data['sentence_obj'])
            all_subjects.extend(sent_data['subjects'])
            all_concepts.extend(sent_data['concepts'])
            all_relations.extend(sent_data['relations'])
        
        # Create legacy-compatible output
        result = {
            "_index": "lingualint_event",
            "_id": self._generate_id(),
            "_score": 1.0,
            "_source": {
                "@timestamp": datetime.now().isoformat(),
                "tag": tag,
                "email": email,
                "identity": {
                    "timestamp": datetime.now().isoformat(),
                    "tag": tag,
                    "email": email,
                    "first_sentence": sentences[0].text.strip() if sentences else ""
                },
                "sentences": processed_sentences,
                "subjects": list(set(all_subjects)),  # Separate subjects field
                "phen": self._extract_phenomena(all_subjects, all_concepts, all_relations),
                "wiki_blues": self._extract_wiki_candidates(all_subjects + all_concepts),
                "wiki": []  # Will be populated by Wikipedia integration
            }
        }
        
        # Enrich with Wikipedia data if requested
        if enrich_wikipedia:
            try:
                result = integrate_wikipedia_sync(result)
            except Exception as e:
                print(f"Wikipedia enrichment failed: {e}")
        
        return result

    def _process_sentence(self, sent, sent_idx: int) -> Dict[str, Any]:
        """Process individual sentence with SpaCy NLP"""
        subjects = self._extract_subjects(sent)
        concepts, relations = self._extract_concepts_and_relations(sent)
        
        # Calculate basic sentiment vectors (placeholder implementation)
        warm_vector = self._calculate_sentiment_vector(sent, 'warm')
        cold_vector = self._calculate_sentiment_vector(sent, 'cold')
        
        return {
            'sentence_obj': {
                "sentence": sent.text.strip(),
                "warm_vector": warm_vector,
                "cold_vector": cold_vector
            },
            'subjects': subjects,
            'concepts': concepts,
            'relations': relations
        }

    def _extract_subjects(self, sent) -> List[str]:
        """Extract core subjects - proper nouns, organizations, key entities"""
        subjects = []
        
        # Use Named Entity Recognition for core subjects
        for ent in sent.ents:
            if ent.label_ in ['PERSON', 'ORG', 'GPE', 'PRODUCT', 'EVENT', 'LAW', 'MONEY']:
                subjects.append(ent.text)
        
        # Extract proper nouns (capitalized) as core subjects
        for token in sent:
            if (token.pos_ == 'PROPN' and 
                token.text[0].isupper() and
                len(token.text) > 2 and
                token.text not in [ent.text for ent in sent.ents]):
                subjects.append(token.text)
        
        # Extract noun phrases that are capitalized (likely subjects)
        for chunk in sent.noun_chunks:
            if (chunk.text[0].isupper() and 
                len(chunk.text.split()) <= 3 and
                chunk.text not in subjects):
                subjects.append(chunk.text)
        
        return list(set(subjects))

    def _extract_concepts_and_relations(self, sent) -> Tuple[List[str], List[str]]:
        """Extract non-capitalized phenomena and relations using Semantic Primes"""
        concepts = []
        relations = []
        
        sent_text = sent.text.lower()
        tokens = [token for token in sent]
        
        # Find semantic primes in the sentence
        prime_positions = self._find_semantic_primes(tokens)
        
        # Extract concepts around primes
        for prime_pos, prime_text in prime_positions:
            concept_window = self._extract_concept_window(tokens, prime_pos, prime_text)
            
            if self._is_relational_prime(prime_text):
                relations.append(concept_window)
            else:
                concepts.append(concept_window)
        
        # Extract non-capitalized noun phrases as phenomena
        for chunk in sent.noun_chunks:
            chunk_text = chunk.text.strip()
            # Only include if it's not capitalized (not a subject) and meaningful
            if (len(chunk_text.split()) > 1 and 
                not chunk_text[0].isupper() and
                chunk_text not in concepts and 
                len(chunk_text) > 3):
                concepts.append(chunk_text)
        
        # Extract verb phrases and descriptive phrases (non-capitalized)
        for token in sent:
            if token.pos_ in ['VERB', 'ADJ'] and not token.text[0].isupper():
                # Get surrounding context for meaningful phrases
                phrase = self._get_phrase_context(token, sent)
                if phrase and len(phrase) > 3 and not phrase[0].isupper():
                    concepts.append(phrase)
        
        return concepts, relations

    def _find_semantic_primes(self, tokens) -> List[Tuple[int, str]]:
        """Find Semantic Primes in token sequence"""
        primes_found = []
        i = 0
        
        while i < len(tokens):
            # Check for multi-word primes first
            for phrase_len in range(min(4, len(tokens) - i), 0, -1):
                phrase = ' '.join(token.text.lower() for token in tokens[i:i+phrase_len])
                if phrase in self.prime_phrases:
                    primes_found.append((i, phrase))
                    i += phrase_len
                    break
            else:
                # Check single word primes
                if tokens[i].text.lower() in self.prime_singles:
                    primes_found.append((i, tokens[i].text.lower()))
                i += 1
        
        return primes_found

    def _extract_concept_window(self, tokens, prime_pos: int, prime_text: str) -> str:
        """Extract concept window around semantic prime"""
        window_size = 3
        start = max(0, prime_pos - window_size)
        end = min(len(tokens), prime_pos + window_size + 1)
        
        window_tokens = []
        for i in range(start, end):
            if i != prime_pos and tokens[i].pos_ not in ['PUNCT', 'SPACE']:
                window_tokens.append(tokens[i].text)
        
        return ' '.join(window_tokens).strip()

    def _is_relational_prime(self, prime_text: str) -> bool:
        """Determine if semantic prime indicates a relation"""
        relational_primes = {
            'because', 'if', 'when', 'where', 'do', 'happen', 'move', 
            'say', 'think', 'feel', 'see', 'hear', 'like', 'can'
        }
        return prime_text in relational_primes

    def _extract_phenomena(self, subjects: List[str], concepts: List[str], relations: List[str]) -> List[str]:
        """Extract phenomena (key phrases) from all components"""
        phenomena = []
        
        # Add all subjects, concepts, and relations
        phenomena.extend(subjects)
        phenomena.extend(concepts)
        phenomena.extend(relations)
        
        # Clean and deduplicate
        phenomena = [p.strip() for p in phenomena if p and len(p.strip()) > 2]
        return list(set(phenomena))

    def _get_phrase_context(self, token, sent) -> str:
        """Get meaningful phrase context around a token"""
        start_idx = max(0, token.i - 2)
        end_idx = min(len(sent), token.i + 3)
        
        phrase_tokens = []
        for i in range(start_idx, end_idx):
            if sent[i].pos_ not in ['PUNCT', 'SPACE', 'DET'] and len(sent[i].text) > 1:
                phrase_tokens.append(sent[i].text)
        
        return ' '.join(phrase_tokens).strip()

    def _extract_wiki_candidates(self, entities: List[str]) -> List[str]:
        """Extract candidates most likely to have Wikipedia entries"""
        candidates = []
        
        # Prioritize entities that are likely to have Wikipedia pages
        wiki_priority_terms = [
            'company', 'corporation', 'inc', 'llc', 'pandemic', 'covid', 'crisis',
            'technology', 'system', 'market', 'industry', 'regulation', 'government',
            'economic', 'financial', 'business', 'operations', 'revenue', 'debt'
        ]
        
        for entity in entities:
            entity_lower = entity.lower()
            # Include if it's a proper noun (capitalized) or contains wiki-priority terms
            if (entity[0].isupper() or 
                any(term in entity_lower for term in wiki_priority_terms) or
                len(entity.split()) >= 2):
                candidates.append(entity)
        
        # Remove duplicates and limit
        return list(set(candidates))[:20]

    def _calculate_sentiment_vector(self, sent, vector_type: str) -> List[float]:
        """Calculate sentiment vectors for warm/cold analysis"""
        # Simple sentiment scoring based on word polarity
        positive_words = {'good', 'strong', 'growth', 'increase', 'positive', 'benefit', 'advantage'}
        negative_words = {'risk', 'adverse', 'decrease', 'decline', 'negative', 'loss', 'threat', 'danger'}
        
        words = [token.text.lower() for token in sent if token.is_alpha]
        
        pos_count = sum(1 for word in words if word in positive_words)
        neg_count = sum(1 for word in words if word in negative_words)
        total_words = len(words)
        
        if vector_type == 'warm':
            # Warm vector: [positivity, engagement, optimism]
            return [
                pos_count / max(total_words, 1),
                len([w for w in words if w in {'will', 'can', 'may', 'could'}]) / max(total_words, 1),
                pos_count / max(pos_count + neg_count, 1)
            ]
        else:
            # Cold vector: [negativity, risk, uncertainty]
            return [
                neg_count / max(total_words, 1),
                len([w for w in words if w in {'risk', 'may', 'could', 'might'}]) / max(total_words, 1),
                neg_count / max(pos_count + neg_count, 1)
            ]

    def _generate_id(self) -> str:
        """Generate unique document ID"""
        return hashlib.md5(f"{time.time()}".encode()).hexdigest()[:20]