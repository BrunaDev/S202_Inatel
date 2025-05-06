import uuid

class GameDatabase:
    def __init__(self, database):
        self.db = database

    def create_player(self, name):
        if not name:
            raise ValueError("Player name cannot be empty")
        player_id = str(uuid.uuid4())
        query = "CREATE (:Player {id: $id, name: $name})"
        parameters = {"id": player_id, "name": name}
        self.db.execute_query(query, parameters)
        return player_id

    def update_player(self, player_id, new_name):
        if not new_name:
            raise ValueError("New name cannot be empty")
        if not self.get_player(player_id):
            raise ValueError(f"Player with ID {player_id} not found")
        query = "MATCH (p:Player {id: $player_id}) SET p.name = $new_name"
        parameters = {"player_id": player_id, "new_name": new_name}
        self.db.execute_query(query, parameters)

    def delete_player(self, player_id):
        if not self.get_player(player_id):
            raise ValueError(f"Player with ID {player_id} not found")
        query = "MATCH (p:Player {id: $player_id}) DETACH DELETE p"
        parameters = {"player_id": player_id}
        self.db.execute_query(query, parameters)

    def get_players(self):
        query = "MATCH (p:Player) RETURN p.id AS id, p.name AS name"
        results = self.db.execute_query(query)
        return [(result["id"], result["name"]) for result in results]

    def get_player(self, player_id):
        query = "MATCH (p:Player {id: $player_id}) RETURN p.id AS id, p.name AS name"
        parameters = {"player_id": player_id}
        results = self.db.execute_query(query, parameters)
        return (results[0]["id"], results[0]["name"]) if results else None

    def create_match(self, player_ids, scores):
        if not player_ids or len(player_ids) < 2:
            raise ValueError("At least two players are required for a match")
        for pid in player_ids:
            if not self.get_player(pid):
                raise ValueError(f"Player with ID {pid} not found")
            if pid not in scores:
                raise ValueError(f"Score missing for player with ID {pid}")
        
        match_id = str(uuid.uuid4())
        query = """
        CREATE (m:Match {id: $match_id})
        WITH m
        UNWIND $player_ids AS pid
        MATCH (p:Player {id: pid})
        CREATE (p)-[:PARTICIPATED {score: $scores[pid]}]->(m)
        RETURN m.id AS id
        """
        parameters = {
            "match_id": match_id,
            "player_ids": player_ids,
            "scores": scores
        }
        results = self.db.execute_query(query, parameters)
        return match_id

    def delete_match(self, match_id):
        if not self.get_match(match_id):
            raise ValueError(f"Match with ID {match_id} not found")
        query = "MATCH (m:Match {id: $match_id}) DETACH DELETE m"
        parameters = {"match_id": match_id}
        self.db.execute_query(query, parameters)

    def get_matches(self):
        query = """
        MATCH (m:Match)<-[r:PARTICIPATED]-(p:Player)
        RETURN m.id AS match_id, 
               collect({player_id: p.id, player_name: p.name, score: r.score}) AS players
        """
        results = self.db.execute_query(query)
        return [(result["match_id"], result["players"]) for result in results]

    def get_match(self, match_id):
        query = """
        MATCH (m:Match {id: $match_id})<-[r:PARTICIPATED]-(p:Player)
        RETURN m.id AS match_id, 
               collect({player_id: p.id, player_name: p.name, score: r.score}) AS players
        """
        parameters = {"match_id": match_id}
        results = self.db.execute_query(query, parameters)
        return (results[0]["match_id"], results[0]["players"]) if results else None

    def get_player_matches(self, player_id):
        """Retorna o histórico de partidas de um jogador."""
        if not self.get_player(player_id):
            raise ValueError(f"Player with ID {player_id} not found")
        query = """
        MATCH (p:Player {id: $player_id})-[r:PARTICIPATED]->(m:Match)
        OPTIONAL MATCH (m)<-[other_r:PARTICIPATED]-(other:Player)
        WHERE other.id <> $player_id
        WITH m, r, other, other_r
        ORDER BY other.id
        RETURN m.id AS match_id, 
               [opponent IN collect(
                   CASE WHEN other IS NOT NULL THEN 
                       {player_id: other.id, player_name: other.name, score: other_r.score}
                   ELSE null END
               ) WHERE opponent IS NOT NULL] AS opponents,
               r.score AS player_score
        """
        parameters = {"player_id": player_id}
        results = self.db.execute_query(query, parameters)
        return [(result["match_id"], 
                result["opponents"],
                result["player_score"]) for result in results]
    