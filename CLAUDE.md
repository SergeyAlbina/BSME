# CLAUDE.md - AI Assistant Guide for BSME

**Last Updated:** 2025-12-17
**Repository:** SergeyAlbina/BSME
**Current Branch:** claude/claude-md-mj9xjd9humapt0g1-5ULu8

## Table of Contents
1. [Repository Overview](#repository-overview)
2. [Current State](#current-state)
3. [Project Structure](#project-structure)
4. [Development Workflow](#development-workflow)
5. [Coding Conventions](#coding-conventions)
6. [Git Practices](#git-practices)
7. [Testing Guidelines](#testing-guidelines)
8. [Documentation Standards](#documentation-standards)
9. [AI Assistant Guidelines](#ai-assistant-guidelines)

---

## Repository Overview

**Repository Name:** BSME
**Owner:** SergeyAlbina
**Type:** Fresh repository (minimal state)

### Purpose
This repository is currently in its initial stage. The purpose and technology stack will be defined as development progresses.

### Key Information
- **Initial Commit:** e959050
- **Main Branch:** TBD (to be determined)
- **Feature Branches:** Follow pattern `claude/claude-md-*` for AI-assisted development

---

## Current State

### Files Present
```
/home/user/BSME/
├── .git/           # Git repository data
├── README.md       # Basic project README (6 bytes)
└── CLAUDE.md       # This file
```

### Repository Status
- **Status:** Clean working directory
- **Branch:** claude/claude-md-mj9xjd9humapt0g1-5ULu8
- **Commits:** 1 (Initial commit)
- **Remote:** http://local_proxy@127.0.0.1:61337/git/SergeyAlbina/BSME

---

## Project Structure

### Recommended Structure (To Be Implemented)

When the project grows, consider organizing it as follows:

```
BSME/
├── docs/              # Documentation files
│   ├── api/          # API documentation
│   ├── guides/       # User/developer guides
│   └── architecture/ # Architecture diagrams and decisions
├── src/              # Source code
│   ├── main/        # Main application code
│   ├── utils/       # Utility functions
│   └── config/      # Configuration files
├── tests/            # Test files
│   ├── unit/        # Unit tests
│   ├── integration/ # Integration tests
│   └── e2e/         # End-to-end tests
├── scripts/          # Build and automation scripts
├── assets/           # Static assets (images, fonts, etc.)
├── .github/          # GitHub workflows and templates
├── .gitignore       # Git ignore patterns
├── README.md        # Project overview and quick start
├── CLAUDE.md        # This file (AI assistant guide)
├── CONTRIBUTING.md  # Contribution guidelines
├── LICENSE          # Project license
└── [config files]   # package.json, requirements.txt, etc.
```

---

## Development Workflow

### Branch Strategy

1. **Feature Branches**: All development work happens on feature branches
   - AI-assisted branches: `claude/claude-md-*`
   - Human-created branches: Follow agreed naming convention

2. **Branch Lifecycle**:
   ```bash
   # Create/checkout feature branch
   git checkout -b claude/claude-md-feature-name

   # Make changes and commit
   git add .
   git commit -m "Clear, descriptive message"

   # Push to remote
   git push -u origin claude/claude-md-feature-name
   ```

3. **Pull Requests**: Always create PRs for review before merging

### Network Resilience

For git operations (push/pull/fetch), implement retry logic with exponential backoff:
- Retry up to 4 times on network failures
- Wait times: 2s, 4s, 8s, 16s between retries

---

## Coding Conventions

### General Principles

1. **KISS (Keep It Simple, Stupid)**
   - Write simple, readable code
   - Avoid over-engineering
   - Don't add features that weren't requested

2. **YAGNI (You Aren't Gonna Need It)**
   - Don't build for hypothetical future requirements
   - Three similar lines are better than premature abstraction

3. **Code Quality**
   - Follow language-specific style guides
   - Use meaningful variable and function names
   - Keep functions small and focused (single responsibility)

### Security Guidelines

**CRITICAL:** Always check for common vulnerabilities:
- SQL Injection
- Cross-Site Scripting (XSS)
- Command Injection
- Path Traversal
- Authentication/Authorization issues
- Sensitive data exposure
- Insecure deserialization
- XML External Entities (XXE)
- Security misconfiguration
- Using components with known vulnerabilities

### Error Handling

- Only add error handling at system boundaries (user input, external APIs)
- Trust internal code and framework guarantees
- Don't validate for scenarios that can't happen
- Fail fast and provide clear error messages

### Comments and Documentation

- Only add comments where logic isn't self-evident
- Don't comment on code you didn't change
- Prefer self-documenting code over comments
- Update comments when changing code

---

## Git Practices

### Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(auth): add user authentication with JWT

Implement JWT-based authentication system with login and logout functionality.
Includes token refresh mechanism.

fix(api): resolve null pointer exception in user endpoint

The getUserById function wasn't checking for null before accessing properties.
Added null check and appropriate error response.
```

### Commit Frequency

- Commit logical units of work
- Don't commit broken code
- Each commit should build/run successfully
- Use feature branches for work in progress

### Pre-commit Checks

Before committing:
1. Run linters/formatters
2. Run relevant tests
3. Verify no sensitive data (API keys, passwords, etc.)
4. Check for debugging code (console.log, print statements, etc.)

---

## Testing Guidelines

### Test Structure (When Implemented)

```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Tests across modules
└── e2e/           # Full system tests
```

### Testing Best Practices

1. **Write Tests First (TDD) When Appropriate**
   - Define expected behavior
   - Write failing test
   - Implement minimal code to pass
   - Refactor

2. **Test Coverage**
   - Aim for high coverage of critical paths
   - Don't obsess over 100% coverage
   - Focus on testing behavior, not implementation

3. **Test Naming**
   - Use descriptive names that explain what's being tested
   - Format: `test_<function>_<scenario>_<expected_result>`
   - Example: `test_user_login_with_invalid_password_returns_error`

4. **Test Independence**
   - Tests should not depend on each other
   - Use setup/teardown for test isolation
   - Avoid shared mutable state

---

## Documentation Standards

### README.md Requirements

Essential sections:
1. **Project Title and Description**
2. **Installation Instructions**
3. **Usage Examples**
4. **Configuration**
5. **API Documentation** (if applicable)
6. **Contributing Guidelines**
7. **License Information**
8. **Contact/Support Information**

### Code Documentation

1. **Public APIs**: Document all public interfaces
2. **Complex Logic**: Explain why, not what
3. **Examples**: Provide usage examples for non-obvious code
4. **Deprecations**: Document deprecated code with migration path

### Architecture Documentation

When the project grows, document:
- System architecture diagrams
- Data flow diagrams
- Technology stack decisions
- Third-party dependencies and why they were chosen

---

## AI Assistant Guidelines

### Before Making Changes

1. **Read First**: NEVER propose changes to code you haven't read
2. **Understand Context**: Explore related files and dependencies
3. **Verify Existing Patterns**: Follow established code patterns
4. **Check Tests**: Run existing tests before making changes

### Task Planning

Use TodoWrite tool for tasks with 3+ steps:
```markdown
1. Task description in imperative form
   - Status: pending/in_progress/completed
   - Active form: "Doing the task"
```

**When to use TodoWrite:**
- Complex multi-step tasks
- Multiple user requests
- Non-trivial implementations
- After receiving new instructions

**When NOT to use TodoWrite:**
- Single straightforward tasks
- Trivial operations (< 3 steps)
- Purely conversational requests

### Making Changes

1. **Minimal Changes**: Only change what's necessary
2. **No Over-engineering**: Don't refactor unless requested
3. **Security First**: Always check for vulnerabilities
4. **Test Changes**: Verify changes work as expected
5. **Clean Up**: Remove debugging code before committing

### Tool Usage Preferences

1. **File Operations**:
   - Use `Read` instead of `cat`
   - Use `Edit` instead of `sed/awk`
   - Use `Write` instead of `echo >>`

2. **Searching**:
   - Use `Glob` for finding files by pattern
   - Use `Grep` for searching file contents
   - Use `Task` with `Explore` agent for open-ended searches

3. **Parallel Operations**:
   - Run independent commands in parallel
   - Use sequential execution only for dependent operations

### Communication Style

- Be concise and direct
- Use markdown for formatting
- Don't use emojis unless requested
- Focus on facts over validation
- Provide objective technical guidance

### File References

When referencing code, use format: `file_path:line_number`

Example: "The error occurs in src/main.js:42"

---

## Project-Specific Notes

### Technology Stack (To Be Determined)

As the project develops, document:
- Programming language(s)
- Frameworks and libraries
- Database system(s)
- Deployment platform
- CI/CD tools

### Known Issues

Track known issues here or link to issue tracker.

### Future Roadmap

Document planned features and improvements:
- [ ] Define project purpose and scope
- [ ] Choose technology stack
- [ ] Set up project structure
- [ ] Implement core functionality
- [ ] Add comprehensive tests
- [ ] Set up CI/CD pipeline
- [ ] Write user documentation

---

## Quick Reference

### Common Commands

```bash
# Check status
git status

# Create feature branch
git checkout -b claude/claude-md-<feature>

# Stage and commit
git add <files>
git commit -m "type(scope): message"

# Push to remote (with retry logic)
git push -u origin <branch-name>

# Run tests (when implemented)
# [Add test commands here]

# Build project (when implemented)
# [Add build commands here]
```

### File Locations

- Configuration: `./` (root level) or `./config/`
- Source code: `./src/`
- Tests: `./tests/`
- Documentation: `./docs/`
- Scripts: `./scripts/`

---

## Version History

| Version | Date       | Changes                              |
|---------|------------|--------------------------------------|
| 1.0.0   | 2025-12-17 | Initial CLAUDE.md creation           |

---

## Questions or Issues?

If you encounter issues or have questions about these guidelines:
1. Check existing documentation
2. Review recent commits for patterns
3. Ask the repository maintainer
4. Update this document with clarifications

---

**Note to AI Assistants:** This document is a living guide. Update it as the project evolves and new conventions are established. Always keep this file in sync with the actual project state.
