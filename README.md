# 🎵 YouTube Integration API

**Backend de Integração com YouTube para Música Offline**

- **Versão:** 0.1.0
- **Data:** 2026
- **Status:** Desenvolvimento inicial
- **Tecnologia:** Backend (Python | Django Ninja) — Mobile em repositório separado

---

> Transforme links do YouTube em músicas organizadas: envie o link, o sistema baixa, extrai o áudio e entrega a faixa pronta para tocar offline, em playlists customizadas a gosto do usuário.

---

## 🔄 Versionamento

- **Git** — Controle de versão
- **GitFlow** — Workflow de branches (`main`, `develop`, `feature/`, `hotfix/`, `release/`)
- **Conventional Commits** — Padronização de mensagens de commit

### Branches

- `main` — Código em produção
- `develop` — Branch de desenvolvimento
- `feature/*` — Novas funcionalidades
- `hotfix/*` — Correções urgentes em produção
- `release/*` — Preparação para nova versão

### Conventional Commits

- `feat:` — Nova funcionalidade
- `fix:` — Correção de bug
- `docs:` — Documentação
- `style:` — Formatação de código
- `refactor:` — Refatoração sem mudança de comportamento
- `test:` — Adição ou ajuste de testes
- `chore:` — Tarefas gerais de manutenção
- `perf:` — Melhoria de performance

---

## 🎯 Sobre o Projeto

**YouTube Integration API** é o backend responsável por permitir que usuários transformem links de vídeos do YouTube em músicas organizadas dentro de **playlists customizadas**. O usuário envia o link do vídeo, o sistema realiza o download do conteúdo, extrai o áudio e entrega a faixa para ser armazenada, organizada e reproduzida — via **streaming** ou **download** para uso totalmente offline.

Este repositório concentra apenas o **backend**: regras de negócio, autenticação, processamento de mídia e exposição da API REST. O aplicativo mobile que consumirá esta API será desenvolvido em um repositório separado.

> O uso da API deve respeitar os Termos de Serviço do YouTube e a legislação de direitos autorais vigente. O projeto é destinado a uso pessoal e educacional, e o usuário é responsável pelo conteúdo que processa através da API.

---

## 🏗️ Arquitetura

- **Backend** (Python + Django Ninja) — Regras de negócio, autenticação e processamento de mídia
- **Banco de Dados** (a definir — PostgreSQL recomendado em produção) — Persistência das entidades
- **Processamento de Mídia** — Download de vídeo e extração de áudio a partir de links do YouTube
- **Mobile** (futuro, repositório separado) — Consumirá a API via REST

### Domínios da API

A comunicação com o backend é feita exclusivamente via API REST, em formato JSON, com autenticação por token. A API é documentada automaticamente via Swagger / OpenAPI, gerada pelo Django Ninja.

- **Accounts** — Cadastro, login e gerenciamento de conta
- **Music** — Músicas, extração de áudio e processamento de links do YouTube
- **Playlists** — Criação, listagem e organização de playlists customizadas
- **Streaming & Download** — Reprodução sob demanda e exportação para uso offline

---

## 🛠️ Stack e Tecnologia

### Backend

- [Python 3.12](https://www.python.org/) — Linguagem principal
- [Django](https://www.djangoproject.com/) — Framework web
- [Django Ninja](https://django-ninja.dev/) — Framework para APIs REST modernas com tipagem via Pydantic
- [Pydantic](https://docs.pydantic.dev/) — Validação de dados e serialização

### Ferramentas

- [uv](https://docs.astral.sh/uv/) — Gerenciador de pacotes e ambientes

---

## 📐 Padrões e Boas Práticas

### Clean Architecture (Hexagonal)

```
Domain Layer        →  Entidades e regras de negócio puras
Application Layer   →  Casos de uso (use_cases.py) e DTOs
Infrastructure       →  Implementações concretas (models Django, repositórios, serviços externos)
Presentation Layer   →  Endpoints e schemas Pydantic (api/)
```

### Princípios SOLID

- **S** — *Single Responsibility:* Cada módulo tem uma única responsabilidade (ex: `music_service.py` cuida apenas da lógica de extração/processamento de áudio)
- **O** — *Open/Closed:* Novas fontes de mídia podem ser adicionadas sem modificar o core do domínio `music`
- **L** — *Liskov Substitution:* Implementações de repositórios podem ser substituídas sem afetar os casos de uso
- **I** — *Interface Segregation:* Schemas Pydantic específicos por operação (criação, leitura, atualização)
- **D** — *Dependency Inversion:* Casos de uso dependem de abstrações (`domain/repositories.py`), não de implementações concretas

### Segurança

- **Autenticação por token** — Acesso restrito a usuários autenticados
- **Validação de dados** — Sanitização de inputs com Pydantic
- **Variáveis de ambiente** — Secrets nunca expostos no repositório
- **Isolamento por usuário** — Cada usuário acessa apenas suas próprias playlists e músicas
- **HTTPS** — Toda comunicação com o backend é criptografada
- **Logs** — Dados sensíveis não são registrados

---

## 🚀 Roadmap de Desenvolvimento

- **Fase 1 — MVP** — Autenticação, criação de conta, playlists e músicas
- **Fase 2 — Processamento de mídia** — Download de vídeo e extração de áudio
- **Fase 3 — Entrega** — Streaming sob demanda e download de músicas/playlists
- **Fase 4 — Expansão** — Início do desenvolvimento do app mobile (repositório separado)

---

## 🔄 Fluxo de Uso

```
1. Usuário cria sua conta
2. Usuário cria uma playlist
3. Usuário envia o link de um vídeo do YouTube
4. Sistema baixa o vídeo e extrai o áudio
5. Música fica disponível para streaming ou download
6. Usuário organiza a música dentro de suas playlists
```

> Uma playlist pode conter múltiplas músicas. Uma música pode pertencer a múltiplas playlists do mesmo usuário.

---

## 🔐 Autenticação

O acesso à API é restrito a usuários cadastrados. O registro exige:

- Nome completo
- E-mail
- Senha

O login é realizado através de **e-mail + senha**, retornando um token de acesso utilizado nas demais requisições autenticadas.

---

## 👥 Permissões

Atualmente o projeto opera com um único perfil de acesso:

**Usuário**
- Cria e gerencia suas próprias playlists
- Adiciona músicas via link do YouTube
- Reproduz e baixa apenas o conteúdo vinculado à sua conta

> Uma hierarquia de perfis (ex: administrador) pode ser adicionada em versões futuras, caso necessário.

---

## 📋 Funcionalidades

### Funcionalidades Principais

- Criação de conta
- Criação de playlists
- Adição de músicas a partir do link do vídeo do YouTube
- Listagem de playlists
- Listagem de músicas
- Reprodução de músicas via streaming
- Download de músicas e playlists para uso offline

### 📋 Casos de Uso

A seguir, os principais casos de uso da aplicação, modelados segundo os princípios de Alistair Cockburn. Cada caso de uso descreve uma interação entre um ator e o sistema para alcançar um objetivo específico.

#### UC01: Criar Conta

- **Escopo:** Sistema YouTube Integration API
- **Nível:** Objetivo do usuário
- **Ator Primário:** Visitante
- **Interessados e Interesses:**
  - Visitante: Deseja criar uma conta para usar a plataforma.
  - Sistema: Deve validar dados e armazenar o novo usuário.
- **Pré-condições:** Nenhuma.
- **Cenário de Sucesso Principal:**
  1. Visitante fornece nome, e-mail e senha.
  2. Sistema valida que o e-mail não está em uso.
  3. Sistema cria a conta.
  4. Sistema confirma o cadastro.
- **Extensões:**
  - 2a. E-mail já existe: Sistema informa erro.
- **Requisitos Especiais:** Senha deve atender critérios mínimos de segurança.
- **Frequência:** Baixa (uma vez por usuário).

#### UC02: Fazer Login

- **Escopo:** Sistema YouTube Integration API
- **Nível:** Subfunção
- **Ator Primário:** Usuário Registrado
- **Interessados e Interesses:**
  - Usuário: Deseja acessar o sistema.
  - Sistema: Deve autenticar e fornecer token de acesso.
- **Pré-condições:** Usuário registrado e ativo.
- **Cenário de Sucesso Principal:**
  1. Usuário fornece e-mail e senha.
  2. Sistema valida as credenciais.
  3. Sistema gera token de acesso.
  4. Sistema retorna o token.
- **Extensões:**
  - 2a. Credenciais inválidas: Sistema informa erro.
- **Requisitos Especiais:** Token com expiração.
- **Frequência:** Alta.

#### UC03: Criar Playlist

- **Escopo:** Sistema YouTube Integration API
- **Nível:** Objetivo do usuário
- **Ator Primário:** Usuário
- **Interessados e Interesses:**
  - Usuário: Deseja organizar suas músicas em uma nova playlist.
  - Sistema: Deve validar e armazenar a playlist.
- **Pré-condições:** Usuário autenticado.
- **Cenário de Sucesso Principal:**
  1. Usuário fornece o nome da playlist.
  2. Sistema valida os dados.
  3. Sistema cria a playlist vinculada ao usuário.
  4. Sistema confirma a criação.
- **Extensões:**
  - 2a. Nome inválido/vazio: Sistema informa erro.
- **Requisitos Especiais:** Nenhum.
- **Frequência:** Média.

#### UC04: Adicionar Música via Link

- **Escopo:** Sistema YouTube Integration API
- **Nível:** Objetivo do usuário
- **Ator Primário:** Usuário
- **Interessados e Interesses:**
  - Usuário: Deseja transformar um vídeo do YouTube em música disponível na plataforma.
  - Sistema: Deve validar o link, baixar o vídeo e extrair o áudio.
- **Pré-condições:** Usuário autenticado; playlist existente (opcional).
- **Cenário de Sucesso Principal:**
  1. Usuário fornece o link do vídeo do YouTube.
  2. Sistema valida o link.
  3. Sistema baixa o conteúdo e extrai o áudio.
  4. Sistema salva a música e a disponibiliza ao usuário.
- **Extensões:**
  - 2a. Link inválido: Sistema informa erro.
  - 3a. Falha no download/extração: Sistema informa erro e não salva a música.
- **Requisitos Especiais:** Processamento assíncrono recomendado para vídeos longos.
- **Frequência:** Alta.

#### UC05: Listar Playlists

- **Escopo:** Sistema YouTube Integration API
- **Nível:** Objetivo do usuário
- **Ator Primário:** Usuário
- **Interessados e Interesses:**
  - Usuário: Deseja visualizar suas playlists.
  - Sistema: Deve listar apenas as playlists do usuário autenticado.
- **Pré-condições:** Usuário autenticado.
- **Cenário de Sucesso Principal:**
  1. Usuário solicita a lista de playlists.
  2. Sistema retorna as playlists vinculadas ao usuário.
- **Extensões:** Nenhuma.
- **Requisitos Especiais:** Paginação.
- **Frequência:** Alta.

#### UC06: Listar Músicas

- **Escopo:** Sistema YouTube Integration API
- **Nível:** Objetivo do usuário
- **Ator Primário:** Usuário
- **Interessados e Interesses:**
  - Usuário: Deseja visualizar suas músicas, isoladas ou dentro de uma playlist.
  - Sistema: Deve listar apenas as músicas do usuário autenticado.
- **Pré-condições:** Usuário autenticado.
- **Cenário de Sucesso Principal:**
  1. Usuário solicita a lista de músicas (geral ou por playlist).
  2. Sistema retorna as músicas correspondentes.
- **Extensões:** Nenhuma.
- **Requisitos Especiais:** Paginação; filtros por playlist.
- **Frequência:** Alta.

#### UC07: Reproduzir Música (Streaming)

- **Escopo:** Sistema YouTube Integration API
- **Nível:** Objetivo do usuário
- **Ator Primário:** Usuário
- **Interessados e Interesses:**
  - Usuário: Deseja ouvir a música sem baixá-la por completo antes.
  - Sistema: Deve entregar o áudio via streaming.
- **Pré-condições:** Usuário autenticado; música processada e disponível.
- **Cenário de Sucesso Principal:**
  1. Usuário solicita a reprodução de uma música.
  2. Sistema valida a posse/permissão sobre a música.
  3. Sistema transmite o áudio via streaming.
- **Extensões:**
  - 2a. Música não pertence ao usuário: Sistema informa erro.
- **Requisitos Especiais:** Suporte a range requests (HTTP).
- **Frequência:** Alta.

#### UC08: Download de Música/Playlist

- **Escopo:** Sistema YouTube Integration API
- **Nível:** Objetivo do usuário
- **Ator Primário:** Usuário
- **Interessados e Interesses:**
  - Usuário: Deseja baixar a música ou a playlist completa para uso offline.
  - Sistema: Deve entregar o(s) arquivo(s) de áudio.
- **Pré-condições:** Usuário autenticado; conteúdo processado e disponível.
- **Cenário de Sucesso Principal:**
  1. Usuário solicita o download de uma música ou playlist.
  2. Sistema valida a posse/permissão sobre o conteúdo.
  3. Sistema disponibiliza o(s) arquivo(s) para download.
- **Extensões:**
  - 2a. Conteúdo não pertence ao usuário: Sistema informa erro.
- **Requisitos Especiais:** Download de playlist deve ser compactado (ex: `.zip`).
- **Frequência:** Média.

### ✅ Planejadas para o MVP

- [ ] Cadastro de usuário
- [ ] Login por e-mail e senha
- [ ] Criação e listagem de playlists
- [ ] Adição de música via link do YouTube
- [ ] Download de vídeo e extração de áudio
- [ ] Listagem de músicas
- [ ] Streaming de músicas
- [ ] Download de músicas e playlists

### 📝 Próximas Versões

- [ ] Hierarquia de permissões (ex: perfis administrativos)
- [ ] Compartilhamento de playlists entre usuários
- [ ] Busca e filtros avançados
- [ ] Processamento assíncrono de downloads (fila/worker)
- [ ] Repositório do app mobile

---
## 📁 Estrutura de pastas

```
├── app
│   ├── accounts
│   │   ├── admin.py
│   │   ├── api
│   │   │   ├── auth.py
│   │   │   ├── dependencies.py
│   │   │   ├── schemas.py
│   │   │   └── views.py
│   │   ├── application
│   │   │   ├── dto.py
│   │   │   └── use_cases.py
│   │   ├── apps.py
│   │   ├── domain
│   │   │   ├── entities.py
│   │   │   ├── repositories.py
│   │   │   └── servicies.py
│   │   ├── infrastructure
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── services.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   ├── users
│   │   ├── admin.py
│   │   ├── api
│   │   │   ├── dependencies.py
│   │   │   ├── schemas.py
│   │   │   └── views.py
│   │   ├── application
│   │   │   ├── dto.py
│   │   │   └── use_cases.py
│   │   ├── apps.py
│   │   ├── domain
│   │   │   ├── entities.py
│   │   │   ├── repositories.py
│   │   │   └── servicies.py
│   │   ├── infrastructure
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── services.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   ├── music
│   │   ├── admin.py
│   │   ├── api
│   │   │   ├── auth.py
│   │   │   ├── dependencies.py
│   │   │   ├── schemas.py
│   │   │   └── views.py
│   │   ├── application
│   │   │   ├── dto.py
│   │   │   └── use_cases.py
│   │   ├── apps.py
│   │   ├── domain
│   │   │   ├── entities.py
│   │   │   ├── repositories.py
│   │   │   └── servicies.py
│   │   ├── infrastructure
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── services.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   └── core
│       ├── entitie.py
│       ├── exceptions.py
│       └── permissions.py
├── config
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── main.py
├── manage.py
├── pyproject.toml
├── README.md
└── uv.lock
```

> O app mobile que consumirá esta API será desenvolvido em um repositório próprio, ainda não iniciado.

---

## ✅ Pré-requisitos

- [Python 3.12+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) instalado

---

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/Thurzinfs/youtube-integration-api.git
cd youtube-integration-api

# Instale as dependências com uv
uv sync

# Copie o arquivo de variáveis de ambiente
cp .env.example .env

# Aplique as migrações
uv run manage.py migrate

# Suba o servidor de desenvolvimento
uv run manage.py runserver
```

---

## ⚙️ Variáveis de Ambiente

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://user:password@localhost:5432/youtube_integration
```

---

## 📡 Documentação da API

A documentação interativa (Swagger/OpenAPI), gerada automaticamente pelo Django Ninja, fica disponível em:

```
http://localhost:8000/api/docs
```

---

## 📌 Projeto Fechado

Este é um projeto público para visualização, mas não está aberto a contribuições externas. O código pode ser lido e estudado livremente, porém Pull Requests e forks com intenção de contribuição não serão aceitos.

---

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📞 Contato

- **Autor** — Arthur França Silva
- **E-mail** — arthurfranca.dev@gmail.com
- **GitHub** — [@Thurzinfs](https://github.com/Thurzinfs)

---

<div align="center">
  Desenvolvido com ❤️ por <a href="https://github.com/Thurzinfs">Arthur França Silva</a>
</div>
