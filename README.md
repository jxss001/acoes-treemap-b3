# 📈 Mapa de Ações B3 - Dashboard Treemap Interativo

Dashboard interativo para visualização e monitoramento de carteira de ações da B3 (Brasil, Bolsa, Balcão) em tempo real, utilizando treemaps dinâmicos e gráficos históricos.


## 🎯 Funcionalidades

- **Visualização em Treemap**: Representação visual da carteira com cores indicando variação percentual
- **3 Modos de Visualização**:
  - Variação do dia
  - Variação dos últimos 7 dias
  - Ganho/Perda total desde a compra
- **Rotação Automática Configurável**: Alterne entre telas com tempos personalizáveis
- **Habilitar/Desabilitar Telas**: Escolha quais visualizações exibir
- **Gráficos Históricos**: Clique em qualquer ação para ver histórico de 30 dias
- **Alertas Inteligentes** (auto-dismiss em 15s):
  - 🚨 Mudanças bruscas (>4% no dia)
  - 💡 Oportunidades de compra
  - 📈 Sugestões de realização de lucro
- **Gerenciamento de Ações**: Interface para adicionar/remover ações da carteira
- **Sistema de Logs**: Acompanhe todas as operações em tempo real
- **Atualização Automática**: Cotações atualizadas a cada 5 minutos

## 📋 Pré-requisitos

- Docker e Docker Compose **OU**
- Python 3.9 ou superior
- Conexão com internet (para buscar cotações via Yahoo Finance)

## 🚀 Instalação e Execução

### Opção 1: Usando Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/cascodigital/acoes-treemap-b3.git
cd acoes-treemap-b3

# Inicie o container
docker-compose up -d

# Acesse no navegador
http://localhost:8050
```

### Opção 2: Instalação Local

```bash
# Clone o repositório
git clone https://github.com/cascodigital/acoes-treemap-b3.git
cd acoes-treemap-b3

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
cd app
python main.py

# Acesse no navegador
http://localhost:8050
```

## 📂 Estrutura de Arquivos

```
.
├── app/
│   ├── assets/
│   │   ├── custom.css       # Estilos personalizados
│   │   └── foco.jpg         # Logo/ícone da aplicação
│   └── main.py              # Aplicação principal
├── docker-compose.yml       # Configuração Docker Compose
├── Dockerfile               # Imagem Docker
├── requirements.txt         # Dependências Python
├── .gitignore              # Arquivos ignorados pelo Git
├── LICENSE                  # Licença do projeto
└── README.md               # Este arquivo
```

**Nota**: O arquivo `acoes.csv` é criado automaticamente na primeira execução. Um exemplo é fornecido.

## 🎮 Como Usar

### 1. Adicionar Ações à Carteira

1. Acesse a página principal
2. Clique no botão **⚙** (Configurações)
3. Na seção "Adicionar Nova Ação", preencha:
   - **Ticker**: código da ação (ex: PETR4, VALE3, ITUB4)
   - **Quantidade**: número de ações
   - **Preço Médio**: preço médio de compra
4. Clique em **Adicionar**

### 2. Configurar Tempos de Rotação

Na página de configurações, você pode:

- **Habilitar/Desabilitar telas**: Use os switches para ativar apenas as visualizações desejadas
- **Ajustar tempo de exibição**: Configure quantos segundos cada tela fica visível (múltiplos de 5)
- **Salvar configurações**: As preferências são salvas no navegador (localStorage)

### 3. Ver Gráfico Histórico

- Clique em qualquer ação no treemap
- Uma janela modal abrirá com o gráfico dos últimos 30 dias

### 4. Acompanhar Logs

- Clique no botão **📋** (Logs)
- Visualize todas as operações, erros e atualizações em tempo real

## ⚙️ Configurações Avançadas

### Editar Porta da Aplicação

No arquivo `docker-compose.yml`:

```yaml
ports:
  - "8050:8050"  # Altere a primeira porta para mudar o acesso externo
```

### Ajustar Intervalo de Atualização

No arquivo `app/main.py`, localize:

```python
dcc.Interval(id='fetch', interval=300000, n_intervals=0)  # 300000ms = 5 minutos
```

### Ajustar Sensibilidade dos Alertas

No arquivo `app/main.py`, função `get_alerts()`:

```python
# Mudança brusca - padrão: 4%
if abs(row['change_pct_day']) > 4:

# Oportunidade - padrão: -3%
if row['change_pct_day'] < -3:

# Realizar lucro - padrão: 10%
if row['change_pct_total'] > 10:
```

### Formato do CSV

O arquivo `acoes.csv` segue o formato:

```csv
ticker,shares,avg_price
PETR4.SA,100,25.50
VALE3.SA,200,70.30
ITUB4.SA,150,28.75
```

**Importante**: Tickers da B3 devem terminar com `.SA`. Usando a GUI o .SA será automáticamente preenchido.

## 🛠️ Tecnologias Utilizadas

- **[Plotly Dash](https://dash.plotly.com/)**: Framework web para dashboards interativos
- **[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)**: Componentes UI baseados em Bootstrap
- **[yfinance](https://github.com/ranaroussi/yfinance)**: API para dados financeiros do Yahoo Finance
- **[Pandas](https://pandas.pydata.org/)**: Manipulação e análise de dados
- **[Plotly](https://plotly.com/python/)**: Gráficos interativos
- **Docker**: Containerização da aplicação

## 🐳 Docker

A aplicação roda em um container leve baseado em Python 3.9-slim. O Docker Compose configura:

- Porta 8050 exposta
- Volume persistente para dados (`./app:/app`)
- Restart automático (`unless-stopped`)
- Timezone configurável

## 🎨 Screenshots

### Dashboard Principal - Treemap Interativo
![Dashboard com visualização em treemap](exemplo.jpg)

### Página de Configurações
![Configurações de tempo e telas](exemploconfig.jpg)

## 📝 Licença

Este projeto está sob a licença MIT. 

## ⚠️ Disclaimer

**Este é um projeto pessoal de hobby desenvolvido para uso privado e interno.**

- ⚠️ A aplicação foi criada para atender uma necessidade pessoal específica
- 🔒 Projetada para uso com túneis Cloudflare em ambiente privado
- 🚨 **Não há implementação de recursos de segurança para exposição pública**
- 🛠️ Não possui autenticação, autorização ou proteção contra ataques externos
- 📝 O código não foi auditado para uso em produção ou ambientes expostos à internet
- 💡 Use por sua conta e risco - não há garantias de segurança, estabilidade ou suporte

**Recomendações:**
- Considere adicionar autenticação (OAuth, Basic Auth, etc.) se for expor publicamente


## 🌟 Diferenciais

Ao contrário de soluções pagas como Status Invest, Kinvo e TradeMap, este projeto oferece:

✅ **100% Gratuito e Open Source** - sem paywall ou limites artificiais  
✅ **Self-Hosted** - total controle dos dados financeiros pessoais  
✅ **Treemap com 3 Visualizações** - recurso único no mercado gratuito  
✅ **Rotação Automática Configurável** - ideal para monitores de parede  
✅ **Sem Limites** - trades, ações, atualizações ilimitadas  
✅ **Customizável** - código aberto para adaptar às necessidades  
✅ **Privacidade Total** - roda localmente, sem tracking  
✅ **Docker-ready** - deploy simplificado  

---

**Desenvolvido com ❤️ para investidores da B3**

Se este projeto foi útil para você, considere dar uma ⭐ no repositório!
