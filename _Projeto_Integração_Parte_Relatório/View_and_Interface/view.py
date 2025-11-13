from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from Model import model as md
import controler as ctl
from html import escape
from datetime import datetime
# from src.report_service import ReportService  # Comentado temporariamente para debug


def _esc(v):
    return escape("" if v is None else str(v))


# Instância do controller
controller = ctl.Controller(login_required=False)

# Instância do serviço de relatórios (comentado temporariamente para debug)
# report_service = ReportService()
report_service = None


class BibliotecaController(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(302)
            self.send_header("Location", "/menu")
            self.end_headers()

        elif self.path == "/menu":
            with open("View_and_Interface/menu.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        elif self.path == "/listar_usuarios":
            resposta = ""
            # Filtrar apenas usuários com todos os campos preenchidos e não vazios
            todos_usuarios = controller.get_usuarios()
            usuarios_validos = []

            for u in todos_usuarios:
                # Verificar se todos os campos existem e não são vazios
                id_valido = u.id is not None and str(u.id).strip() != ""
                name_valido = u.name is not None and str(u.name).strip() != ""
                email_valido = u.email is not None and str(u.email).strip() != ""
                type_valido = u.type is not None and str(u.type).strip() != ""

                if id_valido and name_valido and email_valido and type_valido:
                    usuarios_validos.append(u)

            if not usuarios_validos:
                resposta = '<div class="no-users">Nenhum usuário cadastrado com dados completos.</div>'
            else:
                for usuario in usuarios_validos:
                    # Define o ícone e classe baseado no tipo de usuário
                    if usuario.type == "Professor":
                        icon = "👨‍🏫"
                        type_class = "type-professor"
                    elif usuario.type == "Funcionário":
                        icon = "👔"
                        type_class = "type-employee"
                    else:
                        icon = "🎓"
                        type_class = "type-student"

                    resposta += f"""
                    <div class="user-card">
                        <div class="user-header">
                            <div class="user-avatar">{icon}</div>
                            <div class="user-info">
                                <h3>{_esc(usuario.name)}</h3>
                                <div class="user-role">Membro da Comunidade Acadêmica</div>
                            </div>
                        </div>

                        <div class="user-details">
                            <div class="detail-item">
                                <div class="detail-label">Identificação</div>
                                <div class="detail-value">{_esc(usuario.id)}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Email Institucional</div>
                                <div class="detail-value">{_esc(usuario.email)}</div>
                            </div>
                        </div>

                        <div class="user-type-badge {type_class}">
                            <span>{icon}</span>
                            <span>{_esc(usuario.type)}</span>
                        </div>
                    </div>
                    """
            with open("View_and_Interface/listar_usuarios.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            conteudo = conteudo.replace("<!--USUARIOS-->", resposta)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        elif self.path == "/relatorios":
            resposta = ""
            resposta += '<!DOCTYPE html>'
            resposta += '<html lang="pt-BR">'
            resposta += '<head>'
            resposta += '<meta charset="UTF-8">'
            resposta += '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            resposta += '<title>Relatórios Executivos - Sistema de Biblioteca</title>'
            resposta += '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">'
            resposta += '<style>'
            resposta += '*{margin:0;padding:0;box-sizing:border-box}'
            resposta += 'body{font-family:Inter,sans-serif;background:#f8fafc;min-height:100vh;color:#1e293b;padding:20px}'
            resposta += '.header{background:linear-gradient(135deg,#1e293b,#334155);color:white;padding:50px 20px;text-align:center;margin-bottom:40px;box-shadow:0 4px 6px -1px rgba(0,0,0,0.1)}'
            resposta += '.header h1{font-size:2.5em;font-weight:700;margin-bottom:12px;letter-spacing:-0.025em}'
            resposta += '.header p{font-size:1.125em;opacity:0.9;font-weight:400}'
            resposta += '.container{max-width:1000px;margin:0 auto;background:white;border-radius:16px;padding:50px;box-shadow:0 10px 25px -5px rgba(0,0,0,0.1),0 10px 10px -5px rgba(0,0,0,0.04);border:1px solid #e2e8f0}'
            resposta += '.reports-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:30px;margin:40px 0}'
            resposta += '.report-card{background:white;border:1px solid #e2e8f0;border-radius:12px;padding:32px;text-align:center;transition:all 0.2s ease;box-shadow:0 1px 3px 0 rgba(0,0,0,0.1)}'
            resposta += '.report-card:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,0.15);border-color:#3b82f6}'
            resposta += '.report-card-icon{font-size:3em;margin-bottom:20px;display:block;color:#3b82f6}'
            resposta += '.report-card h3{font-size:1.5em;font-weight:600;margin-bottom:16px;color:#1e293b;letter-spacing:-0.025em}'
            resposta += '.report-card p{color:#64748b;margin-bottom:24px;line-height:1.6;font-weight:400}'
            resposta += '.report-card a{display:inline-flex;align-items:center;gap:8px;padding:12px 20px;background:linear-gradient(135deg,#3b82f6,#1d4ed8);color:white;text-decoration:none;border-radius:8px;font-weight:500;transition:all 0.2s;box-shadow:0 1px 3px 0 rgba(59,130,246,0.3)}'
            resposta += '.report-card a:hover{background:linear-gradient(135deg,#1d4ed8,#1e40af);transform:translateY(-1px);box-shadow:0 4px 12px rgba(59,130,246,0.4)}'
            resposta += '.back-btn{display:inline-flex;align-items:center;gap:8px;margin-top:40px;padding:12px 24px;background:#64748b;color:white;text-decoration:none;border-radius:8px;font-weight:500;transition:all 0.2s}'
            resposta += '.back-btn:hover{background:#475569;transform:translateY(-1px)}'
            resposta += '@media(max-width:768px){.container{padding:30px 20px}.reports-grid{grid-template-columns:1fr;gap:24px}.header{padding:40px 20px}.header h1{font-size:2em}}'
            resposta += '</style>'
            resposta += '</head>'
            resposta += '<body>'
            resposta += '<div class="header">'
            resposta += '<h1>Relatórios e Analytics</h1>'
            resposta += '<p>Análises estatísticas e métricas do sistema bibliotecário</p>'
            resposta += '</div>'
            resposta += '<div class="container">'
            resposta += '<div class="reports-grid">'
            resposta += '<div class="report-card">'
            resposta += '<span class="report-card-icon"><i class="fas fa-book"></i></span>'
            resposta += '<h3>Análise de Acervo</h3>'
            resposta += '<p>Relatório detalhado dos livros mais emprestados, identificando tendências de demanda e preferências dos usuários.</p>'
            resposta += '<a href="/relatorios_livros"><i class="fas fa-chart-line"></i> Ver Relatório de Livros</a>'
            resposta += '</div>'
            resposta += '<div class="report-card">'
            resposta += '<span class="report-card-icon"><i class="fas fa-users"></i></span>'
            resposta += '<h3>Perfil dos Usuários</h3>'
            resposta += '<p>Métricas sobre o comportamento dos usuários, destacando os mais ativos e padrões de utilização.</p>'
            resposta += '<a href="/relatorios_usuarios"><i class="fas fa-chart-bar"></i> Ver Relatório de Usuários</a>'
            resposta += '</div>'
            resposta += '</div>'
            resposta += '<div style="text-align:center">'
            resposta += '<a href="/menu" class="back-btn"><i class="fas fa-arrow-left"></i> Retornar ao Portal</a>'
            resposta += '</div>'
            resposta += '</div>'
            resposta += '</body>'
            resposta += '</html>'

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(resposta.encode("utf-8"))

        elif self.path == "/relatorios_livros":
            resposta = ""
            resposta += '<!DOCTYPE html>'
            resposta += '<html lang="pt-BR">'
            resposta += '<head>'
            resposta += '<meta charset="UTF-8">'
            resposta += '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            resposta += '<title>Análise de Acervo - Sistema de Biblioteca</title>'
            resposta += '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">'
            resposta += '<style>'
            resposta += '*{margin:0;padding:0;box-sizing:border-box}'
            resposta += 'body{font-family:Inter,sans-serif;background:#f8fafc;min-height:100vh;color:#1e293b;padding:20px}'
            resposta += '.header{background:linear-gradient(135deg,#1e293b,#334155);color:white;padding:50px 20px;text-align:center;margin-bottom:40px;box-shadow:0 4px 6px -1px rgba(0,0,0,0.1)}'
            resposta += '.header h1{font-size:2.5em;font-weight:700;margin-bottom:12px;letter-spacing:-0.025em}'
            resposta += '.header p{font-size:1.125em;opacity:0.9;font-weight:400}'
            resposta += '.container{max-width:1200px;margin:0 auto;background:white;border-radius:16px;padding:50px;box-shadow:0 10px 25px -5px rgba(0,0,0,0.1),0 10px 10px -5px rgba(0,0,0,0.04);border:1px solid #e2e8f0}'
            resposta += '.report-title{text-align:center;margin-bottom:40px}'
            resposta += '.report-title h1{font-size:2em;font-weight:600;color:#1e293b;margin-bottom:8px;letter-spacing:-0.025em}'
            resposta += '.report-title p{color:#64748b;font-size:1em;font-weight:400}'
            resposta += 'table{width:100%;border-collapse:collapse;margin:30px 0;border-radius:12px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,0.05)}'
            resposta += 'thead{background:linear-gradient(135deg,#3b82f6,#1d4ed8);color:white}'
            resposta += 'th,td{padding:16px 20px;text-align:left;border-bottom:1px solid #e5e7eb}'
            resposta += 'tbody tr:hover{background:#f8fafc}'
            resposta += 'tbody tr:nth-child(even){background:#f9fafb}'
            resposta += '.position-badge{display:inline-block;width:40px;height:40px;background:linear-gradient(135deg,#f59e0b,#d97706);color:white;border-radius:50%;text-align:center;line-height:40px;font-weight:700;margin-right:16px}'
            resposta += '.book-info{display:flex;align-items:center}'
            resposta += '.book-details h4{margin:0 0 4px 0;font-weight:600;color:#1e293b;font-size:1em}'
            resposta += '.book-details p{margin:0;color:#64748b;font-size:0.875em}'
            resposta += '.loans-count{font-weight:700;color:#3b82f6;text-align:center;font-size:1.125em}'
            resposta += '.no-data{text-align:center;color:#64748b;padding:60px 40px;border:2px dashed #e2e8f0;border-radius:12px;margin:40px 0;background:#f8fafc}'
            resposta += '.actions{text-align:center;margin-top:40px}'
            resposta += '.btn{display:inline-flex;align-items:center;gap:8px;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:500;transition:all 0.2s;margin:0 8px}'
            resposta += '.btn-primary{background:linear-gradient(135deg,#3b82f6,#1d4ed8);color:white;box-shadow:0 1px 3px 0 rgba(59,130,246,0.3)}'
            resposta += '.btn-primary:hover{background:linear-gradient(135deg,#1d4ed8,#1e40af);transform:translateY(-1px);box-shadow:0 4px 12px rgba(59,130,246,0.4)}'
            resposta += '.btn-secondary{background:#64748b;color:white}'
            resposta += '.btn-secondary:hover{background:#475569;transform:translateY(-1px)}'
            resposta += '@media(max-width:768px){.container{padding:30px 20px}.header{padding:40px 20px}.header h1{font-size:2em}table{font-size:0.875em}th,td{padding:12px 16px}}'
            resposta += '</style>'
            resposta += '</head>'
            resposta += '<body>'
            resposta += '<div class="header">'
            resposta += '<h1>Análise de Acervo</h1>'
            resposta += '<p>Relatório de livros mais emprestados</p>'
            resposta += '</div>'
            resposta += '<div class="container">'
            resposta += '<div class="report-title">'
            resposta += '<h1>Ranking de Popularidade</h1>'
            resposta += '<p>Métricas de demanda por título bibliográfico</p>'
            resposta += '</div>'

            # Obter dados para o relatório
            emprestimos = controller.get_emprestimos()
            livros = controller.get_livros()
            # relatorio_livros = report_service.get_most_borrowed_books(emprestimos, livros)
            relatorio_livros = []  # Temporário para debug

            if relatorio_livros:
                resposta += '<table>'
                resposta += '<thead>'
                resposta += '<tr>'
                resposta += '<th>Posição</th>'
                resposta += '<th>Título do Livro</th>'
                resposta += '<th>Autor</th>'
                resposta += '<th>Total de Empréstimos</th>'
                resposta += '</tr>'
                resposta += '</thead>'
                resposta += '<tbody>'

                for i, livro in enumerate(relatorio_livros, 1):
                    titulo = livro.get('title', f'ID: {livro.get("book_id", "N/A")}')
                    autor = livro.get('author', 'N/A')
                    emprestimos_count = livro.get('loan_count', 0)

                    resposta += '<tr>'
                    resposta += f'<td><span class="position-badge">{i}</span></td>'
                    resposta += '<td>'
                    resposta += '<div class="book-info">'
                    resposta += f'<div class="book-details"><h4>{_esc(titulo)}</h4><p>Livro técnico</p></div>'
                    resposta += '</div>'
                    resposta += '</td>'
                    resposta += f'<td>{_esc(autor)}</td>'
                    resposta += f'<td><span class="loans-count">{emprestimos_count}</span></td>'
                    resposta += '</tr>'

                resposta += '</tbody>'
                resposta += '</table>'
            else:
                resposta += '<div class="no-data">'
                resposta += '<p>Nenhum empréstimo registrado no sistema ainda.</p>'
                resposta += '<p>Os dados aparecerão aqui após a realização dos primeiros empréstimos.</p>'
                resposta += '</div>'

            resposta += '<div class="actions">'
            resposta += '<a href="/relatorios" class="btn btn-secondary"><i class="fas fa-arrow-left"></i> Retornar aos Relatórios</a>'
            resposta += '<a href="/menu" class="btn btn-primary"><i class="fas fa-home"></i> Ir para o Portal</a>'
            resposta += '</div>'
            resposta += '</div>'
            resposta += '</body>'
            resposta += '</html>'

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(resposta.encode("utf-8"))

        elif self.path == "/relatorios_usuarios":
            resposta = ""
            resposta += '<!DOCTYPE html>'
            resposta += '<html lang="pt-BR">'
            resposta += '<head>'
            resposta += '<meta charset="UTF-8">'
            resposta += '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            resposta += '<title>Perfil dos Usuários - Sistema de Biblioteca</title>'
            resposta += '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">'
            resposta += '<style>'
            resposta += '*{margin:0;padding:0;box-sizing:border-box}'
            resposta += 'body{font-family:Inter,sans-serif;background:#f8fafc;min-height:100vh;color:#1e293b;padding:20px}'
            resposta += '.header{background:linear-gradient(135deg,#1e293b,#334155);color:white;padding:50px 20px;text-align:center;margin-bottom:40px;box-shadow:0 4px 6px -1px rgba(0,0,0,0.1)}'
            resposta += '.header h1{font-size:2.5em;font-weight:700;margin-bottom:12px;letter-spacing:-0.025em}'
            resposta += '.header p{font-size:1.125em;opacity:0.9;font-weight:400}'
            resposta += '.container{max-width:1200px;margin:0 auto;background:white;border-radius:16px;padding:50px;box-shadow:0 10px 25px -5px rgba(0,0,0,0.1),0 10px 10px -5px rgba(0,0,0,0.04);border:1px solid #e2e8f0}'
            resposta += '.report-title{text-align:center;margin-bottom:40px}'
            resposta += '.report-title h1{font-size:2em;font-weight:600;color:#1e293b;margin-bottom:8px;letter-spacing:-0.025em}'
            resposta += '.report-title p{color:#64748b;font-size:1em;font-weight:400}'
            resposta += 'table{width:100%;border-collapse:collapse;margin:30px 0;border-radius:12px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,0.05)}'
            resposta += 'thead{background:linear-gradient(135deg,#3b82f6,#1d4ed8);color:white}'
            resposta += 'th,td{padding:16px 20px;text-align:left;border-bottom:1px solid #e5e7eb}'
            resposta += 'tbody tr:hover{background:#f8fafc}'
            resposta += 'tbody tr:nth-child(even){background:#f9fafb}'
            resposta += '.position-badge{display:inline-block;width:40px;height:40px;background:linear-gradient(135deg,#f59e0b,#d97706);color:white;border-radius:50%;text-align:center;line-height:40px;font-weight:700;margin-right:16px}'
            resposta += '.user-info{display:flex;align-items:center}'
            resposta += '.user-avatar{width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#f1f5f9,#e2e8f0);display:flex;align-items:center;justify-content:center;margin-right:16px;font-size:1.2em;color:#64748b;border:1px solid #cbd5e1}'
            resposta += '.user-details h4{margin:0 0 4px 0;font-weight:600;color:#1e293b;font-size:1em}'
            resposta += '.user-details p{margin:0;color:#64748b;font-size:0.875em}'
            resposta += '.user-type{display:inline-block;padding:4px 12px;background:#dcfce7;color:#166534;border:1px solid #bbf7d0;border-radius:16px;font-size:0.8em;font-weight:600;margin-left:8px}'
            resposta += '.loans-count{font-weight:700;color:#3b82f6;text-align:center;font-size:1.125em}'
            resposta += '.no-data{text-align:center;color:#64748b;padding:60px 40px;border:2px dashed #e2e8f0;border-radius:12px;margin:40px 0;background:#f8fafc}'
            resposta += '.actions{text-align:center;margin-top:40px}'
            resposta += '.btn{display:inline-flex;align-items:center;gap:8px;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:500;transition:all 0.2s;margin:0 8px}'
            resposta += '.btn-primary{background:linear-gradient(135deg,#3b82f6,#1d4ed8);color:white;box-shadow:0 1px 3px 0 rgba(59,130,246,0.3)}'
            resposta += '.btn-primary:hover{background:linear-gradient(135deg,#1d4ed8,#1e40af);transform:translateY(-1px);box-shadow:0 4px 12px rgba(59,130,246,0.4)}'
            resposta += '.btn-secondary{background:#64748b;color:white}'
            resposta += '.btn-secondary:hover{background:#475569;transform:translateY(-1px)}'
            resposta += '@media(max-width:768px){.container{padding:30px 20px}.header{padding:40px 20px}.header h1{font-size:2em}table{font-size:0.875em}th,td{padding:12px 16px}}'
            resposta += '</style>'
            resposta += '</head>'
            resposta += '<body>'
            resposta += '<div class="header">'
            resposta += '<h1>Perfil dos Usuários</h1>'
            resposta += '<p>Relatório de usuários mais ativos</p>'
            resposta += '</div>'
            resposta += '<div class="container">'
            resposta += '<div class="report-title">'
            resposta += '<h1>Ranking de Atividade</h1>'
            resposta += '<p>Métricas de engajamento e frequência de empréstimos</p>'
            resposta += '</div>'

            # Obter dados para o relatório
            emprestimos = controller.get_emprestimos()
            usuarios = controller.get_usuarios()
            # relatorio_usuarios = report_service.get_most_active_users(emprestimos, usuarios)
            relatorio_usuarios = []  # Temporário para debug

            if relatorio_usuarios:
                resposta += '<table>'
                resposta += '<thead>'
                resposta += '<tr>'
                resposta += '<th>Posição</th>'
                resposta += '<th>Usuário</th>'
                resposta += '<th>Email</th>'
                resposta += '<th>Categoria</th>'
                resposta += '<th>Total de Empréstimos</th>'
                resposta += '</tr>'
                resposta += '</thead>'
                resposta += '<tbody>'

                for i, usuario in enumerate(relatorio_usuarios, 1):
                    nome = usuario.get('name', f'ID: {usuario.get("user_id", "N/A")}')
                    email = usuario.get('email', 'N/A')
                    tipo = usuario.get('type', 'N/A')
                    emprestimos_count = usuario.get('loan_count', 0)

                    # Emoji baseado no tipo de usuário
                    avatar_emoji = "🎓" if tipo == "Estudante" else "👨‍🏫" if tipo == "Professor" else "👔"

                    resposta += '<tr>'
                    resposta += f'<td><span class="position-badge">{i}</span></td>'
                    resposta += '<td>'
                    resposta += '<div class="user-info">'
                    resposta += f'<div class="user-avatar">{avatar_emoji}</div>'
                    resposta += f'<div class="user-details"><h4>{_esc(nome)}</h4><p>ID: {usuario.get("user_id", "N/A")}</p></div>'
                    resposta += '</div>'
                    resposta += '</td>'
                    resposta += f'<td>{_esc(email)}</td>'
                    resposta += f'<td><span class="user-type">{_esc(tipo)}</span></td>'
                    resposta += f'<td><span class="loans-count">{emprestimos_count}</span></td>'
                    resposta += '</tr>'

                resposta += '</tbody>'
                resposta += '</table>'
            else:
                resposta += '<div class="no-data">'
                resposta += '<p>Nenhum empréstimo registrado no sistema ainda.</p>'
                resposta += '<p>Os dados aparecerão aqui após a realização dos primeiros empréstimos.</p>'
                resposta += '</div>'

            resposta += '<div class="actions">'
            resposta += '<a href="/relatorios" class="btn btn-secondary"><i class="fas fa-arrow-left"></i> Retornar aos Relatórios</a>'
            resposta += '<a href="/menu" class="btn btn-primary"><i class="fas fa-home"></i> Ir para o Portal</a>'
            resposta += '</div>'
            resposta += '</div>'
            resposta += '</body>'
            resposta += '</html>'

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(resposta.encode("utf-8"))

        elif self.path == "/listar_livros":
            resposta = ""
            cards = []
            # Filtrar apenas livros com todos os campos preenchidos
            livros_validos = [
                l for l in controller.get_livros()
                if l.id and l.title and l.author and l.isbn and
                   str(l.id).strip() and str(l.title).strip() and
                   str(l.author).strip() and str(l.isbn).strip()
            ]

            # FONTE DA VERDADE: empréstimos ativos determinam status dos livros
            emprestimos_ativos_set = {
                str(e.book_id).strip() for e in controller.get_emprestimos() if (e.return_date is None)
            }

            if not livros_validos:
                resposta = '<div class="no-users">Nenhum livro cadastrado com dados completos.</div>'
            else:
                for livro in livros_validos:
                    # Verificar status baseado em empréstimos ativos (fonte da verdade)
                    is_borrowed = (str(livro.id).strip() in emprestimos_ativos_set)
                    status = "Emprestado" if is_borrowed else "Disponível"
                    status_class = "status-borrowed" if is_borrowed else "status-available"
                    icon = "🔒" if is_borrowed else "📚"

                    # Determinar categoria baseada no título (simplificado)
                    categoria = "Livro Técnico"
                    if "Python" in livro.title or "JavaScript" in livro.title or "Java" in livro.title:
                        categoria = "Programação"
                    elif "Banco" in livro.title or "MongoDB" in livro.title or "SQL" in livro.title:
                        categoria = "Banco de Dados"
                    elif "Cálculo" in livro.title or "Matemática" in livro.title or "Estatística" in livro.title:
                        categoria = "Matemática"
                    elif "Engenharia" in livro.title or "Scrum" in livro.title or "TDD" in livro.title:
                        categoria = "Engenharia de Software"
                    elif "Algoritmos" in livro.title or "Estrutura" in livro.title:
                        categoria = "Ciência da Computação"
                    elif "1984" in livro.title or "Dom Casmurro" in livro.title:
                        categoria = "Literatura"

                    cards.append(f"""
                    <div class="book-card">
                        <div class="book-header">
                            <div class="book-icon">{icon}</div>
                            <div class="book-title-section">
                                <h3>{_esc(livro.title)}</h3>
                                <div class="book-category">{categoria}</div>
                            </div>
                        </div>

                        <div class="book-details">
                            <div class="detail-item">
                                <div class="detail-label">Autor</div>
                                <div class="detail-value">{_esc(livro.author)}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Código ISBN</div>
                                <div class="detail-value">{_esc(livro.isbn)}</div>
                            </div>
                        </div>

                        <div class="status-section">
                            <div class="status-badge {status_class}">
                                <span>{icon}</span>
                                <span>{status}</span>
                            </div>
                        </div>
                    </div>
                    """)
                resposta = "".join(cards)
            with open("View_and_Interface/listar_livros.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            conteudo = conteudo.replace("<!--LIVROS-->", resposta)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        elif self.path == "/listar_emprestimos":
            resposta = ""
            # Obter todos os livros emprestados (fonte da verdade dos empréstimos ativos)
            emprestimos_ativos_set = {
                str(e.book_id).strip() for e in controller.get_emprestimos() if (e.return_date is None)
            }

            # Filtrar livros emprestados com dados válidos
            livros_emprestados = [
                l for l in controller.get_livros()
                if l.id and l.title and l.author and l.isbn and
                   str(l.id).strip() and str(l.title).strip() and
                   str(l.author).strip() and str(l.isbn).strip() and
                   (str(l.id).strip() in emprestimos_ativos_set)  # Livro tem empréstimo ativo
            ]

            if not livros_emprestados:
                resposta = '<div class="no-users">Nenhum livro emprestado no momento.</div>'
            else:
                for livro in livros_emprestados:
                    # Buscar o empréstimo ativo para este livro
                    emprestimo_ativo = None
                    for e in controller.get_emprestimos():
                        if str(e.book_id).strip() == str(livro.id).strip() and e.return_date is None:
                            emprestimo_ativo = e
                            break

                    if emprestimo_ativo:
                        usuario = controller.get_usuario_por_id(emprestimo_ativo.user_id)
                        usuario_nome = usuario.name if usuario else "Usuário não encontrado"
                        data_devolucao = "Não devolvido"
                        status_class = "status-active"
                        status_text = "Em andamento"
                        icon = "📖"
                        emprestimo_id = emprestimo_ativo.id
                        data_emprestimo = emprestimo_ativo.loan_date.strftime("%d/%m/%Y")
                    else:
                        # Fallback se não encontrar empréstimo (não deveria acontecer)
                        usuario_nome = "Dados não disponíveis"
                        data_devolucao = "Não devolvido"
                        status_class = "status-active"
                        status_text = "Em andamento"
                        icon = "📖"
                        emprestimo_id = f"temp_{livro.id}"
                        data_emprestimo = "Data não disponível"

                    resposta += f"""
                    <div class="loan-card">
                        <div class="loan-header">
                            <div class="loan-icon">{icon}</div>
                            <div class="loan-info">
                                <h3>{_esc(livro.title)}</h3>
                                <div class="loan-id">Empréstimo {_esc(emprestimo_id)}</div>
                            </div>
                        </div>

                        <div class="loan-details">
                            <div class="detail-item">
                                <div class="detail-label">Usuário Responsável</div>
                                <div class="detail-value">{_esc(usuario_nome)}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Data do Empréstimo</div>
                                <div class="detail-value">{data_emprestimo}</div>
                            </div>
                        </div>

                        <div class="status-section">
                            <div class="status-badge {status_class}">
                                <span>{icon}</span>
                                <span>{status_text}</span>
                            </div>
                        </div>
                    </div>
                    """
            with open("View_and_Interface/listar_emprestimos.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            conteudo = conteudo.replace("<!--EMPRESTIMOS-->", resposta)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))



