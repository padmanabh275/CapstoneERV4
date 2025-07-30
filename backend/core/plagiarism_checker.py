import asyncio
import logging
import re
import hashlib
from typing import List, Dict, Tuple
import requests
from difflib import SequenceMatcher
import json

logger = logging.getLogger(__name__)

class PlagiarismChecker:
    """
    Plagiarism & Fact-Check Agent - Checks content originality and factual accuracy
    """
    
    def __init__(self):
        # Initialize APIs (mock for now - replace with actual API keys)
        self.copyscape_api_key = "your_copyscape_api_key"
        self.fact_check_api_key = "your_fact_check_api_key"
        
        # Common phrases that might trigger false positives
        self.common_phrases = [
            "in conclusion", "it is important to note", "furthermore",
            "moreover", "however", "therefore", "as a result",
            "in addition", "on the other hand", "for example"
        ]
        
        # Fact-checking sources
        self.fact_check_sources = [
            "wikipedia", "britannica", "factcheck.org", "snopes",
            "reuters", "ap", "bbc", "npr"
        ]
        
        # Plagiarism detection thresholds
        self.plagiarism_thresholds = {
            "exact_match": 0.95,
            "similar_content": 0.85,
            "suspicious": 0.70
        }
    
    async def check(
        self, 
        content: str, 
        check_facts: bool = True
    ) -> Tuple[float, List[Dict]]:
        """
        Check content for plagiarism and factual accuracy
        
        Args:
            content: Content to check
            check_facts: Whether to perform fact-checking
            
        Returns:
            Tuple of (plagiarism_score, fact_check_results)
        """
        try:
            plagiarism_score = 0.0
            fact_check_results = []
            
            # Check for plagiarism
            plagiarism_score = await self._check_plagiarism(content)
            
            # Check facts if requested
            if check_facts:
                fact_check_results = await self._check_facts(content)
            
            return plagiarism_score, fact_check_results
            
        except Exception as e:
            logger.error(f"Plagiarism check failed: {e}")
            return 0.0, []
    
    async def _check_plagiarism(self, content: str) -> float:
        """Check content for plagiarism using multiple methods"""
        try:
            # Method 1: Check against common phrases
            common_phrase_score = self._check_common_phrases(content)
            
            # Method 2: Check for exact matches (simulated)
            exact_match_score = await self._check_exact_matches(content)
            
            # Method 3: Check for similar content (simulated)
            similar_content_score = await self._check_similar_content(content)
            
            # Method 4: Check for copied sentences
            copied_sentence_score = self._check_copied_sentences(content)
            
            # Calculate overall plagiarism score
            scores = [common_phrase_score, exact_match_score, similar_content_score, copied_sentence_score]
            plagiarism_score = sum(scores) / len(scores)
            
            return min(plagiarism_score, 1.0)
            
        except Exception as e:
            logger.error(f"Plagiarism detection failed: {e}")
            return 0.0
    
    def _check_common_phrases(self, content: str) -> float:
        """Check for overuse of common phrases"""
        content_lower = content.lower()
        phrase_count = 0
        
        for phrase in self.common_phrases:
            phrase_count += content_lower.count(phrase)
        
        # Calculate score based on phrase density
        words = content.split()
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
        
        phrase_density = phrase_count / total_words
        
        # Higher density = higher plagiarism risk
        if phrase_density > 0.05:  # More than 5% common phrases
            return 0.3
        elif phrase_density > 0.03:  # More than 3% common phrases
            return 0.2
        elif phrase_density > 0.01:  # More than 1% common phrases
            return 0.1
        else:
            return 0.0
    
    async def _check_exact_matches(self, content: str) -> float:
        """Check for exact matches with online content (simulated)"""
        try:
            # Simulate API call to plagiarism detection service
            await asyncio.sleep(1)  # Simulate API delay
            
            # Mock exact match detection
            sentences = content.split('. ')
            exact_matches = 0
            
            for sentence in sentences:
                if len(sentence.strip()) > 10:  # Only check substantial sentences
                    # Simulate finding exact matches
                    if self._simulate_exact_match(sentence):
                        exact_matches += 1
            
            if len(sentences) == 0:
                return 0.0
            
            match_ratio = exact_matches / len(sentences)
            
            if match_ratio > 0.1:  # More than 10% exact matches
                return 0.8
            elif match_ratio > 0.05:  # More than 5% exact matches
                return 0.5
            elif match_ratio > 0.02:  # More than 2% exact matches
                return 0.2
            else:
                return 0.0
                
        except Exception as e:
            logger.error(f"Exact match check failed: {e}")
            return 0.0
    
    def _simulate_exact_match(self, sentence: str) -> bool:
        """Simulate exact match detection"""
        # Mock logic - in reality, this would call an API
        # Check for very common sentence patterns
        common_patterns = [
            "This is a comprehensive guide",
            "In this article, we will",
            "The importance of",
            "It is essential to",
            "As mentioned earlier"
        ]
        
        sentence_lower = sentence.lower()
        for pattern in common_patterns:
            if pattern.lower() in sentence_lower:
                return True
        
        return False
    
    async def _check_similar_content(self, content: str) -> float:
        """Check for similar content using fuzzy matching"""
        try:
            # Simulate checking against a database of content
            await asyncio.sleep(1)  # Simulate API delay
            
            # Mock similar content detection
            paragraphs = content.split('\n\n')
            similar_paragraphs = 0
            
            for paragraph in paragraphs:
                if len(paragraph.strip()) > 20:  # Only check substantial paragraphs
                    if self._simulate_similar_content(paragraph):
                        similar_paragraphs += 1
            
            if len(paragraphs) == 0:
                return 0.0
            
            similarity_ratio = similar_paragraphs / len(paragraphs)
            
            if similarity_ratio > 0.3:  # More than 30% similar content
                return 0.7
            elif similarity_ratio > 0.15:  # More than 15% similar content
                return 0.4
            elif similarity_ratio > 0.05:  # More than 5% similar content
                return 0.2
            else:
                return 0.0
                
        except Exception as e:
            logger.error(f"Similar content check failed: {e}")
            return 0.0
    
    def _simulate_similar_content(self, paragraph: str) -> bool:
        """Simulate similar content detection"""
        # Mock logic - in reality, this would use fuzzy matching
        # Check for very similar paragraph structures
        similar_structures = [
            "The key benefits include",
            "There are several advantages",
            "It is important to consider",
            "This approach provides",
            "The main advantages are"
        ]
        
        paragraph_lower = paragraph.lower()
        for structure in similar_structures:
            if structure.lower() in paragraph_lower:
                return True
        
        return False
    
    def _check_copied_sentences(self, content: str) -> float:
        """Check for copied sentences within the content"""
        sentences = content.split('. ')
        copied_sentences = 0
        
        # Check for duplicate sentences
        sentence_counts = {}
        for sentence in sentences:
            sentence_clean = sentence.strip().lower()
            if sentence_clean:
                sentence_counts[sentence_clean] = sentence_counts.get(sentence_clean, 0) + 1
        
        # Count sentences that appear more than once
        for sentence, count in sentence_counts.items():
            if count > 1:
                copied_sentences += count - 1
        
        if len(sentences) == 0:
            return 0.0
        
        copy_ratio = copied_sentences / len(sentences)
        
        if copy_ratio > 0.1:  # More than 10% copied sentences
            return 0.6
        elif copy_ratio > 0.05:  # More than 5% copied sentences
            return 0.3
        elif copy_ratio > 0.02:  # More than 2% copied sentences
            return 0.1
        else:
            return 0.0
    
    async def _check_facts(self, content: str) -> List[Dict]:
        """Check factual accuracy of content"""
        try:
            fact_check_results = []
            
            # Extract potential facts from content
            facts = self._extract_facts(content)
            
            for fact in facts:
                # Simulate fact-checking API call
                await asyncio.sleep(0.5)  # Simulate API delay
                
                fact_result = await self._verify_fact(fact)
                fact_check_results.append(fact_result)
            
            return fact_check_results
            
        except Exception as e:
            logger.error(f"Fact checking failed: {e}")
            return []
    
    def _extract_facts(self, content: str) -> List[str]:
        """Extract potential facts from content"""
        facts = []
        
        # Look for factual statements
        factual_patterns = [
            r'\d{4}',  # Years
            r'\d+%',   # Percentages
            r'\$\d+',  # Dollar amounts
            r'according to [^.]*',
            r'studies show [^.]*',
            r'research indicates [^.]*',
            r'the fact that [^.]*',
            r'it is known that [^.]*'
        ]
        
        for pattern in factual_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            facts.extend(matches)
        
        # Also extract sentences with numbers or specific claims
        sentences = content.split('. ')
        for sentence in sentences:
            if any(char.isdigit() for char in sentence):
                facts.append(sentence)
            elif any(word in sentence.lower() for word in ['study', 'research', 'found', 'discovered', 'proved']):
                facts.append(sentence)
        
        return facts[:10]  # Limit to 10 facts to check
    
    async def _verify_fact(self, fact: str) -> Dict:
        """Verify a single fact (simulated)"""
        try:
            # Mock fact verification
            # In reality, this would call fact-checking APIs
            
            # Simulate different verification results
            verification_results = [
                {"status": "verified", "confidence": 0.9, "source": "reliable_source"},
                {"status": "disputed", "confidence": 0.7, "source": "multiple_sources"},
                {"status": "unverified", "confidence": 0.3, "source": "no_sources"},
                {"status": "false", "confidence": 0.8, "source": "fact_check_org"}
            ]
            
            # Use fact hash to determine result (for consistency)
            fact_hash = hashlib.md5(fact.encode()).hexdigest()
            result_index = int(fact_hash[:2], 16) % len(verification_results)
            
            result = verification_results[result_index].copy()
            result["fact"] = fact
            result["suggestion"] = self._get_fact_suggestion(result["status"])
            
            return result
            
        except Exception as e:
            logger.error(f"Fact verification failed: {e}")
            return {
                "fact": fact,
                "status": "error",
                "confidence": 0.0,
                "source": "unknown",
                "suggestion": "Unable to verify this fact"
            }
    
    def _get_fact_suggestion(self, status: str) -> str:
        """Get suggestion based on fact verification status"""
        suggestions = {
            "verified": "This fact appears to be accurate based on reliable sources.",
            "disputed": "This claim is disputed by multiple sources. Consider providing additional context.",
            "unverified": "This claim could not be verified. Consider adding a source or removing the claim.",
            "false": "This claim appears to be incorrect. Please verify and correct the information.",
            "error": "Unable to verify this claim. Please check your sources."
        }
        
        return suggestions.get(status, "Please verify this information.")
    
    def get_recommendations(self, plagiarism_score: float, fact_check_results: List[Dict]) -> List[str]:
        """Get recommendations based on plagiarism and fact-check results"""
        recommendations = []
        
        # Plagiarism recommendations
        if plagiarism_score > 0.8:
            recommendations.append("High plagiarism risk detected. Consider rewriting the content completely.")
        elif plagiarism_score > 0.6:
            recommendations.append("Moderate plagiarism risk. Review and rewrite suspicious sections.")
        elif plagiarism_score > 0.3:
            recommendations.append("Some plagiarism detected. Consider paraphrasing certain sections.")
        else:
            recommendations.append("Content appears to be original. Good job!")
        
        # Fact-check recommendations
        if fact_check_results:
            disputed_facts = [r for r in fact_check_results if r.get("status") == "disputed"]
            false_facts = [r for r in fact_check_results if r.get("status") == "false"]
            unverified_facts = [r for r in fact_check_results if r.get("status") == "unverified"]
            
            if false_facts:
                recommendations.append(f"Found {len(false_facts)} potentially false claims. Please verify and correct.")
            
            if disputed_facts:
                recommendations.append(f"Found {len(disputed_facts)} disputed claims. Consider providing additional context.")
            
            if unverified_facts:
                recommendations.append(f"Found {len(unverified_facts)} unverified claims. Consider adding sources or removing claims.")
        
        # General recommendations
        if plagiarism_score < 0.2 and not fact_check_results:
            recommendations.append("Content appears to be original and factual. Ready for publication!")
        
        return recommendations 