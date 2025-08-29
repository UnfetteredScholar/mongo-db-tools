# MongoDB Tools

A FastAPI-based service that provides MongoDB database management tools through a REST API and Model Context Protocol (MCP) integration. This service allows you to perform common MongoDB operations like listing databases, collections, and performing CRUD operations on documents.

## Features

- **Database Management**: List databases and collections
- **Document Operations**: Insert, find, update, and delete documents
- **REST API**: Full REST API with FastAPI
- **MCP Integration**: Model Context Protocol support for AI agent integration
- **Authentication**: Subscription-based access control
- **Platform Integration**: Connects to external platform services
- **Docker Support**: Containerized deployment with Docker Compose

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (for containerized deployment)
- MongoDB instance
- Platform integration credentials

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd mongo-db-tools
```

2. Create a `.env` file with your configuration:
```env
PLATFRORM_INT_URL=your_platform_integration_url
QUEST_AI_SECRET_KEY=your_quest_ai_secret_key
PUBLIC_KEY_B64=your_public_key_base64
MARKETPLACE_URL=your_marketplace_url
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The service will be available at `http://localhost:8100`

### Local Development

1. Install dependencies using uv:
```bash
cd app
uv sync
```

2. Set up environment variables (see `.env` file above)

3. Run the application:
```bash
uv run fastapi run main.py --host 0.0.0.0 --port 8000
```

## API Endpoints

### Database Operations

- `GET /api/v1/databases` - List all databases
- `GET /api/v1/databases/{db_name}/collections` - List collections in a database

### Document Operations

- `POST /api/v1/databases/{db_name}/collections/{collection_name}/documents/insert` - Insert documents
- `POST /api/v1/databases/{db_name}/collections/{collection_name}/documents/find` - Find documents
- `POST /api/v1/databases/{db_name}/collections/{collection_name}/documents/update` - Update documents
- `POST /api/v1/databases/{db_name}/collections/{collection_name}/documents/delete` - Delete documents

### MCP Integration

- `POST /streamable-http/mcp` - Model Context Protocol endpoint

## Configuration

The service uses the following environment variables:

- `PLATFRORM_INT_URL`: URL for platform integration service
- `QUEST_AI_SECRET_KEY`: Secret key for Quest AI integration
- `PUBLIC_KEY_B64`: Base64 encoded public key
- `MARKETPLACE_URL`: URL for the marketplace service
- `SERVICE_TIER`: Service tier level (default: BASIC)

## Project Structure

```
mongo-db-tools/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── routers/
│   │           └── database.py      # Database operation endpoints
│   ├── core/
│   │   ├── authentication/          # Authentication logic
│   │   ├── config.py               # Configuration settings
│   │   └── platfom_integration_client.py  # Platform integration
│   ├── schemas/                    # Pydantic data models
│   ├── main.py                     # FastAPI application entry point
│   ├── pyproject.toml             # Python project configuration
│   └── uv.lock                    # Dependency lock file
├── compose.yaml                    # Docker Compose configuration
├── Dockerfile                      # Docker image definition
└── logs/                          # Application logs
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **PyMongo**: MongoDB driver for Python
- **Pydantic**: Data validation using Python type annotations
- **FastAPI-MCP**: Model Context Protocol integration
- **uv**: Fast Python package installer and resolver

## Logging

The service includes comprehensive logging with:
- Console output for development
- File-based logging with daily rotation
- Detailed debug logs for troubleshooting
- Log files stored in the `logs/` directory

## Development

### Adding New Endpoints

1. Create new router files in `app/api/v1/routers/`
2. Define your endpoints using FastAPI decorators
3. Include the router in `main.py`

### Testing

The service can be tested using:
- FastAPI's automatic interactive documentation at `/docs`
- HTTP clients like curl, Postman, or Insomnia
- MCP clients for protocol-specific testing

## Deployment

### Production Considerations

- Set appropriate environment variables for production
- Configure proper CORS settings
- Set up monitoring and health checks
- Use production-grade MongoDB instances
- Implement proper security measures

### Scaling

The service can be scaled horizontally by:
- Running multiple container instances
- Using a load balancer
- Implementing connection pooling for MongoDB

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the logs for troubleshooting information
