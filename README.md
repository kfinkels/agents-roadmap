# Agents Roadmap

A comprehensive exploration of AI agent architectures using Anthropic's Claude API.

## Overview

This project demonstrates different agent design patterns through a series of Jupyter notebooks, progressing from simple agents to more sophisticated architectures.

## Project Structure

```
agents-roadmap/
├── notebooks/
│   ├── 01_simple_agent.ipynb       # Basic agent implementation
│   ├── 02_react_agent.ipynb        # ReAct (Reasoning + Acting) pattern
│   ├── 03_simple_vs_react.ipynb    # Comparison of simple vs ReAct agents
│   ├── 04_planning_agent.ipynb     # Planning-based agent architecture
│   ├── 05_react_vs_planning.ipynb  # Comparison of ReAct vs Planning agents
│   ├── 06_summary.ipynb            # Summary and conclusions
│   ├── db_helper.py                # Database utilities
│   ├── db_tools.py                 # Customer support database tools
│   ├── inventory_tools.py          # Inventory management tools
│   ├── customer_support.db         # Sample customer support database
│   └── inventory.db                # Sample inventory database
└── .env_example                    # Environment configuration template

```

## Getting Started

### Prerequisites

- Python 3.8+
- Jupyter Notebook or JupyterLab
- Anthropic API access

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd agents-roadmap
   ```

2. Install dependencies:
   ```bash
   pip install anthropic jupyter
   ```

3. Set up environment variables:
   ```bash
   cp notebooks/.env_example notebooks/.env
   ```

   Edit `notebooks/.env` with your API credentials:
   - `ANTHROPIC_BASE_URL`: Your API endpoint
   - `ANTHROPIC_AUTH_TOKEN`: Your API authentication token
   - `ANTHROPIC_MODEL`: The Claude model to use

4. Launch Jupyter:
   ```bash
   jupyter notebook notebooks/
   ```

## Notebook Series

### 1. Simple Agent
Introduction to basic agent architecture with direct prompting.

### 2. ReAct Agent
Implementation of the ReAct pattern where agents reason about actions before taking them.

### 3. Simple vs ReAct Comparison
Comparative analysis of simple and ReAct agent approaches.

### 4. Planning Agent
Advanced agent that creates plans before execution.

### 5. ReAct vs Planning Comparison
Evaluation of different agent architectures for complex tasks.

### 6. Summary
Conclusions and best practices for choosing agent architectures.

## Tools and Databases

The project includes sample databases and tools for:
- **Customer Support**: Query and manage customer support tickets
- **Inventory Management**: Track and manage product inventory

These tools are used throughout the notebooks to demonstrate real-world agent applications.

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]