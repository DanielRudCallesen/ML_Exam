# Task Planner & Estimator Agent

An AI-powered system that breaks down high-level development tasks into manageable subtasks and provides accurate cost estimates. Built using AutoGen framework with Mistral LLM and custom tools for comprehensive project analysis.

## Features

- **Task Breakdown**: Automatically decomposes complex tasks into structured subtasks with dependencies
- **Web Research**: Integrates DuckDuckGo API for real-time development insights
- **Cost Estimation**: Regional and skill-level specific pricing with 20% project buffer
- **Multiple Scenarios**: Supports different developer levels (Junior/Mid/Senior) across various regions
- **Professional Output**: Generate client-ready project estimates with detailed analysis

## Dependencies

### Required Packages

The project requires the following Python packages:

```
autogen-agentchat @ git+https://github.com/patrickstolc/autogen.git@0.2
mistralai==1.2.3
ollama==0.3.3
fix-busted-json==0.0.18
requests>=2.25.0
```

### API Requirements

- **Mistral API Key**: Required for LLM functionality
- **Internet Connection**: For DuckDuckGo web research (no API key needed)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ML_Exam
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. API Key Configuration

The demo uses a pre-configured Mistral API key. For production use, you should:

1. Get your own Mistral API key from [Mistral AI](https://mistral.ai/)
2. Replace the hardcoded API key in `main.py` (line 41) or use environment variables:


## Project Structure

```
ML_Exam/
├── main.py                    # Demo script with 3 scenarios
├── requirements.txt           # Project dependencies
├── Agent/
│   ├── __init__.py
│   └── task_planner_agent.py  # Main agent orchestrator
└── Tools/
    ├── __init__.py
    ├── task_breakdown_tool.py  # Task decomposition logic
    ├── web_research_tool.py    # DuckDuckGo API integration
    └── cost_estimation_tool.py # Regional pricing calculator
```

## How to Run

### Quick Start

Run the demo with three pre-configured scenarios:

```bash
python main.py
```

This will demonstrate:
1. **Junior Developer** (Eastern Europe) - Simple bakery landing page
2. **Mid-Level Developer** (Global Average) - Corporate website  
3. **Senior Developer** (US/Canada) - Complex e-commerce platform
