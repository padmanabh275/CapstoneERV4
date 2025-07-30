import asyncio
import logging
import re
from typing import List, Dict, Tuple
from collections import Counter
import requests
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class SEOOptimizer:
    """
    SEO Optimization Agent - Optimizes content for search engines
    """
    
    def __init__(self):
        # SEO best practices and rules
        self.seo_rules = {
            "title_length": {"min": 30, "max": 60},
            "meta_description_length": {"min": 120, "max": 160},
            "keyword_density": {"min": 0.5, "max": 2.5},  # percentage
            "heading_structure": ["h1", "h2", "h3"],
            "content_length": {"min": 300, "max": 2000}
        }
        
        # Common SEO stop words to avoid
        self.stop_words = {
            "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
            "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
            "to", "was", "will", "with"
        }
        
        # SEO improvement suggestions
        self.improvement_suggestions = {
            "keyword_density_low": "Increase keyword density by naturally incorporating target keywords",
            "keyword_density_high": "Reduce keyword stuffing - aim for natural keyword usage",
            "title_missing": "Add a compelling title with target keywords",
            "headings_missing": "Add H2 and H3 headings to improve structure",
            "content_short": "Expand content to provide more value to readers",
            "meta_missing": "Add meta description for better search results",
            "links_missing": "Add relevant internal and external links"
        }
    
    async def optimize(
        self, 
        content: str, 
        keywords: List[str], 
        target_url: str = None
    ) -> Tuple[str, Dict, float]:
        """
        Optimize content for SEO
        
        Args:
            content: Original content to optimize
            keywords: Target keywords for optimization
            target_url: Target URL for the content
            
        Returns:
            Tuple of (optimized_content, keyword_density, seo_score)
        """
        try:
            optimized_content = content
            changes = []
            
            # Analyze current content
            current_density = self._calculate_keyword_density(content, keywords)
            current_score = self._calculate_seo_score(content, keywords)
            
            # Optimize title
            optimized_content = self._optimize_title(optimized_content, keywords)
            
            # Optimize headings
            optimized_content = self._optimize_headings(optimized_content, keywords)
            
            # Optimize keyword usage
            optimized_content = self._optimize_keyword_usage(optimized_content, keywords)
            
            # Add meta description
            optimized_content = self._add_meta_description(optimized_content, keywords)
            
            # Optimize content structure
            optimized_content = self._optimize_content_structure(optimized_content)
            
            # Add internal links suggestions
            optimized_content = self._add_link_suggestions(optimized_content, target_url)
            
            # Recalculate metrics
            final_density = self._calculate_keyword_density(optimized_content, keywords)
            final_score = self._calculate_seo_score(optimized_content, keywords)
            
            return optimized_content, final_density, final_score
            
        except Exception as e:
            logger.error(f"SEO optimization failed: {e}")
            return content, {}, 0.0
    
    def _calculate_keyword_density(self, content: str, keywords: List[str]) -> Dict:
        """Calculate keyword density for each keyword"""
        density = {}
        words = content.lower().split()
        total_words = len(words)
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Count exact matches
            exact_matches = words.count(keyword_lower)
            # Count partial matches (keyword as part of other words)
            partial_matches = sum(1 for word in words if keyword_lower in word)
            
            total_matches = exact_matches + partial_matches
            density_percentage = (total_matches / total_words) * 100 if total_words > 0 else 0
            
            density[keyword] = {
                "count": total_matches,
                "density": round(density_percentage, 2),
                "optimal": self.seo_rules["keyword_density"]["min"] <= density_percentage <= self.seo_rules["keyword_density"]["max"]
            }
        
        return density
    
    def _calculate_seo_score(self, content: str, keywords: List[str]) -> float:
        """Calculate overall SEO score (0-100)"""
        score = 0.0
        max_score = 100.0
        
        # Title optimization (20 points)
        title_score = self._evaluate_title(content, keywords)
        score += title_score * 20
        
        # Keyword density (25 points)
        density_score = self._evaluate_keyword_density(content, keywords)
        score += density_score * 25
        
        # Content structure (20 points)
        structure_score = self._evaluate_content_structure(content)
        score += structure_score * 20
        
        # Content length (15 points)
        length_score = self._evaluate_content_length(content)
        score += length_score * 15
        
        # Meta description (10 points)
        meta_score = self._evaluate_meta_description(content)
        score += meta_score * 10
        
        # Internal links (10 points)
        links_score = self._evaluate_internal_links(content)
        score += links_score * 10
        
        return min(score, max_score)
    
    def _evaluate_title(self, content: str, keywords: List[str]) -> float:
        """Evaluate title optimization"""
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE)
        if not title_match:
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        
        if title_match:
            title = title_match.group(1)
            title_length = len(title)
            
            # Check length
            if self.seo_rules["title_length"]["min"] <= title_length <= self.seo_rules["title_length"]["max"]:
                score = 0.5
            else:
                score = 0.2
            
            # Check keyword presence
            title_lower = title.lower()
            keyword_present = any(keyword.lower() in title_lower for keyword in keywords)
            if keyword_present:
                score += 0.5
            
            return score
        
        return 0.0
    
    def _evaluate_keyword_density(self, content: str, keywords: List[str]) -> float:
        """Evaluate keyword density"""
        density = self._calculate_keyword_density(content, keywords)
        
        optimal_count = 0
        for keyword_data in density.values():
            if keyword_data["optimal"]:
                optimal_count += 1
        
        return optimal_count / len(keywords) if keywords else 0.0
    
    def _evaluate_content_structure(self, content: str) -> float:
        """Evaluate content structure"""
        score = 0.0
        
        # Check for headings
        h1_count = len(re.findall(r'<h1[^>]*>', content, re.IGNORECASE))
        h2_count = len(re.findall(r'<h2[^>]*>', content, re.IGNORECASE))
        h3_count = len(re.findall(r'<h3[^>]*>', content, re.IGNORECASE))
        
        if h1_count > 0:
            score += 0.3
        if h2_count > 0:
            score += 0.4
        if h3_count > 0:
            score += 0.3
        
        return min(score, 1.0)
    
    def _evaluate_content_length(self, content: str) -> float:
        """Evaluate content length"""
        word_count = len(content.split())
        
        if self.seo_rules["content_length"]["min"] <= word_count <= self.seo_rules["content_length"]["max"]:
            return 1.0
        elif word_count < self.seo_rules["content_length"]["min"]:
            return 0.3
        else:
            return 0.7
    
    def _evaluate_meta_description(self, content: str) -> float:
        """Evaluate meta description"""
        meta_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
        
        if meta_match:
            meta_length = len(meta_match.group(1))
            if self.seo_rules["meta_description_length"]["min"] <= meta_length <= self.seo_rules["meta_description_length"]["max"]:
                return 1.0
            else:
                return 0.5
        
        return 0.0
    
    def _evaluate_internal_links(self, content: str) -> float:
        """Evaluate internal links"""
        link_count = len(re.findall(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>', content))
        
        if link_count >= 2:
            return 1.0
        elif link_count == 1:
            return 0.5
        else:
            return 0.0
    
    def _optimize_title(self, content: str, keywords: List[str]) -> str:
        """Optimize title with keywords"""
        # Check if title exists
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE)
        if not title_match:
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        
        if not title_match and keywords:
            # Add title if missing
            primary_keyword = keywords[0]
            title = f"# {primary_keyword.title()} - Complete Guide"
            content = f"{title}\n\n{content}"
        
        return content
    
    def _optimize_headings(self, content: str, keywords: List[str]) -> str:
        """Optimize headings with keywords"""
        # Add H2 headings if missing
        if not re.search(r'<h2[^>]*>', content, re.IGNORECASE) and not re.search(r'^##\s+', content, re.MULTILINE):
            if keywords:
                primary_keyword = keywords[0]
                h2_section = f"\n## Why {primary_keyword.title()} Matters\n"
                # Insert after first paragraph
                paragraphs = content.split('\n\n')
                if len(paragraphs) > 1:
                    paragraphs.insert(1, h2_section)
                    content = '\n\n'.join(paragraphs)
        
        return content
    
    def _optimize_keyword_usage(self, content: str, keywords: List[str]) -> str:
        """Optimize keyword usage throughout content"""
        optimized_content = content
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            content_lower = optimized_content.lower()
            
            # Count current usage
            current_count = content_lower.count(keyword_lower)
            words = optimized_content.split()
            total_words = len(words)
            
            # Calculate target usage
            target_density = 1.5  # 1.5% density
            target_count = int((target_density / 100) * total_words)
            
            if current_count < target_count:
                # Add keyword naturally
                optimized_content = self._add_keyword_naturally(optimized_content, keyword)
        
        return optimized_content
    
    def _add_keyword_naturally(self, content: str, keyword: str) -> str:
        """Add keyword naturally to content"""
        # Find good insertion points (end of sentences)
        sentences = content.split('. ')
        
        for i, sentence in enumerate(sentences):
            if keyword.lower() not in sentence.lower() and len(sentence) > 20:
                # Add keyword to sentence
                sentences[i] = f"{sentence} This is particularly important when considering {keyword}."
                break
        
        return '. '.join(sentences)
    
    def _add_meta_description(self, content: str, keywords: List[str]) -> str:
        """Add meta description if missing"""
        if not re.search(r'<meta[^>]*name=["\']description["\']', content, re.IGNORECASE):
            # Create meta description
            primary_keyword = keywords[0] if keywords else "content"
            meta_desc = f"Learn about {primary_keyword} with our comprehensive guide. Discover best practices, tips, and insights."
            
            # Add to head section or beginning
            if '<head>' in content:
                content = content.replace('<head>', f'<head>\n<meta name="description" content="{meta_desc}">')
            else:
                content = f'<meta name="description" content="{meta_desc}">\n\n{content}'
        
        return content
    
    def _optimize_content_structure(self, content: str) -> str:
        """Optimize content structure for better readability"""
        # Add bullet points for better structure
        if 'Key Points' in content or 'Benefits' in content:
            # Convert to bullet points
            content = re.sub(r'(\d+\.\s+)', r'* ', content)
        
        # Add conclusion if missing
        if not re.search(r'conclusion|summary|final', content, re.IGNORECASE):
            content += "\n\n## Summary\nThis comprehensive guide provides valuable insights and practical advice."
        
        return content
    
    def _add_link_suggestions(self, content: str, target_url: str) -> str:
        """Add internal link suggestions"""
        if target_url:
            domain = urlparse(target_url).netloc
            if domain:
                # Add related content links
                link_section = f"\n\n## Related Content\n- [More about this topic](/related)\n- [Best practices](/best-practices)\n- [FAQ](/faq)"
                content += link_section
        
        return content
    
    def get_suggestions(self, content: str, keywords: List[str]) -> List[str]:
        """Get SEO improvement suggestions"""
        suggestions = []
        
        # Check keyword density
        density = self._calculate_keyword_density(content, keywords)
        for keyword, data in density.items():
            if data["density"] < self.seo_rules["keyword_density"]["min"]:
                suggestions.append(f"Low keyword density for '{keyword}' - consider adding more naturally")
            elif data["density"] > self.seo_rules["keyword_density"]["max"]:
                suggestions.append(f"High keyword density for '{keyword}' - reduce keyword stuffing")
        
        # Check title
        if not re.search(r'<h1[^>]*>|^#\s+', content, re.IGNORECASE):
            suggestions.append("Missing H1 title - add a compelling title with target keywords")
        
        # Check headings
        if not re.search(r'<h2[^>]*>|^##\s+', content, re.IGNORECASE):
            suggestions.append("Missing H2 headings - add subheadings to improve structure")
        
        # Check content length
        word_count = len(content.split())
        if word_count < self.seo_rules["content_length"]["min"]:
            suggestions.append("Content is too short - expand to provide more value")
        
        # Check meta description
        if not re.search(r'<meta[^>]*name=["\']description["\']', content, re.IGNORECASE):
            suggestions.append("Missing meta description - add for better search results")
        
        # Check internal links
        link_count = len(re.findall(r'<a[^>]*href=["\']([^"\']*)["\']', content))
        if link_count < 2:
            suggestions.append("Add more internal links to improve site structure")
        
        return suggestions 