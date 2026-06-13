# Project 1 – MCP Tool-Using Agent on AWS Using CrewAI

## Overview

This project demonstrates how to build a tool-using AI agent using:

- Amazon EC2
- Python Flask MCP Server
- CrewAI Agent
- Amazon Bedrock
- CSV-based business data

The architecture consists of a CrewAI agent running externally (local machine) that connects to a custom MCP server hosted on AWS EC2. The MCP server exposes tools that allow the agent to read CSV data and compute statistics. The agent then uses Amazon Bedrock to generate a business summary from the tool results.

## Architecture

```text
Local Machine
├── CrewAI Agent
├── Bedrock Client
└── HTTP Requests
        │
        ▼
AWS EC2 Instance
├── Flask MCP Server
├── /mcp/tools
├── /mcp/tools/file_read_csv
├── /mcp/tools/compute_stats
└── CSV Data
```

## Prerequisites

### AWS

- AWS Account
- EC2 Instance
- IAM Role with Bedrock permissions

### Software

- Python 3.10+
- pip
- git

## EC2 Setup

```bash
sudo mkdir -p /opt/data
sudo mkdir -p /opt/mcp-server
```

Copy CSV:

```bash
scp orders_4000_lines.csv ubuntu@<EC2_IP>:/opt/data/
```

Install dependencies:

```bash
python3 -m venv ~/.venv
source ~/.venv/bin/activate
pip install flask pandas requests boto3
```

## Starting the MCP Server

```bash
python server.py
```

Expected:

```text
* Running on http://0.0.0.0:8080
```

## Verify Server

```bash
curl http://<EC2_IP>:8080/mcp/tools
```

Expected:

```json
{
  "tools": [
    {"name":"file_read_csv"},
    {"name":"compute_stats"}
  ]
}
```

## Local CrewAI Setup

```bash
pip install crewai crewai-tools boto3 requests
```

Configure AWS credentials:

```bash
aws configure
aws sts get-caller-identity
```

## Project Structure

```text
project/
├── agent.py
├── mcp_tools.py
├── requirements.txt
└── README.md
```

## Example MCP Calls

### Read CSV

Request:

```json
{
  "sample": 5
}
```

Response:

```json
{
  "columns": ["order_id","customer","order_total"],
  "preview": [
    {
      "order_id":"1",
      "customer":"Alice",
      "order_total":"120.50"
    }
  ]
}
```

### Compute Statistics

Request:

```json
{
  "rows":[
    {"order_total":"120.50"},
    {"order_total":"95.20"}
  ],
  "column":"order_total"
}
```

Response:

```json
{
  "column":"order_total",
  "count":2,
  "sum":215.7,
  "mean":107.85
}
```

## Running the Agent

```bash
python agent.py
```

Expected output:

```text
Crew Started
Running Task

Thought: Read CSV data
Action: file_read_csv

Observation: 100 rows returned

Final Answer:
Average order value is $125.42.
Revenue appears stable.
```

## Sample Data

```csv
order_id,customer,order_total
1,Alice,120.50
2,Bob,95.20
3,Charlie,210.75
4,David,155.00
5,Eve,80.25
```

## Troubleshooting

### Connection Refused

```text
curl: (7) Failed to connect
```

Check:

```bash
sudo systemctl status mcp-server
```

### Connection Timed Out

```text
curl: (28) Operation timed out
```

Check:

```bash
sudo ss -tulpn | grep 8080
```

Expected:

```text
LISTEN 0 128 0.0.0.0:8080
```

### Bedrock AccessDenied

Verify:

- IAM role attached
- Model access granted
- Correct region configured

### OPENAI_API_KEY Missing

CrewAI defaulted to OpenAI.

Explicitly configure Bedrock:

```python
llm = LLM(
    model="bedrock/anthropic.claude-3-haiku-20240307-v1:0",
    region_name="us-east-1"
)
```

### Pydantic args_schema Error

Remove args_schema or add proper type annotations.

## Success Criteria

- MCP server reachable from outside AWS
- CrewAI calls MCP endpoints successfully
- CSV data returned correctly
- Statistics computed successfully
- Bedrock generates final summary
- Final answer displayed to user
