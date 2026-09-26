"""
Núcleo algorítmico — Fase 3.

Implementa el patrón de método plantilla que pide el apunte del curso:
una clase base Transformador con el contrato ajustar()/transformar(),
y una clase Pipeline que compone varios transformadores y los recorre
de forma polimórfica (el bucle no consulta el tipo concreto de cada
paso).

El pipeline de preparación se organiza en cuatro responsabilidades:
filtrado por período, filtrado por centrales, transformación de formato
ancho a largo y construcción de variables derivadas. Cada responsabilidad
se implementa como una clase derivada de Transformador.

La lógica funcional existente se reutiliza desde los módulos de src,
especialmente transformacion.py, evitando duplicación de código y
manteniendo una separación clara entre la lógica de transformación y la
composición orientada a objetos.

Verificado: Pipeline([...]).ajustar(datos_crudos).transformar(datos_crudos)
produce un resultado idéntico, fila por fila, al dataset procesado
oficial de F2 (pd.testing.assert_frame_equal).
"""

from __future__ import annotations
import pandas as pd

from src.transformacion import (
    filtrar_periodo,
    filtrar_centrales,
    transformar_ancho_largo,
    crear_dia_semana,
    crear_id_observacion,
)

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

class FiltradorPeriodo(Transformador):
    """Delimita el dataset al período temporal definido para el análisis."""

    def __init__(self, fecha_inicio: str, fecha_fin: str):
        super().__init__()
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def aprender(self, df: pd.DataFrame) -> dict:
        if "Fecha" not in df.columns:
            raise KeyError("La columna 'Fecha' no existe en el dataset.")

        return {
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
        }

    def aplicar(self, df: pd.DataFrame) -> pd.DataFrame:
        return filtrar_periodo(
            df,
            self.fecha_inicio,
            self.fecha_fin,
        )
    
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
        return filtrar_centrales(df, self.centrales)


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
        df = crear_dia_semana(df)
        df = crear_id_observacion(df)
        orden = [
            "ID_Observacion",
            "Año",
            "Mes",
            "Llave",
            "Central",
            "Coordinado",
            "Grupo_Reporte",
            "Tipo",
            "Subtipo",
            "Fecha",
            "Dia_Semana",
            "Hora",
            "Generacion_MWh",
        ]
        df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.strftime("%Y-%m-%d")
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
