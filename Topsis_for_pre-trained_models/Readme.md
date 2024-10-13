# TOPSIS for Pre-trained Models

![Python](https://img.shields.io/badge/Python-3.7%2B-blue) 
![License](https://img.shields.io/badge/License-MIT-green)

## Overview
The `topsis_pre_trained_models` project applies the **TOPSIS** (Technique for Order Preference by Similarity to Ideal Solution) method to evaluate and select the best pre-trained models for various natural language processing (NLP) tasks. These tasks include:

- **Text Summarization**
- **Text Generation**
- **Text Classification**
- **Conversational Models**
- **Sentence Similarity**

## Purpose
In the rapidly evolving field of NLP, selecting the most effective pre-trained model can be challenging due to the variety of available models and their differing performance metrics. This project facilitates the comparison of these models using TOPSIS, allowing researchers and practitioners to make informed decisions based on performance metrics.

## Supported Tasks
1. **Text Summarization**: Evaluates models that condense lengthy texts into concise summaries while preserving key information.
2. **Text Generation**: Assesses models capable of generating coherent and contextually relevant text based on prompts.
3. **Text Classification**: Compares models that categorize text into predefined classes or labels.
4. **Conversational Models**: Evaluates models designed to understand and generate human-like responses in a conversation.
5. **Sentence Similarity**: Compares models that assess how similar two sentences are based on their meanings.

## Prerequisites
- **Python 3.7 or higher**
- Required Python packages:
  - `pandas`
  - `numpy`
  - `matplotlib`

You can install the required packages using pip:

```bash
pip install pandas numpy matplotlib
