
# Pizzaria Py

**Pizzaria Py** é um sistema de pedidos de pizzaria desenvolvido com **React** no frontend e **MySQL** no backend. O sistema permite que o usuário selecione o sabor da pizza, bebida, borda, quantidade, cidade (para cálculo de frete) e veja o valor total do pedido.

---

## **Como Executar o Projeto**

Siga os passos abaixo para executar o projeto localmente:

### **Pré-requisitos**

Certifique-se de ter as seguintes ferramentas instaladas em sua máquina:

- **Node.js** - [Baixe o Node.js](https://nodejs.org/)
- **MySQL** - [Baixe o MySQL](https://dev.mysql.com/downloads/installer/)
- **npm** - O npm é instalado automaticamente com o Node.js
- **Git** - [Baixe o Git](https://git-scm.com/)

---

### **Passo 1: Clonando o Repositório**

Primeiro, clone o repositório do GitHub para sua máquina local:

```bash
git clone https://github.com/gustavo-oliveira22/pizzariaPy.git
cd pizzariaPy
```

---

### **Passo 2: Configuração do Backend (MySQL)**

1. **Inicie o MySQL** em seu computador.
2. **Crie o banco de dados** `pizzaria`:

```sql
CREATE DATABASE pizzaria;
```

3. **Crie as tabelas necessárias** no banco de dados:

Execute o seguinte código SQL para criar as tabelas no banco de dados:

```sql
CREATE TABLE pizzas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    preco DECIMAL(10, 2)
);

CREATE TABLE bebidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    preco DECIMAL(10, 2)
);

CREATE TABLE bordas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    preco DECIMAL(10, 2)
);

CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pizza_id INT,
    bebida_id INT,
    borda_id INT,
    quantidade INT,
    cidade VARCHAR(100),
    total DECIMAL(10, 2),
    FOREIGN KEY (pizza_id) REFERENCES pizzas(id),
    FOREIGN KEY (bebida_id) REFERENCES bebidas(id),
    FOREIGN KEY (borda_id) REFERENCES bordas(id)
);
```

4. **Conectar o backend** ao banco de dados:

No arquivo **`backend/server.js`**, configure a conexão com o banco de dados MySQL:

```js
const mysql = require('mysql2');

const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'sua_senha',
  database: 'pizzaria'
});

db.connect((err) => {
  if (err) {
    console.error('Erro de conexão com o banco de dados:', err);
  } else {
    console.log('Conectado ao banco de dados MySQL');
  }
});
```

---

### **Passo 3: Configuração do Frontend (React)**

1. **Instalar as dependências do frontend**:

Na pasta do projeto, execute o comando abaixo para instalar as dependências do frontend:

```bash
cd pizzaria-py
npm install
```

2. **Iniciar o servidor React**:

Execute o comando abaixo para iniciar o servidor React:

```bash
cd pizzaria-py
cd src
npm start
```

Isso abrirá o aplicativo React no navegador, geralmente em `http://localhost:3000`.

---

### **Passo 4: Testar a Aplicação**

Após configurar o backend e o frontend, a aplicação estará disponível. Você pode acessar a página no navegador e fazer pedidos de pizza, selecionando as opções de pizza, bebida, borda, quantidade e cidade.
