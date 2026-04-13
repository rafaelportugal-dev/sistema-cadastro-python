import json
import os

ARQUIVO = "usuarios.json"


def limpar():
    os.system("cls" if os.name == "nt" else "clear")


def carregar_usuarios():
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def salvar_usuarios(usuarios):
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=4)
    except OSError:
        print("Erro ao salvar os dados.")


def pausar():
    input("\nPressione Enter para continuar...")


def validar_nome(nome):
    return len(nome.strip()) >= 3


def validar_idade(idade):
    return idade.isdigit() and 0 < int(idade) <= 120


def validar_email(email):
    email = email.strip()
    return "@" in email and "." in email and " " not in email


def email_ja_existe(usuarios, email):
    email = email.strip().lower()
    return any(usuario["email"].lower() == email for usuario in usuarios)


def cadastrar_usuario(usuarios):
    limpar()
    print("=== CADASTRAR USUÁRIO ===")

    nome = input("Nome: ").strip()
    if not validar_nome(nome):
        print("Nome inválido. Digite pelo menos 3 caracteres.")
        return

    idade = input("Idade: ").strip()
    if not validar_idade(idade):
        print("Idade inválida.")
        return

    email = input("Email: ").strip()
    if not validar_email(email):
        print("Email inválido.")
        return

    if email_ja_existe(usuarios, email):
        print("Já existe um usuário com esse email.")
        return

    usuario = {
        "nome": nome,
        "idade": int(idade),
        "email": email
    }

    usuarios.append(usuario)
    salvar_usuarios(usuarios)
    print("Usuário cadastrado com sucesso!")


def listar_usuarios(usuarios):
    limpar()
    print("=== LISTA DE USUÁRIOS ===")

    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for i, usuario in enumerate(usuarios, start=1):
        print(f"{i}. {usuario['nome']} | {usuario['idade']} anos | {usuario['email']}")


def buscar_usuario(usuarios):
    limpar()
    print("=== BUSCAR USUÁRIO ===")

    busca = input("Digite o nome para buscar: ").strip().lower()
    encontrados = [
        usuario for usuario in usuarios
        if busca in usuario["nome"].lower()
    ]

    if not encontrados:
        print("Usuário não encontrado.")
        return

    print("\nResultados encontrados:")
    for usuario in encontrados:
        print(f"- {usuario['nome']} | {usuario['idade']} anos | {usuario['email']}")


def atualizar_usuario(usuarios):
    limpar()
    print("=== ATUALIZAR USUÁRIO ===")

    email = input("Digite o email do usuário que deseja atualizar: ").strip()

    for usuario in usuarios:
        if usuario["email"].lower() == email.lower():
            print("\nDeixe em branco para manter o valor atual.")

            novo_nome = input(f"Novo nome ({usuario['nome']}): ").strip()
            nova_idade = input(f"Nova idade ({usuario['idade']}): ").strip()
            novo_email = input(f"Novo email ({usuario['email']}): ").strip()

            if novo_nome:
                if validar_nome(novo_nome):
                    usuario["nome"] = novo_nome
                else:
                    print("Nome inválido.")
                    return

            if nova_idade:
                if validar_idade(nova_idade):
                    usuario["idade"] = int(nova_idade)
                else:
                    print("Idade inválida.")
                    return

            if novo_email:
                if not validar_email(novo_email):
                    print("Email inválido.")
                    return

                if novo_email.lower() != usuario["email"].lower() and email_ja_existe(usuarios, novo_email):
                    print("Já existe outro usuário com esse email.")
                    return

                usuario["email"] = novo_email

            salvar_usuarios(usuarios)
            print("Usuário atualizado com sucesso!")
            return

    print("Usuário não encontrado.")


def remover_usuario(usuarios):
    limpar()
    print("=== REMOVER USUÁRIO ===")

    email = input("Digite o email do usuário a remover: ").strip()

    for usuario in usuarios:
        if usuario["email"].lower() == email.lower():
            usuarios.remove(usuario)
            salvar_usuarios(usuarios)
            print("Usuário removido com sucesso!")
            return

    print("Usuário não encontrado.")


def menu():
    usuarios = carregar_usuarios()

    while True:
        limpar()
        print("=== SISTEMA DE CADASTRO ===")
        print("1 - Cadastrar usuário")
        print("2 - Listar usuários")
        print("3 - Buscar usuário")
        print("4 - Atualizar usuário")
        print("5 - Remover usuário")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_usuario(usuarios)
            pausar()
        elif opcao == "2":
            listar_usuarios(usuarios)
            pausar()
        elif opcao == "3":
            buscar_usuario(usuarios)
            pausar()
        elif opcao == "4":
            atualizar_usuario(usuarios)
            pausar()
        elif opcao == "5":
            remover_usuario(usuarios)
            pausar()
        elif opcao == "0":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida.")
            pausar()


if __name__ == "__main__":
    menu()
