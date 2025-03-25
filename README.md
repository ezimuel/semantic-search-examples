# Semantic Search example with Elasticsearch

This project contains some example in how to use Elasticsearch for
performing semantic search.

All the examples are written in Python. You need Python version 3.11+ installed.

[Here](https://www.python.org/downloads/) you can find information on how to install Python.

## Install Ollama

As embedding model we use [Llama 3.2](https://www.llama.com/llama-downloads/) at 3B.
You can install this model using the [ollama](https://ollama.com/) tool.

```bash
ollama pull llama3.2:3b
```

You can try the model in the console running the following command:

```bash
ollama run llama3.2:3b
```

You can then chat with the model. To exit from the chat you need to write `/bye`.

## Install Elasticsearch

To install Elasticsearch you can execute the following command:

```bash
curl -fsSL https://elastic.co/start-local | sh
```

Elasticsearch will be run on `localhost:9200`. You will have also Kibana running
at `http://localhost:5601`. You can enter in the web management console using the
`elastic` user and the password provided during the installation (stored in the `.env` file).

If you want to have a quick introduction to Elasticsearch, you can read the following
[basics](https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro.html).

## Install the Python examples

To run the Python examples you need to install all the dependecies.
Before, we suggest to activate the virtual environment for Python, using the
following command:

```bash
python -m venv .venv
```
And then activate the virtual environment with the command:

```bash
source .venv/bin/activate
```

After, you can install the dependencies as follows:

```bash
pip install -r requirements.txt
```

If you don't have **pip** installed you can install it following this [guide](https://pip.pypa.io/en/stable/installation/).

## Run the examples

We provided a list of talks from the [CloudConf 2025](https://2025.cloudconf.it/) conference.
The information about the talks are stored in the `data` folder.

To perform a semantic search we need to populate the Elasticsearch
vector database.

You need to execute the following script to store vectors in Elasticsearch:

```bash
python src/embedding.py
```

After you can perform semantic search running the following command:

```bash
python src/search.py
```