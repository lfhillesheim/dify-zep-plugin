# Plugin Zep para Dify

Um plugin para o Dify que adiciona gerenciamento de memória usando o Zep. Isso ajuda seu assistente de IA a lembrar conversas passadas e informações do usuário.

[Ver no GitHub](https://github.com/obadakhalili/dify-zep-plugin)

## Instalação

1. Instale o plugin no seu workspace do Dify
2. Crie um projeto no Zep e obtenha uma chave de API
3. Adicione sua chave de API do Zep para autorizar o plugin
4. (Opcional) Use o campo `zep_api_url` para definir uma URL base customizada da API se estiver usando uma instância do Zep diferente

   ![authorize-1](_assets/authorize-1.png)
   ![authorize-2](_assets/authorize-2.png)

## Ferramentas

### 1. Iniciar Sessão

Cria um usuário e sessão no Zep caso ainda não existam. Deve ser usada primeiro antes das outras ferramentas.

**Parâmetros:**

- ID do usuário - Identificador único do usuário
- ID da sessão - Identificador único da conversa

Retorna os detalhes da sessão criada ou existente.

  ![init-session](_assets/init-session.png)

### 2. Adicionar Mensagem à Sessão

Salva uma mensagem na memória da conversa.

**Parâmetros:**

- ID da sessão - A conversa que será atualizada
- Mensagem - O texto a ser salvo
- Tipo de papel - Quem enviou a mensagem (usuário ou assistente)
- Retornar contexto (opcional) - Se verdadeiro, retorna também o contexto de memória relevante
- Ignorar papéis (opcional) - Papéis a serem ignorados ao adicionar a mensagem à memória do grafo

  ![add-message.png](_assets/add-message.png)

### 3. Obter Memória da Sessão

Obtém a memória do usuário relevante para as últimas mensagens da conversa.

**Parâmetros:**

- ID da sessão - A conversa da qual obter a memória
- Últimas N mensagens (opcional) - Quantidade de mensagens recentes a considerar (máx. 50)
- Pontuação mínima (opcional) - Somente retornar memórias acima dessa relevância

  ![get-memory](_assets/get-memory.png)

### 4. Buscar no Gráfico do Usuário

Busca na memória do usuário por informações relevantes.

**Parâmetros:**

- ID do usuário - O usuário para buscar memórias
- Consulta - O que buscar na memória

  ![search-graph](_assets/search-graph.png)

**Diferença entre as ferramentas `Obter Memória da Sessão` e `Buscar no Gráfico do Usuário`:**

- `Obter Memória da Sessão` usa as últimas mensagens da conversa para compor uma consulta e buscar na memória do usuário informações relevantes.
- `Buscar no Gráfico do Usuário` pesquisa na memória do usuário usando uma consulta fornecida por você.

### 5. Excluir Sessão

Remove uma sessão e toda a sua memória armazenada.

**Parâmetros:**

- ID da sessão - A sessão a ser removida

### 6. Obter Sessão

Recupera detalhes de uma sessão.

**Parâmetros:**

- ID da sessão - A sessão a ser buscada

## Exemplo de fluxo

![workflow](_assets/workflow.png)

## Tarefas pendentes:

- [ ] E se o usuário quiser usar o plugin com chaves de API diferentes de mais de um projeto?
- [ ] Como usar em aplicativos fora de fluxo de trabalho?
- [ ] Usar `return_context` em `memory.get()` para utilizar o contexto imediatamente.
