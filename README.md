# Contract-Advisor-RAG
## Towards Building A High-Precision Legal Expert LLM APP

---

### Business Objective
**Lizzy AI** is an early-stage Israeli startup, developing the next-generation contract AI. We leverage Hybrid LLM technology (edge, private cloud, and LLM services) to build the first fully autonomous artificial contract lawyer.

Our journey begins with a powerful contract assistant, aiming to evolve into a fully autonomous contract bot capable of drafting, reviewing, and negotiating contracts independently, end-to-end, without human assistance.

Our task is to build, evaluate, and improve a **Retrieval-Augmented Generation (RAG)** system for Contract Q&A (chatting with a contract and asking questions about the contract).

<img src="Workflow.png" width="50%" alt="Workflow" style="display: block; margin: 0 auto;">

---

### Goal
To create the best possible RAG system with the most effective strategies to provide users with the most relevant information about contracts.

---

### Evaluation
To evaluate the RAG pipeline, we use two different test datasets:
- **Synthetic dataset** generated by the RAGAS tool.
- **Manually curated test dataset**.

By evaluating the RAG pipeline's performance on these datasets, we can assess the effectiveness of the current RAG strategies. Based on the evaluation results, we will update and refine the RAG strategies to improve the bot's question-answering capabilities.

The overall workflow is to use the RAGAS evaluation to assess the RAG pipeline, iterating on the RAG strategies based on the evaluation findings to continuously enhance the question-answering contract bot.

---

### Variables Affecting RAG Performance
1. **User query**
2. **Retrieved data (Context)**
3. **LLM**

By modifying these variables, we can improve the RAG performance.

---

### RAGAS Evaluation Metrics
- **Faithfulness:** Measures the factual consistency of the generated answer against the given context. The answer is scaled to a (0,1) range; higher is better.
- **Answer Relevancy:** Assesses how pertinent the generated answer is to the given prompt. Lower scores are assigned to incomplete or redundant answers, and higher scores indicate better relevancy.
- **Context Recall:** Measures the extent to which the retrieved context aligns with the annotated answer, treated as the ground truth. Values range between 0 and 1, with higher values indicating better performance.
- **Context Precision:** Evaluates whether all of the ground-truth relevant items present in the contexts are ranked higher or not.

Based on the metrics we have evaluated, we can determine which strategies to modify to improve overall performance.

---

### Strategies

- **Simple RAG system**
- **Multiquery RAG**
- **RAG Fusion**
- **Autogen**

---

### Installation
```sh
# Create a virtual environment
python -m venv env

# Activate the virtual environment
# For Windows
env\Scripts\activate
# For MacOS/Linux
source env/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
pip install -r frontend_requirements.txt
```

### Usage 
Run the backend:
```sh
cd Contract-Advisor-RAG
cd backend
python3 app.py
```
Run the frontend:
```sh
cd Contract-Advisor-RAG
cd frontend
npm start
```
