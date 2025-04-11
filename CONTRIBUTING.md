# Contributing to Gas Tracker

Thank you for your interest in contributing to Gas Tracker! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and considerate of others.

## How Can I Contribute?

### Reporting Bugs
- Use the bug report template
- Provide detailed steps to reproduce
- Include screenshots if applicable
- Describe the expected behavior

### Suggesting Enhancements
- Use the feature request template
- Explain why this enhancement would be useful
- Provide examples of how it would work

### Pull Requests
1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Run tests and ensure they pass
5. Submit a pull request

## Development Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL
- Git

### Setting Up the Development Environment

1. Fork and clone the repository
2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

4. Create a `.env` file with the necessary environment variables

### Running Tests

Backend tests:
```bash
cd backend
pytest
```

Frontend tests:
```bash
cd frontend
npm test
```

## Coding Standards

### Python
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all functions and classes
- Keep functions small and focused

### JavaScript/TypeScript
- Follow ESLint rules
- Use TypeScript for type safety
- Write meaningful comments
- Follow React best practices

## Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally

## Documentation
- Update documentation for any changes
- Include examples for new features
- Keep the README up to date

## Questions?
If you have any questions, feel free to open an issue or contact the maintainers. 