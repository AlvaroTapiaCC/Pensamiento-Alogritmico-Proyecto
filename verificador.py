#!/usr/bin/env python3


class Verificador:
    def cargar(self):
        # {task_id: (duracion, categoria)}
        self.tareas = {}
        with open("data/tareas.txt") as f:
            for line in f:
                if line.strip():
                    p = line.strip().split(",")
                    self.tareas[p[0]] = (int(p[1]), p[2])

        # {resource_id: {categorias}}
        self.recursos = {}
        with open("data/recursos.txt") as f:
            for line in f:
                if line.strip():
                    p = line.strip().split(",")
                    self.recursos[p[0]] = set(p[1:])

        # {task_id: (resource_id, tiempo_inicio, tiempo_fin)}
        self.asignaciones = {}
        # {resource_id: [(inicio, fin, task_id), ...]}
        self.asignaciones_por_recurso = {}
        with open("data/output.txt") as f:
            for line in f:
                if line.strip():
                    p = line.strip().split(",")
                    task_id = p[0]
                    recurso_id = p[1]
                    inicio = int(p[2])
                    fin = int(p[3])
                    self.validar_tiempo(inicio, fin)
                    self.asignaciones[task_id] = (recurso_id, inicio, fin)
                    if recurso_id not in self.asignaciones_por_recurso:
                        self.asignaciones_por_recurso[recurso_id] = []
                    self.asignaciones_por_recurso[recurso_id].append(
                        (inicio, fin, task_id)
                    )

    def validar_tiempo(self, tiempo_inicio, tiempo_fin):
        if tiempo_inicio < 0:
            raise Exception(f"Tiempo negativo en asignacion: {tiempo_inicio}")
        if tiempo_fin <= tiempo_inicio:
            raise Exception(
                f"Duracion invalida en asignacion: {tiempo_fin} <= {tiempo_inicio}"
            )

    def validar_completitud(self):
        faltan = set(self.tareas) - set(self.asignaciones)
        if faltan:
            raise Exception(f"Faltan tareas: {sorted(faltan)}")

    def validar_compatibilidad(self):
        for task_id, (_duracion, categoria) in self.tareas.items():
            recurso_id = self.asignaciones[task_id][0]
            categorias = self.recursos[recurso_id]
            if categoria not in categorias:
                raise Exception(
                    f"Tarea {task_id} no es compatible con recurso {recurso_id}"
                )

    def validar_duracion_tareas(self):
        for task_id, (duracion, _categoria) in self.tareas.items():
            inicio, fin = self.asignaciones[task_id][1:3]
            if duracion != fin - inicio:
                raise Exception(
                    f"Duración de tarea {task_id} no es la esperada: {duracion} ≠ {fin - inicio}"
                )

    def validar_exclusividad_temporal(self):
        for recurso_id, intervalos in self.asignaciones_por_recurso.items():
            intervalos_ordenados = sorted(intervalos, key=lambda x: x[0])
            for i in range(len(intervalos_ordenados) - 1):
                fin_actual = intervalos_ordenados[i][1]
                inicio_siguiente = intervalos_ordenados[i + 1][0]
                if fin_actual > inicio_siguiente:
                    tarea_actual = intervalos_ordenados[i][2]
                    tarea_siguiente = intervalos_ordenados[i + 1][2]
                    raise Exception(
                        f"Solapamiento de tiempos en {recurso_id}: {tarea_actual} y {tarea_siguiente}"
                    )

    def call(self):
        self.cargar()
        self.validar_completitud()
        self.validar_compatibilidad()
        self.validar_duracion_tareas()
        self.validar_exclusividad_temporal()
        print("Solución válida")


if __name__ == "__main__":
    Verificador().call()
