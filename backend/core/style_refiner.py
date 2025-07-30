import asyncio
import logging
import re
from typing import List, Tuple, Dict
# SpaCy import is optional - will use basic text processing if not available
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
# Textstat import is optional - will use mock implementation if not available
try:
    from textstat import textstat
    TEXTSTAT_AVAILABLE = True
except ImportError:
    TEXTSTAT_AVAILABLE = False

logger = logging.getLogger(__name__)

class StyleRefiner:
    """
    Style & Tone Refinement Agent - Adjusts content style and tone based on user preferences
    """
    
    def __init__(self):
        # Load spaCy model for text processing
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                logger.warning("spaCy model not found. Using basic text processing.")
                self.nlp = None
        else:
            logger.warning("SpaCy not available. Using basic text processing.")
            self.nlp = None
        
        # Define style transformation rules
        self.style_rules = {
            "professional": {
                "formal_words": ["utilize", "implement", "facilitate", "optimize"],
                "avoid_words": ["gonna", "wanna", "kinda", "sorta"],
                "sentence_structure": "complex",
                "tone": "formal"
            },
            "casual": {
                "informal_words": ["gonna", "wanna", "kinda", "sorta"],
                "avoid_words": ["utilize", "implement", "facilitate"],
                "sentence_structure": "simple",
                "tone": "friendly"
            },
            "humorous": {
                "humor_words": ["hilarious", "amazing", "incredible", "mind-blowing"],
                "avoid_words": ["utilize", "implement", "facilitate"],
                "sentence_structure": "varied",
                "tone": "entertaining"
            },
            "academic": {
                "academic_words": ["furthermore", "moreover", "consequently", "nevertheless"],
                "avoid_words": ["gonna", "wanna", "kinda", "sorta"],
                "sentence_structure": "complex",
                "tone": "scholarly"
            }
        }
        
        # Length adjustment rules
        self.length_rules = {
            "short": {"target_ratio": 0.5, "max_sentences": 3},
            "medium": {"target_ratio": 1.0, "max_sentences": 6},
            "long": {"target_ratio": 1.5, "max_sentences": 10}
        }
    
    async def refine(
        self, 
        content: str, 
        style: str = "casual",
        length: str = "medium",
        target_audience: str = "general"
    ) -> Tuple[str, List[str]]:
        """
        Refine content based on style, length, and audience preferences
        
        Args:
            content: Original content to refine
            style: Target style (professional, casual, humorous, academic)
            length: Target length (short, medium, long)
            target_audience: Target audience
            
        Returns:
            Tuple of (refined_content, changes_made)
        """
        try:
            changes = []
            refined_content = content
            
            # Apply style transformations
            refined_content, style_changes = self._apply_style_transformations(
                refined_content, style, target_audience
            )
            changes.extend(style_changes)
            
            # Apply length adjustments
            refined_content, length_changes = self._adjust_length(
                refined_content, length
            )
            changes.extend(length_changes)
            
            # Apply audience-specific adjustments
            refined_content, audience_changes = self._adjust_for_audience(
                refined_content, target_audience
            )
            changes.extend(audience_changes)
            
            # Final polish
            refined_content = self._polish_content(refined_content)
            
            return refined_content, changes
            
        except Exception as e:
            logger.error(f"Content refinement failed: {e}")
            return content, [f"Refinement failed: {str(e)}"]
    
    def _apply_style_transformations(
        self, 
        content: str, 
        style: str, 
        target_audience: str
    ) -> Tuple[str, List[str]]:
        """Apply style-specific transformations to content"""
        changes = []
        
        if style not in self.style_rules:
            style = "casual"  # Default fallback
        
        rules = self.style_rules[style]
        
        # Apply word replacements
        for old_word, new_word in self._get_word_replacements(style):
            if old_word in content.lower():
                content = re.sub(rf'\b{old_word}\b', new_word, content, flags=re.IGNORECASE)
                changes.append(f"Replaced '{old_word}' with '{new_word}' for {style} style")
        
        # Adjust sentence structure
        if rules["sentence_structure"] == "simple":
            content = self._simplify_sentences(content)
            changes.append("Simplified sentence structure for better readability")
        elif rules["sentence_structure"] == "complex":
            content = self._complexify_sentences(content)
            changes.append("Enhanced sentence complexity for professional tone")
        
        # Adjust tone markers
        content = self._adjust_tone_markers(content, style)
        changes.append(f"Applied {style} tone markers")
        
        return content, changes
    
    def _get_word_replacements(self, style: str) -> List[Tuple[str, str]]:
        """Get word replacement pairs for specific style"""
        replacements = {
            "professional": [
                ("use", "utilize"),
                ("make", "implement"),
                ("help", "facilitate"),
                ("improve", "optimize"),
                ("start", "initiate"),
                ("end", "conclude")
            ],
            "casual": [
                ("utilize", "use"),
                ("implement", "make"),
                ("facilitate", "help"),
                ("optimize", "improve"),
                ("initiate", "start"),
                ("conclude", "end")
            ],
            "humorous": [
                ("good", "amazing"),
                ("great", "incredible"),
                ("excellent", "mind-blowing"),
                ("bad", "hilarious"),
                ("problem", "adventure"),
                ("issue", "challenge")
            ],
            "academic": [
                ("also", "furthermore"),
                ("but", "however"),
                ("so", "consequently"),
                ("and", "moreover"),
                ("though", "nevertheless"),
                ("because", "due to the fact that")
            ]
        }
        
        return replacements.get(style, [])
    
    def _simplify_sentences(self, content: str) -> str:
        """Simplify complex sentences"""
        sentences = content.split('. ')
        simplified_sentences = []
        
        for sentence in sentences:
            if len(sentence.split()) > 20:  # Long sentence
                # Split into shorter sentences
                parts = sentence.split(', ')
                if len(parts) > 1:
                    simplified_sentences.extend(parts)
                else:
                    simplified_sentences.append(sentence)
            else:
                simplified_sentences.append(sentence)
        
        return '. '.join(simplified_sentences)
    
    def _complexify_sentences(self, content: str) -> str:
        """Make sentences more complex for professional tone"""
        sentences = content.split('. ')
        complex_sentences = []
        
        for i, sentence in enumerate(sentences):
            if len(sentence.split()) < 10 and i < len(sentences) - 1:
                # Combine with next sentence
                if i + 1 < len(sentences):
                    combined = f"{sentence}, and {sentences[i + 1].lower()}"
                    complex_sentences.append(combined)
                    sentences[i + 1] = ""  # Skip next sentence
                else:
                    complex_sentences.append(sentence)
            else:
                complex_sentences.append(sentence)
        
        return '. '.join([s for s in complex_sentences if s])
    
    def _adjust_tone_markers(self, content: str, style: str) -> str:
        """Add tone-specific markers to content"""
        markers = {
            "professional": [
                "It is important to note that",
                "Furthermore,",
                "In conclusion,",
                "Based on the analysis,"
            ],
            "casual": [
                "You know what?",
                "Here's the thing:",
                "Bottom line:",
                "So there you have it!"
            ],
            "humorous": [
                "Here's the funny thing:",
                "Plot twist:",
                "Spoiler alert:",
                "Drumroll please..."
            ],
            "academic": [
                "It is worth noting that",
                "Furthermore, it can be argued that",
                "In light of these findings,",
                "The implications of this are significant."
            ]
        }
        
        if style in markers:
            # Add markers at strategic points
            sentences = content.split('. ')
            if len(sentences) > 2:
                # Add marker to second sentence
                sentences[1] = f"{markers[style][0]} {sentences[1].lower()}"
            
            # Add conclusion marker
            if len(sentences) > 1:
                sentences[-1] = f"{markers[style][-1]} {sentences[-1]}"
        
        return '. '.join(sentences)
    
    def _adjust_length(self, content: str, length: str) -> Tuple[str, List[str]]:
        """Adjust content length based on target"""
        changes = []
        
        if length not in self.length_rules:
            length = "medium"
        
        rules = self.length_rules[length]
        current_sentences = len(content.split('. '))
        target_sentences = rules["max_sentences"]
        
        if current_sentences > target_sentences:
            # Shorten content
            sentences = content.split('. ')
            content = '. '.join(sentences[:target_sentences])
            changes.append(f"Shortened content to {target_sentences} sentences")
        elif current_sentences < target_sentences * 0.7:
            # Expand content
            content = self._expand_content(content, target_sentences - current_sentences)
            changes.append(f"Expanded content to meet {length} length requirements")
        
        return content, changes
    
    def _expand_content(self, content: str, additional_sentences: int) -> str:
        """Expand content by adding relevant sentences"""
        expansion_templates = [
            "This aspect is particularly important to consider.",
            "It's worth exploring this topic further.",
            "Additional research supports these findings.",
            "This approach has proven effective in various contexts.",
            "Further analysis reveals interesting insights.",
            "This perspective offers valuable insights.",
            "Consider the implications of this approach.",
            "This method has demonstrated consistent results."
        ]
        
        sentences = content.split('. ')
        for i in range(additional_sentences):
            if i < len(expansion_templates):
                sentences.append(expansion_templates[i])
        
        return '. '.join(sentences)
    
    def _adjust_for_audience(self, content: str, target_audience: str) -> Tuple[str, List[str]]:
        """Adjust content for specific target audience"""
        changes = []
        
        audience_adjustments = {
            "general": [],
            "technical": [
                ("simple", "straightforward"),
                ("easy", "efficient"),
                ("basic", "fundamental")
            ],
            "beginners": [
                ("complex", "detailed"),
                ("advanced", "comprehensive"),
                ("sophisticated", "thorough")
            ],
            "experts": [
                ("simple", "elementary"),
                ("basic", "fundamental"),
                ("easy", "straightforward")
            ]
        }
        
        if target_audience in audience_adjustments:
            for old_word, new_word in audience_adjustments[target_audience]:
                if old_word in content.lower():
                    content = re.sub(rf'\b{old_word}\b', new_word, content, flags=re.IGNORECASE)
                    changes.append(f"Adjusted vocabulary for {target_audience} audience")
        
        return content, changes
    
    def _polish_content(self, content: str) -> str:
        """Final polish of the content"""
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Fix punctuation
        content = re.sub(r'\s+([.,!?])', r'\1', content)
        
        # Ensure proper capitalization
        sentences = content.split('. ')
        capitalized_sentences = []
        for sentence in sentences:
            if sentence:
                capitalized_sentences.append(sentence[0].upper() + sentence[1:])
        
        return '. '.join(capitalized_sentences)
    
    def calculate_readability(self, content: str) -> float:
        """Calculate readability score using Flesch Reading Ease"""
        if not TEXTSTAT_AVAILABLE:
            logger.warning("Textstat not available - using default readability score")
            return 60.0  # Default score
        
        try:
            return textstat.flesch_reading_ease(content)
        except Exception as e:
            logger.error(f"Readability calculation failed: {e}")
            return 60.0  # Default score 