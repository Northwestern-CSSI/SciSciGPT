# Release Notes

## Cross-Platform Compatibility & Enhanced Installation

We are pleased to announce significant improvements to SciSciGPT's deployment pipeline, focusing on cross-platform compatibility and streamlined installation procedures.

### Cross-Platform Validation

SciSciGPT has been thoroughly tested and validated across multiple operating systems:

- **Ubuntu 24.04 LTS**
- **CentOS Stream 10**
- **macOS Sequoia 15.5**
- **Windows 11**

All core functionalities—including multi-agent orchestration, database integration, multi-language analytics (Python/R/Julia), and the web interface—operate consistently across these platforms using our unified Anaconda-based dependency management.

### Streamlined Installation Process

The installation workflow has been simplified into intuitive command-line operations:

**Backend Setup:**
```bash
cd backend
conda create -n sciscigpt python=3.11 -y
conda activate sciscigpt
pip install -r requirements.txt
bash setup-sandbox.sh  # Optional: comprehensive package installation
bash start.sh
```

**Frontend Setup:**
```bash
cd frontend
bash setup.sh
bash start.sh
```

### Enhanced Documentation

The README has been substantially expanded with:

- **Step-by-step cloud infrastructure setup** for Google Cloud Platform (BigQuery, Cloud Storage, Vertex AI), Pinecone vector database, and Upstash Redis
- **Automated database construction** via ready-to-execute Jupyter notebooks that download datasets from HuggingFace and deploy to cloud services
- **Comprehensive troubleshooting section** addressing common deployment challenges including:
  - Package version constraints for BigQuery and Pinecone clients
  - Google Cloud service account permissions and IAM roles
  - GCS bucket public-access configuration
  - Frontend-backend synchronization issues
- **Complete environment variable templates** with clear documentation for all required credentials and endpoints

### Technical Improvements

- **Unified Conda environment** (`sciscigpt`) harmonizes dependencies across operating systems
- **Multi-language support** with properly configured rpy2 and juliacall bridges for seamless Python/R/Julia interoperability
- **Modular installation options** distinguishing minimal setup (core functionality) from comprehensive sandbox (extended scientific packages)

### Documentation Fixes

- Corrected License badge (AGPL-3.0)
- Fixed file references to match actual project structure
- Added missing environment variables to configuration templates
- Updated protocol specifications for local development environments

These improvements significantly lower the barrier for researchers to deploy, customize, and extend SciSciGPT for their own Science of Science investigations across diverse computing environments.
