"""
Núcleo algorítmico — Fase 3.

Implementa el patrón de método plantilla que pide el apunte del curso:
una clase base Transformador con el contrato ajustar()/transformar(),
y una clase Pipeline que compone varios transformadores y los recorre
de forma polimórfica (el bucle no consulta el tipo concreto de cada
paso).

Los tres pasos del pipeline de F2 (filtrar centrales, transformar
ancho -> largo, construir variables derivadas) se reorganizan como
tres clases derivadas de Transformador. No se cambia la lógica de F2:
se reutilizan carga.py, transformacion.py y validacion.py tal como
están; solo se reorganiza bajo un contrato común orientado a objetos.

Verificado: Pipeline([...]).ajustar(datos_crudos).transformar(datos_crudos)
produce un resultado idéntico, fila por fila, al dataset procesado
oficial de F2 (pd.testing.assert_frame_equal).
"""

from __future__ import annotations
import pandas as pd

from src.transformacion import transformar_ancho_largo

DIAS_ES = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves",
           4: "Viernes", 5: "Sábado", 6: "Domingo"}


class Transformador:
    """Clase base: define el contrato común de todo paso del pipeline.

    Separa ajustar() (aprende parámetros y valida) de transformar()
    (aplica la transformación ya aprendida), siguiendo el método
    plantilla: el orden y el control de estado quedan fijos aquí, y
    cada clase derivada solo implementa aprender() y aplicar().
    """

    def __init__(self):
        self._parametros: dict = {}
        self._ajustado: bool = False

    def ajustar(self, df: pd.DataFrame) -> "Transformador":
        self._parametros = self.aprender(df)
        self._ajustado = True
        return self

    def transformar(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self._ajustado:
            raise RuntimeError("Hay que ajustar antes de transformar.")
        return self.aplicar(df.copy())  # copia: no se muta la entrada

    def aprender(self, df: pd.DataFrame) -> dict:
        raise NotImplementedError("Cada clase derivada debe implementarlo.")

    def aplicar(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("Cada clase derivada debe implementarlo.")


class FiltradorCentrales(Transformador):
    """Delimita el dataset a las centrales del alcance del proyecto."""

    def __init__(self, centrales: list[str]):
        super().__init__()
        self.centrales = centrales

    def aprender(self, df: pd.DataFrame) -> dict:
        if "Central" not in df.columns:
            raise KeyError("La columna 'Central' no existe en el dataset.")
        presentes = sorted(set(df["Central"].unique()) & set(self.centrales))
        return {"centrales_presentes": presentes}

    def aplicar(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[df["Central"].isin(self.centrales)].reset_index(drop=True)

        


class TransformadorAnchoLargo(Transformador):
    """Convierte de formato ancho (24 columnas Hora 1..Hora 24) a
    formato largo (una fila por central-fecha-hora).

    Reutiliza transformar_ancho_largo de transformacion.py: esta
    clase no reimplementa la lógica, solo la expone bajo el contrato
    Transformador para poder componerla en el Pipeline.
    """

    def __init__(self, columnas_base: list[str], columnas_hora: list[str]):
        super().__init__()
        self.columnas_base = columnas_base
        self.columnas_hora = columnas_hora

    def aprender(self, df: pd.DataFrame) -> dict:
        faltantes = [c for c in self.columnas_base + self.columnas_hora
                     if c not in df.columns]
        if faltantes:
            raise KeyError(f"Columnas no encontradas en el dataset: {faltantes}")
        return {"columnas_base": self.columnas_base, "columnas_hora": self.columnas_hora}

    def aplicar(self, df: pd.DataFrame) -> pd.DataFrame:
        return transformar_ancho_largo(df, self.columnas_base, self.columnas_hora)


class ConstructorVariablesDerivadas(Transformador):
    """Renombra Grupo reporte -> Grupo_Reporte, y agrega Dia_Semana
    e ID_Observacion, dejando el dataset con el esquema final de 13
    columnas ya validado en F2.
    """

    def aprender(self, df: pd.DataFrame) -> dict:
        return {}  # no hay parámetros que aprender en este paso

    def aplicar(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(columns={"Grupo reporte": "Grupo_Reporte"})
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        df["Dia_Semana"] = df["Fecha"].dt.weekday.map(DIAS_ES)
        df["ID_Observacion"] = (
            df["Central"].str.replace(" ", "_", regex=False) + "_"
            + df["Fecha"].dt.strftime("%Y%m%d")
            + "_H" + df["Hora"].astype(str).str.zfill(2)
        )
        orden = ["ID_Observacion", "Año", "Mes", "Llave", "Central", "Coordinado",
                 "Grupo_Reporte", "Tipo", "Subtipo", "Fecha", "Dia_Semana",
                 "Hora", "Generacion_MWh"]
        df["Fecha"] = df["Fecha"].dt.strftime("%Y-%m-%d")
        return df[orden]


class Pipeline:
    """Compone una lista de Transformador y los ejecuta en orden.

    El bucle recorre self._pasos sin preguntar nunca qué clase
    concreta es cada paso: solo invoca ajustar()/transformar(), que
    cada Transformador implementa a su manera. Esa ausencia de
    condicionales sobre el tipo es la evidencia de polimorfismo.
    Agregar un cuarto paso no exige modificar esta clase (principio
    de abierto y cerrado).
    """

    def __init__(self, pasos: list[Transformador]):
        self._pasos = list(pasos)
        self._ajustado = False

    def ajustar(self, df: pd.DataFrame) -> "Pipeline":
        intermedio = df.copy()
        for paso in self._pasos:
            intermedio = paso.ajustar(intermedio).transformar(intermedio)
        self._ajustado = True
        return self

    def transformar(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self._ajustado:
            raise RuntimeError("Hay que ajustar antes de transformar.")
        resultado = df.copy()
        for paso in self._pasos:
            resultado = paso.transformar(resultado)
        return resultado

    def ejecutar(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ajusta y transforma en una sola llamada (caso de uso de
        este proyecto: no hay separación train/test, todo el
        histórico se procesa de una vez)."""
        return self.ajustar(df).transformar(df)
