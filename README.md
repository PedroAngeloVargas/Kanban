# Kanban

→ Descrição do Sistema

  A aplicação é um Kanban Board (quadro de tarefas) desenvolvido em python que permite adicionar, editar, mover e excluir tarefas entre colunas, utilizando o Redis como sistema de armazenamento para persistência dos dados.

Possui as seguintes funcionalidades:

    • Adicionar Tarefa: Permite inserir novas tarefas no estágio "A Começar".
    • Editar Tarefa: Permite editar uma tarefa existente, alterando seus detalhes como título, responsável, data de início e prazo.
    • Mover Tarefa: Permite mover tarefas entre as colunas (ex: de "A Começar" para "Em Progresso" ou de "Em Progresso" para "Concluída").
    • Excluir Tarefa: Permite remover uma tarefa das colunas.

→ Princípios de Engenharia de Software

    • Modularidade: O código foi dividido em componentes independentes e reutilizáveis, como a interface gráfica (KanbanApp), a lógica de tarefas (KanbanManager) e o armazenamento de dados (Redis).
    • Encapsulamento: A classe KanbanManager esconde a complexidade da manipulação e armazenamento das tarefas, expondo apenas métodos claros para adicionar, editar, mover e excluir tarefas.
    • Separação de Interesses: A interface gráfica, a lógica de tarefas e o armazenamento de dados são claramente separados, permitindo modificações em uma parte sem afetar as outras.

→ Como executar

    1) Instale o Redis: https://redis.io/downloads/
    2) Teste seu funcionamento:
           No terminal:
               redis-cli
               ping (Deve retornar “pong”)
    3) Crie um ambiente virtual (opcional, mas recomendado)
           python3 -m venv venv
    4) Acesse o ambiente:
           No Linux/macOS
		source venv/bin/activate
           No Windows
                venv\Scripts\activate
    5) Instale as dependências necessárias:
	        pip install redis ttkbootstrap
    6) Baixe ou clone o repositório: https://github.com/PedroAngeloVargas/Kanban
    7) Execute a aplicação
	        python3 main.py



		
               
           