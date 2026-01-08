# Plano: Sistema de Tracking Diário de Ativos

**Data:** 05/01/2026
**Objetivo:** Criar sistema para registrar dados diários de ativos financeiros globais e estudar correlações com o Real brasileiro

---

## ⚡ RESUMO EXECUTIVO

### O Que Vamos Construir?
Sistema de tracking diário de 23 ativos financeiros + registro de eventos econômicos para:
1. **Entender drivers do USD/BRL** através de correlações
2. **Integrar com análise COT** (já existente, semanal)
3. **Contextualizar movimentos** com dados macro (IPCA, Payroll, Focus, etc.)
4. **Calcular métricas** como cupom cambial implícito

### Por Que Esses Ativos Específicos?

✅ **Faz sentido estudar:**
- **Treasuries (2Y e 10Y)** - Para calcular cupom cambial e integrar com COT T10Y
- **DXY, VIX, S&P 500** - Risk-on/risk-off global
- **Commodities (Ferro, Petróleo)** - Brasil é exportador, afeta balança
- **Moedas EM (MXN, CLP, ZAR, TRY)** - Correlação carry trade
- **ADRs brasileiras (VALE, PBR, ITUB, BBDC)** - Apetite gringo por Brasil
- **ETFs (EWZ, EMB)** - Fluxo estrangeiro
- **BRL Futures CME** - Confirma posicionamento COT
- **CDS BR** - Prêmio de risco

✅ **Mudança: BBAS3.SA → BBDC (Bradesco ADR)**
- Consistência: todas ADRs na NYSE
- Mais líquido para gringos
- Mesma exposição (setor bancário)

✅ **Eventos Econômicos:**
- Registro manual de: IPCA, Focus, Payroll, Copom, fiscal
- **Formato:** Expectativa vs Realidade
- **Objetivo:** Explicar movimentos anormais, não esquecer context

### Implementação em 3 Fases

| Fase | O Que | Quando |
|------|-------|--------|
| **1. MVP Streamlit** | Formulário manual para preencher dados diários | Esta semana |
| **2. Automação** | Web scraping busca dados automaticamente | Futuro (após 2-3 semanas de uso) |
| **3. Análise** | Correlações, cupom cambial, regime analysis | Após acumular 30-60 dias |

### Próximo Passo: Começar?
Se aprovado, começamos implementando o app Streamlit para input manual.

---

## 1. ESCOPO - Ativos a Rastrear

### Índices e Volatilidade
- **DXY** - Dollar Index
- **VIX** - Volatility Index
- **S&P 500 Fut** - Futuro do S&P 500

### Commodities
- **Minério de Ferro (China)** - Iron Ore Futures
- **Petróleo Brent** - Brent Crude Oil
- **Petróleo WTI** - WTI Crude Oil

### Pares de Moeda (USD/XXX)
- **USD/ARS** - Peso Argentino
- **USD/AUD** - Dólar Australiano
- **USD/CLP** - Peso Chileno
- **USD/MXN** - Peso Mexicano
- **USD/INR** - Rupia Indiana
- **USD/TRY** - Lira Turca
- **USD/ZAR** - Rand Sul-Africano

### Treasuries
- **U.S. 2Y** - Treasury 2 anos (yield)
- **U.S. 10Y** - Treasury 10 anos (yield)

### Risco Brasil
- **CDS BR 5Y** - Credit Default Swap Brasil 5 anos

### Futuros Brasil (CME)
- **Brazilian Real Futures** - Contrato futuro BRL na CME

### ETFs - Países/Emergentes
- **EWZ** - iShares MSCI Brazil ETF
- **EWW** - iShares MSCI Mexico ETF
- **TUR** - iShares MSCI Turkey ETF
- **EMB** - iShares J.P. Morgan USD Emerging Markets Bond ETF

### ETFs/ADRs - Ações Brasileiras
- **VALE** - Vale ADR (NYSE)
- **PBR-A** - Petrobras ADR (NYSE)
- **ITUB** - Itaú ADR (NYSE)
- **BBDC** - Bradesco ADR (NYSE) - *Substituindo BBAS3 por consistência (todas ADRs NYSE)*

**Total:** 23 ativos

### 📰 Notícias e Eventos Econômicos (Registro Manual)
**Separado em arquivo:** `data/economic_events.csv`

Campos para registrar:
- **Data do evento**
- **Categoria:** Focus, Fiscal, Inflação, Emprego, etc.
- **Indicador:** IPCA, IPCA-15, Payroll, Selic, etc.
- **Expectativa (Forecast):** O que o mercado esperava
- **Dado Anterior (Previous):** Último valor divulgado
- **Dado Real (Actual):** Como veio o dado
- **Impacto:** Alta/Média/Baixa
- **Observações:** Contexto, reação do mercado, etc.

**Exemplos:**
```
2026-01-10 | Inflação | IPCA-15 Dez | Exp: 0.42% | Ant: 0.62% | Real: 0.48% | Impacto: Médio | "Veio acima mas abaixo do anterior"
2026-01-15 | Focus | Selic Fim 2026 | Exp: - | Ant: 14.75% | Real: 15.00% | Impacto: Alto | "Mercado elevou projeção após Copom"
```

---

## 1.1. RACIONALIZAÇÃO - Por Que Rastrear Esses Ativos?

### 🎯 Objetivo Central: Entender o USD/BRL

Todos os ativos escolhidos têm **relação direta ou indireta** com o Real brasileiro:

#### **Fluxo de Capital Estrangeiro para o Brasil**
- **EWZ** (Brasil ETF) - Principal veículo de investimento gringo no Brasil
- **VALE, PBR-A, ITUB, BBDC** - ADRs mais líquidas, indicam apetite por Brasil
- **EMB** (Bonds EM) - Fluxo para dívida emergente compete com equity
- **USD/ZAR, USD/TRY** - Outros emergentes, mostram apetite por risco EM

#### **Treasuries e Cupom Cambial**
- **U.S. 2Y** - Taxa curta, reflete expectativa de Fed
- **U.S. 10Y** - Taxa longa, custo de oportunidade global
- **Cupom Cambial (2Y-10Y)** - Será calculado e monitorado
- **Conexão COT:** Leveraged Funds short em T10Y = yields altos = dólar forte

#### **Carry Trade e Moedas Emergentes**
- **USD/MXN, USD/CLP** - Latam, correlação com BRL
- **USD/ARS** - Argentina, extremos afetam região
- **USD/AUD** - Proxy de commodities e China
- **USD/INR** - Outro grande emergente asiático

#### **Commodities (Brasil = Exportador)**
- **Minério de Ferro** - 15% das exportações brasileiras (Vale)
- **Petróleo (Brent + WTI)** - Petrobras + balança comercial
- **Commodity up = BRL tende a fortalecer** (se outros fatores constantes)

#### **Risk-On / Risk-Off Global**
- **VIX** - Medo = fuga para dólar = BRL cai
- **S&P 500 Fut** - Risk-on = fluxo para emergentes
- **DXY** - Força global do dólar vs cesta

#### **Risco Brasil**
- **CDS BR 5Y** - Prêmio de risco soberano
- **BRL Futures CME** - Como gringos apostam no Real
- **Integração COT:** Asset Managers comprados em BRL Futures = otimismo externo

### 🔗 Conexões com Análise COT (Semanal)

| Dado COT | Dado Diário | Relação |
|----------|-------------|---------|
| T10Y Leveraged Funds (Short) | U.S. 10Y Yield | Short alto = yield alto = pressão em EM |
| BRL Asset Managers (Net Long) | BRL Futures CME | Confirma posicionamento institucional |
| DXY Leveraged Funds (Net) | DXY spot | Validação do sentimento especulativo |

### 📊 Análises Futuras Possíveis

Com esses dados + COT + eventos econômicos, poderemos:

1. **Calcular Cupom Cambial Implícito**
   - Spread entre Treasuries e DI Futuro B3
   - Identificar quando carry trade fica "caro" ou "barato"

2. **Correlação com Surpresas Econômicas**
   - "IPCA veio 0.1% acima, Real caiu X%"
   - Identificar quais surpresas mais impactam

3. **Early Warning System**
   - Se VIX > 25 + DXY > 107 + CDS BR > 200 = Regime de stress
   - Se T10Y > 4.5% + Specs short extremo = Pressão em EM

4. **Análise de Regime**
   - Quanto o BRL se move quando há mudança no COT?
   - Em regime de stress, correlações mudam?

---

## 2. ARQUITETURA DO SISTEMA

### Fase 1: Input Manual (Streamlit) ✅ COMEÇAR AQUI
```
Interface Streamlit
    ↓
Formulário com campos para cada ativo
    ↓
Salva em CSV/Excel com timestamp
    ↓
Visualização básica dos dados
```

### Fase 2: Automação (Futuro)
```
Web Scraping / APIs
    ↓
Coleta automática diária
    ↓
Atualiza CSV/Excel
    ↓
Dashboard atualizado
```

### Fase 3: Análise de Correlação (Futuro)
```
Dados históricos B3 (colar manualmente):
  - Dólar Futuro
  - Índice Futuro (Mini Índice)
  - DI Futuro
    ↓
Cálculo de correlações
    ↓
Matriz de correlação
    ↓
Insights automáticos
```

---

## 3. ESTRUTURA DE DADOS

### Arquivo CSV: `data/market_tracking.csv`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `date` | Date | Data do registro (YYYY-MM-DD) |
| `time` | Time | Hora do registro (HH:MM) |
| `dxy` | Float | Dollar Index |
| `vix` | Float | VIX |
| `iron_ore` | Float | Minério Ferro (USD/ton) |
| `brent` | Float | Petróleo Brent (USD/barril) |
| `wti` | Float | Petróleo WTI (USD/barril) |
| `usd_ars` | Float | USD/ARS |
| `usd_aud` | Float | USD/AUD |
| `usd_clp` | Float | USD/CLP |
| `usd_mxn` | Float | USD/MXN |
| `usd_inr` | Float | USD/INR |
| `usd_try` | Float | USD/TRY |
| `usd_zar` | Float | USD/ZAR |
| `sp500_fut` | Float | S&P 500 Futures |
| `us_2y` | Float | Treasury 2Y yield (%) |
| `us_10y` | Float | Treasury 10Y yield (%) |
| `cds_br_5y` | Float | CDS Brasil 5Y (bps) |
| `brl_futures_cme` | Float | BRL Futures (CME) |
| `ewz` | Float | ETF EWZ |
| `eww` | Float | ETF EWW |
| `tur` | Float | ETF TUR |
| `emb` | Float | ETF EMB |
| `vale` | Float | VALE ADR |
| `pbr_a` | Float | PBR-A ADR |
| `itub` | Float | ITUB ADR |
| `bbdc` | Float | BBDC ADR |
| `notes` | Text | Observações opcionais |

### Arquivo CSV: `data/economic_events.csv`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `date` | Date | Data do evento/divulgação |
| `time` | Time | Hora da divulgação (opcional) |
| `category` | Text | Focus, Fiscal, Inflação, Emprego, Político, etc. |
| `indicator` | Text | IPCA, IPCA-15, Payroll, Selic, PIB, etc. |
| `forecast` | Float/Text | Expectativa do mercado |
| `previous` | Float/Text | Dado anterior |
| `actual` | Float/Text | Dado real divulgado |
| `impact` | Text | Alto, Médio, Baixo |
| `notes` | Text | Contexto, reação, decisões políticas, etc. |

**Exemplos de uso:**
- Quando IPCA-15 vier diferente do esperado, teremos o contexto
- Quando Copom mudar Selic, registro da decisão + comunicado resumido
- Payroll forte nos EUA = explica movimento em Treasuries
- Focus revisando Selic = contexto de expectativas

---

## 4. FASE 1 - APP STREAMLIT (Manual)

### Arquivos a Criar

```
trad/
├── app/
│   ├── market_tracker.py          # App Streamlit principal
│   ├── economic_events.py         # Formulário de eventos econômicos
│   └── utils.py                   # Funções auxiliares
├── data/
│   ├── market_tracking.csv        # Dados de mercado diários
│   └── economic_events.csv        # Eventos econômicos
└── requirements_app.txt           # Dependências Streamlit
```

### Funcionalidades do App

1. **Formulário de Entrada**
   - Campo de data (default: hoje)
   - Campo de hora (default: agora)
   - Campos numéricos para cada ativo
   - Campo de texto para notas
   - Botão "Salvar Registro"

2. **Validações**
   - Data não pode ser futura
   - Valores numéricos válidos
   - Aviso se já existe registro para a data

3. **Visualização**
   - Tabela com últimos 10 registros
   - Gráficos de linha para ativos selecionados
   - Estatísticas básicas (média, min, max últimos 30 dias)

4. **Export**
   - Botão para baixar CSV completo
   - Botão para baixar Excel formatado

---

## 5. FONTES DE DADOS (Para Fase 2 - Automação)

### APIs Gratuitas
- **yfinance** - Ações, ETFs, Índices, Commodities
- **FRED API** - Treasuries, VIX
- **investing.com** - Web scraping (CDS, algumas moedas)

### Web Scraping
- **CME Group** - BRL Futures
- **Bloomberg/Investing** - CDS Brasil
- **Banco Central** - Dados alternativos

### Frequência
- **Coleta:** 1x por dia (após fechamento NY - 18h BRT)
- **Backup manual:** Interface Streamlit sempre disponível

---

## 6. ANÁLISE DE CORRELAÇÃO (Fase 3)

### Dados B3 (Input Manual Inicial)

**Arquivos CSV separados:**
```
data/b3_dolar_futuro.csv
data/b3_indice_futuro.csv
data/b3_di_futuro.csv
```

Formato:
```csv
date,open,high,low,close,volume
2025-01-05,5.95,6.00,5.93,5.98,125000
```

### Análises Planejadas

1. **Correlação Pearson**
   - Matriz de correlação entre todos ativos
   - Heatmap visual

2. **Lead/Lag Analysis**
   - Qual ativo "antecipa" movimentos no BRL?
   - Janelas de 1, 3, 5 dias

3. **Regressão Múltipla**
   - Prever USD/BRL baseado em outros ativos
   - Identificar principais drivers

4. **Regime Analysis**
   - Correlações em períodos de stress vs normal
   - Breakdown por quintis de VIX

---

## 7. ROADMAP DE IMPLEMENTAÇÃO

### Sprint 1: MVP Streamlit (Esta Semana)
- [ ] Criar estrutura de pastas
- [ ] Implementar formulário Streamlit
- [ ] Salvar dados em CSV
- [ ] Visualização básica (tabela + 1 gráfico)
- [ ] Testar com 5 dias de dados

### Sprint 2: Melhorias UX (Semana 2)
- [ ] Gráficos interativos (plotly)
- [ ] Comparação multi-ativos
- [ ] Estatísticas descritivas
- [ ] Export para Excel formatado
- [ ] Validações robustas

### Sprint 3: Preparação para Automação (Semana 3-4)
- [ ] Pesquisar APIs disponíveis
- [ ] Testar coleta via yfinance
- [ ] Criar script de scraping CME
- [ ] Documentar fontes de cada ativo

### Sprint 4: Automação (Futuro)
- [ ] Scheduler diário (cron/task scheduler)
- [ ] Fallback para coleta manual
- [ ] Alertas em caso de falha
- [ ] Dashboard de monitoramento

### Sprint 5: Correlações (Futuro)
- [ ] Interface para upload de dados B3
- [ ] Cálculo de correlações
- [ ] Visualizações avançadas
- [ ] Relatório automático de insights

---

## 8. DECISÕES TÉCNICAS

### Stack Fase 1 (Manual)
- **Frontend:** Streamlit
- **Storage:** CSV (simples, fácil de editar)
- **Visualização:** Plotly (interativo)
- **Deploy:** Local (rodar com `streamlit run`)

### Stack Fase 2+ (Automação)
- **Coleta:** yfinance + requests + BeautifulSoup
- **Scheduler:** APScheduler ou cron
- **Database:** SQLite ou continuar CSV (decisão posterior)
- **Dashboard:** Continuar Streamlit ou migrar para Dash

---

## 9. PRÓXIMOS PASSOS IMEDIATOS

1. ✅ **Criar este plano**
2. ⏭️ **Implementar app Streamlit básico**
   - Formulário com os 23 ativos
   - Salvar em CSV
   - Mostrar últimos registros
3. ⏭️ **Testar com dados reais por 1 semana**
4. ⏭️ **Ajustar baseado no uso**
5. ⏭️ **Planejar automação baseado em aprendizado**

---

## 10. OBSERVAÇÕES

- **Flexibilidade:** Começar simples, iterar baseado no uso real
- **Manual é OK:** Preencher manualmente por algumas semanas ajuda a entender os dados
- **Correlação vem depois:** Precisamos de pelo menos 30-60 dias de dados para análises significativas
- **Integração COT:** Possível merge futuro entre dados COT (semanal) e tracking diário

---

**Status:** 📋 PLANEJADO - Aguardando aprovação para iniciar implementação
