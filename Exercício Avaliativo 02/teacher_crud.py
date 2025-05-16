from database import Database

class TeacherCRUD:
    def __init__(self, uri, user, password):
        self.db = Database(uri, user, password)

    def create(self, name, ano_nasc, cpf):
        query = """
        CREATE (t:Teacher {name: $name, ano_nasc: $ano_nasc, cpf: $cpf})
        RETURN t
        """
        parameters = {"name": name, "ano_nasc": ano_nasc, "cpf": cpf}
        return self.db.execute_query(query, parameters)

    def read(self, name):
        query = """
        MATCH (t:Teacher {name: $name})
        RETURN t
        """
        parameters = {"name": name}
        return self.db.execute_query(query, parameters)

    def update(self, name, new_cpf):
        query = """
        MATCH (t:Teacher {name: $name})
        SET t.cpf = $new_cpf
        RETURN t
        """
        parameters = {"name": name, "new_cpf": new_cpf}
        return self.db.execute_query(query, parameters)

    def delete(self, name):
        query = """
        MATCH (t:Teacher {name: $name})
        DELETE t
        """
        parameters = {"name": name}
        return self.db.execute_query(query, parameters)

    def close(self):
        self.db.close()