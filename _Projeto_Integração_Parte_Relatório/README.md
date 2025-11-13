# Sistema de Gestão Bibliotecária

**Arquitetura MVC seguindo exatamente o padrão PersonalExpenseOrganizer-1**

## 🚀 Como Executar

### Opção 1: Node.js (Mais Fácil - Já Instalado)
```bash
# Execute o arquivo .bat
iniciar_servidor.bat
```

### Opção 2: Python (Recomendado)
```bash
# 1. Instale Python oficial: https://www.python.org/downloads/
# 2. Marque "Add Python to PATH" durante instalação
# 3. Execute:
iniciar_servidor_python.bat
```

### 📱 Acesse no Navegador
- **URL:** http://localhost:8000
- **Menu Principal:** http://localhost:8000/menu
- **Livros:** http://localhost:8000/listar_livros
- **Usuários:** http://localhost:8000/listar_usuarios
- **Empréstimos:** http://localhost:8000/listar_emprestimos

### 🛠️ Solução de Problemas
- **ERRO: Python não encontrado** → Instale Python oficial
- **Porta 8000 ocupada** → Servidor encontra porta disponível automaticamente
- **Página não carrega** → Verifique se servidor está rodando

## 🎯 Visão Geral

Sistema web completo para gestão de biblioteca universitária, desenvolvido seguindo **rigorosamente** o padrão arquitetural **MVC (Model-View-Controller)** do projeto de referência **PersonalExpenseOrganizer-1**.

## 🏗️ Arquitetura MVC Identica

### **Estrutura Igual ao PersonalExpenseOrganizer-1:**

```
📁 Projeto/
├── 📄 main.py                 # 🚀 Ponto de entrada da aplicação
├── 📄 controler.py           # 🎮 Controlador (lógica de negócio)
├── 📁 Model/                 # 💾 Camada de dados
│   ├── 📄 model.py          # 🗄️ Modelo de dados e banco
│   └── 📄 ...
├── 📁 View_and_Interface/    # 🎨 Camada de apresentação
│   ├── 📄 view.py           # 🌐 Controlador web HTTP
│   └── 📄 *.html            # 📱 Templates HTML
└── 📁 config/               # ⚙️ Configurações
    └── 📄 database.py       # 🛢️ Configuração do banco
```

### **Fluxo de Dados (MVC Puro):**
```
👤 Usuário → 🌐 View (HTML) → 🎮 Controller → 💾 Model → 🗄️ Database
```

## 🚀 Como Executar

### **Modo Recomendado (igual PersonalExpenseOrganizer-1):**
```bash
# 1. Execute diretamente (sem MongoDB necessário)
python main.py
```

### **Modo MongoDB (opcional):**
```bash
# 1. Instalar e iniciar MongoDB
# 2. Popular dados de exemplo
python populate_sample_data.py

# 3. Executar aplicação
python src/main.py
```

### **Acesso:**
- 🌐 **URL**: http://localhost:8000
- 🎨 **Interface**: Moderna, profissional e responsiva

## 📊 Funcionalidades

### **🎓 Gestão de Usuários**
- 👥 Cadastro de estudantes, professores e funcionários
- 🔍 Busca e listagem organizada
- 📧 Controle de emails institucionais

### **📚 Catálogo Inteligente**
- 📖 Cadastro completo de livros
- 🏷️ Organização por categorias
- 🔍 Busca avançada
- 📊 Controle de disponibilidade

### **📋 Controle Operacional**
- 📝 Registro de empréstimos
- ⏰ Controle de prazos
- 🔄 Gestão de devoluções
- 📈 Histórico completo

### **📊 Analytics e Relatórios**
- 📈 Relatórios de livros mais emprestados
- 👤 Perfil de usuários mais ativos
- 📊 Métricas de utilização

## 🗄️ Banco de Dados

### **Modo Duplo (igual PersonalExpenseOrganizer-1):**

#### **1. Memória (Padrão - Sem Dependências)**
- ✅ **Funcionamento imediato** (igual PersonalExpenseOrganizer-1)
- ✅ **Dados em RAM** - sem instalação de MongoDB
- ✅ **Carregamento automático** de dados exemplo
- ✅ **Perfeito para desenvolvimento/teste**

#### **2. MongoDB (Produção)**
```python
# Arquivo: config/database.py
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=biblioteca_universitaria
```

## 🎨 Interface Moderna Profissional

### **Design Corporativo:**
- 🎯 **Cores Sórias**: Azul, cinza, branco (profissional)
- 📱 **Totalmente Responsiva**: Desktop, tablet, mobile
- ⚡ **Performance Otimizada**: Animações sutis e eficientes
- ♿ **Acessibilidade**: Contraste adequado, navegação por teclado

### **Páginas Principais:**
- 🏠 **Menu**: Portal administrativo central
- 👥 **Usuários**: Gestão completa da comunidade
- 📚 **Livros**: Catálogo inteligente e organizado
- 📋 **Empréstimos**: Controle operacional detalhado
- 📊 **Relatórios**: Analytics avançados e insights

## 🛠️ Tecnologias

- **🐍 Backend**: Python 3.8+ (HTTP Server nativo)
- **💾 Banco**: MongoDB / Memória (fallback automático)
- **🌐 Frontend**: HTML5, CSS3, JavaScript (moderno)
- **🎨 UI/UX**: Design system consistente e profissional
- **📦 Arquitetura**: MVC puro (exatamente igual PersonalExpenseOrganizer-1)

## 👥 Equipe

- **RICARDO WAGNER MORI MOREIRA**
- **PEDRO HENRIQUE DA SILVA**
- **DOUGLAS KENJI MATSUMOTO**
- **VICTOR HUGO RODRIGUES DE OLIVEIRA**
- **VICTOR HUGO SILVA GARCIA**

**Professor:** DACIO

## 🎓 Padrão de Desenvolvimento

Este projeto segue **exatamente** o mesmo padrão arquitetural do **PersonalExpenseOrganizer-1**:

### **✅ Estrutura Identica:**
1. **`main.py`** → Inicialização do servidor HTTP
2. **`controler.py`** → Lógica de negócio e coordenação
3. **`Model/model.py`** → Acesso a dados e persistência
4. **`View_and_Interface/view.py`** → Controlador web e renderização

### **✅ Imports Consistentes:**
```python
# Seguindo exatamente PersonalExpenseOrganizer-1
from Model import model as md
from View_and_Interface import view as vw
import controler as ctl
```

### **✅ Separação de Responsabilidades:**
- **Model**: Dados e regras de negócio
- **View**: Apresentação e interface
- **Controller**: Coordenação e processamento

## 🚀 Status da Implementação

- ✅ **Arquitetura MVC**: Implementada e testada (igual PersonalExpenseOrganizer-1)
- ✅ **Interface Moderna**: Completamente redesenhada (profissional)
- ✅ **Banco Duplo**: MongoDB + Memória (fallback automático)
- ✅ **Padrão Consistente**: 100% compatível com PersonalExpenseOrganizer-1
- ✅ **Documentação**: Completa e detalhada

---

**🏆 Sistema de Gestão Bibliotecária - MVC Professional (Padrão PersonalExpenseOrganizer-1)**
