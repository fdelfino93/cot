# Plano: Sistema de Tracking Diário de Ativos

**Data inicial:** 05/01/2026
**Última atualização:** 07/01/2026
**Objetivo:** Criar sistema para registrar dados diários de ativos financeiros globais e estudar correlações com o Real brasileiro

**Status:** ✅ FASE 1 IMPLEMENTADA - App Streamlit funcionando com input manual completo

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

| Fase | O Que | Status |
|------|-------|--------|
| **1. MVP Streamlit** | Formulário manual para preencher dados diários | ✅ **CONCLUÍDO** |
| **2. Automação** | Web scraping busca dados automaticamente | ⏭️ Futuro (após 2-3 semanas de uso) |
| **3. Análise** | Correlações, cupom cambial, regime analysis | ⏭️ Após acumular 30-60 dias |

### ✅ Fase 1 Completa!
App Streamlit funcionando em `http://localhost:8501` com:
- Formulário completo para 23 ativos
- **Campos duplos:** Valor + Variação % para TODOS ativos principais, moedas EM e ETFs
- BRL Futures CME expandido (Open/High/Low/Last)
- Treasuries com Yield + Variação em bps
- Sistema de tabs: Novo Registro | Histórico | Eventos Econômicos | Análises
- CSV automático em `data/market_tracking.csv`

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
- **BBDC** - Bradesco ADR (NYSE)

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

**✅ ATUALIZADO 07/01/2026:** Agora inclui campos de variação % para TODOS os ativos principais

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `date` | Date | Data do registro (YYYY-MM-DD) |
| `time` | Time | Hora do registro (HH:MM) |
| **Índices e Volatilidade** | | |
| `dxy` | Float | Dollar Index - Valor |
| `dxy_chg` | Float | DXY - Variação % |
| `vix` | Float | VIX - Valor |
| `vix_chg` | Float | VIX - Variação % |
| `sp500_fut` | Float | S&P 500 Fut - Valor |
| `sp500_chg` | Float | S&P 500 Fut - Variação % |
| **Commodities** | | |
| `iron_ore` | Float | Minério Ferro (USD/ton) - Valor |
| `iron_ore_chg` | Float | Minério Ferro - Variação % |
| `brent` | Float | Petróleo Brent (USD/bbl) - Valor |
| `brent_chg` | Float | Brent - Variação % |
| `wti` | Float | Petróleo WTI (USD/bbl) - Valor |
| `wti_chg` | Float | WTI - Variação % |
| **Pares de Moeda EM** | | |
| `usd_ars` | Float | USD/ARS - Valor |
| `usd_ars_chg` | Float | USD/ARS - Variação % |
| `usd_aud` | Float | USD/AUD - Valor |
| `usd_aud_chg` | Float | USD/AUD - Variação % |
| `usd_clp` | Float | USD/CLP - Valor |
| `usd_clp_chg` | Float | USD/CLP - Variação % |
| `usd_mxn` | Float | USD/MXN - Valor |
| `usd_mxn_chg` | Float | USD/MXN - Variação % |
| `usd_inr` | Float | USD/INR - Valor |
| `usd_inr_chg` | Float | USD/INR - Variação % |
| `usd_try` | Float | USD/TRY - Valor |
| `usd_try_chg` | Float | USD/TRY - Variação % |
| `usd_zar` | Float | USD/ZAR - Valor |
| `usd_zar_chg` | Float | USD/ZAR - Variação % |
| **Treasuries** | | |
| `us_2y` | Float | Treasury 2Y - Yield (%) |
| `us_2y_chg` | Float | Treasury 2Y - Variação (bps) |
| `us_10y` | Float | Treasury 10Y - Yield (%) |
| `us_10y_chg` | Float | Treasury 10Y - Variação (bps) |
| **Risco Brasil** | | |
| `cds_br_5y` | Float | CDS Brasil 5Y (bps) - Valor |
| `cds_br_chg` | Float | CDS BR - Variação % |
| **BRL Futures CME (OHLC)** | | |
| `brl_fut_open` | Float | BRL Futures - Abertura |
| `brl_fut_high` | Float | BRL Futures - Máxima |
| `brl_fut_low` | Float | BRL Futures - Mínima |
| `brl_fut_last` | Float | BRL Futures - Atual/Fechamento |
| **ETFs** | | |
| `ewz` | Float | EWZ - Valor |
| `ewz_chg` | Float | EWZ - Variação % |
| `eww` | Float | EWW - Valor |
| `eww_chg` | Float | EWW - Variação % |
| `tur` | Float | TUR - Valor |
| `tur_chg` | Float | TUR - Variação % |
| `emb` | Float | EMB - Valor |
| `emb_chg` | Float | EMB - Variação % |
| **ADRs Brasileiras** | | |
| `vale` | Float | VALE - Valor |
| `vale_chg` | Float | VALE - Variação % |
| `pbr_a` | Float | PBR-A - Valor |
| `pbr_chg` | Float | PBR-A - Variação % |
| `itub` | Float | ITUB - Valor |
| `itub_chg` | Float | ITUB - Variação % |
| `bbdc` | Float | BBDC - Valor |
| `bbdc_chg` | Float | BBDC - Variação % |
| **Observações** | | |
| `notes` | Text | Observações opcionais |

**Total de colunas:** 52 (date, time, 24 valores + 24 variações, notes)

### 📝 Nota sobre Treasuries
- **Yield (%)**: Valor absoluto do rendimento (ex: 3.467%)
- **Variação (bps)**: Mudança em basis points
  - Sites mostram: `U.S. 2Y: 3.467 | -0.06%`
  - **Como preencher:**
    - Yield (%): `3.467`
    - Var (bps): `-6.0` (pega o -0.06% e multiplica por 100)
  - **Regra rápida:** -0.06% de variação = -6.0 bps

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

## 4. FASE 1 - APP STREAMLIT (Manual) ✅ IMPLEMENTADO

### Arquivos Criados

```
trad/
├── app/
│   ├── market_tracker.py          # ✅ App Streamlit principal com 4 tabs
│   └── utils.py                   # ✅ Funções auxiliares (CSV handling)
├── data/
│   ├── market_tracking.csv        # ✅ Criado automaticamente ao salvar
│   └── economic_events.csv        # ✅ Criado automaticamente
└── requirements_app.txt           # ✅ Dependências instaladas
```

### Funcionalidades Implementadas

**Tab 1: 📝 Novo Registro** ✅
- Campo de data (default: hoje, editável)
- Campo de hora (default: agora, editável com help text)
- **52 campos numéricos** organizados em seções:
  - 📉 Índices e Volatilidade (DXY, VIX, S&P 500) - Valor + Var %
  - 🛢️ Commodities (Ferro, Brent, WTI) - Valor + Var %
  - 💱 Pares de Moeda EM (7 pares) - Valor + Var %
  - 💵 Treasuries (2Y, 10Y) - Yield + Var bps
  - 🇧🇷 Risco Brasil (CDS) - Valor + Var %
  - 📈 BRL Futures CME - Open/High/Low/Last (OHLC)
  - 📊 ETFs (EWZ, EWW, TUR, EMB) - Valor + Var %
  - 🏢 ADRs Brasileiras (VALE, PBR, ITUB, BBDC) - Valor + Var %
- Campo de texto para observações
- Botão "💾 Salvar Registro"
- Info box explicando que são valores absolutos

**Tab 2: 📊 Histórico** ✅
- Tabela interativa com últimos registros
- Ordenação reversa (mais recente primeiro)
- Visualização de todos os campos salvos

**Tab 3: 📰 Eventos Econômicos** ✅
- Formulário para registrar eventos macro
- Campos: Data, Categoria, Indicador, Forecast, Previous, Actual, Impacto, Notes
- CSV separado: `data/economic_events.csv`

**Tab 4: 📈 Análises** ✅
- Placeholder para gráficos futuros
- Mensagem: "Em breve: correlações, cupom cambial, regime analysis"

### Decisões de UX Implementadas

1. ✅ **Campos duplos obrigatórios** (Valor + % Change)
   - Feedback do usuário: "Melhor colocar o preço e o percentual no momento"
   - Aplicado a: Índices, Commodities, Moedas EM, ETFs, ADRs
   - Total: 24 ativos com valor + variação

2. ✅ **BRL Futures expandido para OHLC**
   - Feedback do usuário: "Preciso que coloque: Abertura, Máxima, Mínima e Preço atual"
   - 4 campos separados para visão completa do dia

3. ✅ **Treasuries em Basis Points**
   - Yield em % + Variação em bps (padrão do mercado)
   - Conversão simples: -0.06% variação = -6.0 bps

4. ✅ **Hora editável com help text**
   - Feedback do usuário: "Não consigo atualizar a hora"
   - Help text adicionado: "Editável - ajuste se necessário"

### Validações Implementadas

- ✅ Data e hora obrigatórias
- ✅ Valores numéricos válidos
- ✅ Update automático se registro já existe para a data
- ✅ Mensagem de sucesso/atualização após salvar
- ✅ CSV criado automaticamente se não existir
- ✅ Ordenação por data (mais recentes primeiro)

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

### Sprint 1: MVP Streamlit ✅ CONCLUÍDO (07/01/2026)
- [x] Criar estrutura de pastas
- [x] Implementar formulário Streamlit com 4 tabs
- [x] Salvar dados em CSV
- [x] Visualização básica (tabela no tab Histórico)
- [x] Adicionar campos de variação % para TODOS os ativos
- [x] Expandir BRL Futures para OHLC
- [x] Implementar sistema de eventos econômicos
- [x] Validações e help texts

### Sprint 2: Melhorias UX e Análises (Próximo)
- [ ] Gráficos interativos (plotly) no tab Análises
- [ ] Comparação multi-ativos (overlay charts)
- [ ] Estatísticas descritivas (média, min, max 30d)
- [ ] Export para Excel formatado
- [ ] Dashboard de overview (cards com últimos valores)
- [ ] Filtros por período no histórico

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
2. ✅ **Implementar app Streamlit completo**
   - Formulário com 23 ativos + campos de variação
   - Sistema de tabs (Registro, Histórico, Eventos, Análises)
   - Salvar em CSV
   - Mostrar últimos registros
3. 🔄 **AGORA: Testar com dados reais**
   - Começar a preencher dados diários
   - Usar por 1-2 semanas para validar UX
   - Identificar padrões e necessidades
4. ⏭️ **Próximo: Adicionar visualizações**
   - Gráficos interativos no tab Análises
   - Estatísticas descritivas
   - Dashboard de overview
5. ⏭️ **Futuro: Planejar automação**
   - Após 2-3 semanas de uso manual
   - Baseado em aprendizado e feedback

---

## 10. OBSERVAÇÕES E APRENDIZADOS

### Decisões de Design Validadas ✅

1. **Campos duplos são essenciais**
   - Inicialmente planejamos apenas valor
   - Feedback do usuário mostrou necessidade de tracking de variação
   - Solução: 24 ativos com valor + % change = 48 campos de dados

2. **OHLC para BRL Futures**
   - Inicialmente era apenas 1 campo "BRL Futures"
   - Usuário solicitou visão completa do dia
   - Implementado: Open/High/Low/Last (4 campos)

3. **Treasuries em Basis Points**
   - Mantido padrão do mercado financeiro
   - Help text para conversão simplificada
   - Sites mostram "-0.06%" → Usuário preenche "-6.0 bps"

4. **Eventos econômicos separados**
   - CSV isolado evita misturar dados de mercado com eventos
   - Facilita análise futura de "surpresas econômicas"

### Princípios Mantidos ✅

- **Flexibilidade:** App evoluiu baseado em feedback real
- **Manual é OK:** Preencher manualmente ajuda a entender os dados
- **Correlação vem depois:** Precisamos de 30-60 dias de dados primeiro
- **Integração COT:** Merge futuro entre COT (semanal) e tracking diário

### Changelog

**07/01/2026:**
- ✅ Adicionados campos `_chg` para todos ativos principais
- ✅ Expandido moedas EM: valor + variação % (7 pares)
- ✅ Expandido ETFs: valor + variação % (4 ETFs)
- ✅ BRL Futures CME: 1 campo → 4 campos OHLC
- ✅ Help texts adicionados (hora editável, basis points)
- ✅ Total de colunas: 52 (date, time, 48 campos de dados, notes)

**05/01/2026:**
- ✅ Plano inicial criado
- ✅ App Streamlit básico implementado
- ✅ Sistema de tabs e CSV automático

---

**Status:** ✅ FASE 1 COMPLETA - Rodando em `http://localhost:8501`

**Próximo:** Sprint 2 - Gráficos e análises interativas
