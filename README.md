# Agents Roadmap

A comprehensive exploration of AI agent architectures using z.ai's LLM API.

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
- z.ai API access

### Get Your z.ai API Key

1. Go to [z.ai API Key Management](https://z.ai/manage-apikey/apikey-list)
2. Create a new API key
3. Copy the key for use in the `.env` file

### Available Models

See the full model list and pricing at: [z.ai Pricing](https://docs.z.ai/guides/overview/pricing)

We use **GLM-4.6V-Flash** which is free.

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd agents-roadmap
   ```

2. Install dependencies:
   ```bash
   pip install openai python-dotenv jupyterlab
   ```

3. Set up environment variables:
   ```bash
   cp notebooks/.env_example notebooks/.env
   ```

   Edit `notebooks/.env` with your z.ai credentials:
   ```
   ZAI_BASE_URL=https://api.z.ai/api/paas/v4
   ZAI_API_KEY=<your-api-key>
   ZAI_MODEL=GLM-4.6V-Flash
   ```

4. Launch Jupyter:
   ```bash
   jupyter labshou
   ```

## Notebook Series

### 1. Simple Agent
Introduction to basic agent architecture with direct prompting and tool use.

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
- **Customer Support**: Query and manage customer orders and refunds
- **Inventory Management**: Track and manage product inventory

These tools are used throughout the notebooks to demonstrate real-world agent applications.

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
