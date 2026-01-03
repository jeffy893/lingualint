# Contributing to LinguaLint

Thank you for your interest in contributing to LinguaLint! We welcome contributions from developers of all skill levels. This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Making Changes](#making-changes)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Ways to Contribute

- **Bug Reports**: Found a bug? Please create an issue with detailed reproduction steps
- **Feature Requests**: Have an idea? Open an issue to discuss it first
- **Code Contributions**: Fix bugs, add features, or improve performance
- **Documentation**: Help improve our docs, examples, or tutorials
- **Testing**: Add test coverage or improve existing tests
- **Translations**: Help make LinguaLint available in more languages

### Before You Start

1. Check existing [issues](https://github.com/jeffy893/lingualint/issues) to avoid duplicates
2. For major changes, open an issue first to discuss the approach
3. Fork the repository and create a feature branch

## Development Environment Setup

### Prerequisites

- **Python 3.10+** (required for core functionality)
- **Node.js 16+** (for web interface)
- **Git** (for version control)
- **Internet connection** (for Wikipedia enrichment)

### Installation Steps

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/lingualint.git
   cd lingualint
   ```

2. **Set Up Python Environment**
   ```bash
   # Create virtual environment
   python3.10 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Install SpaCy model
   python3.10 -m spacy download en_core_web_sm
   ```

3. **Set Up Node.js Dependencies**
   ```bash
   npm install
   ```

4. **Verify Installation**
   ```bash
   # Test Python components
   python3.10 -m pytest tests/
   
   # Test web server
   node web-server.js
   # Should start on http://localhost:3001
   ```

### Development Tools

We recommend these tools for development:

- **IDE**: VS Code with Python and JavaScript extensions
- **Linting**: `flake8` for Python, `eslint` for JavaScript
- **Formatting**: `black` for Python, `prettier` for JavaScript
- **Testing**: `pytest` for Python tests

## Making Changes

### Branch Naming Convention

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `test/description` - Test improvements

### Development Workflow

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Follow our [coding standards](#coding-standards)
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   # Run all tests
   python3.10 -m pytest tests/ -v
   
   # Test specific functionality
   python3.10 run.py "Test input text"
   
   # Test web interface
   node web-server.js
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions or modifications
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `chore:` - Maintenance tasks

## Submitting a Pull Request

1. **Push Your Branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Go to the GitHub repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template

3. **PR Requirements**
   - [ ] Clear description of changes
   - [ ] Tests pass (`pytest tests/`)
   - [ ] Documentation updated (if applicable)
   - [ ] No merge conflicts
   - [ ] Follows coding standards

### PR Review Process

1. **Automated Checks**: CI/CD will run tests and linting
2. **Code Review**: Maintainers will review your code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, your PR will be merged

## Coding Standards

### Python Code Style

- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type annotations where possible
- **Docstrings**: Document all public functions and classes
- **Line Length**: Maximum 88 characters (Black formatter default)

```python
def process_text(text: str, enrich_wikipedia: bool = True) -> Dict[str, Any]:
    """
    Process natural language text for risk factor extraction.
    
    Args:
        text: Input text to process
        enrich_wikipedia: Whether to enrich with Wikipedia data
        
    Returns:
        Dictionary containing extracted subjects, phenomena, and analysis
    """
    # Implementation here
    pass
```

### JavaScript Code Style

- **ES6+**: Use modern JavaScript features
- **Semicolons**: Always use semicolons
- **Camel Case**: Use camelCase for variables and functions
- **Constants**: Use UPPER_CASE for constants

### File Organization

- **Source Code**: `/src/` directory
- **Tests**: `/tests/` directory
- **Documentation**: `/docs/` directory
- **Examples**: `/examples/` directory

## Testing

### Test Structure

```
tests/
├── test_nlp_processor.py      # Core NLP functionality
├── test_responsibility.py     # Responsibility analysis
├── test_report_generator.py   # Report generation
└── fixtures/                  # Test data
    └── sample_data.json
```

### Writing Tests

```python
import pytest
from src.nlp_processor import ModernNLPProcessor

def test_subject_extraction():
    """Test that subjects are correctly extracted from text."""
    processor = ModernNLPProcessor()
    text = "The COVID-19 pandemic has affected business operations."
    
    result = processor.process_text(text)
    subjects = result['_source']['subjects']
    
    assert 'COVID-19 pandemic' in subjects
    assert 'business operations' in subjects
```

### Running Tests

```bash
# Run all tests
python3.10 -m pytest tests/

# Run with coverage
python3.10 -m pytest tests/ --cov=src

# Run specific test file
python3.10 -m pytest tests/test_nlp_processor.py -v
```

## Documentation

### Documentation Standards

- **README**: Keep the main README up-to-date
- **Docstrings**: Document all public APIs
- **Examples**: Provide working code examples
- **Changelog**: Update CHANGELOG.md for significant changes

### Building Documentation

```bash
# Generate API documentation
python3.10 -m pydoc -w src/

# Serve documentation locally
python3.10 -m http.server 8000 -d docs/
```

## Community

### Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: jefferson@richards.plus for security issues

### Communication Guidelines

- Be respectful and inclusive
- Provide clear, detailed information
- Search existing issues before creating new ones
- Use appropriate labels and templates

### Recognition

Contributors are recognized in:
- **CONTRIBUTORS.md**: All contributors listed
- **Release Notes**: Major contributions highlighted
- **GitHub**: Contributor statistics and badges

## License

By contributing to LinguaLint, you agree that your contributions will be licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See our [README.md](README.md#license) for more information about why we chose this license.

## Questions?

If you have questions about contributing, please:

1. Check this guide and our [FAQ](docs/FAQ.md)
2. Search existing [GitHub Issues](https://github.com/jeffy893/lingualint/issues)
3. Create a new issue with the "question" label
4. Join our community discussions

Thank you for contributing to LinguaLint! 🚀