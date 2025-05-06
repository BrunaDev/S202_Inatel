from database import Database
from games_database import GameDatabase

db = Database("bolt://localhost:7687", "neo4j", "neo4j12345")
db.drop_all()

games_db = GameDatabase(db)

# Criando jogadores
print("Criando jogadores...")
alice_id = games_db.create_player("Alice")
bob_id = games_db.create_player("Bobby")
lucy_id = games_db.create_player("Lucy")
apollo_id = games_db.create_player("Apollo")

print("\nJogadores:", games_db.get_players())

# Atualizando jogador
print("\nAtualizando jogador Bobby para Bob...")
games_db.update_player(bob_id, "Bob")

# Criando partidas
print("\nCriando partidas...")
match1 = games_db.create_match([alice_id, bob_id], {alice_id: 10, bob_id: 5})
match2 = games_db.create_match([alice_id, lucy_id], {alice_id: 15, lucy_id: 20})
match3 = games_db.create_match([bob_id, apollo_id], {bob_id: 8, apollo_id: 12})
match4 = games_db.create_match([lucy_id, apollo_id], {lucy_id: 7, apollo_id: 9})

print("Partidas existentes:")
for match in games_db.get_matches():
    print(f"Match {match[0]}:")
    for player in match[1]:
        print(f"  {player['player_name']} - {player['score']}")

# Verificando históricos
print("\nHistóricos antes de deletar:")
print("Alice:", games_db.get_player_matches(alice_id))
print("Bob:", games_db.get_player_matches(bob_id))
print("Lucy:", games_db.get_player_matches(lucy_id))
print("Apollo:", games_db.get_player_matches(apollo_id))

# Deletando partida e jogador
print("\nDeletando a primeira partida e jogador Bob...")
games_db.delete_match(match1)
games_db.delete_player(bob_id)

# Verificando estado final
print("\n=== Estado final ===")
print("Jogadores restantes:", games_db.get_players())
print("Partidas restantes:", len(games_db.get_matches()))

print("\nHistóricos após exclusão:")
print("Alice:", games_db.get_player_matches(alice_id))
print("Lucy:", games_db.get_player_matches(lucy_id))
print("Apollo:", games_db.get_player_matches(apollo_id))

db.close()