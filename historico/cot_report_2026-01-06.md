# Relatorio COT - Analise Institucional

**Data do Relatorio CFTC:** 2026-01-06
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

☑ Short EXTREMO em Treasuries (aposta em yields altos)
☑ Juros pressionando (specs short em bonds)

**⛔ NAO e ambiente limpo para carry trade. Reduzir exposicao.**

---

## Resumo com Contexto Historico

| Ativo | Categoria | Net Position | Percentil | Classificacao | Status |
|-------|-----------|--------------|-----------|---------------|--------|
| **BRL** | Asset Manager | +37,367 | **77%** | LEVEMENTE COMPRADO | 🟢 |
| **DXY** | Leveraged Funds | +766 | **57%** | NEUTRO | 🟢 |
| **T10Y** | Leveraged Funds | -2,335,739 | **0%** | EXTREMO VENDIDO | 🔴 |

---

## 1. BRAZILIAN REAL (BRL)

**Open Interest:** 73,669 contratos

### Posicoes Atuais
| Categoria | Long | Short | Net | Percentil |
|-----------|------|-------|-----|-----------|
| Asset Manager | 41,310 | 3,943 | **+37,367** | **77%** |
| Leveraged Funds | 21,860 | 20,440 | **+1,420** | 60% |
| Dealer | 1,171 | 44,772 | -43,601 | - |

### Contexto Historico (2020-2025)

| Metrica | Asset Manager Net | Leveraged Funds Net |
|---------|-------------------|---------------------|
| **Atual** | **+37,367** | **+1,420** |
| **Percentil** | **77%** | **60%** |
| Minimo | -57,523 | -40,335 |
| Maximo | 78,334 | 31,550 |
| Media | 11,977 | -1,226 |
| P90 | 57,248 | 12,180 |
| P95 | 63,257 | 14,655 |

---

## 2. U.S. DOLLAR INDEX (DXY)

**Open Interest:** 30,078 contratos

### Posicoes Atuais
| Categoria | Long | Short | Net | Percentil |
|-----------|------|-------|-----|-----------|
| Asset Manager | 2,799 | 4,117 | **-1,318** | 24% |
| Leveraged Funds | 15,398 | 14,632 | **+766** | **57%** |
| Dealer | 3,450 | 767 | +2,683 | - |

### Contexto Historico
| Metrica | Leveraged Funds Net |
|---------|---------------------|
| **Atual** | **+766** |
| **Percentil** | **57%** |
| Minimo | -16,501 |
| Maximo | 17,792 |
| Media | 5 |

---

## 3. TREASURIES 10 ANOS (T10Y)

**Open Interest:** 5,536,100 contratos

### Posicoes Atuais
| Categoria | Long | Short | Net | Percentil |
|-----------|------|-------|-----|-----------|
| Asset Manager | 3,129,213 | 909,530 | **+2,219,683** | 100% |
| Leveraged Funds | 431,405 | 2,767,144 | **-2,335,739** | **0%** |
| Dealer | 418,498 | 544,325 | -125,827 | - |

### Contexto Historico
| Metrica | Leveraged Funds Net |
|---------|---------------------|
| **Atual** | **-2,335,739** |
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
| Specs crowded em BRL | ☐ | - |
| Specs short DXY | ☐ | - |
| Yields pressionados | ☑ | Favorece dolar, pressiona Real |

---

## Interpretacao Final

### Cenario Base

**✅ Posicionamento relativamente equilibrado**
- Sem extremos historicos criticos
- Monitorar mudancas semanais

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
