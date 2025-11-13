#!/usr/bin/env python3
"""
Script para testar e demonstrar as pipelines de aggregation do MongoDB
"""
from Model.model import db_manager
from datetime import datetime, timedelta

def test_pipelines():
    """Testa todas as pipelines implementadas"""
    print("=== TESTANDO PIPELINES DE AGGREGATION DO MONGODB ===")
    print("=" * 60)

    # Conectar ao banco
    if not db_manager.connect():
        print("ERRO: Falha na conexao com MongoDB")
        return

    try:
        print("\n1. ESTATISTICAS GERAIS:")
        print("-" * 30)
        stats = db_manager.get_estatisticas_gerais()
        if stats:
            print("Usuarios por tipo:")
            for tipo in stats.get('usuarios_por_tipo', []):
                print(f"   {tipo['_id']}: {tipo['count']}")

            livros = stats.get('livros', {})
            print(f"\nLivros: {livros.get('total_livros', 0)} total")
            print(f"   Disponiveis: {livros.get('livros_disponiveis', 0)}")
            print(f"   Emprestados: {livros.get('livros_emprestados', 0)}")

            emprestimos = stats.get('emprestimos', {})
            print(f"\nEmprestimos: {emprestimos.get('total_emprestimos', 0)} total")
            print(f"   Ativos: {emprestimos.get('emprestimos_ativos', 0)}")
            print(f"   Finalizados: {emprestimos.get('emprestimos_finalizados', 0)}")

        print("\n2. LIVROS MAIS EMPRESTADOS:")
        print("-" * 30)
        livros_populares = db_manager.get_relatorio_livros_mais_emprestados(5)
        if livros_populares:
            for i, livro in enumerate(livros_populares, 1):
                print(f"{i}. '{livro['titulo']}' - {livro['autor']}")
                print(f"   Total emprestimos: {livro['total_emprestimos']}")
                print(f"   Ativos: {livro['emprestimos_ativos']}")
                print(f"   Status: {'Disponivel' if livro['disponivel'] else 'Emprestado'}")
                print()
        else:
            print("Nenhum emprestimo encontrado ainda.")

        print("\n3. USUARIOS MAIS ATIVOS:")
        print("-" * 30)
        usuarios_ativos = db_manager.get_relatorio_usuarios_mais_ativos(5)
        if usuarios_ativos:
            for i, usuario in enumerate(usuarios_ativos, 1):
                print(f"{i}. {usuario['nome']} ({usuario['tipo']})")
                print(f"   Email: {usuario['email']}")
                print(f"   Total emprestimos: {usuario['total_emprestimos']}")
                print(f"   Ativos: {usuario['emprestimos_ativos']}")
                print()
        else:
            print("Nenhum emprestimo encontrado ainda.")

        print("\n4. EMPRESTIMOS RECENTES (ultimos 30 dias):")
        print("-" * 30)
        data_inicio = datetime.now() - timedelta(days=30)
        data_fim = datetime.now()
        emprestimos_recentes = db_manager.get_relatorio_emprestimos_por_periodo(data_inicio, data_fim)

        if emprestimos_recentes:
            for emprestimo in emprestimos_recentes[:5]:  # Mostra apenas os 5 mais recentes
                print(f"ID: {emprestimo['emprestimo_id']}")
                print(f"   Usuario: {emprestimo['usuario']['nome']} ({emprestimo['usuario']['tipo']})")
                print(f"   Livro: '{emprestimo['livro']['titulo']}' - {emprestimo['livro']['autor']}")
                print(f"   Data emprestimo: {emprestimo['data_emprestimo'][:10]}")
                print(f"   Status: {emprestimo['status']}")
                print()
        else:
            print("Nenhum emprestimo recente encontrado.")

        print("\n5. LIVROS ATRASADOS:")
        print("-" * 30)
        livros_atrasados = db_manager.get_relatorio_livros_atrasados()
        if livros_atrasados:
            for livro in livros_atrasados:
                print(f"ID: {livro['emprestimo_id']}")
                print(f"   Usuario: {livro['usuario']['nome']} ({livro['usuario']['tipo']})")
                print(f"   Livro: '{livro['livro']['titulo']}' - {livro['livro']['autor']}")
                print(f"   Data emprestimo: {livro['data_emprestimo'][:10]}")
                print(f"   Dias de atraso: {livro['dias_atraso']}")
                print()
        else:
            print("Nenhum livro atrasado encontrado!")

        print("\n6. POPULARIDADE POR CATEGORIA:")
        print("-" * 30)
        popularidade = db_manager.get_relatorio_popularidade_por_categoria()
        if popularidade:
            for categoria in popularidade:
                print(f"{categoria['categoria_usuario']}:")
                print(f"   Total emprestimos: {categoria['total_emprestimos']}")
                print(f"   Ativos: {categoria['emprestimos_ativos']}")
                print(f"   Usuarios unicos: {categoria['numero_usuarios_unicos']}")
                print(".2f")
                print()
        else:
            print("Dados insuficientes para analise de popularidade.")

        print("\nSISTEMA DE GESTA DE BIBLIOTECA")

    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")

    finally:
        db_manager.disconnect()

def demonstrar_pipeline_codigo():
    """Mostra exemplos do código das pipelines"""
    print("\n" + "=" * 60)
    print("EXEMPLOS DE PIPELINES IMPLEMENTADAS:")
    print("=" * 60)

    print("""
LIVROS MAIS EMPRESTADOS:
```javascript
[
  {$group: {_id: "$book_id", total_emprestimos: {$sum: 1}}},
  {$lookup: {from: "livros", localField: "_id", foreignField: "id", as: "livro_info"}},
  {$sort: {total_emprestimos: -1}},
  {$limit: 10}
]
```

USUARIOS MAIS ATIVOS:
```javascript
[
  {$group: {_id: "$user_id", total_emprestimos: {$sum: 1}}},
  {$lookup: {from: "usuarios", localField: "_id", foreignField: "id", as: "usuario_info"}},
  {$sort: {total_emprestimos: -1}},
  {$limit: 10}
]
```

LIVROS ATRASADOS:
```javascript
[
  {$match: {return_date: null, loan_date: {$lt: "data_limite"}}},
  {$lookup: {from: "usuarios", localField: "user_id", foreignField: "id", as: "usuario"}},
  {$lookup: {from: "livros", localField: "book_id", foreignField: "id", as: "livro"}},
  {$sort: {data_emprestimo: 1}}
]
```
    """)

if __name__ == "__main__":
    test_pipelines()
    demonstrar_pipeline_codigo()
