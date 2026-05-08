# Compliance-Aware Multi-Agent System

A robust, intelligent multi-agent system designed to process queries, reason through complex data with chain-of-thought capabilities, and ensure strict compliance with data regulations like HIPAA and GDPR.

## Features

- **Multi-Agent Architecture**: Leverages specialized agents for distinct tasks:
  - **Retrieval Agent**: Efficiently fetches and aggregates data based on user queries.
  - **Reasoning Agent**: Analyzes data using chain-of-thought reasoning to generate hypotheses and insights.
  - **Compliance Agent**: Validates processed data against strict regulatory frameworks (e.g., HIPAA, GDPR).
- **Persistent Memory System**: Tracks historical query success rates, learns from past interactions, and monitors agent performance to continuously improve efficiency.
- **Interactive CLI**: Engage with the system through an interactive terminal interface.
- **Comprehensive Analytics**: Generate system health scores, compliance rates, and processing metrics.
- **Batch Processing**: Support for handling multiple queries asynchronously and evaluating efficiency scores.

## Prerequisites

Ensure you have Python 3.8+ installed. The project relies on the following key dependencies:
- `requests`
- `python-dateutil`
- `pytest` & `pytest-cov` (for testing)
- `psutil`

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd project
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The primary entry point for the application is `run_system.py`. You can run the system in several different modes:

### Interactive Mode
Launch an interactive chat session to query the multi-agent system in real-time.
```bash
python run_system.py interactive
```

### Examples
Run a predefined set of example queries to see the system's reasoning and compliance checking in action.
```bash
python run_system.py examples
```

### Demo
Execute a comprehensive demonstration of the system's full capabilities, including learning insights and memory persistence.
```bash
python run_system.py demo
```

## Testing

To run the test suite and check code coverage, ensure you have installed the testing dependencies (`pytest`, `pytest-cov`), then run:

```bash
pytest tests/ -v
```

## Architecture Summary

1. **Query Input**: The user provides a query string.
2. **Retrieval**: The Retrieval Agent fetches relevant data.
3. **Reasoning**: The Reasoning Agent formulates insights using chain-of-thought analysis.
4. **Compliance Check**: The Compliance Agent ensures no regulatory violations exist in the insights or retrieved data.
5. **Memory Logging**: The Memory System logs the interaction, learns from patterns, and updates system analytics.
6. **Result Delivery**: A structured response, complete with performance metrics and compliance status, is returned to the user.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

Modified and extended by Muhammad Abdullah.
