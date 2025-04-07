import warnings

warnings.simplefilter("ignore")

import gym
from gym import spaces
import numpy as np
from neo4j import GraphDatabase
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from sentence_transformers import SentenceTransformer
import time
import random
from queries import templates
import matplotlib.pyplot as plt


class Neo4jIndexEnv(gym.Env):
    def __init__(self, uri, queries_generator):
        super(Neo4jIndexEnv, self).__init__()

        self.driver = GraphDatabase.driver(uri)
        self.queries_generator = queries_generator
        self.index_candidates = self._generate_index_candidates()
        self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.current_query = None
        self.reward_scale = 100.0
        self.action_space = spaces.Discrete(len(self.index_candidates))
        self.observation_space = spaces.Box(
            low=-1, high=1, shape=(384,), dtype=np.float32
        )

    def reset(self):
        self._drop_all_indexes()
        self.current_query = next(self.queries_generator)
        obs = self.embedder.encode(self.current_query)
        return np.array(obs, dtype=np.float32)

    def step(self, action):
        # if action < len(self.index_candidates):
        candidate = self.index_candidates[action]
        props = candidate["property"]
        if isinstance(props, str):
            prop_string = f"n.{props}"
        else:
            prop_string = ", ".join(f"n.{p}" for p in props)

        index_stmt = f"CREATE INDEX FOR (n:{candidate['label']}) ON ({prop_string})"

        with self.driver.session() as session:
            # Run query without index
            session.run("CALL db.clearQueryCaches()")
            start_no_index = time.time()
            session.run(self.current_query).consume()
            end_no_index = time.time()

            # if action < len(self.index_candidates):
            # Apply index and wait
            session.run(index_stmt)
            session.run("CALL db.awaitIndexes()")

            # Run query with index
            session.run("CALL db.clearQueryCaches()")
            start_with_index = time.time()
            session.run(self.current_query).consume()
            end_with_index = time.time()

            reward = (end_no_index - start_no_index) - (
                end_with_index - start_with_index
            )
            reward = self.reward_scale * reward
            # else:
            #     reward = 0.0
        # print("Reward:", reward)

        done = True
        obs = self.embedder.encode(self.current_query)
        return np.array(obs, dtype=np.float32), reward, done, {}

    def _drop_all_indexes(self):
        with self.driver.session() as session:
            result = session.run("SHOW INDEXES")
            for record in result:
                name = record["name"]
                session.run(f"DROP INDEX {name}")

    def _generate_index_candidates(self):
        candidates = []
        with self.driver.session() as session:
            result = session.run("CALL db.schema.visualization()").single()
            if result:
                for node in result.get("nodes", []):
                    labels = node.get("labels")
                    if labels:
                        label = labels[0]
                        for prop in node.get("properties", []):
                            candidates.append({"label": label, "property": prop})
        if not candidates:
            # Fallback to hardcoded defaults (Movie DB)
            print("Using hardcoded index candidates...")
            candidates = [
                {"label": "Movie", "property": ["released"]},
                {"label": "Movie", "property": ["title"]},
                {"label": "Movie", "property": ["tagline"]},
                {"label": "Movie", "property": ["title", "released"]},
                {"label": "Movie", "property": ["tagline", "released"]},
                {"label": "Movie", "property": ["tagline", "title"]},
                {"label": "Person", "property": ["name"]},
                {"label": "Person", "property": ["born"]},
                {"label": "Person", "property": ["name", "born"]},
            ]
        return candidates

    def close(self):
        self.driver.close()


def extract_dynamic_data(uri):
    driver = GraphDatabase.driver(uri)
    with driver.session() as session:
        actors = [
            r["name"]
            for r in session.run("MATCH (p:Person) RETURN p.name AS name").data()
        ]
        years = [
            r["year"]
            for r in session.run(
                "MATCH (m:Movie) RETURN DISTINCT m.released AS year"
            ).data()
            if r["year"] is not None
        ]
        titles = [
            r["title"]
            for r in session.run("MATCH (m:Movie) RETURN m.title AS title").data()
        ]
    driver.close()
    return actors, years, titles


def infinite_query_generator(uri):
    actors, years, titles = extract_dynamic_data(uri)

    print("Actors:", len(actors))
    print("Years:", len(years))
    print("Movies:", len(titles))

    while True:
        template = random.choice(templates)

        # Randomly use a specific actor or leave unfiltered
        actor = random.choice(actors)
        actor_str = actor.replace("'", "\\'")
        actor_clause = f"a.name = '{actor_str}'" if random.random() < 0.1 else "true"

        # Randomly use a specific title or leave unfiltered
        title = random.choice(titles)
        title_str = title.replace("'", "\\'")
        title_clause = f"m.title = '{title_str}'" if random.random() < 0.1 else "true"

        year = random.choice(years)
        year2 = random.choice(years)
        start_year, end_year = sorted([year, year2])

        query = template.format(
            actor=actor_str,
            title=title_str,
            actor_clause=actor_clause,
            title_clause=title_clause,
            year=start_year,
            year2=end_year,
        )

        yield query


if __name__ == "__main__":
    uri = "bolt://localhost:7687"

    query_gen = infinite_query_generator(uri)
    for i in range(5):
        print(next(query_gen))

    env = Neo4jIndexEnv(uri, query_gen)
    eval_callback = EvalCallback(env, log_path="./logs/", eval_freq=100)

    model = PPO("MlpPolicy", env, verbose=0)
    model.learn(total_timesteps=100000, callback=eval_callback)
    env.close()

    data = np.load("./logs/evaluations.npz")
    timesteps = data["timesteps"]
    results = data["results"]

    mean_rewards = results.mean(axis=1)

    plt.plot(timesteps, mean_rewards)
    plt.xlabel("Timesteps")
    plt.ylabel("Mean Reward")
    plt.title("Evaluation Reward over Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("rewards.png")
