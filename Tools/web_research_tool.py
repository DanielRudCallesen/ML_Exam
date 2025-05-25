import requests
import json
from typing import Dict, List, Any
import time
import re

class WebResearchTool:
    """Tool for researching web development tasks, technologies, and time estimates."""
    
    def __init__(self):
        self.name = "web_research_tool"
        self.description = "Search for information about web development tasks, technologies, and time estimates"
    
    def search_development_info(self, query: str) -> Dict[str, Any]:
        """
        Search for development-related information using DuckDuckGo API
        
        Args:
            query: Search query related to development tasks or technologies
            
        Returns:
            Dictionary containing search results and relevant information
        """
        try:
            # Use DuckDuckGo Instant Answer API
            url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            result = {
                'query': query,
                'abstract': data.get('Abstract', ''),
                'definition': data.get('Definition', ''),
                'answer': data.get('Answer', ''),
                'infobox': data.get('Infobox', {}),
                'related_topics': [topic.get('Text', '') for topic in data.get('RelatedTopics', [])[:5]],
                'results': data.get('Results', [])[:3]
            }
            
            return result
            
        except Exception as e:
            return {
                'query': query,
                'error': f"Search failed: {str(e)}",
            }
    
    
    def get_technology_info(self, technology: str) -> Dict[str, Any]:
        """Get information about a specific technology or framework."""
        
        query = f"{technology} web development framework tutorial time"
        return self.search_development_info(query)
    
    def estimate_task_complexity(self, task_description: str) -> Dict[str, Any]:
        """Analyze task description to estimate complexity level."""
        
        complexity_indicators = {
            'simple': ['basic', 'simple', 'static', 'minimal', 'standard'],
            'medium': ['responsive', 'interactive', 'dynamic', 'moderate', 'custom'],
            'complex': ['advanced', 'complex', 'animated', 'integration', 'api', 'database']
        }
        
        task_lower = task_description.lower()
        scores = {'simple': 0, 'medium': 0, 'complex': 0}
        
        for level, indicators in complexity_indicators.items():
            for indicator in indicators:
                if indicator in task_lower:
                    scores[level] += 1
        
        # Determine complexity level
        max_score = max(scores.values())
        if max_score == 0:
            complexity = 'medium'  # default
        else:
            complexity = max(scores, key=scores.get)
        
        return {
            'complexity': complexity,
            'scores': scores,
            'analysis': f"Task appears to be {complexity} complexity based on keywords",
            'indicators_found': [word for word in task_lower.split() 
                               if any(word in indicators for indicators in complexity_indicators.values())]
        } 