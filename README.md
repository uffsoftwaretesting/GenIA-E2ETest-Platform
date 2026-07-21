# GenIA-E2ETest: A Generative AI-Based Platform for End-to-End Test Automation

This repository contains the artifact accompanying the paper:

**GenIA-E2ETest: A Generative AI-Based Platform for End-to-End Test Automation**, accepted for publication at the **XL Brazilian Symposium on Software Engineering (SBES - Tools Track 2026)**.  

## 🔗 Link to the Accepted Paper

The full paper is available at:  
📄 [./GenIA-E2ETest-Platform.pdf](./GenIA-E2ETest-Platform.pdf)  

Authors:  
- Elvis Júnior (Universidade Federal Fluminense, Brazil)  
- Pedro Amaro (Universidade Federal Fluminense, Brazil)  
- Allber Ferreira (Universidade Federal Fluminense, Brazil)  
- Vânia de Oliveira Neves (Universidade Federal Fluminense, Brazil)

---

## 🧪 Artifact Overview

GenIA-E2ETest Platform is a full-stack artifact for generating, validating, executing, and refining end-to-end test scripts with generative AI. The platform includes:

- a web frontend for test configuration, prompt inspection, and result visualization;
- a Flask-based backend that exposes the pipeline API and orchestrates the generation flow;
- prompt templates for each pipeline stage;
- execution strategies for the supported framework/language combinations;
- automated tests covering the backend refactor and execution dispatch.

The artifact is self-contained and organized to support both reuse and reproducibility. The pipeline can generate tests from natural language inputs, continue after manual validation, and execute the produced scripts using the supported runner for each target framework and language.

- Demo video: https://youtu.be/-9xh_ThdfV4

---

## 📁 Repository Structure

```text
GenIA-E2ETest-Platform/
├── backend/
│   ├── api.py
│   ├── app.py
│   ├── config.py
│   ├── application/
│   ├── domain/
│   ├── http/
│   ├── infrastructure/
│   ├── llms/
│   ├── pipelines/
│   ├── prompts/
│   └── tests/
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── geniaLogo.jpg
│   └── scripts/
│       ├── core/
│       ├── features/
│       ├── services/
│       └── ui/
├── LICENSE
└── README.md
```

---

## 📋 Requirements

### Hardware

The artifact was evaluated using the following configuration:

- Operating System: Windows 11 Home Single Language 64-bit (Build 22631)
- Processor: Intel(R) Core(TM) i7-1165G7 @ 2.80GHz (8 cores)
- RAM: 12 GB
- Disk Space: At least 1 GB of free space

This hardware profile is sufficient for the local backend, the browser-based frontend, and the supported test execution strategies.

### Software

The artifact depends on:

- Python 3.12.3 or newer
- Google Chrome v135 or newer
- Git
- The Python dependencies listed in [`backend/requirements.txt`](backend/requirements.txt)

For the supported execution strategies, the environment must also allow the selected framework runtime to be launched locally. The backend is compatible with local execution on Windows, and the provided Dockerfile can be used when a containerized environment is preferred.

---

## ⚙️ Installation & Usage

1. Clone the repository:

```bash
git clone https://github.com/uffsoftwaretesting/GenIA-E2ETest-Platform.git
cd GenIA-E2ETest-Platform
```

2. Create and activate a Python virtual environment inside the backend folder:

```bash
cd backend
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install the backend dependencies:

```bash
pip install -r requirements.txt
playwright install
playwright install-deps  # Optional: needed only for Linux systems
```

4. Start the backend API:

```bash
python api.py
```

By default, the backend starts on port `5000`.

5. In a second terminal, serve the frontend on a local HTTP origin:

```bash
cd ..\frontend
python -m http.server 5500
```

6. Open the frontend in the browser:

```text
http://localhost:5500
```

## Basic Usage

1. Register or log in through the frontend.
2. Configure the LLM provider and model.
3. Select the target framework and language.
4. Provide either a test case or a user story, depending on the selected input mode.
5. Run the generation pipeline.
6. Review the validation output, apply any necessary manual changes, and continue the pipeline.
7. Inspect the execution logs, generated artifacts, and final reports.

---

## 📞 Support and Contact

For questions or support, please contact:
- Elvis Júnior 
- Vânia Neves 

---

## 📚 Citation
[![Cite this paper](https://img.shields.io/badge/Cite%20this%20paper-SBES%202026-blue)](#citation)

If you use **GenIA-E2ETest Platform** in your research or project, please cite:

```bibtex

@inproceedings{junior2025genia,
  author       = {Elvis Junior and Pedro Amaro and Allber Ferreira and Vânia O. Neves},
  title        = {GenIA‑E2ETest: A Generative AI‑Based Platform for End‑to‑End Test Automation},
  booktitle    = {Anais do XL Simpósio Brasileiro de Engenharia de Software},
  year         = {2026},
  address      = {São Paulo, SP, Brazil}
} 
