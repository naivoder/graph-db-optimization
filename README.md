# Graph DB Index Optimization with Reinforcement Learning

This project uses **reinforcement learning (PPO)** to optimize **Neo4j graph database performance** by learning which indexes improve query execution time. An RL agent observes semantic embeddings of Cypher queries and chooses index actions that reduce query latency.

## What It Does

- Connects to the [Neo4j Movie Database](https://neo4j.com/docs/getting-started/data-model/)
- Embeds Cypher queries with a pretrained transformer
- Selects candidate indexes based on node labels and properties
- Measures reward as reduction in query execution time (before vs after indexing)
- Trains an RL agent to learn efficient indexing strategies

## Installation

```bash
git clone https://github.com/naivoder/graph-db-optimization.git
cd graph-db-optimization

python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

pip install -r requirements.txt
```

Make sure Neo4j is running locally at bolt://localhost:7687 with the Movie DB dataset loaded.

## How to Run

```bash
python train_agent.py
```

Logs and evaluation results are stored in `./logs/`.
