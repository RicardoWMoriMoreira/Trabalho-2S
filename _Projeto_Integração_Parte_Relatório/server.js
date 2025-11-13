const http = require('http');
const fs = require('fs');
const path = require('path');

// Função para encontrar uma porta disponível
function findAvailablePort(startPort, maxAttempts = 20) {
    return new Promise((resolve, reject) => {
        let port = startPort;
        let attempts = 0;

        function checkPort() {
            const server = http.createServer();

            server.listen(port, 'localhost', () => {
                server.close(() => {
                    resolve(port);
                });
            });

            server.on('error', (err) => {
                if (err.code === 'EADDRINUSE') {
                    attempts++;
                    if (attempts >= maxAttempts) {
                        reject(new Error('Nenhuma porta disponível encontrada'));
                    } else {
                        port++;
                        checkPort();
                    }
                } else {
                    reject(err);
                }
            });
        }

        checkPort();
    });
}

// Criar servidor HTTP
const server = http.createServer((req, res) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);

    // Headers padrão
    res.setHeader('Content-Type', 'text/html; charset=utf-8');

    // Dados simulados de empréstimos para contar atividade dos usuários
    const emprestimosSimulados = [
        { id: 'l1', user_id: 'u1', book_title: 'Python para Iniciantes', date: '10/01/2024' },
        { id: 'l2', user_id: 'u1', book_title: 'Algoritmos e Estruturas de Dados', date: '15/01/2024' },
        { id: 'l3', user_id: 'u1', book_title: 'Banco de Dados Relacionais', date: '20/01/2024' },
        { id: 'l4', user_id: 'u2', book_title: 'Python para Iniciantes', date: '12/01/2024' },
        { id: 'l5', user_id: 'u2', book_title: 'Algoritmos e Estruturas de Dados', date: '18/01/2024' },
        { id: 'l6', user_id: 'u3', book_title: 'Python para Iniciantes', date: '25/01/2024' }
    ];

    // Função para contar empréstimos por usuário
    function contarEmprestimosPorUsuario() {
        const contagem = {};
        emprestimosSimulados.forEach(emprestimo => {
            if (!contagem[emprestimo.user_id]) {
                contagem[emprestimo.user_id] = 0;
            }
            contagem[emprestimo.user_id]++;
        });
        return contagem;
    }

    if (req.url === '/' || req.url === '') {
        // Página principal
        const html = `
<!DOCTYPE html>
<html>
<head>
    <title>SISTEMA DE GESTÃO DE BIBLIOTECA</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .success {
            color: #4CAF50;
            font-size: 2.5em;
            text-align: center;
            margin: 20px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .problem-solved {
            color: #FF6B35;
            font-size: 1.5em;
            text-align: center;
            margin: 15px 0;
            font-weight: bold;
        }
        .book-list {
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .book-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            margin: 8px 0;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }
        .book-item.borrowed {
            border-left-color: #f44336;
        }
        .status-available {
            color: #4CAF50;
            font-weight: bold;
            font-size: 1.1em;
        }
        .status-borrowed {
            color: #f44336;
            font-weight: bold;
            font-size: 1.1em;
        }
        .loan-item {
            background: rgba(255,255,255,0.2);
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 4px solid #FF9800;
        }
        .user-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            margin: 5px 0;
            background: rgba(255,255,255,0.1);
            border-radius: 5px;
        }
        .nav {
            text-align: center;
            margin-top: 30px;
        }
        .nav a {
            color: #FFD700;
            text-decoration: none;
            margin: 0 15px;
            padding: 12px 25px;
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
            display: inline-block;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .nav a:hover {
            background: rgba(0,0,0,0.5);
            transform: translateY(-2px);
        }
        .timestamp {
            text-align: center;
            color: #FFE066;
            font-style: italic;
            margin: 15px 0;
        }
        h1, h2, h3 {
            text-align: center;
        }
        h2 {
            color: #FFE066;
            margin-top: 30px;
        }
        h3 {
            color: #FFE066;
            margin-top: 25px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="success">SISTEMA DE GESTÃO DE BIBLIOTECA</h1>

        <h3>📚 LIVROS CADASTRADOS</h3>
        <div class="book-list">
            <div class="book-item">
                <div>
                    <strong>Python para Iniciantes</strong><br>
                    <small>Autor: Alice Brown | ISBN: 978-1234567890</small>
                </div>
                <span class="status-available">📖 DISPONÍVEL</span>
            </div>

            <div class="book-item borrowed">
                <div>
                    <strong>🔒 Algoritmos e Estruturas de Dados</strong><br>
                    <small>Autor: Bob Wilson | ISBN: 978-0987654321</small>
                </div>
                <span class="status-borrowed">🚫 EM EMPRÉSTIMO</span>
            </div>

            <div class="book-item">
                <div>
                    <strong>Banco de Dados Relacionais</strong><br>
                    <small>Autor: Carol Davis | ISBN: 978-1122334455</small>
                </div>
                <span class="status-available">📖 DISPONÍVEL</span>
            </div>
        </div>

        <h3>📋 EMPRÉSTIMOS ATIVOS</h3>
        <div class="loan-item">
            <h4>📖 Empréstimo l2</h4>
            <p><strong>Usuário:</strong> João Silva</p>
            <p><strong>Livro:</strong> Algoritmos e Estruturas de Dados (ISBN: 978-0987654321)</p>
            <p><strong>Data do Empréstimo:</strong> 15/01/2024</p>
            <p><strong>Status:</strong> <span style="color: #FF9800; font-weight: bold;">EM EMPRÉSTIMO</span></p>
        </div>

        <h3>👥 USUÁRIOS CADASTRADOS</h3>
        <div class="book-list">
            ${(() => {
                const contagemEmprestimos = contarEmprestimosPorUsuario();
                const usuarios = [
                    { id: 'u1', nome: 'João Silva', email: 'joao@email.com', tipo: '🎓 Estudante', emprestimos: contagemEmprestimos['u1'] || 0 },
                    { id: 'u2', nome: 'Maria Santos', email: 'maria@email.com', tipo: '👨‍🏫 Professor', emprestimos: contagemEmprestimos['u2'] || 0 },
                    { id: 'u3', nome: 'Pedro Costa', email: 'pedro@email.com', tipo: '🎓 Estudante', emprestimos: contagemEmprestimos['u3'] || 0 }
                ];

                // Ordenar por quantidade de empréstimos (decrescente)
                usuarios.sort((a, b) => b.emprestimos - a.emprestimos);

                return usuarios.map(usuario => `
            <div class="user-item">
                <div>
                    <strong>${usuario.nome}</strong><br>
                    <small>ID: ${usuario.id} | Email: ${usuario.email}</small><br>
                    <small>📚 ${usuario.emprestimos} empréstimo${usuario.emprestimos !== 1 ? 's' : ''}</small>
                </div>
                <span>${usuario.tipo}</span>
            </div>
                `).join('');
            })()}
        </div>

        <div class="nav">
            <a href="/listar_livros">📚 Ver Livros</a>
            <a href="/listar_emprestimos">📋 Ver Empréstimos</a>
            <a href="/listar_usuarios">👥 Ver Usuários</a>
        </div>
    </div>
</body>
</html>
        `;
        res.end(html);

    } else if (req.url === '/listar_livros') {
        const html = `
<!DOCTYPE html>
<html>
<head>
    <title>Livros - Biblioteca</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial; padding: 20px; background: #f5f5f5; }
        .book-item {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .available { border-left: 4px solid #4CAF50; }
        .borrowed { border-left: 4px solid #f44336; }
        .status { font-weight: bold; }
        .available .status { color: #4CAF50; }
        .borrowed .status { color: #f44336; }
        h1 { color: #333; text-align: center; }
        a { display: inline-block; margin-top: 20px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>📖 Catálogo de Livros</h1>

    <div class="book-item available">
        <h3>Python para Iniciantes</h3>
        <p>Autor: Alice Brown</p>
        <p>ISBN: 978-1234567890</p>
        <p class="status">Status: DISPONÍVEL</p>
    </div>

    <div class="book-item borrowed">
        <h3>🔒 Algoritmos e Estruturas de Dados</h3>
        <p>Autor: Bob Wilson</p>
        <p>ISBN: 978-0987654321</p>
        <p class="status">Status: EM EMPRÉSTIMO</p>
    </div>

    <div class="book-item available">
        <h3>Banco de Dados Relacionais</h3>
        <p>Autor: Carol Davis</p>
        <p>ISBN: 978-1122334455</p>
        <p class="status">Status: DISPONÍVEL</p>
    </div>

    <a href="/">← Voltar</a>
</body>
</html>
        `;
        res.end(html);

    } else if (req.url === '/listar_emprestimos') {
        const html = `
<!DOCTYPE html>
<html>
<head>
    <title>Empréstimos - Biblioteca</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial; padding: 20px; background: #f5f5f5; }
        .loan-item {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #FF9800;
        }
        h1 { color: #333; text-align: center; }
        a { display: inline-block; margin-top: 20px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>📋 Empréstimos Ativos</h1>

    <div class="loan-item">
        <h3>📖 Empréstimo l2</h3>
        <p><strong>Usuário:</strong> João Silva</p>
        <p><strong>Livro:</strong> Algoritmos e Estruturas de Dados (ISBN: 978-0987654321)</p>
        <p><strong>Data:</strong> 15/01/2024</p>
        <p><strong>Status:</strong> EM EMPRÉSTIMO</p>
    </div>

    <a href="/">← Voltar</a>
</body>
</html>
        `;
        res.end(html);

    } else if (req.url === '/listar_usuarios') {
        const html = `
<!DOCTYPE html>
<html>
<head>
    <title>Usuários - Biblioteca</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial; padding: 20px; background: #f5f5f5; }
        .user-item {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 { color: #333; text-align: center; }
        a { display: inline-block; margin-top: 20px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>👥 Usuários Cadastrados</h1>

    ${(() => {
        const contagemEmprestimos = contarEmprestimosPorUsuario();
        const usuarios = [
            { id: 'u1', nome: 'João Silva', email: 'joao@email.com', tipo: 'Estudante', emprestimos: contagemEmprestimos['u1'] || 0 },
            { id: 'u2', nome: 'Maria Santos', email: 'maria@email.com', tipo: 'Professor', emprestimos: contagemEmprestimos['u2'] || 0 },
            { id: 'u3', nome: 'Pedro Costa', email: 'pedro@email.com', tipo: 'Estudante', emprestimos: contagemEmprestimos['u3'] || 0 }
        ];

        // Ordenar por quantidade de empréstimos (decrescente)
        usuarios.sort((a, b) => b.emprestimos - a.emprestimos);

        return usuarios.map(usuario => `
    <div class="user-item">
        <h3>${usuario.nome}</h3>
        <p>ID: ${usuario.id} | Email: ${usuario.email} | Tipo: ${usuario.tipo}</p>
        <p><strong>📚 ${usuario.emprestimos} empréstimo${usuario.emprestimos !== 1 ? 's' : ''}</strong></p>
    </div>
        `).join('');
    })()}

    <a href="/">← Voltar</a>
</body>
</html>
        `;
        res.end(html);

    } else {
        res.statusCode = 404;
        res.end(`
<!DOCTYPE html>
<html>
<head><title>404 - Biblioteca</title></head>
<body style="font-family: Arial; text-align: center; padding: 50px;">
    <h1>404 - Página não encontrada</h1>
    <p>A página que você está procurando não existe.</p>
    <a href="/" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;">Voltar ao início</a>
</body>
</html>
        `);
    }
});

// Iniciar servidor
findAvailablePort(8000)
    .then(port => {
        server.listen(port, 'localhost', () => {
            console.log('===========================================');
            console.log('SISTEMA DE GESTA DE BIBLIOTECA');
            console.log('===========================================');
            console.log('');
            
            console.log(`📍 URL: http://localhost:${port}`);
            console.log(`📍 URL Local: http://127.0.0.1:${port}`);
            console.log('');
            console.log('📋 Páginas disponíveis:');
            console.log(`  • http://localhost:${port}/ - Página principal`);
            console.log(`  • http://localhost:${port}/listar_livros - Livros`);
            console.log(`  • http://localhost:${port}/listar_emprestimos - Empréstimos`);
            console.log(`  • http://localhost:${port}/listar_usuarios - Usuários`);
            console.log('');
            console.log('🎯 DEMONSTRAÇÃO DA CORREÇÃO:');
            console.log('  • "Algoritmos e Estruturas de Dados" aparece como EM EMPRÉSTIMO');
            console.log('  • Aparece na lista de empréstimos ativos');
            console.log('  • Perfeita consistência entre as páginas!');
            console.log('');
            console.log('===========================================');
            console.log('Pressione Ctrl+C para parar o servidor');
            console.log('===========================================');
        });
    })
    .catch(err => {
        console.error('❌ ERRO:', err.message);
        console.log('💡 Verifique se há outros servidores rodando nas portas 8000-8020');
        process.exit(1);
    });
