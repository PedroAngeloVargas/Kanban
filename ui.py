import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import tkinter as tk
from logic import KanbanManager

class KanbanApp:
    def __init__(self, root):
        self.manager = KanbanManager()
        self.root = root
        self.root.title("Kanban Board")
        self.style = ttk.Style("darkly")

       
        self.btn_add = ttk.Button(root, text="➕ Nova Tarefa", command=self.popup_adicionar, bootstyle=SUCCESS)
        self.btn_add.grid(row=0, column=0, columnspan=3, pady=10)

        self.listboxes = {}
        for i, coluna in enumerate(self.manager.colunas):
            ttk.Label(root, text=coluna.upper(), font=("Helvetica", 10, "bold")).grid(row=1, column=i)
            lb = tk.Listbox(root, width=30, height=15)
            lb.grid(row=2, column=i, padx=5)
            self.listboxes[coluna] = lb

       
        ttk.Button(root, text="⬅️ Retroceder", command=self.retroceder, bootstyle=WARNING).grid(row=3, column=0, pady=10)
        ttk.Button(root, text="Avançar ➡️", command=self.avancar, bootstyle=PRIMARY).grid(row=3, column=2, pady=10)
        ttk.Button(root, text="✏️ Editar", command=self.popup_editar, bootstyle=INFO).grid(row=4, column=0, pady=10)
        ttk.Button(root, text="🗑️ Excluir", command=self.excluir_tarefa, bootstyle=DANGER).grid(row=4, column=2, pady=10)

        self.atualizar()

    def popup_adicionar(self):
        self.popup_formulario("Adicionar Tarefa", None, None)

    def popup_editar(self):
        for coluna, lb in self.listboxes.items():
            sel = lb.curselection()
            if sel:
                titulo = lb.get(sel[0])
                tarefa = self.manager.buscar_tarefa_completa(coluna, titulo)
                self.popup_formulario("Editar Tarefa", coluna, tarefa)
                break

    def popup_formulario(self, titulo_janela, coluna=None, tarefa=None):
        janela = ttk.Toplevel(self.root)
        janela.title(titulo_janela)
        janela.geometry("400x300")
        janela.grab_set()

        campos = ["Título", "Responsável", "Data de Início", "Prazo"]
        entradas = {}

        for i, campo in enumerate(campos):
            ttk.Label(janela, text=campo).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entrada = ttk.Entry(janela, width=30)
            entrada.grid(row=i, column=1, padx=10, pady=5)
            entradas[campo.lower()] = entrada


        if tarefa:
            for key in entradas:
                entradas[key].insert(0, tarefa.get(key, ""))

        def salvar():
            dados = {}

            for key in entradas:  
                dados[key] = entradas[key].get()


            print(f"Dados Capturados: {dados}")


            if tarefa:  
                self.manager.editar_tarefa(coluna, tarefa["título"], dados)
            else:  

                self.manager.adicionar_tarefa(dados)

            janela.destroy()
            self.atualizar()


        ttk.Button(janela, text="Salvar", command=salvar, bootstyle=SUCCESS).grid(row=5, column=0, columnspan=2, pady=15)

    def atualizar(self):
        for coluna in self.manager.colunas:
            self.listboxes[coluna].delete(0, ttk.END)
            for titulo in self.manager.listar_tarefas_por_coluna(coluna):
                self.listboxes[coluna].insert(ttk.END, titulo)

    def retroceder(self):
        for coluna in self.manager.colunas[1:]:  
            lb = self.listboxes[coluna]
            sel = lb.curselection()
            if sel:
                titulo = lb.get(sel[0])
                destino = self.manager.colunas[self.manager.colunas.index(coluna) - 1]
                self.manager.mover_tarefa(titulo, coluna, destino)
                self.atualizar()
                break

    def avancar(self):
        for i, coluna in enumerate(self.manager.colunas[:-1]):
            lb = self.listboxes[coluna]
            sel = lb.curselection()
            if sel:
                titulo = lb.get(sel[0])
                destino = self.manager.colunas[i + 1]
                self.manager.mover_tarefa(titulo, coluna, destino)
                self.atualizar()
                break

    def excluir_tarefa(self):
        for coluna, lb in self.listboxes.items():
            sel = lb.curselection()
            if sel:
                titulo = lb.get(sel[0])
                if messagebox.askyesno("Confirmar", f"Deseja excluir a tarefa '{titulo}'?"):
                    self.manager.excluir_tarefa(titulo, coluna)
                    self.atualizar()
                break
