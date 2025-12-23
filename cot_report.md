# Relatorio COT - Analise Institucional

**Data do Relatorio CFTC:** 2025-12-09
**Periodo Historico:** 2020-2025 (~5 anos, ~310 semanas)
**Fonte:** CFTC Commitments of Traders

---

## LEGENDA DE REGIME

| Nivel | Icone | Significado | Acao Sugerida |
|-------|-------|-------------|---------------|
| **BAIXO** | ✅ | Posicionamento equilibrado, sem extremos | Operar normalmente |
| **MODERADO** | ⚠️ | Algum indicador em nivel elevado | Gestao de risco ativa |
| **ELEVADO** | ⛔ | Multiplos indicadores em extremos historicos | Evitar carry trade, reduzir exposicao |

### Criterios para cada nivel:
- **BAIXO:** Nenhum percentil acima de 85% ou abaixo de 15%
- **MODERADO:** 1 indicador em extremo (>85% ou <15%)
- **ELEVADO:** 2+ indicadores em extremo OU qualquer indicador em <5% ou >95%

---

## ⛔ REGIME ATUAL: ELEVADO

☑ Crowded trade em BRL (specs muito comprados)
☑ Specs muito vendidos em DXY (aposta em dolar fraco)
☑ Short EXTREMO em Treasuries (aposta em yields altos)
☑ Juros pressionando (specs short em bonds)

**⛔ NAO e ambiente limpo para carry trade. Reduzir exposicao.**

---

## Resumo com Contexto Historico

| Ativo | Categoria | Net Position | Percentil | Classificacao | Status |
|-------|-----------|--------------|-----------|---------------|--------|
| **BRL** | Asset Manager | +59,763 | **93%** | MUITO COMPRADO | 🟡 |
| **DXY** | Leveraged Funds | -21,260 | **0%** | MUITO VENDIDO | 🟡 |
| **T10Y** | Leveraged Funds | -2,281,123 | **0%** | EXTREMO VENDIDO | 🔴 |

---

## 1. BRAZILIAN REAL (BRL)

**Open Interest:** 98,454 contratos

### Posicoes Atuais
| Categoria | Long | Short | Net | Percentil |
|-----------|------|-------|-----|-----------|
| Asset Manager | 62,153 | 2,390 | **+59,763** | **93%** |
| Leveraged Funds | 22,874 | 13,538 | **+9,336** | 84% |
| Dealer | 3,611 | 69,515 | -65,904 | - |

### Contexto Historico (2020-2025)

| Metrica | Asset Manager Net | Leveraged Funds Net |
|---------|-------------------|---------------------|
| **Atual** | **+59,763** | **+9,336** |
| **Percentil** | **93%** | **84%** |
| Minimo | -57,523 | -40,335 |
| Maximo | 78,334 | 31,550 |
| Media | 11,677 | -1,326 |
| P90 | 57,328 | 12,142 |
| P95 | 63,276 | 14,679 |

### 🟡 ALERTA: Posicao no TOP 7% historico
- Em apenas **7%** das semanas desde 2020, a posicao foi MAIOR que agora
- **RISCO DE REVERSAO:** Quando todos estao comprados, nao ha compradores marginais
- Qualquer catalisador negativo (Copom, fiscal, Fed) pode gerar liquidacao violenta

---

## 2. U.S. DOLLAR INDEX (DXY)

**Open Interest:** 42,972 contratos

### Posicoes Atuais
| Categoria | Long | Short | Net | Percentil |
|-----------|------|-------|-----|-----------|
| Asset Manager | 6,781 | 2,250 | **+4,531** | 45% |
| Leveraged Funds | 6,908 | 28,168 | **-21,260** | **0%** |
| Dealer | 18,483 | 62 | +18,421 | - |

### Contexto Historico
| Metrica | Leveraged Funds Net |
|---------|---------------------|
| **Atual** | **-21,260** |
| **Percentil** | **0%** |
| Minimo | -16,501 |
| Maximo | 17,792 |
| Media | 5 |

### 🟡 Specs VENDIDOS no Dolar
- Posicao no **BOTTOM 0%** historico
- Hedge Funds apostam na FRAQUEZA do dolar
- **DIVERGENCIA:** Se DXY subir, podem ter que cobrir shorts (dolar mais forte)

---

## 3. TREASURIES 10 ANOS (T10Y)

**Open Interest:** 5,513,724 contratos

### Posicoes Atuais
| Categoria | Long | Short | Net | Percentil |
|-----------|------|-------|-----|-----------|
| Asset Manager | 3,000,483 | 929,853 | **+2,070,630** | 100% |
| Leveraged Funds | 577,108 | 2,858,231 | **-2,281,123** | **0%** |
| Dealer | 386,595 | 510,523 | -123,928 | - |

### Contexto Historico
| Metrica | Leveraged Funds Net |
|---------|---------------------|
| **Atual** | **-2,281,123** |
| **Percentil** | **0%** |
| Minimo | -817,169 |
| Maximo | 607,705 |
| Media | 18,451 |

### 🔴 ALERTA: Short EXTREMO Historico
- Posicao no **BOTTOM 0%** - uma das maiores posicoes vendidas desde 2020
- Specs apostam MASSIVAMENTE em yields mais altos
- **IMPLICACAO DIRETA:**
  - Yields altos = Dolar mais forte globalmente
  - Dolar forte = Pressao de ALTA no USD/BRL
  - Ambiente DESFAVORAVEL para Real e emergentes

---

## Matriz de Regime

| Condicao | Status | Impacto USD/BRL |
|----------|--------|-----------------|
| Specs crowded em BRL | ☑ | Risco de reversao ALTA |
| Specs short DXY | ☑ | Se cobrirem, dolar sobe |
| Yields pressionados | ☑ | Favorece dolar, pressiona Real |

---

## Interpretacao Final

### Cenario Base

**⛔ CONTRADICAO NO POSICIONAMENTO:**
- Specs estao COMPRADOS em Real (apostando em dolar fraco no Brasil)
- MAS tambem estao SHORT em Treasuries (apostando em yields altos = dolar forte)
- Essas posicoes sao **INCONSISTENTES** no medio prazo

**Resolucao provavel:**
1. Yields sobem -> Dolar fortalece -> Real cai -> Specs vendem BRL (reversao)
2. OU dados macro mudam -> Yields caem -> Posicao em T10Y reverte primeiro

De qualquer forma, **uma dessas posicoes vai reverter**.

---

## Glossario

| Termo | Definicao |
|-------|-----------|
| **Percentil** | % de observacoes historicas ABAIXO do valor atual |
| **P95** | Valor esta no TOP 5% historico (muito alto) |
| **P5** | Valor esta no BOTTOM 5% historico (muito baixo) |
| **Crowded Trade** | Quando todos estao do mesmo lado - risco de reversao |
| **Net Position** | Long - Short |
| **Asset Manager** | Fundos de pensao, seguradoras, institucionais |
| **Leveraged Funds** | Hedge funds, CTAs, macro funds |

---

## LEGENDA DE ALERTAS (Status)

| Icone | Percentil | Significado |
|-------|-----------|-------------|
| 🟢 | 20% - 80% | Normal - dentro da faixa historica |
| 🟡 | 5% - 20% ou 80% - 95% | Atencao - posicao elevada |
| 🔴 | <5% ou >95% | Extremo - posicao historicamente rara |

---

## LEGENDA DE CLASSIFICACAO (Posicao)

| Classificacao | Percentil | Significado |
|---------------|-----------|-------------|
| EXTREMO COMPRADO | >95% | Posicao no TOP 5% historico - risco maximo de reversao |
| MUITO COMPRADO | 80% - 95% | Posicao elevada - atencao |
| LEVEMENTE COMPRADO | 60% - 80% | Acima da media, mas normal |
| NEUTRO | 40% - 60% | Proximo da media historica |
| LEVEMENTE VENDIDO | 20% - 40% | Abaixo da media, mas normal |
| MUITO VENDIDO | 5% - 20% | Posicao baixa - atencao |
| EXTREMO VENDIDO | <5% | Posicao no BOTTOM 5% historico - risco maximo de reversao |

---

## COMO LER ESTE RELATORIO

1. **Olhe o REGIME primeiro** (topo) - ele resume tudo
2. **Verifique os percentis** - quanto mais proximo de 0% ou 100%, mais extremo
3. **Leia os alertas** 🔴 - sao os pontos criticos
4. **A Matriz de Regime** mostra o impacto combinado

### Este relatorio e AUTO-SUFICIENTE
Voce NAO precisa de IA para interpretar. Os alertas, percentis e regime ja indicam a situacao.

| Se o regime for... | Entao... |
|--------------------|----------|
| ✅ BAIXO | Operar normalmente |
| ⚠️ MODERADO | Gestao de risco ativa |
| ⛔ ELEVADO | Evitar carry trade, reduzir exposicao |

---

*Relatorio gerado com dados atuais + historico de 5 anos (2020-2025)*
*Atualizacao do COT: toda sexta-feira apos fechamento do mercado americano*
*Para atualizar: python cot_final_report.py*
