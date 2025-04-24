import redis
import json

class RedisClient:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    def adicionar_tarefa(self, coluna, dados):
        titulo = dados["titulo"]
        self.client.hset(f"kanban:{coluna}", titulo, json.dumps(dados))

    def listar_titulos(self, coluna):
        return list(self.client.hkeys(f"kanban:{coluna}"))

    def buscar_tarefa(self, coluna, titulo):
        dados_json = self.client.hget(f"kanban:{coluna}", titulo)
        return json.loads(dados_json) if dados_json else None

    def mover_tarefa(self, titulo, origem, destino):
        tarefa = self.hget_json(f"kanban:{origem}", titulo)
        if tarefa:
            self.hdel(f"kanban:{origem}", titulo)
            self.hset_json(f"kanban:{destino}", titulo, tarefa)

    def editar_tarefa(self, coluna, titulo_antigo, novos_dados):
        self.hdel(f"kanban:{coluna}", titulo_antigo)
        self.hset_json(f"kanban:{coluna}", novos_dados["titulo"], novos_dados)

    def excluir_tarefa(self, titulo, coluna):
        self.client.hdel(f"kanban:{coluna}", titulo)

    # Auxiliares
    def hset_json(self, chave, campo, dados):
        self.client.hset(chave, campo, json.dumps(dados))

    def hget_json(self, chave, campo):
        valor = self.client.hget(chave, campo)
        return json.loads(valor) if valor else None

    def hdel(self, chave, campo):
        self.client.hdel(chave, campo)
