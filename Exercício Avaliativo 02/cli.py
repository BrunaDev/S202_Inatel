from teacher_crud import TeacherCRUD
from query import SchoolQueries

class TeacherCLI:
    def __init__(self, uri, user, password):
        self.teacher_crud = TeacherCRUD(uri, user, password)
        self.queries = SchoolQueries(uri, user, password)

    def menu(self):
        while True:
            print("\n=== MENU PRINCIPAL ===")
            print("1. Gerenciar Professores")
            print("2. Executar Consultas Específicas (questão 01)")
            print("3. Executar Consultas Específicas (questão 02)")
            print("4. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.menu_crud()
            elif opcao == "2":
                self.menu_queries_questao1()
            elif opcao == "3":
                self.menu_queries_questao2()
            elif opcao == "4":
                self.teacher_crud.close()
                self.queries.close()
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida! Tente novamente.")

    def menu_crud(self):
        while True:
            print("\n=== CRUD DE PROFESSORES ===")
            print("1. Criar Professor")
            print("2. Consultar Professor")
            print("3. Atualizar CPF")
            print("4. Deletar Professor")
            print("5. Teste Chris Lima (Criar, Consultar, Atualizar)")
            print("6. Voltar")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.criar_professor()
            elif opcao == "2":
                self.consultar_professor()
            elif opcao == "3":
                self.atualizar_cpf()
            elif opcao == "4":
                self.deletar_professor()
            elif opcao == "5":
                self.teste_chris_lima()
            elif opcao == "6":
                break
            else:
                print("Opção inválida!")

    def menu_queries_questao1(self):
        while True:
            print("\n=== CONSULTAS ESPECÍFICAS ===")
            print("1. Dados do Professor Renzo")
            print("2. Professores com nome começando em M")
            print("3. Listar todas as cidades")
            print("4. Escolas com número entre 150-550")
            print("5. Voltar")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.mostrar_renzo()
            elif opcao == "2":
                self.mostrar_professores_m()
            elif opcao == "3":
                self.mostrar_cidades()
            elif opcao == "4":
                self.mostrar_escolas()
            elif opcao == "5":
                break
            else:
                print("Opção inválida!")

    def menu_queries_questao2(self):
        while True:
            print("\n=== CONSULTAS QUESTÃO 02 ===")
            print("1. Ano nascimento professor mais jovem e mais velho")
            print("2. Média de habitantes das cidades")
            print("3. Cidade com CEP 37540-000 (substituir 'a' por 'A')")
            print("4. Terceira letra dos nomes dos professores")
            print("5. Voltar")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.mostrar_idades_professores()
            elif opcao == "2":
                self.mostrar_media_populacao()
            elif opcao == "3":
                self.mostrar_cidade_cep()
            elif opcao == "4":
                self.mostrar_terceira_letra()
            elif opcao == "5":
                break
            else:
                print("Opção inválida!")

    def criar_professor(self):
        try:
            print("\n--- NOVO PROFESSOR ---")
            name = input("Nome: ")
            ano_nasc = int(input("Ano de nascimento: "))
            cpf = input("CPF: ")
            
            self.teacher_crud.create(name, ano_nasc, cpf)
            print("\nProfessor criado com sucesso!")
        except ValueError:
            print("Erro: Ano de nascimento deve ser um número!")
        except Exception as e:
            print(f"Erro: {str(e)}")

    def consultar_professor(self):
        print("\n--- CONSULTAR PROFESSOR ---")
        name = input("Nome do professor: ")
        results = self.teacher_crud.read(name)
        
        if results:
            print("\nDados do Professor:")
            for record in results:
                teacher = record['t']
                print(f"Nome: {teacher['name']}")
                print(f"Ano Nascimento: {teacher['ano_nasc']}")
                print(f"CPF: {teacher['cpf']}")
        else:
            print("\nProfessor não encontrado.")

    def atualizar_cpf(self):
        print("\n--- ATUALIZAR CPF ---")
        name = input("Nome do professor: ")
        new_cpf = input("Novo CPF: ")
        
        if not self.teacher_crud.read(name):
            print("\nProfessor não encontrado.")
            return
            
        self.teacher_crud.update(name, new_cpf)
        print("\nCPF atualizado com sucesso!")

    def deletar_professor(self):
        print("\n--- DELETAR PROFESSOR ---")
        name = input("Nome do professor: ")
        
        if not self.teacher_crud.read(name):
            print("\nProfessor não encontrado.")
            return
            
        self.teacher_crud.delete(name)
        print("\nProfessor deletado com sucesso!")

    def teste_chris_lima(self):
        print("\n=== TESTE CHRIS LIMA ===")
        
        # 1. Criar o professor Chris Lima
        print("\n1. Criando professor Chris Lima...")
        self.teacher_crud.create("Chris Lima", 1956, "189.052.396-66")
        print("✅ Professor Chris Lima criado com sucesso!")
        
        # 2. Consultar o professor
        print("\n2. Consultando professor Chris Lima...")
        results = self.teacher_crud.read("Chris Lima")
        if results:
            print("✅ Professor encontrado:")
            for record in results:
                teacher = record['t']
                print(f"Nome: {teacher['name']}")
                print(f"Ano Nascimento: {teacher['ano_nasc']}")
                print(f"CPF: {teacher['cpf']}")
        else:
            print("❌ Professor não encontrado!")
            return
        
        # 3. Atualizar o CPF
        print("\n3. Atualizando CPF para '162.052.777-77'...")
        self.teacher_crud.update("Chris Lima", "162.052.777-77")
        
        # Verificar a atualização
        updated = self.teacher_crud.read("Chris Lima")
        if updated and updated[0]['t']['cpf'] == "162.052.777-77":
            print("✅ CPF atualizado com sucesso!")
            print(f"Novo CPF: {updated[0]['t']['cpf']}")
        else:
            print("❌ Falha ao atualizar CPF!")
    
    print("\nTeste completo! O professor Chris Lima permanece no banco.")

    def mostrar_renzo(self):
        results = self.queries.find_teacher_renzo()
        if results:
            print("\nDados do Professor Renzo:")
            for record in results:
                print(f"Ano Nascimento: {record['ano_nasc']}")
                print(f"CPF: {record['cpf']}")
        else:
            print("\nProfessor Renzo não encontrado.")

    def mostrar_professores_m(self):
        results = self.queries.find_teachers_starting_with_m()
        if results:
            print("\nProfessores com nome começando em M:")
            for record in results:
                print(f"Nome: {record['name']}, CPF: {record['cpf']}")
        else:
            print("\nNenhum professor encontrado.")

    def mostrar_cidades(self):
        results = self.queries.find_all_cities()
        if results:
            print("\nLista de Cidades:")
            for record in results:
                print(f"- {record['name']}")
        else:
            print("\nNenhuma cidade encontrada.")

    def mostrar_escolas(self):
        results = self.queries.find_schools_by_number()
        if results:
            print("\nEscolas (número entre 150-550):")
            for record in results:
                print(f"Nome: {record['name']}")
                print(f"Endereço: {record['address']}")
                print(f"Número: {record['number']}\n")
        else:
            print("\nNenhuma escola encontrada.")

    def mostrar_idades_professores(self):
        results = self.queries.find_youngest_and_oldest_teachers()
        if results and results[0]['mais_jovem'] is not None:
            print("\nAnos de nascimento dos professores:")
            print(f"Mais jovem: {results[0]['mais_jovem']}")
            print(f"Mais velho: {results[0]['mais_velho']}")
        else:
            print("\nNenhum professor encontrado no banco de dados.")

    def mostrar_media_populacao(self):
        results = self.queries.find_average_city_population()
        if results and results[0]['media_populacao'] is not None:
            media = results[0]['media_populacao']
            print(f"\nMédia de habitantes das cidades: {media:.2f}")
        else:
            print("\nNenhuma cidade encontrada no banco de dados.")

    def mostrar_cidade_cep(self):
        results = self.queries.find_city_by_cep()
        if results:
            print("\nNome da cidade com CEP 37540-000:")
            print(results[0]['nome_modificado'])
        else:
            print("\nCidade com CEP 37540-000 não encontrada.")

    def mostrar_terceira_letra(self):
        results = self.queries.find_third_character_of_teachers()
        if results:
            print("\nTerceira letra dos nomes dos professores:")
            for record in results:
                print(f"- {record['terceira_letra']}")
        else:
            print("\nNenhum professor encontrado no banco de dados.")

if __name__ == "__main__":
    try:
        cli = TeacherCLI("bolt://localhost:7687", "neo4j", "neo4j12345")
        cli.menu()
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário")
    except Exception as e:
        print(f"\nErro: {str(e)}")
