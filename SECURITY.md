# Security Policy

## Supported versions

Security fixes are applied to the `main` branch. Older commits and unpublished development branches may not receive security updates.

## Reporting a vulnerability

Please do not open a public issue for a suspected vulnerability. Instead, contact the repository owner through the contact information on the [Bosaj GitHub profile](https://github.com/Bosaj) and include a concise description, affected files or endpoints, reproduction steps, and the potential impact.

Allow reasonable time for investigation before publicly disclosing the issue. Do not include API keys, database credentials, private documents, or other sensitive data in an issue, pull request, log, or reproduction.

## Secret handling

Copy the environment template to a local `.env` file and keep credentials outside version control. If a secret is accidentally committed or exposed, revoke it immediately, remove it from active configuration, and rotate any related credentials. Removing a secret from the latest commit does not make an already exposed credential safe.
