import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  // Estados para o pedido
  const [pizza, setPizza] = useState("");
  const [bebida, setBebida] = useState("");
  const [borda, setBorda] = useState("");
  const [quantidade, setQuantidade] = useState(1);
  const [cidade, setCidade] = useState("");
  const [total, setTotal] = useState(0);
  const [pedidoFinalizado, setPedidoFinalizado] = useState(false); // Controlar a finalização do pedido
  const [tempoEntrega, setTempoEntrega] = useState(""); // Tempo de entrega
  const [pizzas, setPizzas] = useState([
    { nome: "Pizza Calabresa", preco: 30.00 },
    { nome: "Pizza Margherita", preco: 28.00 },
    { nome: "Pizza Frango com Catupiry", preco: 32.00 },
    { nome: "Pizza Portuguesa", preco: 35.00 },
    { nome: "Pizza Quatro Queijos", preco: 36.00 },
  ]);
  const [bebidas, setBebidas] = useState([
    { nome: "Coca-Cola", preco: 5.00 },
    { nome: "Pepsi", preco: 4.50 },
    { nome: "Fanta", preco: 4.00 },
    { nome: "Guaraná", preco: 4.00 },
    { nome: "Sprite", preco: 4.50 },
  ]);
  const [bordas, setBordas] = useState([
    { nome: "Tradicional", preco: 0.00 },
    { nome: "Recheada", preco: 5.00 },
  ]);

  // Lista de cidades do Distrito Federal
  const cidadesDF = [
    { nome: "Brasília", frete: 10.00 },
    { nome: "Águas Claras", frete: 12.00 },
    { nome: "Taguatinga", frete: 15.00 },
    { nome: "Ceilândia", frete: 12.00 },
    { nome: "Samambaia", frete: 14.00 },
  ];

  // Função para calcular o valor total do pedido
  const calcularValorTotal = (pizzaPreco, bebidaPreco, bordaPreco, quantidade, frete) => {
    return (pizzaPreco + bebidaPreco + bordaPreco) * quantidade + frete;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const pizzaSelecionada = pizzas.find(p => p.nome === pizza);
    const bebidaSelecionada = bebidas.find(b => b.nome === bebida);
    const bordaSelecionada = bordas.find(b => b.nome === borda);
    const cidadeSelecionada = cidadesDF.find(c => c.nome === cidade);

    if (!cidadeSelecionada) {
      alert("Selecione uma cidade válida!");
      return;
    }

    const frete = cidadeSelecionada.frete;

    const valorTotal = calcularValorTotal(pizzaSelecionada.preco, bebidaSelecionada.preco, bordaSelecionada.preco, quantidade, frete);
    setTotal(valorTotal);

    // Definir o tempo de entrega (simulação simples)
    setTempoEntrega("30-45 minutos");

    // Finalizar o pedido
    setPedidoFinalizado(true);
  };

  return (
    <div className="app">
      {!pedidoFinalizado ? (
        <div>
          <header>
            <h1>Pizzaria Py</h1>
          </header>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Sabor da Pizza</label>
              <select onChange={(e) => setPizza(e.target.value)} required>
                <option value="">Selecione</option>
                {pizzas.map((p, index) => (
                  <option key={index} value={p.nome}>{p.nome}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Bebida</label>
              <select onChange={(e) => setBebida(e.target.value)} required>
                <option value="">Selecione</option>
                {bebidas.map((b, index) => (
                  <option key={index} value={b.nome}>{b.nome}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Borda</label>
              <select onChange={(e) => setBorda(e.target.value)} required>
                <option value="">Selecione</option>
                {bordas.map((borda, index) => (
                  <option key={index} value={borda.nome}>{borda.nome}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Quantidade</label>
              <input type="number" value={quantidade} onChange={(e) => setQuantidade(e.target.value)} min="1" />
            </div>

            <div className="form-group">
              <label>Cidade</label>
              <select onChange={(e) => setCidade(e.target.value)} required>
                <option value="">Selecione</option>
                {cidadesDF.map((cidade, index) => (
                  <option key={index} value={cidade.nome}>{cidade.nome}</option>
                ))}
              </select>
            </div>

            <button type="submit">Fazer Pedido</button>
          </form>

          <div className="total">
            <h2>Total do Pedido</h2>
            {total > 0 ? (
              <p>Valor Total: R${total.toFixed(2)}</p>
            ) : (
              <p>Aguarde, selecione os itens!</p>
            )}
          </div>
        </div>
      ) : (
        <div>
          <h1>Pedido Finalizado</h1>
          <p><strong>Pizza:</strong> {pizza}</p>
          <p><strong>Bebida:</strong> {bebida}</p>
          <p><strong>Borda:</strong> {borda}</p>
          <p><strong>Quantidade:</strong> {quantidade}</p>
          <p><strong>Cidade:</strong> {cidade}</p>
          <p><strong>Valor Total:</strong> R${total.toFixed(2)}</p>
          <p><strong>Tempo Estimado de Entrega:</strong> {tempoEntrega}</p>
        </div>
      )}
    </div>
  );
};

export default App;