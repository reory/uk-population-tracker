# 🗺️ Contributing to UK Population Tracker GB

---

Thank you for your interest in contributing to the **UK Population Tracker GB** project!  
By contributing to this repository, you help make demographic data processing and visualization more accessible, structured, and performant.

---

## 🛠️ Contribution Workflow
Step 1: Create a Feature Branch
Keep your branch names concise and descriptive:

```Bash
git checkout -b feature/london-borough-mapping
```
### OR
```bash
git checkout -b fix/mongodb-reconnection-issue
```

### Code Quality and Standards
Style Guide: 
- Adhere to PEP 8 standards. Keep variable names explicit and maps properly typed.

### Documentation: 
- If you add new data endpoints or data generation algorithms, make sure to add descriptive docstrings and update comments.

- No Real Records: Never check real ONS individual datasets or restricted PII files into the repository. The tracker relies strictly on the structured generation tools provided.

### Commit Messages
Write meaningful, imperative commit messages:

- Good: feat: add borough-level boundary parser using geopandas

- Bad: fixed data things

### Open a Pull Request (PR)
Push your branch to your GitHub fork:

```Bash
git push origin feature/london-borough-mapping
```
Navigate to the main repository and open a Pull Request.

Your PR description should include:

### Context: 
- What problem does this PR solve or - what feature does it introduce?

### How it was tested: 
- Provide the pytest output snippet or structural confirmation.

- Visuals (if applicable): Screenshots of any UI adjustments made to the Plotly engine or Flask templates.

---

## 📝 Code of Conduct & Credits
- Maintainer: Roy Peters

- Data Sources: Open Geography Portal (ONS) boundary frameworks.

### Etiquette: 
- Be respectful, clear, and collaborative during code reviews and Issue discussions.

- Thank you for contributing to the growth of the UK Population Tracker GB platform! Feel free to open an issue if you discover a bug or want to discuss a new feature idea. 😊