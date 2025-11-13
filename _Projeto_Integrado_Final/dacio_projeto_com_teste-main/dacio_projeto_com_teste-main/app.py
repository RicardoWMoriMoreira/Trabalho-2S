from flask import Flask, render_template, request, jsonify
from models import (
    UsuarioService,
    Livro, adicionar_livro, listar_livros, remover_livro, buscar_livro_por_id,
    LoanController, LoanError, ValidationError, NotFoundError,
    RelatorioService
)

app = Flask(__name__)

service = UsuarioService()
loan_controller = LoanController(service)
relatorio_service = RelatorioService(loan_controller, service)


@app.route('/')
def index():
    usuarios = service.listar()
    livros = listar_livros()
    emprestimos = loan_controller.listar_emprestimos()
    
    stats = relatorio_service.contar_status_acervo()
    
    return render_template(
        'index.html',
        usuarios=usuarios,
        livros=livros,
        emprestimos=emprestimos,
        stats=stats
    )


@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = service.listar()
    return jsonify([u.to_dict() for u in usuarios])


@app.route('/api/usuarios', methods=['POST'])
def cadastrar_usuario():
    try:
        dados = request.get_json()
        
        usuario = service.cadastrar(
            nome=dados['nome'],
            matricula=dados['matricula'],
            tipo=dados['tipo'],
            email=dados.get('email')
        )
        
        return jsonify(usuario.to_dict()), 201
    
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor'}), 500


@app.route('/api/usuarios/<int:usuario_id>', methods=['GET'])
def buscar_usuario(usuario_id):
    usuario = service.buscar_por_id(usuario_id)
    
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    return jsonify(usuario.to_dict())


@app.route('/api/usuarios/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    try:
        dados = request.get_json()
        
        usuario = service.atualizar(
            usuario_id,
            nome=dados.get('nome'),
            email=dados.get('email'),
            status=dados.get('status')
        )
        
        return jsonify(usuario.to_dict())
    
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/api/usuarios/<int:usuario_id>', methods=['DELETE'])
def remover_usuario(usuario_id):
    resultado = service.remover(usuario_id)
    
    if not resultado:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    return jsonify({'mensagem': 'Usuário removido com sucesso'})


@app.route('/api/livros', methods=['GET'])
def livros_listar():
    livros = listar_livros()
    return jsonify([
        {
            'id': l.get_id(),
            'titulo': l.get_titulo(),
            'autor': l.get_autor(),
            'estoque': l.get_estoque(),
            'status': l.get_status(),
        }
        for l in livros
    ])


@app.route('/api/livros', methods=['POST'])
def livros_criar():
    try:
        dados = request.get_json()
        novo = Livro(
            id=int(dados['id']),
            titulo=dados['titulo'],
            autor=dados['autor'],
            estoque=int(dados['estoque'])
        )
        adicionar_livro(novo)
        return jsonify({
            'id': novo.get_id(),
            'titulo': novo.get_titulo(),
            'autor': novo.get_autor(),
            'estoque': novo.get_estoque(),
            'status': novo.get_status(),
        }), 201
    except (KeyError, ValueError) as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/api/livros/<int:livro_id>', methods=['GET'])
def livros_buscar(livro_id: int):
    livro = buscar_livro_por_id(livro_id)
    if not livro:
        return jsonify({'erro': 'Livro não encontrado'}), 404
    return jsonify({
        'id': livro.get_id(),
        'titulo': livro.get_titulo(),
        'autor': livro.get_autor(),
        'estoque': livro.get_estoque(),
        'status': livro.get_status(),
    })


@app.route('/api/livros/<int:livro_id>', methods=['DELETE'])
def livros_remover(livro_id: int):
    livro = buscar_livro_por_id(livro_id)
    if not livro:
        return jsonify({'erro': 'Livro não encontrado'}), 404
    remover_livro(livro_id)
    return jsonify({'mensagem': 'Livro removido com sucesso'})


@app.route('/api/emprestimos', methods=['GET'])
def emprestimos_listar():
    loans = loan_controller.listar_emprestimos()
    return jsonify([l.to_dict() for l in loans])


@app.route('/api/emprestimos', methods=['POST'])
def emprestimos_criar():
    try:
        dados = request.get_json()
        loan = loan_controller.registrar_emprestimo(
            user_id=int(dados['user_id']),
            book_id=int(dados['book_id'])
        )
        return jsonify(loan.to_dict()), 201
    except (LoanError, ValidationError, NotFoundError) as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/api/devolucoes', methods=['POST'])
def emprestimos_devolver():
    try:
        dados = request.get_json()
        loan = loan_controller.registrar_devolucao(
            user_id=int(dados['user_id']),
            book_id=int(dados['book_id'])
        )
        return jsonify(loan.to_dict())
    except (LoanError, ValidationError, NotFoundError) as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/api/relatorios/livros-mais-emprestados', methods=['GET'])
def relatorio_livros_mais_emprestados():
    relatorio = relatorio_service.gerar_relatorio_livros_mais_emprestados()
    return jsonify(relatorio)


@app.route('/api/relatorios/usuarios-mais-ativos', methods=['GET'])
def relatorio_usuarios_mais_ativos():
    relatorio = relatorio_service.gerar_relatorio_usuarios_mais_ativos()
    return jsonify(relatorio)


@app.route('/api/relatorios/status-acervo', methods=['GET'])
def relatorio_status_acervo():
    status = relatorio_service.contar_status_acervo()
    return jsonify(status)


@app.route('/api/relatorios/emprestimos-detalhado', methods=['GET'])
def relatorio_emprestimos_detalhado():
    relatorio = relatorio_service.relatorio_detalhado_emprestimos()
    return jsonify(relatorio)


@app.route('/api/relatorios/por-periodo', methods=['GET'])
def relatorio_por_periodo():
    try:
        data_inicio = request.args.get('inicio')
        data_fim = request.args.get('fim')
        
        if not data_inicio or not data_fim:
            return jsonify({'erro': 'Parâmetros início e fim são obrigatórios'}), 400
        
        relatorio = relatorio_service.filtrar_por_periodo(data_inicio, data_fim)
        return jsonify(relatorio)
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)

