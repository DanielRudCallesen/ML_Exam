from typing import Dict, List, Any
import re

class TaskBreakdownTool:
    """Tool for breaking down high-level tasks into smaller, manageable subtasks."""
    
    def __init__(self):
        self.name = "task_breakdown_tool"
        self.description = "Break down complex tasks into smaller, manageable subtasks"
    
    def break_down_task(self, task_description: str, project_type: str = "web_development") -> Dict[str, Any]:
        """
        Break down a high-level task into smaller subtasks.
        
        Args:
            task_description: The high-level task description
            project_type: Type of project (default: web_development)
            
        Returns:
            Dictionary containing the breakdown of tasks
        """
        
        # Extract key requirements from the task description
        requirements = self._extract_requirements(task_description)
        
        # Generate subtasks based on project type and requirements
        if project_type == "web_development":
            subtasks = self._break_down_web_project(requirements, task_description)
        else:
            subtasks = self._break_down_generic_project(requirements, task_description)
        
        return {
            'main_task': task_description,
            'project_type': project_type,
            'requirements_found': requirements,
            'subtasks': subtasks,
            'total_subtasks': len(subtasks),
            'breakdown_method': 'automated_analysis'
        }
    
    def _extract_requirements(self, description: str) -> List[str]:
        """Extract specific requirements from the task description."""
        
        lines = [line.strip() for line in description.split('\n') if line.strip()]
        
        # Extract bulleted/numbered requirements
        list_pattern = r'^[-*•]\s+|^\d+\.\s+'
        list_requirements = [
            re.sub(list_pattern, '', line) 
            for line in lines 
            if re.match(list_pattern, line)
        ]
        
        # Extract "must have" style requirements
        must_have_phrases = ['must have', 'must include', 'should have', 'needs to', 'require']
        must_have_requirements = [
            line for line in lines 
            if any(phrase in line.lower() for phrase in must_have_phrases)
        ]
        
        # Combine all found requirements
        requirements = list_requirements + must_have_requirements

        return requirements
    
    def _break_down_web_project(self, requirements: List[str], full_description: str) -> List[Dict[str, Any]]:
        """Break down a web development project into subtasks."""
        
        subtasks = []
        
        # Standard web development phases
        standard_phases = [
            {
                'name': 'Project Setup & Planning',
                'description': 'Set up development environment and plan project structure',
                'category': 'setup',
                'dependencies': [],
                'estimated_hours': '2-4'
            },
            {
                'name': 'Design & Wireframing',
                'description': 'Create visual design and layout wireframes',
                'category': 'design',
                'dependencies': ['Project Setup & Planning'],
                'estimated_hours': '4-8'
            }
        ]
        
        # Add standard phases
        subtasks.extend(standard_phases)
        
        # Process specific requirements
        for i, requirement in enumerate(requirements):
            req_lower = requirement.lower()
            
            # Header-related tasks
            if 'header' in req_lower:
                subtasks.append({
                    'name': 'Implement Header Component',
                    'description': f'Create header component: {requirement}',
                    'category': 'frontend',
                    'dependencies': ['Design & Wireframing'],
                    'estimated_hours': '2-6',
                    'complexity_factors': ['navigation complexity', 'responsive design', 'branding elements']
                })
            
            # Footer-related tasks
            elif 'footer' in req_lower:
                subtasks.append({
                    'name': 'Implement Footer Component',
                    'description': f'Create footer component: {requirement}',
                    'category': 'frontend',
                    'dependencies': ['Design & Wireframing'],
                    'estimated_hours': '1-3',
                    'complexity_factors': ['content amount', 'social links', 'responsive layout']
                })
            
            # Product description tasks
            elif any(word in req_lower for word in ['product', 'service', 'description']):
                subtasks.append({
                    'name': 'Implement Product Description Section',
                    'description': f'Create product/service description: {requirement}',
                    'category': 'frontend',
                    'dependencies': ['Design & Wireframing'],
                    'estimated_hours': '3-8',
                    'complexity_factors': ['content structure', 'media integration', 'interactive elements']
                })
            

            
            # Contact-related tasks
            elif any(word in req_lower for word in ['contact', 'form']):
                subtasks.append({
                    'name': 'Implement Contact Section',
                    'description': f'Create contact functionality: {requirement}',
                    'category': 'frontend',
                    'dependencies': ['Design & Wireframing'],
                    'estimated_hours': '2-8',
                    'complexity_factors': ['form complexity', 'validation', 'email integration']
                })
            
            # Generic requirement
            else:
                subtasks.append({
                    'name': f'Implement Requirement {i+1}',
                    'description': requirement,
                    'category': 'frontend',
                    'dependencies': ['Design & Wireframing'],
                    'estimated_hours': '2-8',
                    'complexity_factors': ['requirement complexity', 'integration needs']
                })
        
        # Add final phases
        final_phases = [
            {
                'name': 'Responsive Design Implementation',
                'description': 'Ensure all components work across different devices',
                'category': 'frontend',
                'dependencies': [task['name'] for task in subtasks if task['category'] == 'frontend'],
                'estimated_hours': '4-12'
            },
            {
                'name': 'Testing & Quality Assurance',
                'description': 'Test functionality and fix bugs',
                'category': 'testing',
                'dependencies': ['Responsive Design Implementation'],
                'estimated_hours': '4-8'
            },
            {
                'name': 'Deployment & Launch',
                'description': 'Deploy to production and configure hosting',
                'category': 'deployment',
                'dependencies': ['Testing & Quality Assurance'],
                'estimated_hours': '2-4'
            }
        ]
        
        subtasks.extend(final_phases)
        
        return subtasks