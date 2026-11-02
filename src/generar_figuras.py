"""Genera las figuras del informe a partir de data/processed.

Uso: python src/generar_figuras.py
Salida: informe/figuras/*.png (150 dpi, sin títulos: el informe trae el pie de figura).
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "data" / "processed"
SALIDA = RAIZ / "informe" / "figuras"

AZUL = "#1F3864"
GRIS = "#A6A6A6"
DPI = 150

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
         "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

plt.rcParams.update({
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#555555",
    "axes.labelcolor": "#222222",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "axes.grid": True,
    "grid.color": "#E0E0E0",
    "grid.linewidth": 0.6,
    "legend.frameon": False,
})


def guardar(fig, nombre):
    ruta = SALIDA / nombre
    fig.tight_layout()
    fig.savefig(ruta, dpi=DPI, facecolor="white")
    plt.close(fig)
    print(f"Generada: {ruta.relative_to(RAIZ)}")


def cargar(nombre):
    return pd.read_csv(DATOS / nombre, parse_dates=["fecha"])


def fig_perfil_horario(horaria):
    df = horaria.copy()
    df["hora"] = df["fecha"].dt.hour
    df["fin_semana"] = df["fecha"].dt.day_of_week >= 5
    kwh = df.groupby(["fin_semana", "hora"])["kWh"].mean().unstack(0)
    fp = df.groupby("hora")["FP"].median()

    fig, (izq, der) = plt.subplots(1, 2, figsize=(10, 3.8))
    izq.plot(kwh.index, kwh[False], color=AZUL, lw=2, label="Lunes a viernes")
    izq.plot(kwh.index, kwh[True], color=GRIS, lw=2, label="Sábado y domingo")
    izq.set_xlabel("Hora del día")
    izq.set_ylabel("kWh promedio por hora")
    izq.set_xticks(range(0, 24, 3))
    izq.set_ylim(bottom=0)
    izq.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2)

    der.plot(fp.index, fp.values, color=AZUL, lw=2, label="FP mediano")
    der.axhline(90, color=GRIS, ls="--", lw=1.5, label="Referencia 90 %")
    der.set_xlabel("Hora del día")
    der.set_ylabel("Factor de potencia (%)")
    der.set_xticks(range(0, 24, 3))
    der.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2)
    guardar(fig, "perfil_horario.png")


def fig_exceso_creg_hora(horaria):
    df = horaria.copy()
    df["hora"] = df["fecha"].dt.hour
    exceso = df.groupby("hora")["exceso_kVArh"].sum() / 1000

    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.bar(exceso.index, exceso.values, color=AZUL, width=0.75)
    ax.set_xlabel("Hora del día")
    ax.set_ylabel("Reactiva en exceso (MVArh)")
    ax.set_xticks(range(0, 24))
    ax.grid(axis="x", visible=False)
    guardar(fig, "exceso_creg_hora.png")


def fig_pronostico_semana(pron):
    inicio, fin = pd.Timestamp("2018-10-15"), pd.Timestamp("2018-10-22")
    sem = pron[(pron["fecha"] >= inicio) & (pron["fecha"] < fin)]

    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.plot(sem["fecha"], sem["kWh"], color=AZUL, lw=1.6, label="Consumo real")
    ax.plot(sem["fecha"], sem["pred_kWh"], color=GRIS, lw=1.6,
            label="Pronóstico próxima hora")
    ax.set_ylabel("kWh por hora")
    ax.set_xlabel("Fecha")
    dias = pd.date_range(inicio, fin - pd.Timedelta(days=1), freq="D")
    nombres = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    ax.set_xticks(dias)
    ax.set_xticklabels([f"{nombres[d.day_of_week]} {d.day:02d}/{d.month:02d}" for d in dias])
    ax.set_xlim(inicio, fin)
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper right", ncol=2)
    guardar(fig, "pronostico_semana.png")


def fig_anomalias_mes(pron):
    df = pron[pron["anomalia"].isin(["consumo_alto", "consumo_bajo"])].copy()
    df["mes"] = df["fecha"].dt.month
    tabla = (df.groupby(["mes", "anomalia"]).size().unstack(fill_value=0)
             .reindex(index=range(1, 13), columns=["consumo_alto", "consumo_bajo"],
                      fill_value=0))
    meses = sorted(pron["fecha"].dt.month.unique())
    tabla = tabla.loc[meses]

    fig, ax = plt.subplots(figsize=(8, 3.8))
    x = range(len(tabla))
    ax.bar(x, tabla["consumo_alto"], color=AZUL, width=0.7, label="Consumo alto")
    ax.bar(x, tabla["consumo_bajo"], bottom=tabla["consumo_alto"], color=GRIS,
           width=0.7, label="Consumo bajo")
    ax.set_xticks(list(x))
    ax.set_xticklabels([MESES[m - 1] for m in tabla.index])
    ax.set_xlabel("Mes")
    ax.set_ylabel("Horas anómalas")
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper right")
    guardar(fig, "anomalias_mes.png")


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    horaria = cargar("energia_horaria.csv")
    pron = cargar("pronostico_anomalias.csv")
    fig_perfil_horario(horaria)
    fig_exceso_creg_hora(horaria)
    fig_pronostico_semana(pron)
    fig_anomalias_mes(pron)


if __name__ == "__main__":
    main()
