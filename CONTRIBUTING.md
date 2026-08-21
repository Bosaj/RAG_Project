# Contributing to RAG Project

Thank you for your interest in contributing to **RAG Project**! We welcome contributions that improve reliability, performance, developer experience, and document-processing capabilities.

---

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Coding Standards](#coding-standards)
- [Security Disclosures](#security-disclosures)

---

## 📜 Code of Conduct
All contributors are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before participating.

---

## 🚀 Getting Started
1. **Fork** the repository and clone it to your local environment.
2. Create a new topic branch from \main\ (e.g., \eature/vector-search-filter\ or \ix/pdf-encoding\).

---

## 💻 Development Setup

The application runs from the \src\ directory where environment configurations are loaded.

\\\ash
# 1. Navigate to src
cd src

# 2. Set up a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pytest

# 4. Configure local environment
cp .env.exemple .env
\\\

---

## 🧪 Running Tests

Ensure all unit tests pass before opening a Pull Request:

\\\ash
# Run tests from the repository root
PYTHONPATH=src pytest -v
\\\

---

## 🔄 Submitting a Pull Request

1. Ensure code is formatted and clean of any hardcoded credentials or debug prints.
2. Add unit tests for new features or bug fixes under the \	ests/\ directory.
3. Open a Pull Request against the \main\ branch with a clear title and description of changes.
4. Verify that all automated GitHub Actions CI tests pass.

---

## 🔒 Security Disclosures
If you discover a potential security vulnerability, please follow our [Security Policy](SECURITY.md) to report it privately.
