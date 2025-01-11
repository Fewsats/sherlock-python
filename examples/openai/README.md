# OpenAI agent for Sherlock Domains API

This agent uses OpenAI's GPT models to provide a natural language interface for managing your domain and DNS records through the Sherlock Domains API.

## Prerequisites

- Python 3.8 or higher
- An OpenAI API key
- (Optional) A Sherlock agent private key for authenticated operations

## Installation

1. Install the agent dependencies:

```bash
pip install -r requirements.txt
```

2. Set up your environment variables:

```bash
export OPENAI_API_KEY=your_api_key
export SHERLOCK_AGENT_PRIVATE_KEY_HEX=your_private_key  # Optional for authenticated calls
export MODEL=gpt-4  # Optional, defaults to gpt-4-mini
```

## Usage

1. Start the agent:

```bash
python main.py
```

2. Interact with the agent using natural language. Example commands:

- Search for available domains: "Is example.com available?"
- Purchase domains: "I want to buy example.com"
- List your domains: "Show me my domains"
- Manage DNS: "Add an A record for example.com pointing to 1.2.3.4"

For multiline input (like bulk operations), wrap your text with triple quotes:
```
"""
Check if these domains are available:
example.com
example.net
example.org
"""
```

## Features

- Domain availability checking
- Domain registration
- DNS management
- Domain portfolio viewing
- Auto-renewal management

## Troubleshooting

If you encounter authentication issues, ensure your API keys are correctly set in the environment variables.

For support, please open an issue in the repository.
