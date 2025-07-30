# Alfred: AI Prompt Evaluator 🧠

**Alfred** is a production-grade backend system designed to evaluate and improve AI prompts using large language models. It empowers users to become better prompt engineers by analyzing prompt quality, offering structured feedback, and enabling iterative refinement.

This system uses OpenAI's LLMs to assess prompts across five key dimensions — **Clarity**, **Specificity**, **Completeness**, **Consistency**, and **Complexity** — and provides both scores and tailored suggestions for improvement. It also supports secure user authentication, stores user and prompt data in PostgreSQL, and is built for scalability with Docker and CI/CD pipelines.

### 🔧 Key Features
- **LLM-based Prompt Grading** – Quantitative evaluation with justifications across five structured dimensions.
- **Prompt Refinement API** – Feedback-driven improvement suggestions for iterative editing.
- **Secure Auth & User Storage** – JWT-based authentication with hashed credentials.
- **Modular Architecture** – FastAPI backend with structured routing and service layers.
- **CI/CD Ready** – Pytest test coverage with automated GitHub Actions for deployments.
- **PostgreSQL Integration** – Efficient storage and retrieval of prompts, scores, and users.
- **Production-ready** – Fully containerized and deployable to cloud infrastructure.

This project is part of a broader vision to make **context and prompt engineering accessible, measurable, and improvable** — enabling better LLM outputs for everyone.
