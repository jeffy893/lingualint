# Frequently Asked Questions (FAQ)

## License & Legal Questions

### Q: Can I use LinguaLint in my commercial product?

**A: Yes!** You can use LinguaLint commercially under AGPL-3.0, but with conditions:

- ✅ **Internal use**: Use LinguaLint within your company for analysis, reports, etc.
- ✅ **Desktop applications**: Distribute LinguaLint as part of desktop software
- ✅ **Open source SaaS**: Run LinguaLint as a web service if you share your source code
- ❌ **Proprietary SaaS**: Cannot run as a closed-source web service without commercial license

**Need proprietary licensing?** Contact licensing@lingualint.com

### Q: What does "network service" mean in AGPL?

**A: Web services, APIs, or cloud applications.** If users interact with LinguaLint through a network (web browser, API calls, etc.), you must provide your source code under AGPL-3.0.

**Examples:**
- ✅ **OK**: Using LinguaLint to analyze your company's 10-K filings internally
- ✅ **OK**: Distributing LinguaLint as part of an open-source desktop app
- ❌ **Requires commercial license**: Running LinguaLint as a proprietary web service

### Q: Can I modify LinguaLint without sharing my changes?

**A: Depends on how you use it:**

- ✅ **Internal modifications**: Keep private if only used within your organization
- ❌ **Distributed modifications**: Must share if you distribute the software
- ❌ **Network service modifications**: Must share if you run it as a web service

### Q: Is AGPL compatible with my MIT/BSD project?

**A: No, not directly.** AGPL is a copyleft license that's incompatible with permissive licenses like MIT/BSD. You would need:

1. **Separate the components**: Keep LinguaLint as a separate service/process
2. **Commercial license**: Get a proprietary license for integration
3. **Dual licensing**: We offer commercial licenses for this use case

### Q: What's the difference between GPL and AGPL?

**A: Network services.**

- **GPL**: Only requires source sharing when you distribute the software
- **AGPL**: Also requires source sharing when you run it as a network service

AGPL closes the "SaaS loophole" where companies could use GPL software in web services without sharing improvements.

## Technical Questions

### Q: What are the system requirements?

**Minimum:**
- Python 3.10+
- 4GB RAM
- 2GB disk space
- Internet connection (for Wikipedia enrichment)

**Recommended:**
- Python 3.10+
- 8GB RAM
- 5GB disk space
- SSD storage for better performance

### Q: Can I run LinguaLint offline?

**A: Mostly yes.** Core NLP processing works offline, but:

- ✅ **Text analysis**: Works completely offline
- ✅ **Report generation**: Works offline
- ❌ **Wikipedia enrichment**: Requires internet connection
- ❌ **Package installation**: Requires internet for initial setup

### Q: What file formats does LinguaLint support?

**Input:**
- Plain text (`.txt`)
- JSON files
- Direct text input via web interface or CLI

**Output:**
- JSON (structured data)
- HTML (interactive reports)
- PNG (visualizations)
- PDF (comprehensive reports)
- CSV (project plans)

### Q: How accurate is the NLP analysis?

**A: Depends on the content type:**

- **Financial documents**: Optimized for 10-K filings, SEC reports
- **News articles**: Good performance on structured news content
- **General text**: Reasonable performance, but may need tuning
- **Technical documents**: May require domain-specific customization

**Accuracy factors:**
- Text quality and structure
- Domain-specific terminology
- Language complexity
- Document length

### Q: Can I customize the analysis for my domain?

**A: Yes, several ways:**

1. **Semantic Primes**: Extend Wierzbicka's 65 primes for your domain
2. **Custom Models**: Train SpaCy models on your data
3. **Wikipedia Sources**: Use domain-specific knowledge bases
4. **Vector Weights**: Adjust warm/cold vector calculations
5. **Custom Reports**: Modify HTML/PDF templates

## Usage Questions

### Q: How do I get started quickly?

**A: Three options:**

1. **Web Interface** (easiest):
   ```bash
   node web-server.js
   # Open http://localhost:3001
   ```

2. **Command Line**:
   ```bash
   python3.10 run.py "Your text here"
   ```

3. **MCP Server** (for AI assistants):
   ```bash
   python3.10 server.py
   ```

### Q: What's the difference between the interfaces?

- **Web Interface**: User-friendly, good for occasional use
- **Command Line**: Scriptable, good for batch processing
- **MCP Server**: Integration with AI assistants like Claude
- **Python API**: Direct integration into other Python applications

### Q: How do I process multiple documents?

**A: Batch processing:**

```bash
# Process multiple files
for file in *.txt; do
    python3.10 run.py --file "$file"
done

# Or use Python API
from src.nlp_processor import ModernNLPProcessor
processor = ModernNLPProcessor()

for filename in file_list:
    with open(filename, 'r') as f:
        result = processor.process_text(f.read())
```

### Q: Can I integrate LinguaLint with my existing system?

**A: Yes, several integration options:**

1. **REST API**: Run the web server and make HTTP requests
2. **Python Library**: Import and use directly in Python code
3. **Command Line**: Call via subprocess from any language
4. **MCP Protocol**: Integrate with AI assistants and tools
5. **File Processing**: Process files and read JSON outputs

## Performance Questions

### Q: How fast is LinguaLint?

**A: Typical performance:**

- **Short text** (< 1KB): < 1 second
- **Medium document** (10KB): 2-5 seconds
- **Large document** (100KB): 10-30 seconds
- **Very large** (1MB+): 1-5 minutes

**Performance factors:**
- Text length and complexity
- Wikipedia enrichment (adds network latency)
- Hardware specifications
- Python/SpaCy model size

### Q: How can I improve performance?

**A: Several optimizations:**

1. **Disable Wikipedia enrichment** for faster processing
2. **Use SSD storage** for better I/O performance
3. **Increase RAM** for larger documents
4. **Batch processing** for multiple documents
5. **Custom SpaCy models** (smaller = faster)

### Q: Can I run LinguaLint in production?

**A: Yes, with considerations:**

- **Scaling**: Single-threaded by default, use multiple processes
- **Memory**: Monitor memory usage for large documents
- **Caching**: Cache Wikipedia results for repeated concepts
- **Error handling**: Implement proper error handling and logging
- **Monitoring**: Monitor performance and resource usage

## Support Questions

### Q: How do I report bugs or request features?

**A: GitHub Issues:**

1. **Search existing issues** first
2. **Use issue templates** for bugs and features
3. **Provide detailed information** (version, OS, steps to reproduce)
4. **Include sample data** if possible (anonymized)

### Q: How do I get help with implementation?

**A: Multiple channels:**

- **GitHub Discussions**: Community Q&A
- **Documentation**: Check `/docs/` directory
- **Examples**: See `/examples/` directory
- **Code**: Read the source code (it's open!)
- **Email**: hello@lingualint.com for general questions

### Q: Do you offer commercial support?

**A: Yes!** We offer:

- **Commercial licenses** for proprietary use
- **Professional support** contracts
- **Custom development** services
- **Training and consulting**

Contact **support@lingualint.com** for enterprise options.

### Q: How do I contribute to LinguaLint?

**A: We welcome contributions!**

1. **Read** [CONTRIBUTING.md](../CONTRIBUTING.md)
2. **Follow** [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md)
3. **Fork** the repository
4. **Create** a feature branch
5. **Submit** a pull request

**Types of contributions:**
- Bug fixes and improvements
- New features and enhancements
- Documentation and examples
- Tests and quality assurance
- Translations and localization

---

**Still have questions?** 

- 📧 **Email**: hello@lingualint.com
- 💬 **Discussions**: [GitHub Discussions](https://github.com/jeffy893/lingualint/discussions)
- 🐛 **Issues**: [GitHub Issues](https://github.com/jeffy893/lingualint/issues)
- 🌐 **Website**: [lingualint.com](https://lingualint.com)