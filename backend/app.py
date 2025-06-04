import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import os
import time
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Função para simular cálculo de frete (pode ser ajustada conforme a lógica desejada)
def calcular_frete(cep):
    # Simulação do cálculo com base no CEP, por exemplo, um valor fixo
    return 10.00

# Função para calcular o valor total
def calcular_valor_total(pizza_preco, bebida_preco, borda_preco, quantidade, frete):
    return (pizza_preco + bebida_preco + borda_preco) * quantidade + frete

# Configuração de Conexão com o Banco de Dados
class DatabaseConnection:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        self.cursor = self.connection.cursor()

    def fetch_pizzas(self):
        return [
            ("Pizza Calabresa", 30.00),
            ("Pizza Margherita", 28.00),
            ("Pizza Frango com Catupiry", 35.00),
            ("Pizza de Nutella", 40.00),
            ("Pizza de Doce de Leite", 38.00),
            ("Pizza Portuguesa", 32.00),
            ("Pizza de Bacon", 36.00)
        ]

    def fetch_bebidas(self):
        return [
            ("Coca-Cola", 5.00),
            ("Pepsi", 4.50),
            ("Sprite", 4.00),
            ("Guaraná", 4.00),
            ("Fanta", 4.50),
            ("Água", 2.00)
        ]

    def fetch_bordas(self):
        return [
            ("Tradicional", 0.00),
            ("Recheada", 5.00)
        ]

    def add_order(self, cliente_id, pizza_id, bebida, borda, quantidade, valor_total, status='Em preparo'):
        self.cursor.execute("INSERT INTO pedidos (cliente_id, status, valor_total) VALUES (%s, %s, %s)",
                            (cliente_id, status, valor_total))
        self.connection.commit()
        pedido_id = self.cursor.lastrowid

        # Inserir pizza
        self.cursor.execute("INSERT INTO itens_pedido (pedido_id, pizza_id, quantidade) VALUES (%s, %s, %s)",
                            (pedido_id, pizza_id, quantidade))
        self.connection.commit()

        # Inserir bebida
        self.cursor.execute("INSERT INTO itens_pedido (pedido_id, pizza_id, quantidade) VALUES (%s, %s, %s)",
                            (pedido_id, bebida[0], quantidade))
        self.connection.commit()

        # Inserir borda
        self.cursor.execute("INSERT INTO itens_pedido (pedido_id, pizza_id, quantidade) VALUES (%s, %s, %s)",
                            (pedido_id, borda[0], quantidade))
        self.connection.commit()

        return pedido_id

# Classe de Interface Gráfica
class PizzaApp:
    def __init__(self, root, db):
        self.root = root
        self.root.title("Pizzaria Py")
        self.root.geometry("600x650")
        self.root.config(bg="#f4f4f4")
        
        self.db = db

        # Título
        self.title_label = tk.Label(root, text="Pizzaria Py", font=("Helvetica", 20, "bold"), bg="#f4f4f4")
        self.title_label.pack(pady=10)

        # Frame para o conteúdo principal
        self.main_frame = tk.Frame(root, bg="#ffffff", bd=10, relief="solid")
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Seção de Pizzas
        self.pizza_label = tk.Label(self.main_frame, text="Escolha o Sabor da Pizza:", font=("Helvetica", 12), bg="#ffffff")
        self.pizza_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.pizza_combo = ttk.Combobox(self.main_frame, width=40, state="readonly")
        pizzas = self.db.fetch_pizzas()
        self.pizza_combo['values'] = [f"{pizza[0]} - R${pizza[1]:.2f}" for pizza in pizzas]
        self.pizza_combo.grid(row=1, column=0, padx=10, pady=10)

        # Seção de Bebidas
        self.bebida_label = tk.Label(self.main_frame, text="Escolha a Bebida:", font=("Helvetica", 12), bg="#ffffff")
        self.bebida_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.bebida_combo = ttk.Combobox(self.main_frame, width=40, state="readonly")
        bebidas = self.db.fetch_bebidas()
        self.bebida_combo['values'] = [f"{bebida[0]} - R${bebida[1]:.2f}" for bebida in bebidas]
        self.bebida_combo.grid(row=3, column=0, padx=10, pady=10)

        # Seção de Bordas
        self.borda_label = tk.Label(self.main_frame, text="Escolha a Borda:", font=("Helvetica", 12), bg="#ffffff")
        self.borda_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.borda_combo = ttk.Combobox(self.main_frame, width=40, state="readonly")
        bordas = self.db.fetch_bordas()
        self.borda_combo['values'] = [f"{borda[0]} - R${borda[1]:.2f}" for borda in bordas]
        self.borda_combo.grid(row=5, column=0, padx=10, pady=10)

        # Quantidade
        self.quantity_label = tk.Label(self.main_frame, text="Quantidade:", font=("Helvetica", 12), bg="#ffffff")
        self.quantity_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        
        self.quantity_entry = tk.Entry(self.main_frame, width=15)
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.grid(row=7, column=0, padx=10, pady=10)

        # CEP (para calcular o frete)
        self.cep_label = tk.Label(self.main_frame, text="CEP:", font=("Helvetica", 12), bg="#ffffff")
        self.cep_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        self.cep_entry = tk.Entry(self.main_frame, width=15)
        self.cep_entry.insert(0, "00000-000")
        self.cep_entry.grid(row=9, column=0, padx=10, pady=10)

        # Botão de pedido
        self.order_button = tk.Button(self.main_frame, text="Fazer Pedido", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", command=self.fazer_pedido)
        self.order_button.grid(row=10, column=0, padx=10, pady=20)

    def fazer_pedido(self):
        try:
            # Definindo dados do pedido
            cliente_id = 1  # Cliente fixo por enquanto
            selected_pizza_index = self.pizza_combo.current()
            if selected_pizza_index == -1:
                messagebox.showerror("Erro", "Por favor, selecione uma pizza.")
                return

            pizza = self.pizza_combo.get().split(" - ")
            pizza_nome = pizza[0]
            pizza_preco = float(pizza[1].replace("R$", "").replace(",", "."))
            pizza_id = selected_pizza_index + 1

            bebida = self.bebida_combo.get().split(" - ")
            bebida_nome = bebida[0]
            bebida_preco = float(bebida[1].replace("R$", "").replace(",", "."))
            bebida = (bebida_nome, bebida_preco)

            borda = self.borda_combo.get().split(" - ")
            borda_nome = borda[0]
            borda_preco = float(borda[1].replace("R$", "").replace(",", "."))
            borda = (borda_nome, borda_preco)

            quantidade = int(self.quantity_entry.get())

            # Calcular o frete
            cep = self.cep_entry.get()
            frete = calcular_frete(cep)

            # Calcular o valor total
            valor_total = calcular_valor_total(pizza_preco, bebida_preco, borda_preco, quantidade, frete)

            # Adicionar pedido ao banco de dados
            pedido_id = self.db.add_order(cliente_id, pizza_id, bebida, borda, quantidade, valor_total)

            # Tela de espera
            self.exibir_tela_espera(pedido_id, valor_total)

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def exibir_tela_espera(self, pedido_id, valor_total):
        # Limpa a tela principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Exibir detalhes do pedido
        self.wait_label = tk.Label(self.main_frame, text="Aguarde... Seu pedido está sendo preparado!", font=("Helvetica", 16, "bold"), bg="#ffffff")
        self.wait_label.pack(pady=20)

        self.pedido_label = tk.Label(self.main_frame, text=f"Pedido ID: {pedido_id}\nValor Total: R${valor_total:.2f}", font=("Helvetica", 12), bg="#ffffff")
        self.pedido_label.pack(pady=20)

        # Simulando tempo de entrega
        self.tempo_estimado_label = tk.Label(self.main_frame, text="Tempo estimado: 30 minutos", font=("Helvetica", 12), bg="#ffffff")
        self.tempo_estimado_label.pack(pady=20)

        # Atualizar status
        self.status_label = tk.Label(self.main_frame, text="Status: Em preparo", font=("Helvetica", 12), bg="#ffffff")
        self.status_label.pack(pady=20)


# Função Principal
def main():
    db = DatabaseConnection()
    root = tk.Tk()
    app = PizzaApp(root, db)
    root.mainloop()

if __name__ == "__main__":
    main()
