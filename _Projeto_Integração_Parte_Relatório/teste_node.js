const http = require('http');

const server = http.createServer((req, res) => {
    res.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'});
    res.end(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>SISTEMA DE GESTA DE BIBLIOTECA</title>
        </head>
        <body>
            <h1>SISTEMA DE GESTA DE BIBLIOTECA</h1>
            <p>Servidor Node.js funcionando!</p>
            <p>✅ Teste bem-sucedido</p>
        </body>
        </html>
    `);
});

server.listen(8000, 'localhost', () => {
    console.log('===========================================');
    console.log('SISTEMA DE GESTA DE BIBLIOTECA');
    console.log('===========================================');
    console.log('✅ Servidor Node.js rodando em http://localhost:8000');
    console.log('Pressione Ctrl+C para parar');
});

server.on('error', (err) => {
    console.error('❌ Erro:', err.message);
});
