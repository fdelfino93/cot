"""
Gera relatorio final com dados atuais + contexto historico
Usa dados atuais extraidos do site + historico para percentis
"""

import pandas as pd
import requests
import zipfile
import io
from scipy import stats
import json
import os
from datetime import datetime


# DADOS ATUAIS (extraidos automaticamente em 2026-01-05 09:18, relatorio de 2025-12-23)
CURRENT_DATA = {
    "report_date": "2025-12-23",
    "BRL": {
        "open_interest": 113899,
        "asset_manager": {"long": 42195, "short": 853, "net": 41342},
        "leveraged_funds": {"long": 23770, "short": 14566, "net": 9204},
        "dealer": {"long": 10212, "short": 65390, "net": -55178}
    },
    "DXY": {
        "open_interest": 28181,
        "asset_manager": {"long": 3320, "short": 2152, "net": 1168},
        "leveraged_funds": {"long": 13485, "short": 14811, "net": -1326},
        "dealer": {"long": 3663, "short": 767, "net": 2896}
    },
    "T10Y": {
        "open_interest": 5569530,
        "asset_manager": {"long": 3046897, "short": 960365, "net": 2086532},
        "leveraged_funds": {"long": 527617, "short": 2825944, "net": -2298327},
        "dealer": {"long": 398925, "short": 519474, "net": -120549}
    }
}


def get_historical_data():
    """Baixa dados historicos 2020-2025"""

    base_url = "https://www.cftc.gov/files/dea/history"
    years = [2025, 2024, 2023, 2022, 2021, 2020]

    all_dfs = []

    print("Baixando dados historicos...")
    for year in years:
        url = f"{base_url}/fut_fin_txt_{year}.zip"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                z = zipfile.ZipFile(io.BytesIO(response.content))
                for filename in z.namelist():
                    if filename.endswith('.txt'):
                        with z.open(filename) as f:
                            df = pd.read_csv(f)
                            all_dfs.append(df)
                            print(f"  {year}: OK")
        except Exception as e:
            print(f"  {year}: ERRO - {e}")

    return pd.concat(all_dfs, ignore_index=True) if all_dfs else None


def get_asset_history(df, asset_filter):
    """Extrai historico de um ativo"""
    mask = df["Market_and_Exchange_Names"].str.upper().str.contains(asset_filter, na=False)
    asset_df = df[mask].copy()

    if len(asset_df) == 0:
        return None

    asset_df["Report_Date_as_YYYY-MM-DD"] = pd.to_datetime(asset_df["Report_Date_as_YYYY-MM-DD"])
    asset_df = asset_df.sort_values("Report_Date_as_YYYY-MM-DD")

    # Net positions
    asset_df["AM_Net"] = asset_df["Asset_Mgr_Positions_Long_All"] - asset_df["Asset_Mgr_Positions_Short_All"]
    asset_df["LF_Net"] = asset_df["Lev_Money_Positions_Long_All"] - asset_df["Lev_Money_Positions_Short_All"]

    return asset_df[["Report_Date_as_YYYY-MM-DD", "AM_Net", "LF_Net"]].dropna()


def calculate_percentile(series, current_value):
    """Calcula percentil do valor atual na serie historica"""
    return stats.percentileofscore(series, current_value)


def classify_position(percentile):
    """Classifica posicao baseada no percentil"""
    if percentile >= 95:
        return "EXTREMO COMPRADO", "🔴"
    elif percentile >= 80:
        return "MUITO COMPRADO", "🟡"
    elif percentile >= 60:
        return "LEVEMENTE COMPRADO", "🟢"
    elif percentile >= 40:
        return "NEUTRO", "⚪"
    elif percentile >= 20:
        return "LEVEMENTE VENDIDO", "🟢"
    elif percentile >= 5:
        return "MUITO VENDIDO", "🟡"
    else:
        return "EXTREMO VENDIDO", "🔴"


def generate_report(current, history):
    """Gera o relatorio final"""

    # Calcula percentis
    brl_hist = history.get("BRL")
    dxy_hist = history.get("DXY")
    t10y_hist = history.get("T10Y")

    # BRL
    brl_am_pct = calculate_percentile(brl_hist["AM_Net"], current["BRL"]["asset_manager"]["net"]) if brl_hist is not None else 0
    brl_lf_pct = calculate_percentile(brl_hist["LF_Net"], current["BRL"]["leveraged_funds"]["net"]) if brl_hist is not None else 0

    # DXY
    dxy_am_pct = calculate_percentile(dxy_hist["AM_Net"], current["DXY"]["asset_manager"]["net"]) if dxy_hist is not None else 0
    dxy_lf_pct = calculate_percentile(dxy_hist["LF_Net"], current["DXY"]["leveraged_funds"]["net"]) if dxy_hist is not None else 0

    # T10Y
    t10y_am_pct = calculate_percentile(t10y_hist["AM_Net"], current["T10Y"]["asset_manager"]["net"]) if t10y_hist is not None else 0
    t10y_lf_pct = calculate_percentile(t10y_hist["LF_Net"], current["T10Y"]["leveraged_funds"]["net"]) if t10y_hist is not None else 0

    # Classificacoes
    brl_class, brl_emoji = classify_position(brl_am_pct)
    dxy_class, dxy_emoji = classify_position(100 - dxy_lf_pct)  # Inverte pq short = baixo percentil
    t10y_class, t10y_emoji = classify_position(100 - t10y_lf_pct)  # Inverte

    # Determina regime
    regime_flags = []

    if brl_am_pct >= 90:
        regime_flags.append("☑ Crowded trade em BRL (specs muito comprados)")
    if dxy_lf_pct <= 10:
        regime_flags.append("☑ Specs muito vendidos em DXY (aposta em dolar fraco)")
    if t10y_lf_pct <= 5:
        regime_flags.append("☑ Short EXTREMO em Treasuries (aposta em yields altos)")
    if t10y_lf_pct <= 10:
        regime_flags.append("☑ Juros pressionando (specs short em bonds)")

    if t10y_lf_pct <= 5 or brl_am_pct >= 95:
        regime_type = "ELEVADO"
        regime_icon = "⛔"
        regime_msg = "NAO e ambiente limpo para carry trade. Reduzir exposicao."
    elif t10y_lf_pct <= 15 or brl_am_pct >= 85:
        regime_type = "MODERADO"
        regime_icon = "⚠️"
        regime_msg = "Ambiente requer gestao de risco ativa"
    else:
        regime_type = "BAIXO"
        regime_icon = "✅"
        regime_msg = "Ambiente relativamente normal. Operar normalmente."

    report = f"""# Relatorio COT - Analise Institucional

**Data do Relatorio CFTC:** {current['report_date']}
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

## {regime_icon} REGIME ATUAL: {regime_type}

"""

    for flag in regime_flags:
        report += f"{flag}\n"

    if not regime_flags:
        report += "☐ Sem alertas significativos\n"

    report += f"""
**{regime_icon} {regime_msg}**

---

## Resumo com Contexto Historico

| Ativo | Categoria | Net Position | Percentil | Classificacao | Status |
|-------|-----------|--------------|-----------|---------------|--------|
| **BRL** | Asset Manager | {current['BRL']['asset_manager']['net']:+,} | **{brl_am_pct:.0f}%** | {brl_class} | {brl_emoji} |
| **DXY** | Leveraged Funds | {current['DXY']['leveraged_funds']['net']:+,} | **{dxy_lf_pct:.0f}%** | {"MUITO VENDIDO" if dxy_lf_pct <= 20 else "LEVEMENTE VENDIDO" if dxy_lf_pct <= 40 else "NEUTRO"} | {"🟡" if dxy_lf_pct <= 20 else "🟢"} |
| **T10Y** | Leveraged Funds | {current['T10Y']['leveraged_funds']['net']:+,} | **{t10y_lf_pct:.0f}%** | {"EXTREMO VENDIDO" if t10y_lf_pct <= 5 else "MUITO VENDIDO" if t10y_lf_pct <= 20 else "VENDIDO"} | {"🔴" if t10y_lf_pct <= 5 else "🟡"} |

---

## 1. BRAZILIAN REAL (BRL)

**Open Interest:** {current['BRL']['open_interest']:,} contratos

### Posicoes Atuais
| Categoria | Long | Short | Net | Percentil |
|-----------|------|-------|-----|-----------|
| Asset Manager | {current['BRL']['asset_manager']['long']:,} | {current['BRL']['asset_manager']['short']:,} | **{current['BRL']['asset_manager']['net']:+,}** | **{brl_am_pct:.0f}%** |
| Leveraged Funds | {current['BRL']['leveraged_funds']['long']:,} | {current['BRL']['leveraged_funds']['short']:,} | **{current['BRL']['leveraged_funds']['net']:+,}** | {brl_lf_pct:.0f}% |
| Dealer | {current['BRL']['dealer']['long']:,} | {current['BRL']['dealer']['short']:,} | {current['BRL']['dealer']['net']:+,} | - |

### Contexto Historico (2020-2025)
"""

    if brl_hist is not None:
        report += f"""
| Metrica | Asset Manager Net | Leveraged Funds Net |
|---------|-------------------|---------------------|
| **Atual** | **{current['BRL']['asset_manager']['net']:+,}** | **{current['BRL']['leveraged_funds']['net']:+,}** |
| **Percentil** | **{brl_am_pct:.0f}%** | **{brl_lf_pct:.0f}%** |
| Minimo | {int(brl_hist['AM_Net'].min()):,} | {int(brl_hist['LF_Net'].min()):,} |
| Maximo | {int(brl_hist['AM_Net'].max()):,} | {int(brl_hist['LF_Net'].max()):,} |
| Media | {int(brl_hist['AM_Net'].mean()):,} | {int(brl_hist['LF_Net'].mean()):,} |
| P90 | {int(brl_hist['AM_Net'].quantile(0.90)):,} | {int(brl_hist['LF_Net'].quantile(0.90)):,} |
| P95 | {int(brl_hist['AM_Net'].quantile(0.95)):,} | {int(brl_hist['LF_Net'].quantile(0.95)):,} |
"""

    if brl_am_pct >= 90:
        report += f"""
### {brl_emoji} ALERTA: Posicao no TOP {100-brl_am_pct:.0f}% historico
- Em apenas **{100-brl_am_pct:.0f}%** das semanas desde 2020, a posicao foi MAIOR que agora
- **RISCO DE REVERSAO:** Quando todos estao comprados, nao ha compradores marginais
- Qualquer catalisador negativo (Copom, fiscal, Fed) pode gerar liquidacao violenta
"""

    report += f"""
---

## 2. U.S. DOLLAR INDEX (DXY)

**Open Interest:** {current['DXY']['open_interest']:,} contratos

### Posicoes Atuais
| Categoria | Long | Short | Net | Percentil |
|-----------|------|-------|-----|-----------|
| Asset Manager | {current['DXY']['asset_manager']['long']:,} | {current['DXY']['asset_manager']['short']:,} | **{current['DXY']['asset_manager']['net']:+,}** | {dxy_am_pct:.0f}% |
| Leveraged Funds | {current['DXY']['leveraged_funds']['long']:,} | {current['DXY']['leveraged_funds']['short']:,} | **{current['DXY']['leveraged_funds']['net']:+,}** | **{dxy_lf_pct:.0f}%** |
| Dealer | {current['DXY']['dealer']['long']:,} | {current['DXY']['dealer']['short']:,} | {current['DXY']['dealer']['net']:+,} | - |
"""

    if dxy_hist is not None:
        report += f"""
### Contexto Historico
| Metrica | Leveraged Funds Net |
|---------|---------------------|
| **Atual** | **{current['DXY']['leveraged_funds']['net']:+,}** |
| **Percentil** | **{dxy_lf_pct:.0f}%** |
| Minimo | {int(dxy_hist['LF_Net'].min()):,} |
| Maximo | {int(dxy_hist['LF_Net'].max()):,} |
| Media | {int(dxy_hist['LF_Net'].mean()):,} |
"""

    if dxy_lf_pct <= 15:
        report += f"""
### 🟡 Specs VENDIDOS no Dolar
- Posicao no **BOTTOM {dxy_lf_pct:.0f}%** historico
- Hedge Funds apostam na FRAQUEZA do dolar
- **DIVERGENCIA:** Se DXY subir, podem ter que cobrir shorts (dolar mais forte)
"""

    report += f"""
---

## 3. TREASURIES 10 ANOS (T10Y)

**Open Interest:** {current['T10Y']['open_interest']:,} contratos

### Posicoes Atuais
| Categoria | Long | Short | Net | Percentil |
|-----------|------|-------|-----|-----------|
| Asset Manager | {current['T10Y']['asset_manager']['long']:,} | {current['T10Y']['asset_manager']['short']:,} | **{current['T10Y']['asset_manager']['net']:+,}** | {t10y_am_pct:.0f}% |
| Leveraged Funds | {current['T10Y']['leveraged_funds']['long']:,} | {current['T10Y']['leveraged_funds']['short']:,} | **{current['T10Y']['leveraged_funds']['net']:+,}** | **{t10y_lf_pct:.0f}%** |
| Dealer | {current['T10Y']['dealer']['long']:,} | {current['T10Y']['dealer']['short']:,} | {current['T10Y']['dealer']['net']:+,} | - |
"""

    if t10y_hist is not None:
        report += f"""
### Contexto Historico
| Metrica | Leveraged Funds Net |
|---------|---------------------|
| **Atual** | **{current['T10Y']['leveraged_funds']['net']:+,}** |
| **Percentil** | **{t10y_lf_pct:.0f}%** |
| Minimo | {int(t10y_hist['LF_Net'].min()):,} |
| Maximo | {int(t10y_hist['LF_Net'].max()):,} |
| Media | {int(t10y_hist['LF_Net'].mean()):,} |
"""

    if t10y_lf_pct <= 5:
        report += f"""
### 🔴 ALERTA: Short EXTREMO Historico
- Posicao no **BOTTOM {t10y_lf_pct:.0f}%** - uma das maiores posicoes vendidas desde 2020
- Specs apostam MASSIVAMENTE em yields mais altos
- **IMPLICACAO DIRETA:**
  - Yields altos = Dolar mais forte globalmente
  - Dolar forte = Pressao de ALTA no USD/BRL
  - Ambiente DESFAVORAVEL para Real e emergentes
"""
    elif t10y_lf_pct <= 15:
        report += f"""
### 🟡 Posicao Short Significativa
- Specs vendidos em bonds (percentil {t10y_lf_pct:.0f}%)
- Pressao de alta nos yields deve persistir
"""

    report += """
---

## Matriz de Regime

| Condicao | Status | Impacto USD/BRL |
|----------|--------|-----------------|
"""

    # BRL
    if brl_am_pct >= 90:
        report += "| Specs crowded em BRL | ☑ | Risco de reversao ALTA |\n"
    else:
        report += "| Specs crowded em BRL | ☐ | - |\n"

    # DXY
    if dxy_lf_pct <= 20:
        report += "| Specs short DXY | ☑ | Se cobrirem, dolar sobe |\n"
    else:
        report += "| Specs short DXY | ☐ | - |\n"

    # T10Y
    if t10y_lf_pct <= 10:
        report += "| Yields pressionados | ☑ | Favorece dolar, pressiona Real |\n"
    else:
        report += "| Yields pressionados | ☐ | - |\n"

    report += f"""
---

## Interpretacao Final

### Cenario Base
"""

    if brl_am_pct >= 85 and t10y_lf_pct <= 15:
        report += """
**⛔ CONTRADICAO NO POSICIONAMENTO:**
- Specs estao COMPRADOS em Real (apostando em dolar fraco no Brasil)
- MAS tambem estao SHORT em Treasuries (apostando em yields altos = dolar forte)
- Essas posicoes sao **INCONSISTENTES** no medio prazo

**Resolucao provavel:**
1. Yields sobem -> Dolar fortalece -> Real cai -> Specs vendem BRL (reversao)
2. OU dados macro mudam -> Yields caem -> Posicao em T10Y reverte primeiro

De qualquer forma, **uma dessas posicoes vai reverter**.
"""
    elif brl_am_pct >= 85:
        report += """
**⚠️ CROWDED TRADE EM BRL:**
- Cuidado com posicoes compradas em Real
- O mercado esta muito inclinado para um lado
"""
    else:
        report += """
**✅ Posicionamento relativamente equilibrado**
- Sem extremos historicos criticos
- Monitorar mudancas semanais
"""

    report += """
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
"""

    return report


def save_percentile_history(report_date, brl_pct, dxy_pct, t10y_pct, current_data):
    """Salva percentis no arquivo de historico JSON"""
    # Cria pasta historico se nao existir
    os.makedirs("historico", exist_ok=True)
    history_file = os.path.join("historico", "cot_historico.json")

    # Carrega historico existente ou cria novo
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = {"registros": []}

    # Verifica se ja existe registro para esta data
    existing_dates = [r["report_date"] for r in history["registros"]]

    if report_date in existing_dates:
        # Atualiza registro existente
        for r in history["registros"]:
            if r["report_date"] == report_date:
                r["BRL"] = {
                    "am_net": current_data["BRL"]["asset_manager"]["net"],
                    "am_pct": round(brl_pct, 1)
                }
                r["DXY"] = {
                    "lf_net": current_data["DXY"]["leveraged_funds"]["net"],
                    "lf_pct": round(dxy_pct, 1)
                }
                r["T10Y"] = {
                    "lf_net": current_data["T10Y"]["leveraged_funds"]["net"],
                    "lf_pct": round(t10y_pct, 1)
                }
                r["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                break
    else:
        # Adiciona novo registro
        novo_registro = {
            "report_date": report_date,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "BRL": {
                "am_net": current_data["BRL"]["asset_manager"]["net"],
                "am_pct": round(brl_pct, 1)
            },
            "DXY": {
                "lf_net": current_data["DXY"]["leveraged_funds"]["net"],
                "lf_pct": round(dxy_pct, 1)
            },
            "T10Y": {
                "lf_net": current_data["T10Y"]["leveraged_funds"]["net"],
                "lf_pct": round(t10y_pct, 1)
            }
        }
        history["registros"].append(novo_registro)
        # Ordena por data
        history["registros"].sort(key=lambda x: x["report_date"])

    # Salva
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    return history


def generate_evolution_report(history):
    """Gera relatorio de evolucao semanal (ultimas 10 semanas)"""
    registros = history.get("registros", [])

    if len(registros) < 2:
        return None

    # Pega apenas as ultimas 10 semanas (ou todas se tiver menos)
    ultimas_semanas = registros[-10:]
    total_registros = len(registros)

    report = f"""# Evolucao COT - Historico Semanal

**Acompanhamento da evolucao dos percentis ao longo do tempo**
**Exibindo:** {len(ultimas_semanas)} ultimas semanas (de {total_registros} total)

---

## Tabela de Evolucao

| Data | BRL AM Net | BRL Pct | Var | DXY LF Net | DXY Pct | Var | T10Y LF Net | T10Y Pct | Var |
|------|------------|---------|-----|------------|---------|-----|-------------|----------|-----|
"""

    # Para calcular variacao da primeira linha visivel, precisamos do registro anterior
    if len(registros) > len(ultimas_semanas):
        prev = registros[-(len(ultimas_semanas) + 1)]
    else:
        prev = None

    for r in ultimas_semanas:
        # Calcula variacao
        if prev:
            brl_var = r["BRL"]["am_pct"] - prev["BRL"]["am_pct"]
            dxy_var = r["DXY"]["lf_pct"] - prev["DXY"]["lf_pct"]
            t10y_var = r["T10Y"]["lf_pct"] - prev["T10Y"]["lf_pct"]

            brl_var_str = f"+{brl_var:.0f}pp" if brl_var > 0 else f"{brl_var:.0f}pp"
            dxy_var_str = f"+{dxy_var:.0f}pp" if dxy_var > 0 else f"{dxy_var:.0f}pp"
            t10y_var_str = f"+{t10y_var:.0f}pp" if t10y_var > 0 else f"{t10y_var:.0f}pp"
        else:
            brl_var_str = "-"
            dxy_var_str = "-"
            t10y_var_str = "-"

        report += f"| {r['report_date']} | {r['BRL']['am_net']:+,} | {r['BRL']['am_pct']:.0f}% | {brl_var_str} | {r['DXY']['lf_net']:+,} | {r['DXY']['lf_pct']:.0f}% | {dxy_var_str} | {r['T10Y']['lf_net']:+,} | {r['T10Y']['lf_pct']:.0f}% | {t10y_var_str} |\n"

        prev = r

    # Adiciona resumo do periodo visivel
    primeiro = ultimas_semanas[0]
    ultimo = ultimas_semanas[-1]

    brl_total = ultimo["BRL"]["am_pct"] - primeiro["BRL"]["am_pct"]
    dxy_total = ultimo["DXY"]["lf_pct"] - primeiro["DXY"]["lf_pct"]
    t10y_total = ultimo["T10Y"]["lf_pct"] - primeiro["T10Y"]["lf_pct"]

    report += f"""
---

## Resumo do Periodo ({primeiro['report_date']} a {ultimo['report_date']})

| Ativo | Categoria | Pct Inicial | Pct Final | Variacao Total |
|-------|-----------|-------------|-----------|----------------|
| BRL | Asset Manager | {primeiro['BRL']['am_pct']:.0f}% | {ultimo['BRL']['am_pct']:.0f}% | {brl_total:+.0f}pp |
| DXY | Leveraged Funds | {primeiro['DXY']['lf_pct']:.0f}% | {ultimo['DXY']['lf_pct']:.0f}% | {dxy_total:+.0f}pp |
| T10Y | Leveraged Funds | {primeiro['T10Y']['lf_pct']:.0f}% | {ultimo['T10Y']['lf_pct']:.0f}% | {t10y_total:+.0f}pp |

### Interpretacao:
"""

    # BRL
    if brl_total > 5:
        report += f"- **BRL:** Asset Managers AUMENTARAM posicao comprada ({brl_total:+.0f}pp)\n"
    elif brl_total < -5:
        report += f"- **BRL:** Asset Managers REDUZIRAM posicao comprada ({brl_total:+.0f}pp)\n"
    else:
        report += f"- **BRL:** Posicao estavel ({brl_total:+.0f}pp)\n"

    # DXY
    if dxy_total > 5:
        report += f"- **DXY:** Leveraged Funds REDUZIRAM short ({dxy_total:+.0f}pp) - menos aposta em dolar fraco\n"
    elif dxy_total < -5:
        report += f"- **DXY:** Leveraged Funds AUMENTARAM short ({dxy_total:+.0f}pp) - mais aposta em dolar fraco\n"
    else:
        report += f"- **DXY:** Posicao estavel ({dxy_total:+.0f}pp)\n"

    # T10Y
    if t10y_total > 5:
        report += f"- **T10Y:** Leveraged Funds REDUZIRAM short ({t10y_total:+.0f}pp) - menos aposta em yields altos\n"
    elif t10y_total < -5:
        report += f"- **T10Y:** Leveraged Funds AUMENTARAM short ({t10y_total:+.0f}pp) - mais aposta em yields altos\n"
    else:
        report += f"- **T10Y:** Posicao estavel ({t10y_total:+.0f}pp)\n"

    report += """
---

## Legenda

- **Pct**: Percentil historico (0-100%)
- **Var**: Variacao em pontos percentuais vs semana anterior
- **pp**: Pontos percentuais

---

*Arquivo atualizado automaticamente pelo script cot_final_report.py*
"""

    return report


def main():
    # Baixa historico
    df = get_historical_data()

    if df is None:
        print("Erro ao baixar dados!")
        return

    # Extrai historico de cada ativo
    history = {}

    print("\nExtraindo historico...")
    brl = get_asset_history(df, "BRAZILIAN REAL")
    if brl is not None:
        history["BRL"] = brl
        print(f"  BRL: {len(brl)} semanas")

    dxy = get_asset_history(df, "DOLLAR INDEX")
    if dxy is not None:
        history["DXY"] = dxy
        print(f"  DXY: {len(dxy)} semanas")

    t10y = get_asset_history(df, "10-YEAR")
    if t10y is not None:
        history["T10Y"] = t10y
        print(f"  T10Y: {len(t10y)} semanas")

    # Calcula percentis
    brl_pct = calculate_percentile(history["BRL"]["AM_Net"], CURRENT_DATA["BRL"]["asset_manager"]["net"])
    dxy_pct = calculate_percentile(history["DXY"]["LF_Net"], CURRENT_DATA["DXY"]["leveraged_funds"]["net"])
    t10y_pct = calculate_percentile(history["T10Y"]["LF_Net"], CURRENT_DATA["T10Y"]["leveraged_funds"]["net"])

    # Gera relatorio principal
    print("\nGerando relatorio...")
    report = generate_report(CURRENT_DATA, history)

    # Salva relatorio principal (sempre atualizado)
    with open("cot_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    print("Relatorio salvo em cot_report.md")

    # Salva copia com data
    report_date = CURRENT_DATA["report_date"]
    dated_filename = f"cot_report_{report_date}.md"

    # Cria pasta historico se nao existir
    os.makedirs("historico", exist_ok=True)

    dated_path = os.path.join("historico", dated_filename)
    with open(dated_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Copia datada salva em {dated_path}")

    # Salva no historico JSON
    percentile_history = save_percentile_history(
        report_date, brl_pct, dxy_pct, t10y_pct, CURRENT_DATA
    )
    print("Historico de percentis atualizado em cot_historico.json")

    # Gera arquivo de evolucao
    evolution_report = generate_evolution_report(percentile_history)
    if evolution_report:
        with open("cot_evolucao.md", "w", encoding="utf-8") as f:
            f.write(evolution_report)
        print("Evolucao salva em cot_evolucao.md")
    else:
        print("Evolucao: precisa de pelo menos 2 semanas para gerar comparativo")

    # Mostra resumo
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)

    print(f"\nBRL (Asset Manager): {CURRENT_DATA['BRL']['asset_manager']['net']:+,}")
    print(f"  -> Percentil: {brl_pct:.1f}% (TOP {100-brl_pct:.1f}% historico)")

    print(f"\nDXY (Leveraged Funds): {CURRENT_DATA['DXY']['leveraged_funds']['net']:+,}")
    print(f"  -> Percentil: {dxy_pct:.1f}% (BOTTOM {dxy_pct:.1f}% historico)")

    print(f"\nT10Y (Leveraged Funds): {CURRENT_DATA['T10Y']['leveraged_funds']['net']:+,}")
    print(f"  -> Percentil: {t10y_pct:.1f}% (BOTTOM {t10y_pct:.1f}% historico)")

    # Mostra evolucao se tiver historico
    registros = percentile_history.get("registros", [])
    if len(registros) >= 2:
        anterior = registros[-2]
        print("\n" + "-" * 40)
        print("EVOLUCAO vs SEMANA ANTERIOR")
        print("-" * 40)
        print(f"BRL: {anterior['BRL']['am_pct']:.0f}% -> {brl_pct:.0f}% ({brl_pct - anterior['BRL']['am_pct']:+.0f}pp)")
        print(f"DXY: {anterior['DXY']['lf_pct']:.0f}% -> {dxy_pct:.0f}% ({dxy_pct - anterior['DXY']['lf_pct']:+.0f}pp)")
        print(f"T10Y: {anterior['T10Y']['lf_pct']:.0f}% -> {t10y_pct:.0f}% ({t10y_pct - anterior['T10Y']['lf_pct']:+.0f}pp)")


if __name__ == "__main__":
    main()
