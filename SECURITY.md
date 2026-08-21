# Security Policy

## 🛡️ Supported Versions

We actively maintain and release security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| `v1.x`  | :white_check_mark: |
| `< 1.0` | :x:                |

---

## 🚨 Reporting a Vulnerability

The security of **RAG Project** is a top priority. If you discover a vulnerability or potential security risk:

1. **Do NOT open a public issue** on GitHub.
2. Report the vulnerability privately using **[GitHub Security Advisory](https://github.com/Bosaj/RAG_Project/security/advisories/new)** or by reaching out to the maintainer via the [Bosaj GitHub Profile](https://github.com/Bosaj).
3. Provide a detailed summary including:
   - Affected endpoints or files
   - Step-by-step reproduction instructions
   - Potential security impact

We will acknowledge receipt within 48 hours and work with you to remediate and publish a patch.

---

## 🔑 Credential & Secret Hygiene

- Never commit `.env` files, API keys, or database credentials into Git.
- Always use `.env.exemple` as the template for local configurations.
- Ensure automated secret scanning remains enabled in GitHub settings.
