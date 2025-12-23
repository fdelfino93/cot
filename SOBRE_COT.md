# O que e o COT (Commitments of Traders)?

## Resumo Rapido

O **COT (Commitments of Traders)** e um relatorio publicado pela **CFTC** (Commodity Futures Trading Commission), a agencia reguladora do mercado de futuros dos EUA. Ele mostra **quem esta comprado e quem esta vendido** nos principais contratos futuros negociados nas bolsas americanas.

---

## Fonte dos Dados

| Item | Detalhe |
|------|---------|
| **Orgao** | CFTC (Commodity Futures Trading Commission) |
| **Site Oficial** | https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm |
| **Pais** | Estados Unidos |
| **Tipo de Dado** | Posicoes em contratos futuros |

---

## Frequencia de Atualizacao

| Evento | Dia |
|--------|-----|
| **Posicoes sao fotografadas** | Toda TERCA-FEIRA (fechamento) |
| **Relatorio e publicado** | Toda SEXTA-FEIRA (15:30 horario de NY) |
| **Defasagem** | 3 dias uteis |

**Exemplo:**
- Posicoes de terca 17/dez/2025
- Publicadas na sexta 20/dez/2025
- Voce ve os dados na segunda 23/dez/2025

---

## O que o Relatorio Mostra

O COT revela as posicoes de **todos os grandes participantes reportaveis**, alem do agregado dos pequenos traders (non-reportable). As categorias utilizadas seguem o **Financial Futures COT**, aplicavel a moedas, juros e indices financeiros.

### Categorias de Participantes

| Categoria | Quem sao | O que fazem |
|-----------|----------|-------------|
| **Asset Managers** | Fundos de pensao, seguradoras, fundos mutuos | Investem no longo prazo |
| **Leveraged Funds** | Hedge funds, CTAs, macro funds | Especulam e seguem tendencias |
| **Dealers** | Bancos, corretoras | Fazem mercado e hedge |
| **Other Reportables** | Outros grandes players | Diversos |
| **Non-Reportable** | Pequenos traders (retail) | Posicoes pequenas |

---

## Ativos que Analisamos

Nesta pesquisa, focamos em **3 ativos** que impactam diretamente o mercado brasileiro:

### 1. Brazilian Real (BRL)
| Item | Detalhe |
|------|---------|
| **Contrato** | BRL/USD Futures |
| **Bolsa** | CME (Chicago Mercantile Exchange) |
| **Tamanho** | 100,000 BRL por contrato |
| **Codigo CFTC** | 102741 |
| **Por que importa** | Mostra se gringos estao apostando a favor ou contra o Real |

### 2. U.S. Dollar Index (DXY)
| Item | Detalhe |
|------|---------|
| **Contrato** | DXY Futures |
| **Bolsa** | ICE Futures U.S. |
| **Tamanho** | $1,000 x indice |
| **Codigo CFTC** | 098662 |
| **Por que importa** | Mostra a forca do dolar globalmente |

### 3. Treasuries 10 Anos (T10Y)
| Item | Detalhe |
|------|---------|
| **Contrato** | 10-Year T-Note Futures |
| **Bolsa** | CBOT (Chicago Board of Trade) |
| **Tamanho** | $100,000 face value |
| **Codigo CFTC** | 043602 |
| **Por que importa** | Mostra expectativa de juros americanos (afeta dolar e emergentes) |

---

## Periodo Historico Analisado

| Metrica | Valor |
|---------|-------|
| **Data inicial** | Janeiro de 2020 |
| **Data final** | Ultimo relatorio disponivel |
| **Total de semanas** | ~310 semanas |
| **Total de anos** | ~5 anos |

### Por que 5 anos?
- Inclui periodo pre-pandemia (2020)
- Inclui crise COVID (2020)
- Inclui alta de juros do Fed (2022-2023)
- Inclui diversos ciclos de mercado
- Periodo suficiente para calcular percentis significativos

---

## O que Calculamos

### 1. Net Position (Posicao Liquida)
```
Net Position = Contratos Long - Contratos Short
```
- **Positivo:** Participante esta COMPRADO (aposta na alta)
- **Negativo:** Participante esta VENDIDO (aposta na baixa)

### 2. Percentil Historico
```
Percentil = % de observacoes historicas que foram MENORES que o valor atual
```
- **Percentil 95%:** Apenas 5% das observacoes historicas foram MAIORES que o valor atual (extremamente comprado)
- **Percentil 5%:** Apenas 5% das observacoes historicas foram MENORES que o valor atual (extremamente vendido)

### 3. Classificacao de Regime
Baseado nos percentis, classificamos o ambiente de mercado:
- **BAIXO:** Sem extremos
- **MODERADO:** Algum indicador em extremo
- **ELEVADO:** Multiplos indicadores em extremo

---

## Fluxo de Dados

```
1. Traders operam futuros nas bolsas (CME, ICE, CBOT)
           |
           v
2. CFTC coleta posicoes de todos os grandes players
           |
           v
3. Posicoes sao "fotografadas" toda TERCA-FEIRA
           |
           v
4. Relatorio e publicado toda SEXTA-FEIRA
           |
           v
5. Nosso script baixa os dados do site da CFTC
           |
           v
6. Calculamos percentis comparando com historico de 5 anos
           |
           v
7. Geramos o relatorio cot_report.md
```

---

## Por que isso Importa para o Brasil?

### Conexao entre os ativos:

```
Treasuries 10Y (yields)
        |
        v
    DXY (dolar global)
        |
        v
    USD/BRL (dolar no Brasil)
        |
        v
    Bolsa, juros, inflacao brasileira
```

### Logica:
1. Posicionamento especulativo SHORT em Treasuries indica **expectativa de yields mais altos**
2. Yields mais altos historicamente se associam a **dolar mais forte**
3. Dolar mais forte historicamente se associa a **pressao de ALTA no USD/BRL**
4. Real mais fraco tende a aumentar **inflacao importada**, elevando o risco de resposta monetaria mais restritiva

### Por isso monitoramos:
- **BRL:** Posicao direta no Real
- **DXY:** Forca do dolar global
- **T10Y:** Expectativa de juros americanos

---

## Limitacoes

| Limitacao | Explicacao |
|-----------|------------|
| **Defasagem de 3 dias** | Dados de terca, publicados na sexta |
| **Apenas futuros** | Nao inclui mercado spot ou opcoes |
| **Apenas bolsas americanas** | Nao inclui B3 ou outras bolsas |
| **Posicoes agregadas** | Nao sabemos quem especificamente esta comprando/vendendo |
| **Nao mostra timing** | Extremos podem persistir por semanas ou meses antes de reverter |

---

## Arquivos Gerados

| Arquivo | Funcao |
|---------|--------|
| `cot_report.md` | Relatorio principal com analise (sempre atualizado) |
| `cot_evolucao.md` | Comparativo de evolucao semana a semana |
| `historico/cot_historico.json` | Historico de percentis para acompanhamento semanal |
| `historico/cot_report_YYYY-MM-DD.md` | Copias datadas de cada relatorio |
| `scripts/cot_final_report.py` | Script principal para gerar o relatorio |
| `atualizar.bat` | Atalho para rodar o script no Windows |

---

## Como Atualizar

Para obter os dados mais recentes, execute:

```bash
cd c:\Users\Fernando\Desktop\trad
python scripts/cot_final_report.py
```

Ou simplesmente clique em `atualizar.bat`.

O script ira:
1. Baixar dados historicos (2020-2025)
2. Calcular percentis comparando com historico
3. Gerar novo `cot_report.md`
4. Salvar copia datada em `historico/`
5. Atualizar `cot_historico.json` com os percentis
6. Gerar `cot_evolucao.md` (apos 2+ semanas)

---

## Cronograma Tipico

| Dia | Evento |
|-----|--------|
| **Terca** | CFTC "fotografa" posicoes |
| **Sexta 15:30 NY** | CFTC publica relatorio |
| **Sabado/Domingo** | Voce pode rodar o script |
| **Segunda** | Analisar antes da abertura do mercado |

---

## Resumo Final

| Pergunta | Resposta |
|----------|----------|
| **O que e?** | Relatorio de posicoes em futuros da CFTC |
| **Quem publica?** | CFTC (regulador americano) |
| **Quando?** | Toda sexta-feira |
| **O que mostra?** | Quem esta comprado/vendido nos futuros |
| **Periodo analisado?** | 5 anos (2020-2025, ~310 semanas) |
| **Para que serve?** | Identificar posicionamento de grandes players e extremos historicos |
| **Ativos monitorados?** | BRL, DXY, Treasuries 10Y |

---

## Nota Importante

> **Este e um indicador de POSICIONAMENTO, nao de PREVISAO.**
>
> O COT mostra onde os participantes estao posicionados, nao para onde o mercado vai.
> Extremos indicam **risco de reversao**, mas nao garantem quando ela ocorrera.
> Use como ferramenta de contexto, nao como sinal de entrada/saida.

---

*Documento criado em 23/12/2025*
*Fonte: CFTC - Commitments of Traders*
