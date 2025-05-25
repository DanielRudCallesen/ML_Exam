from typing import Dict, List, Any

class CostEstimationTool:
    """Tool for estimating costs and time for development tasks."""
    
    def __init__(self):
        self.name = "cost_estimation_tool"
        self.description = "Estimate time and cost for development tasks"
        
        # Hourly rates by region and experience level (USD)
        self.hourly_rates = {
            'junior': {
                'US/Canada': 30, 'Western Europe': 25, 'Eastern Europe': 15,
                'Asia': 10, 'Latin America': 12, 'Global Average': 20
            },
            'mid': {
                'US/Canada': 60, 'Western Europe': 50, 'Eastern Europe': 30,
                'Asia': 20, 'Latin America': 25, 'Global Average': 40
            },
            'senior': {
                'US/Canada': 100, 'Western Europe': 80, 'Eastern Europe': 50,
                'Asia': 35, 'Latin America': 40, 'Global Average': 65
            }
        }
    
    def estimate_project_cost(self, subtasks: List[Dict[str, Any]], 
                            developer_level: str, region: str) -> Dict[str, Any]:
        """Estimate total cost and time for entire project."""
        
        total_hours = 0
        task_estimates = []
        hourly_rate = self.hourly_rates[developer_level][region]
        
        for task in subtasks:
            hours = self._parse_hours(task.get('estimated_hours', '4'))
            cost = hours * hourly_rate
            
            task_estimates.append({
                'name': task.get('name', 'Unknown Task'),
                'hours': hours,
                'cost': cost
            })
            
            total_hours += hours
        
        # Add 20% buffer
        buffered_hours = total_hours * 1.2
        total_cost = buffered_hours * hourly_rate
        
        # Calculate timeline
        days = buffered_hours / 8  # 8 hours per day
        weeks = days / 5  # 5 days per week
        
        return {
            'total_hours': f"{total_hours:.0f} hours (+ 20% buffer = {buffered_hours:.0f} hours)",
            'total_cost': f"${total_cost:.0f}",
            'timeline': f"{weeks:.1f} weeks",
            'hourly_rate': f"${hourly_rate}/hour",
            'developer_level': developer_level,
            'region': region,
            'task_breakdown': task_estimates
        }
    
    def _parse_hours(self, hours_str: str) -> float:
        """Parse hours string like '4-8' or '10' into average hours."""
        
        if '-' in hours_str:
            parts = hours_str.split('-')
            min_hours = float(parts[0])
            max_hours = float(parts[1])
            return (min_hours + max_hours) / 2  # Return average
        else:
            return float(hours_str) 