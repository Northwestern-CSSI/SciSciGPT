# SciSciGPT Frontend

This is the frontend for SciSciGPT, an advanced LLM agent research assistant for the field of science of science (SciSci). This project is adapted from the [Vercel AI Chatbot](https://github.com/vercel/ai-chatbot) and is designed to be integrated with a LLM agent API backend supported by LangServe.

## About

The SciSciGPT frontend, built with Next.js and supported by Vercel, provides the user interface for an intelligent research assistant in the science of science (SciSci) field. It's designed to interact with a separate LangServe-powered backend that handles the LLM agent functionality.

## SciSciGPT Capabilities

SciSciGPT is a Language Model Agent (LLMA) specifically designed for SciSci research. It interacts with researcher-defined, gym-like environments through coordinated actions, differentiating it from traditional text-generating LLMs. SciSciGPT's capabilities are facilitated by a specially designed toolkit with an extensive suite of tools tailored for data science applications in SciSci research. These tools support four critical categories of actions in scientific inquiry:

1. **Information Retrieval**: Tools engineered to search and extract relevant information from vast scientific literature repositories, generating literature reviews on SciSci topics.

2. **Data Extraction**: Tools that serve as the interface between SciSciGPT and databases, facilitating data extraction from complex, multifaceted databases like SciSciNet to create subsets of data for analysis.

3. **Data Analysis**: Tools capable of performing advanced data analyses and generating insights from extracted data.

4. **Self-Evaluation**: Tools that leverage the literature review provided by information retrieval tools to assess and even refine the outputs from the data analysis or data extraction tools.

These tools are predefined by tool descriptions, invocation formats, and external implementations, serving as the interface between the space of text generation and the space of actions in the environment.

## Features

- User-friendly interface for interacting with the SciSciGPT agent
- Integration with Next.js and Vercel AI SDK for smooth frontend performance
- Designed to connect with a LangServe-powered backend for LLM agent capabilities

## Model Providers

While this frontend template ships with OpenAI `gpt-3.5-turbo` as the default, the actual model used will depend on the LangServe backend configuration. The frontend is designed to be flexible and can work with various LLM providers as determined by the backend setup.

Note: You will need to configure the deployed frontend to connect with your LangServe backend.

## Creating a KV Database Instance
Follow the steps outlined in the [quick start guide](https://vercel.com/docs/storage/vercel-kv/quickstart#create-a-kv-database) provided by Vercel. This guide will assist you in creating and configuring your KV database instance on Vercel, enabling your application to interact with it.

Remember to update your environment variables (`KV_URL`, `KV_REST_API_URL`, `KV_REST_API_TOKEN`, `KV_REST_API_READ_ONLY_TOKEN`) in the `.env` file with the appropriate credentials provided during the KV database setup.

## Running locally

You will need to use the environment variables [defined in `.env.example`](.env.example) to run the SciSciGPT frontend. It's recommended you use [Vercel Environment Variables](https://vercel.com/docs/projects/environment-variables) for this, but a `.env` file is all that is necessary.

> Note: You should not commit your `.env` file or it will expose secrets that will allow others to control access to your various OpenAI and authentication provider accounts.

1. Install Vercel CLI: `npm i -g vercel`
2. Link local instance with Vercel and GitHub accounts (creates `.vercel` directory): `vercel link`
3. Download your environment variables: `vercel env pull`

```bash
pnpm install
pnpm dev

rm -rf .next    
npm run build && npm run start
```

Your frontend should now be running on [localhost:3000](http://localhost:3000/). Remember to configure it to connect with your LangServe backend.

## Contributing

We welcome contributions to improve the SciSciGPT frontend. Please feel free to submit issues or pull requests.

## Contact

For any questions or concerns, please contact:

Erzhuo Shao (shaoerzhuo@gmail.com)
The Center for Science of Science & Innovation (CSSI)

## Acknowledgements

This frontend is based on the [Vercel AI Chatbot](https://github.com/vercel/ai-chatbot). We thank the original authors and contributors for their work.

## License

(Include appropriate license information here)

---

For more information about the project, please refer to our [Google Docs](https://docs.google.com/document/d/1CZzSY2O1lD4M3LJe6zWFVbpAJ8_UwWZGw3b1Sd-MUpw/edit?usp=sharing).