# Security Policy

## Supported Versions

We actively support the following versions of LinguaLint with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

The LinguaLint team takes security seriously. We appreciate your efforts to responsibly disclose your findings, and will make every effort to acknowledge your contributions.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by email to:

**jefferson@richards.plus**

### What to Include

To help us understand the nature and scope of the possible issue, please include as much of the following information as possible:

- **Type of issue** (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
- **Full paths of source file(s)** related to the manifestation of the issue
- **The location of the affected source code** (tag/branch/commit or direct URL)
- **Any special configuration** required to reproduce the issue
- **Step-by-step instructions** to reproduce the issue
- **Proof-of-concept or exploit code** (if possible)
- **Impact of the issue**, including how an attacker might exploit the issue

This information will help us triage your report more quickly.

### Response Timeline

We will acknowledge receipt of your vulnerability report within **48 hours** and will send a more detailed response within **7 days** indicating the next steps in handling your report.

After the initial reply to your report, we will:

- Keep you informed of the progress towards a fix and full announcement
- May ask for additional information or guidance
- Notify you when the issue is fixed

### Disclosure Policy

- We ask that you give us a reasonable amount of time to fix the issue before any disclosure to the public or a third party
- We will credit you in our security advisory (unless you prefer to remain anonymous)
- We will coordinate the timing of the disclosure with you

### Security Update Process

When we receive a security bug report, we will:

1. **Confirm the problem** and determine the affected versions
2. **Audit code** to find any potential similar problems
3. **Prepare fixes** for all releases still under maintenance
4. **Release new versions** as soon as possible
5. **Publish a security advisory** with details about the vulnerability

### Scope

This security policy applies to:

- **Core LinguaLint application** (Python codebase)
- **Web interface** (Node.js server)
- **MCP server implementation**
- **Generated reports and outputs**
- **Dependencies and third-party integrations**

### Security Considerations

#### Data Privacy

LinguaLint processes text data that may contain sensitive information:

- **Local Processing**: All NLP processing happens locally by default
- **Wikipedia API**: Only concept names are sent to Wikipedia for enrichment
- **No Data Storage**: We don't store or transmit your input data to external services
- **Report Generation**: Generated reports are saved locally unless explicitly configured otherwise

#### Network Security

- **HTTPS Only**: All external API calls use HTTPS
- **No Telemetry**: We don't collect usage statistics or telemetry by default
- **Minimal Dependencies**: We minimize external dependencies to reduce attack surface

#### Input Validation

- **Text Sanitization**: All user input is sanitized before processing
- **File Upload Limits**: File size limits are enforced for uploaded documents
- **Path Traversal Protection**: File operations are restricted to designated directories

### Known Security Considerations

#### AGPL License Compliance

- **Source Code Availability**: If you modify LinguaLint and provide it as a network service, you must make your source code available under AGPL-3.0
- **License Compatibility**: Ensure any modifications or integrations comply with AGPL-3.0 requirements

#### Dependencies

We regularly audit our dependencies for known vulnerabilities:

- **Python packages**: Monitored via `pip-audit` and GitHub security advisories
- **Node.js packages**: Monitored via `npm audit` and GitHub security advisories
- **SpaCy models**: We use official SpaCy language models from trusted sources

### Security Best Practices for Users

#### Installation Security

```bash
# Verify package integrity
pip install --require-hashes -r requirements.txt

# Use virtual environments
python3.10 -m venv venv
source venv/bin/activate
```

#### Runtime Security

- **Firewall**: If running the web server, ensure proper firewall configuration
- **Access Control**: Limit access to the web interface to trusted networks
- **Regular Updates**: Keep LinguaLint and its dependencies up to date

#### Data Handling

- **Sensitive Data**: Be cautious when processing confidential documents
- **Report Storage**: Secure generated reports appropriately for your use case
- **Cleanup**: Remove temporary files and reports when no longer needed

### Vulnerability Disclosure Examples

#### What Qualifies as a Security Issue

- **Remote Code Execution**: Ability to execute arbitrary code
- **Path Traversal**: Unauthorized file system access
- **Injection Attacks**: SQL, command, or script injection vulnerabilities
- **Authentication Bypass**: Circumventing security controls
- **Information Disclosure**: Unauthorized access to sensitive data
- **Denial of Service**: Attacks that could crash or overwhelm the system

#### What Does NOT Qualify

- **Feature requests** or **enhancement suggestions**
- **Issues requiring physical access** to the machine
- **Social engineering attacks**
- **Issues in third-party dependencies** (report to the respective maintainers)
- **Theoretical vulnerabilities** without proof of concept

### Contact Information

- **Security Email**: jefferson@richards.plus
- **General Contact**: jefferson@richards.plus
- **Website**: https://lingualint.com

### PGP Key

For sensitive communications, you may encrypt your message using our PGP key:

```
-----BEGIN PGP PUBLIC KEY BLOCK-----
[PGP key will be provided upon request to jefferson@richards.plus]
-----END PGP PUBLIC KEY BLOCK-----
```

### Hall of Fame

We maintain a security hall of fame to recognize researchers who have helped improve LinguaLint's security:

- *Your name could be here!*

### Legal

This security policy is provided in good faith. LinguaLint is provided "as is" under the AGPL-3.0 license. While we make every effort to address security issues promptly, we cannot guarantee the security of the software or accept liability for security vulnerabilities.

---

**Thank you for helping keep LinguaLint and our users safe!**