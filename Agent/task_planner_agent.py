import json
import os
from typing import Dict, List, Any, Optional
import autogen

# Import our custom tools
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Tools.web_research_tool import WebResearchTool
from Tools.task_breakdown_tool import TaskBreakdownTool
from Tools.cost_estimation_tool import CostEstimationTool

class TaskPlannerAgent:
    """
    AI Agent for Task Planning and Cost Estimation using AutoGen.
    
    This agent can break down high-level tasks into smaller subtasks and estimate
    the time and cost required to complete each subtask using various tools.
    """
    
    def __init__(self, api_key: str, developer_level: str, region: str):
        """
        Initialize the Task Planner Agent.
        
        Args:
            api_key: Mistral API key
            developer_level: Developer experience level (junior, mid, senior)
            region: Geographic region for cost calculations
        """
        self.api_key = api_key
        self.developer_level = developer_level
        self.region = region
        
        # Initialize tools
        self.web_research_tool = WebResearchTool()
        self.task_breakdown_tool = TaskBreakdownTool()
        self.cost_estimation_tool = CostEstimationTool()
        
        # LLM Configuration
        self.llm_config = {
            "config_list": [
                {
                    "model": "open-mistral-nemo",
                    "api_key": "cKjjuUBJEaMWPrF2OvKMiqDR2nPf1I6a",
                    "api_type": "mistral",
                    "api_rate_limit": 0.25,
                    "repeat_penalty": 1.1,
                    "temperature": 0.0,
                    "seed": 42,
                    "stream": False,
                    "native_tool_calls": False,
                    "cache_seed": None,
                }
            ]
        }
        
        # Initialize the AutoGen agent
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the AutoGen assistant agent with tools."""
        
        # Define the system message for the agent
        system_message = """
        You are a Task Planner & Estimator Agent specialized in breaking down high-level tasks into smaller, manageable subtasks and estimating their time and cost.

        Your capabilities include:
        1. Analyzing task descriptions to extract requirements
        2. Breaking down complex tasks into smaller subtasks with dependencies
        3. Researching development information and best practices
        4. Estimating time and cost for individual tasks and entire projects
        5. Providing detailed analysis of complexity factors

        When given a task, you should:
        1. First analyze the task description to understand the requirements
        2. Use the web research tool to gather relevant information about similar tasks
        3. Break down the task into smaller subtasks using the task breakdown tool
        4. Estimate costs and timeline for each subtask using the cost estimation tool
        5. Provide a comprehensive summary with total estimates and recommendations

        Always provide detailed explanations for your estimates and include factors that might affect the cost or timeline.
        Be specific about assumptions and provide ranges rather than single point estimates.
        """
        
                
        # Create the assistant agent
        self.agent = autogen.AssistantAgent(
            name="TaskPlannerAgent",
            system_message=system_message,
            llm_config=self.llm_config
        )
    
    async def plan_and_estimate(self, task_description: str, 
                              project_type: str = "web_development") -> Dict[str, Any]:
        """
        Main method to plan and estimate a task.
        
        Args:
            task_description: High-level description of the task
            project_type: Type of project (web_development)
            tech_stack: Technology stack to be used
            
        Returns:
            Dictionary containing the complete analysis and estimates
        """
        
        # Step 1: Break down the task into subtasks
        breakdown_result = self.task_breakdown_tool.break_down_task(
                task_description=task_description,
                project_type=project_type
            )
            
        # Step 2: Get complexity analysis and web research
        research_result = self.web_research_tool.estimate_task_complexity(task_description)
        
        # Step 3: Get web search results for development insights
        search_query = f"web development {project_type} time estimate cost"
        web_search_result = self.web_research_tool.search_development_info(search_query)
            
        # Step 4: Estimate costs using scenario-specific parameters
        cost_result = self.cost_estimation_tool.estimate_project_cost(
                subtasks=breakdown_result['subtasks'],
                developer_level=self.developer_level,
                region=self.region
            )
            
        # Step 5: Create comprehensive analysis using LLM
        prompt = f"""
            Analyze this web development project and provide a professional summary:

            TASK: {task_description}
            DEVELOPER: {self.developer_level.title()} level in {self.region}
            
            BREAKDOWN: {len(breakdown_result['subtasks'])} subtasks identified
            COMPLEXITY: {research_result['complexity']} complexity level
            
            WEB RESEARCH INSIGHTS:
            {web_search_result.get('abstract', 'No specific insights found')}
            
            COST ANALYSIS:
            - Total Hours: {cost_result['total_hours']}
            - Total Cost: {cost_result['total_cost']}
            - Timeline: {cost_result['timeline']}
            - Rate: {cost_result['hourly_rate']}
            
            SUBTASKS:
            {chr(10).join([f"• {task['name']}: {task.get('estimated_hours', 'TBD')} hours" for task in breakdown_result['subtasks']])}

            Please provide:
            1. Executive Summary
            2. Detailed Task Breakdown
            3. Cost & Timeline Analysis
            4. Risk Factors & Recommendations

            Format as a professional project estimate.
            """
            
            # Get LLM analysis
        llm_response = self.agent.generate_reply(messages=[{"content": prompt, "role": "user"}])
            
        return {
                'status': 'success',
                'task_description': task_description,
                'developer_level': self.developer_level,
                'region': self.region,
                'breakdown': breakdown_result,
                'research': research_result,
                'web_search': web_search_result,
                'cost_analysis': cost_result,
                'analysis': llm_response
            }