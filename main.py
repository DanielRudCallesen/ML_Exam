import asyncio
import warnings
from Agent.task_planner_agent import TaskPlannerAgent

# Suppress the cost calculation warning from AutoGen
warnings.filterwarnings("ignore", message="Cost calculation is not implemented for model*")
warnings.filterwarnings("ignore", category=UserWarning, module="autogen.oai.mistral")
warnings.filterwarnings("ignore", message="flaml.automl is not available*")
warnings.filterwarnings("ignore", category=UserWarning, module="flaml")

def print_section(title: str, content: str = "", separator: str = "="):
    """Print a formatted section with title and content."""
    print(f"\n{separator * 60}")
    print(f"{title}")
    print(f"{separator * 60}")
    if content:
        print(content)

def format_json_output(data: dict, max_depth: int = 3, current_depth: int = 0) -> str:
    """Format JSON output for better readability."""
    if current_depth >= max_depth:
        return str(data)
    
    if isinstance(data, dict):
        result = ""
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                if current_depth < max_depth - 1:
                    result += f"\n{' ' * (current_depth * 2)}{key}:\n"
                    result += format_json_output(value, max_depth, current_depth + 1)
                else:
                    result += f"\n{' ' * (current_depth * 2)}{key}: [Complex object - {type(value).__name__}]"
            else:
                result += f"\n{' ' * (current_depth * 2)}{key}: {value}"
        return result

async def main():
    """Main function to demonstrate the Task Planner & Estimator Agent."""
    
    print_section("TASK PLANNER & ESTIMATOR AGENT", "Demonstrating Multiple Scenarios...")
    
    api_key = "cKjjuUBJEaMWPrF2OvKMiqDR2nPf1I6a"  

    # Define different scenarios
    scenarios = [
        {
            "name": "Junior Developer - Simple Landing Page",
            "developer_level": "junior",
            "region": "Eastern Europe",
            "task": """
I need to create a basic landing page for a local bakery.
Requirements:
- Simple header with bakery name and phone number
- One section showcasing popular items with images
- Basic contact information in the footer
- Must work on mobile phones
- Simple, clean design (no fancy animations)

This is my first professional web project and I want realistic time estimates.
"""
        },
        {
            "name": "Mid-Level Developer - Corporate Website",
            "developer_level": "mid", 
            "region": "Global Average",
            "task": """
I'm tasked with building a new product landing page for "Acme Inc."
They have the following requirements:
- The page must have a header with the name of the company
- The page must have a section describing the product
- The page must have a section describing the team
- The page must have a footer with the company contact details
- The page should be responsive and work on all devices
- The page should have a modern, professional design

I'm a team of one and I need to estimate how long it will take me to complete the task and roughly how much it will cost.
"""
        },
        {
            "name": "Senior Developer - Complex E-commerce Platform",
            "developer_level": "senior",
            "region": "US/Canada", 
            "task": """
I need to architect and develop a sophisticated e-commerce platform for a luxury fashion brand.
Requirements:
- Advanced product catalog with filtering, search, and recommendations
- Custom shopping cart with saved items and wish lists
- Multi-step checkout with payment gateway integration
- User accounts with order history and preferences
- Admin dashboard with analytics and inventory management
- Mobile-first responsive design with advanced animations
- SEO optimization and performance monitoring
- Integration with CRM and email marketing systems

This requires senior-level architecture decisions and complex integrations.
"""
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print_section(f"SCENARIO {i}: {scenario['name']}")
        print(f"Developer Level: {scenario['developer_level'].title()}")
        print(f"Region: {scenario['region']}")
        print(f"Task Description:")
        print(scenario['task'].strip())
        
        # Initialize agent for this scenario
        agent = TaskPlannerAgent(
            api_key=api_key,
            developer_level=scenario['developer_level'],
            region=scenario['region']
        )
        
        print(f"\nAnalyzing with {scenario['developer_level']} developer rates in {scenario['region']}...")
        
        # Get analysis
        result = await agent.plan_and_estimate(
            task_description=scenario['task'],
            project_type="web_development"
        )
        
        # Display results
        if result['status'] == 'success':
            # Extract and clean up the LLM response
            analysis = result.get('analysis', '')
            
            if isinstance(analysis, dict):
                content = analysis.get('content', str(analysis))
            elif isinstance(analysis, str):
                content = analysis
            else:
                content = str(analysis)
            
            formatted_content = content.replace('\\n', '\n').replace('\\"', '"')
            print(formatted_content)
            
        else:
            print(f"Analysis failed: {result.get('error', 'Unknown error')}")
        
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    print("Starting Task Planner & Estimator Agent Demo")
    
    asyncio.run(main())
    
    print("\n🏁 Demo completed!") 