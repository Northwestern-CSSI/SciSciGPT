<h1 align="center">
  🧬 <em>SciSciGPT</em>
</h1>

<h3 align="center">Advancing Human-AI Collaboration in the Science of Science</h3>

<p align="center">
  <img src="public/sciscigpt.png" style="width: 100%" alt="SciSciGPT Diagram" />
</p>

<p align="center">
  <a href="https://github.com/Northwestern-CSSI/SciSciGPT/stargazers">
    <img src="https://img.shields.io/github/stars/Northwestern-CSSI/SciSciGPT?style=social" alt="GitHub Stars">
  </a>
  <a href="https://github.com/Northwestern-CSSI/SciSciGPT/network/members">
    <img src="https://img.shields.io/github/forks/Northwestern-CSSI/SciSciGPT?style=social" alt="GitHub Forks">
  </a>
  <a href="https://github.com/Northwestern-CSSI/SciSciGPT/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  </a>
  <a href="https://arxiv.org/abs/2504.05559">
    <img src="https://img.shields.io/badge/arXiv-2504.05559-b31b1b.svg" alt="arXiv">
  </a>
</p>

<p align="center">
  <a href="https://sciscigpt.com">
    <img src="https://img.shields.io/badge/🚀_Try_Live_Demo-4f2984?style=for-the-badge&logoColor=white" alt="Live Demo">
  </a>
  <a href="https://arxiv.org/abs/2504.05559">
    <img src="https://img.shields.io/badge/📄_Read_Paper-4f2984?style=for-the-badge&logoColor=white" alt="Paper">
  </a>
  <a href="https://github.com/Northwestern-CSSI/SciSciGPT">
    <img src="https://img.shields.io/badge/⭐_GitHub-4f2984?style=for-the-badge&logoColor=white" alt="GitHub">
  </a>
</p>

---

<br>

*SciSciGPT* is an AI collaborator designed to advance human-AI collaboration in the science of science (SciSci) field. As scientific research becomes increasingly complex and data-intensive, researchers face growing technical barriers that limit accessibility and efficiency. *SciSciGPT* addresses these challenges by leveraging recent advances in large language models and AI agents to create a comprehensive research assistant.

The system offers both a **public chat interface** at [sciscigpt.com](https://sciscigpt.com) and a **fully open-source implementation** on GitHub. *SciSciGPT* integrates multiple research capabilities: retrieving relevant SciSci publications, extracting data from complex databases, conducting advanced analytics, creating visualizations, and evaluating its own outputs. This seamless AI-powered workflow lowers technical barriers, enhances research efficiency, and enables new modes of human-AI collaboration.

<br>



---

## Overview

*SciSciGPT* is a multi-agent AI system that includes a *ResearchManager* and four specialist agents, each designed to handle distinct aspects of the science of science research process:

The system comprises five specialized agents:

- ***ResearchManager*** - Orchestrates workflows by breaking complex questions into tasks and coordinating specialist agents
- ***LiteratureSpecialist*** - Uses retrieval-augmented generation (RAG) to process SciSci publications with metadata filters and progressive analysis of abstracts, methodology, and results
- ***DatabaseSpecialist*** - Navigates the SciSci data lake using SQL tools and embedding-based entity matching to extract and preprocess scholarly data
- ***AnalyticsSpecialist*** - Conducts analysis using Python, R, and Julia in isolated sandboxes to generate insights and visualizations
- ***EvaluationSpecialist*** - Performs multi-level quality assessments of tools, visualizations, and workflows, assigning reward scores to guide system improvements and ensure reliable research outputs

---

## Backend Architecture

**Software Service Ecosystem:** The *SciSciGPT* backend is built on a comprehensive software stack that integrates multiple services and technologies to enable seamless AI-powered research workflows. The entire *SciSciGPT* system is developed and deployed on Ubuntu 24.04 LTS with Anaconda 2025.06 version, providing a robust foundation for multi-agent coordination and scientific computing.

### Core Infrastructure

- **AI Orchestration**: [LangChain](https://www.langchain.com/) & [LangGraph](https://www.langchain.com/langgraph) for multi-agent workflow coordination
- **LLM Provider**: [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai) with Claude models (Anthropic)
- **Text Embedding**: Text embeddings (text-embedding-3-large) for vector search in *LiteratureSpecialist*
- **Application Framework**: FastAPI with [LangServe](https://python.langchain.com/docs/langserve) for API endpoints

### Data & Storage Services

- **Vector Database**: [Pinecone](https://www.pinecone.io/) for semantic search in RAG
- **Relational Database**: [Google BigQuery](https://cloud.google.com/bigquery) for hosting SciSci scholarly relational database
- **File System**: [Google Cloud Storage](https://cloud.google.com/storage) for file uploads, artifacts, and visualizations

### Analytics & Computation Environments

- **Python**: Jupyter kernel with pre-installed scientific packages
- **R**: Comprehensive statistical computing environment with 250+ packages
- **Julia**: High-performance scientific computing

The system executes code in isolated sandboxes with persistent state management within sessions.

### System Requirements

- **System**: Ubuntu 24.04 LTS
- **Memory**: 16GB+ RAM recommended for full functionality
- **Storage**: 100GB+ for dependencies and datasets
- **Network**: Internet connection for API calls to LLM providers

---

## Backend Setup Guideline

### Step 1: Google Cloud Platform Setup

*SciSciGPT* leverages three core Google Cloud Platform services to provide comprehensive research capabilities:

- **Vertex AI** provides the backbone LLM API service, enabling *SciSciGPT* to utilize Anthropic Claude models through Google's Vertex AI platform for natural language understanding, reasoning, and generation across all specialist agents
- **BigQuery** serves as the data warehouse for SciSciNet, allowing *SciSciGPT*'s *DatabaseSpecialist* to view, read, and execute SQL queries against large-scale scholarly datasets containing publications, citations, authors, and institutional data
- **Cloud Storage** hosts and manages file artifacts including BigQuery query results, *AnalyticsSpecialist*'s intermediate computational outputs, and generated visualizations, enabling seamless file communication between frontend and backend systems through public URLs

#### GCP Project

Create a Google Cloud Platform Project (`your-gcp-project-id`)

#### BigQuery Database

Enable the [BigQuery API](https://cloud.google.com/bigquery/docs/reference/rest) in your GCP project and create a BigQuery dataset (`your-dataset-name`) to store your SciSci research data.

#### Cloud Storage

1. Create a Google Cloud Storage bucket (`your-gcs-bucket-name`) in your GCP project
2. Configure the bucket for public access (refer to [Make data public](https://cloud.google.com/storage/docs/access-control/making-data-public) for more details):
   - Go to Cloud Storage > Browser in GCP Console
   - Select your bucket > Permissions tab
   - Add principal: `allUsers` and assign role: `Storage Object Viewer`
3. Files, including SQL query results, intermediate outputs, and visualizations will be uploaded to GCS and served via public URLs

#### Vertex AI

Enable the [Vertex AI API](https://cloud.google.com/vertex-ai/docs/reference/rest) in `your-gcp-project-id` project and enable Anthropic Claude models (for example, `claude-3-5-sonnet-v2@20241022`) of required version in Vertex AI's Model Garden.

#### Service Account

Create a service account (refer to [Create service accounts](https://cloud.google.com/iam/docs/service-accounts-create)) and grant the necessary IAM roles (refer to [Grant an IAM role](https://cloud.google.com/iam/docs/grant-role-console)). The service account requires the following roles:

- `BigQuery Data Viewer`: Permission to read datasets and tables in Google BigQuery;
- `BigQuery Job User`: Permission to create query jobs in Google BigQuery API;
- `BigQuery Read Session User`: Permission to use BigQuery Storage API;
- `Storage Object Admin`: Permissions for file read and uploads for GCS bucket;
- `Vertex AI User`: Permission for LLM querying and textual embedding;
- `Owner`;

Then, create and download the service account [JSON credential key file](https://cloud.google.com/iam/docs/keys-list-get), and save as `.google_application_credentials.json` in the `backend` directory and `datasets` directory, should be in the format of the example `google_application_credentials.json` key.

#### SciSciNet Database Construction

Execute the `datasets/SciSciNet.ipynb` notebook (by configuring the `project_id` and `dataset_id` within the notebook), which will automatically download all SciSciNet tables from [SciSciGPT-SciSciNet HuggingFace repository](https://huggingface.co/datasets/ErzhuoShao/SciSciGPT-SciSciNet), and upload to Google BigQuery with the right schema, table description, and column description.

The final dataset should include 19 tables: `institutions`, `nct`, `newsfeed`, `nih`, `nsf`, `paper_author_affiliations`, `paper_citations`, `paper_fields`, `paper_nct`, `paper_newsfeed`, `paper_nih`, `paper_nsf`, `paper_patents`, `paper_twitter`, `papers`, `patents`, and `twitter`, providing comprehensive coverage of scholarly publications, citations, author affiliations, funding sources, patents, and social media engagement data for Science of Science research.

---

### Step 2: Pinecone Vector Database Setup

*SciSciGPT* uses Pinecone as a vector database to host the SciSciCorpus, a comprehensive collection of scientific literature. The corpus is indexed using vector embeddings to enable semantic search capabilities, allowing the *LiteratureSpecialist* agent to perform Retrieval-Augmented Generation (RAG) operations for Science of Science research.

#### Setup Steps

1. Create a Pinecone account at https://www.pinecone.io;
2. Create an index named `your-pinecone-index-name` with the following configuration:
   - Dimensions: 3072 (compatible with OpenAI's text-embedding-3-large model)
   - Metric: Cosine similarity
3. Generate a Pinecone API key with full permissions from your Pinecone dashboard ([Manage API keys](https://docs.pinecone.io/guides/projects/manage-api-keys));
4. Obtain an OpenAI API key for text embedding generation ([OpenAI API keys](https://platform.openai.com/api-keys)).

#### SciSciCorpus Database Construction

Execute the `datasets/SciSciCorpus.ipynb` notebook to build your vector database. You will need to configure your OpenAI API key and Pinecone API key within the notebook. The notebook performs the following operations:

1. Downloads the SciSciCorpus dataset from the [SciSciGPT-SciSciCorpus HuggingFace repository](https://huggingface.co/datasets/ErzhuoShao/SciSciGPT-SciSciCorpus)
2. Generates vector embeddings for research paper abstracts using OpenAI's text-embedding-3-large model
3. Indexes each document with its embedding vector, along with metadata like full textual content and bibliometric information
4. Uploads the indexed data to your Pinecone vector database

The resulting `your-pinecone-index-name` vector database will contain semantically searchable scientific literature with associated metadata, enabling the *LiteratureSpecialist* to perform sophisticated RAG-based research queries and literature discovery.

---

### Step 3: Dependencies Installation

Our dependency installation is divided into two parts:

#### Part 1: Minimal Setup (Required)

The minimal setup is based on [Anaconda](https://anaconda.org) and includes only the essential packages needed to launch and run *SciSciGPT*, including LangChain-related packages for agent orchestration, Google BigQuery client libraries for database access, Pinecone client for vector database operations, and R and Julia environments configured via conda-forge.

Within the Anaconda environment, the *AnalyticsSpecialist* uses a unified [jupyter_client](backend/func/jupyter_async.py) interface with rpy2 and juliacall, which allows the *AnalyticsSpecialist* to execute R and Julia code within the same Python-based environment, enabling seamless multi-language scientific computing. Completing Part 1 is sufficient to get *SciSciGPT* up and running.

To install the minimal dependencies, navigate to the backend directory and run:

```bash
cd backend

conda create -n sciscigpt python=3.11 -y
conda activate sciscigpt

# Install Python dependencies
pip install -r requirements.txt

# Install R using conda-forge
conda install -c conda-forge r-essentials r-base -y
conda install rpy2 -y

# Install Julia using conda-forge
conda install -c conda-forge julia -y
pip install juliacall
```

#### Part 2: Comprehensive Package Installation (Optional)

The second part aims to ensure the *AnalyticsSpecialist* can handle a wide variety of computational tasks. Since the *AnalyticsSpecialist* may generate arbitrary code during execution, we want to minimize the likelihood of runtime failures due to missing packages. Therefore, we install a comprehensive collection of Python, R, and Julia packages that cover most common scientific computing scenarios.

For users who simply want to verify that *SciSciGPT*'s architecture works correctly or for demonstration purposes, Part 2 dependencies are optional. However, for production use where the *AnalyticsSpecialist* needs to handle diverse analytical tasks, installing the full dependency set is recommended.

To install the comprehensive dependencies, navigate to the backend directory and run:

```bash
cd backend
bash setup-sandbox.sh
```

This script will automatically install all packages within the existing `sciscigpt` environment:

- Python packages from `requirements-sandbox-python.txt`
- R packages from `requirements-sandbox-r.R`
- Julia packages from `requirements-sandbox-julia.jl`

---

### Step 4: Environment Variables Setup

Within the `backend` directory, create a `.env` file using `.env.example` as template:

```bash
OPENAI_API_KEY=your-openai-api-key

GOOGLE_APPLICATION_CREDENTIALS=.google_application_credentials.json
GOOGLE_BIGQUERY_URI=bigquery://your-gcp-project-id/your-bigquery-dataset-id

LOCAL_STORAGE_PATH=/tmp/sandbox
GCS_BUCKET_NAME=your-gcs-bucket-name
GCS_BUCKET_URL=https://storage.googleapis.com/your-gcs-bucket-name

PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=your-pinecone-index-name
```

---

### Step 5: Running the Application

Deploy the Backend of *SciSciGPT*:

```bash
bash start.sh
```

The API will be available at:

- LangServe API endpoints: `http://localhost:8080`
- Main *SciSciGPT* agent: `http://localhost:8080/sciscigpt`
- Individual tools: `http://localhost:8080/redoc`

The backend implements a multi-agent system with 5 agents:

#### Agents

- ***ResearchManager***: Orchestrates workflow and delegates tasks
- ***LiteratureSpecialist***: RAG-based literature search and analysis
- ***DatabaseSpecialist***: SQL/Neo4j data extraction and preprocessing
- ***AnalyticsSpecialist***: Python/R/Julia code execution and visualization
- ***EvaluationSpecialist***: Multi-level quality control and validation

#### Tools

- `search_literature`: Semantic search across SciSci papers (Pinecone + RAG)
- `sql_list_table`: List BigQuery database tables
- `sql_get_schema`: Retrieve table schemas with samples
- `sql_query`: Execute SQL queries and return results
- `neo4j_query`: Execute Cypher queries on graph database
- `search_name`: Entity name similarity matching
- `python`: Execute Python code in persistent environment based on Jupyter sandbox
- `r`: Execute R code in persistent environment based on Jupyter sandbox
- `julia`: Execute Julia code in persistent environment based on Jupyter sandbox

---

## Frontend Architecture

**Software Service Ecosystem:** This is the frontend for *SciSciGPT*, an advanced LLM agent research assistant for the field of science of science (SciSci). This project is adapted from the [Vercel AI Chatbot](https://github.com/vercel/ai-chatbot) and is designed to be integrated with a LLM agent API backend supported by LangServe.

### Features

- User-friendly interface for interacting with the *SciSciGPT* agent
- Designed to connect with a LangServe-powered backend for LLM agent capabilities
- Streaming output from *SciSciGPT* with live response updates
- Accessing and downloading generated research materials
- Downloading generated artifacts including tables, code outputs, and visualizations
- Chat history management with persistent conversation

---

## Frontend Setup Guideline

### Step 1: Create KV Database for Chat History Storage

Create a Redis KV database using Upstash at https://console.upstash.com/redis. The frontend code will automatically handle user authentication and chat history management. *SciSciGPT* uses Upstash's Redis database, which provides a hash table-based database for storing and retrieving information based on user ID and chat history ID.

Follow these steps:

1. Visit https://console.upstash.com/redis and create a new Redis database
2. Obtain the API credentials (URL and token) from your Upstash dashboard

---

### Step 2: Environment Variables Setup

1. Update your environment variables (`KV_URL`, `KV_REST_API_URL`, `KV_REST_API_TOKEN`, `KV_REST_API_READ_ONLY_TOKEN`) in the `.env.local` file (using `.env.example` as a template) with the credentials provided by Upstash

2. Set up the LangServe backend API endpoint:
   - `LANGSERVE_URL`: The URL where your LangServe backend is running (default: `http://localhost:8080/sciscigpt` for local development)
   - `LOCAL_STORAGE_PATH`: The local path of the workspace of *SciSciGPT*, which should be aligned with the configuration of backend

3. Configure authentication and deployment URLs:
   - `NEXTAUTH_SECRET`: Secret key for NextAuth.js authentication (default: `sciscigpt`)
   - `NEXTAUTH_URL`: The URL where your frontend will be deployed (default: `https://localhost:3000` for local development)
   - For production deployment, update to your actual domain: `https://your-domain.com`

---

### Step 3: Setup Node.js Environment

Install Node.js, pnpm, and all other required packages within `sciscigpt` environment using conda-forge.

```bash
cd frontend
bash setup.sh
```

---

### Step 4: Running the User Interface

Deploy *SciSciGPT* Frontend:

```bash
cd frontend
bash start.sh
```

The chat interface will be available at `http://localhost:3000`

---

## Citation

If you use *SciSciGPT* in your research, please cite:

```bibtex
@article{sciscigpt2025,
  title={*SciSciGPT*: Advancing Human-AI Collaboration in the Science of Science},
  author={Erzhuo Shao, Yifang Wang, Yifan Qian, Zhenyu Pan, Han Liu, Dashun Wang},
  journal={arXiv preprint arXiv:2504.05559},
  year={2025}
}
```

