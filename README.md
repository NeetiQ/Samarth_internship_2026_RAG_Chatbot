# Legal RAG

Retrieval Augmented Generation system for legal document processing and analysis.
- Utility functions
- Data models
- Constants

## Tech Stack

- **Backend**: Python (FastAPI)
- **Frontend**: React/Next.js
- **Vector DB**: [Configured in vectordb/]
- **LLM**: [Configured in llm/]
- **Embeddings**: [Configured in embeddings/]
- **Deployment**: Docker, Docker Compose

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 14+
- Docker & Docker Compose

### Installation

1. Clone the repository
2. Copy environment variables:
   ```bash
   cp .env.example .env
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   npm install  # for frontend
   ```

4. Start services:
   ```bash
   docker-compose up
   ```

## Project Structure

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## Documentation

- [Architecture Overview](docs/architecture.md)
- [API Contracts](docs/api-contracts.md)
- [Team Deliverables](docs/team-deliverables.md)
- [Deployment Guide](docs/deployment.md)
- [Data Sources](docs/data-sources.md)
- [Testing Checklist](docs/testing-checklist.md)
- [Daily MoM](docs/daily-mom/) - Daily minutes of meeting

## Development

### Running Tests
```bash
pytest backend/app/tests
pytest ingestion/tests
pytest retrieval/tests
pytest rag_chat/tests
```

### Code Style
- Python: Black, isort, flake8
- JavaScript: ESLint, Prettier

## Contributing

1. Create a feature branch
2. Make changes in your team's module
3. Add tests
4. Submit PR with documentation

## Team Assignments

| Team | Module      | Responsibility      |
| ---- | ----------- | ------------------- |
| A    | ingestion/  | Document processing |
| B    | retrieval/  | Search & retrieval  |
| C    | rag_chat/   | Conversation & LLM  |
| D    | frontend/   | User interface      |
| E    | deployment/ | DevOps & deployment |

## Support

For issues and questions, check the daily MoM or contact the relevant team.
