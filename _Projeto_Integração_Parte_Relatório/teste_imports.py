#!/usr/bin/env python3
"""
Script de teste para verificar se todos os imports estão funcionando
seguindo o padrão do PersonalExpenseOrganizer-1
"""

def testar_imports():
    try:
        # Teste 1: Import do Model
        from Model import model as md
        print("✅ Model importado com sucesso")

        # Teste 2: Import do Controller
        import controler as ctl
        print("✅ Controller importado com sucesso")

        # Teste 3: Import da View
        from View_and_Interface import view as vw
        print("✅ View importado com sucesso")

        # Teste 4: Instanciar controller
        controller = ctl.Controler(login_required=False)
        print("✅ Controller instanciado com sucesso")

        # Teste 5: Testar métodos do controller
        usuarios = controller.get_usuarios()
        livros = controller.get_livros()
        emprestimos = controller.get_emprestimos()
        print(f"✅ Dados carregados: {len(usuarios)} usuários, {len(livros)} livros, {len(emprestimos)} empréstimos")

        print("\nSISTEMA DE GESTA DE BIBLIOTECA")
        print("A aplicação segue o mesmo padrão arquitetural do PersonalExpenseOrganizer-1")

        return True

    except Exception as e:
        print(f"❌ Erro nos imports: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    testar_imports()
