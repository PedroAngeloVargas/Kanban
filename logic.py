import json
import redis
import os

class KanbanManager:

    def __init__(self):
        self.colunas = ["a_comecar", "em_progresso", "concluida"]
        self.redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.tarefas = self.carregar_dados()
        self.arquivo = "tarefas.json"

    def carregar_dados(self):
        tarefas = {}
        for coluna in self.colunas:
            dados_json = self.redis.get(coluna)
            if dados_json:
                tarefas[coluna] = json.loads(dados_json)
            else:
                tarefas[coluna] = []
        return tarefas
    
    def salvar_dados(self):
        for coluna in self.colunas:
            self.redis.set(coluna, json.dumps(self.tarefas[coluna], ensure_ascii=False))
            self.salvar_em_arquivo_json()


    def adicionar_tarefa(self, dados):
        self.tarefas["a_comecar"].append(dados)
        self.salvar_dados()

    def editar_tarefa(self, coluna, titulo_antigo, novos_dados):
        for i, tarefa in enumerate(self.tarefas[coluna]):
            if tarefa["título"] == titulo_antigo:
                self.tarefas[coluna][i] = novos_dados
                self.salvar_dados()
                break

    def excluir_tarefa(self, titulo, coluna):
        self.tarefas[coluna] = [t for t in self.tarefas[coluna] if t["título"] != titulo]
        self.salvar_dados()

    def mover_tarefa(self, titulo, origem, destino):
        for tarefa in self.tarefas[origem]:
            if tarefa["título"] == titulo:
                self.tarefas[origem].remove(tarefa)
                self.tarefas[destino].append(tarefa)
                self.salvar_dados()
                break

    def listar_tarefas_por_coluna(self, coluna):
        return [tarefa["título"] for tarefa in self.tarefas[coluna]]

    def buscar_tarefa_completa(self, coluna, titulo):
        for tarefa in self.tarefas[coluna]:
            if tarefa["título"] == titulo:
                return tarefa
        return None
    
    def salvar_em_arquivo_json(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(self.tarefas, f, indent=4, ensure_ascii=False)
