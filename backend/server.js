const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const port = 5000;

// Configurar CORS
app.use(cors());
app.use(bodyParser.json());

// Conectar ao Banco de Dados MySQL
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'Pizzaria@123',
  database: 'pizzaria'
});

db.connect((err) => {
  if (err) {
    console.error('Erro de conexão com o banco de dados:', err);
  } else {
    console.log('Conectado ao banco de dados MySQL');
  }
});

// Endpoint para obter todos os sabores de pizza
app.get('/pizzas', (req, res) => {
  db.query('SELECT * FROM pizzas', (err, results) => {
    if (err) {
      res.status(500).json({ message: 'Erro ao buscar pizzas' });
    } else {
      res.status(200).json(results);
    }
  });
});

// Endpoint para obter todas as bebidas
app.get('/bebidas', (req, res) => {
  db.query('SELECT * FROM bebidas', (err, results) => {
    if (err) {
      res.status(500).json({ message: 'Erro ao buscar bebidas' });
    } else {
      res.status(200).json(results);
    }
  });
});

// Endpoint para criar um pedido
app.post('/pedidos', (req, res) => {
  const { cliente_id, pizza_id, bebida_id, borda_id, quantidade, valor_total } = req.body;

  db.query('INSERT INTO pedidos (cliente_id, status, valor_total) VALUES (?, ?, ?)', 
    [cliente_id, 'Em preparo', valor_total], (err, results) => {
      if (err) {
        res.status(500).json({ message: 'Erro ao criar o pedido' });
      } else {
        const pedido_id = results.insertId;

        db.query('INSERT INTO itens_pedido (pedido_id, pizza_id, bebida_id, borda_id, quantidade) VALUES (?, ?, ?, ?, ?)', 
          [pedido_id, pizza_id, bebida_id, borda_id, quantidade], (err) => {
            if (err) {
              res.status(500).json({ message: 'Erro ao adicionar itens no pedido' });
            } else {
              res.status(200).json({ message: 'Pedido realizado com sucesso', pedido_id });
            }
          });
      }
    });
});

// Iniciar o servidor
app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});
