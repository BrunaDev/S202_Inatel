from database import Database

class SchoolQueries:
    def __init__(self, uri, user, password):
        self.db = Database(uri, user, password)

    # Questão 01
    def find_teacher_renzo(self):
        query = """
        MATCH (t:Teacher {name: 'Renzo'})
        RETURN t.ano_nasc AS ano_nasc, t.cpf AS cpf
        """
        return self.db.execute_query(query)

    def find_teachers_starting_with_m(self):
        query = """
        MATCH (t:Teacher)
        WHERE t.name STARTS WITH 'M'
        RETURN t.name AS name, t.cpf AS cpf
        """
        return self.db.execute_query(query)

    def find_all_cities(self):
        query = """
        MATCH (c:City)
        RETURN c.name AS name
        """
        return self.db.execute_query(query)

    def find_schools_by_number(self):
        query = """
        MATCH (s:School)
        WHERE s.number >= 150 AND s.number <= 550
        RETURN s.name AS name, s.address AS address, s.number AS number
        """
        return self.db.execute_query(query)
    
    # Questão 02
    def find_youngest_and_oldest_teachers(self):
        query = """
        MATCH (t:Teacher)
        RETURN MAX(t.ano_nasc) AS mais_jovem, MIN(t.ano_nasc) AS mais_velho
        """
        return self.db.execute_query(query)

    def find_average_city_population(self):
        query = """
        MATCH (c:City)
        RETURN AVG(c.population) AS media_populacao
        """
        return self.db.execute_query(query)

    def find_city_by_cep(self):
        query = """
        MATCH (c:City {cep: '37540-000'})
        RETURN REPLACE(c.name, 'a', 'A') AS nome_modificado
        """
        return self.db.execute_query(query)

    def find_third_character_of_teachers(self):
        query = """
        MATCH (t:Teacher)
        RETURN SUBSTRING(t.name, 2, 1) AS terceira_letra
        """
        return self.db.execute_query(query)

    def close(self):
        self.db.close()