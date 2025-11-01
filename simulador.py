#!/usr/bin/env python3
"""
Simulador de planificación de procesos SIGET
Autor: (Tu nombre)
Versión completa 2025

Implementa:
- Round Robin (con Bloqueado)
- Prioridad
"""

import time
import heapq
from collections import deque
import random

class Color:
    RESET = "\033[0m"
    AZUL = "\033[94m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    ROJO = "\033[91m"
    MAGENTA = "\033[95m"
    NEGRITA = "\033[1m"

class Proceso:
    def __init__(self, pid, tiempo_irrupcion, prioridad_alerta, tam_datos):
        self.pid = pid
        self.tiempo_irrupcion = tiempo_irrupcion
        self.prioridad_alerta = prioridad_alerta
        self.tam_datos = tam_datos
        self.estado = "Nuevo"
        self.restante = tiempo_irrupcion
        self.tiempo_inicio = None
        self.tiempo_final = None

    def __repr__(self):
        return f"P{self.pid}(t={self.restante}, prio={self.prioridad_alerta})"

# ---------- Algoritmo Round Robin ----------
def round_robin(procesos, quantum=2, delay=0):
    print(Color.AZUL + "\n=== Planificación Round Robin ===" + Color.RESET)
    cola = deque(procesos)
    tiempo = 0

    for p in cola:
        p.estado = "Listo"

    bloqueados = []

    while cola or bloqueados:
        # Revisar si hay procesos que terminan de estar bloqueados
        desbloquear = [p for p in bloqueados if random.random() < 0.3]
        for p in desbloquear:
            bloqueados.remove(p)
            p.estado = "Listo"
            cola.append(p)
            print(f"{Color.MAGENTA}Tiempo {tiempo}: {p} -> Listo (desbloqueado){Color.RESET}")

        if not cola:
            tiempo += 1
            continue

        p = cola.popleft()
        if p.tiempo_inicio is None:
            p.tiempo_inicio = tiempo

        p.estado = "En ejecución"
        print(f"{Color.VERDE}Tiempo {tiempo}: {p} -> En ejecución{Color.RESET}")

        ejecutar = min(quantum, p.restante)
        if delay: time.sleep(delay)

        tiempo += ejecutar
        p.restante -= ejecutar

        # 20% de probabilidad de bloqueo simulado
        if p.restante > 0 and random.random() < 0.2:
            p.estado = "Bloqueado"
            bloqueados.append(p)
            print(f"{Color.ROJO}Tiempo {tiempo}: {p} -> Bloqueado (esperando E/S){Color.RESET}")
        elif p.restante > 0:
            p.estado = "Listo"
            cola.append(p)
            print(f"{Color.AMARILLO}Tiempo {tiempo}: {p} -> Listo (restante={p.restante}){Color.RESET}")
        else:
            p.estado = "Terminado"
            p.tiempo_final = tiempo
            print(f"{Color.ROJO}Tiempo {tiempo}: {p} -> Terminado{Color.RESET}")

    mostrar_metricas(procesos, tiempo, "Round Robin")

# ---------- Algoritmo por Prioridad ----------
def prioridad(procesos, delay=0):
    print(Color.AZUL + "\n=== Planificación por Prioridad ===" + Color.RESET)
    cola = [(p.prioridad_alerta, p.pid, p) for p in procesos]
    heapq.heapify(cola)
    tiempo = 0

    while cola:
        _, _, p = heapq.heappop(cola)
        p.estado = "En ejecución"
        if p.tiempo_inicio is None:
            p.tiempo_inicio = tiempo

        print(f"{Color.VERDE}Tiempo {tiempo}: {p} -> En ejecución (prio={p.prioridad_alerta}){Color.RESET}")

        if delay: time.sleep(delay)
        tiempo += p.restante
        p.restante = 0
        p.estado = "Terminado"
        p.tiempo_final = tiempo
        print(f"{Color.ROJO}Tiempo {tiempo}: {p} -> Terminado{Color.RESET}")

    mostrar_metricas(procesos, tiempo, "Prioridad")

# ---------- Mostrar métricas ----------
def mostrar_metricas(procesos, tiempo_total, algoritmo):
    print(Color.NEGRITA + f"\n--- Métricas del algoritmo {algoritmo} ---" + Color.RESET)
    total_turnaround = 0
    print(f"{'PID':<5}{'Inicio':<10}{'Fin':<10}{'Turnaround':<12}")
    for p in procesos:
        tta = p.tiempo_final - p.tiempo_inicio
        total_turnaround += tta
        print(f"{p.pid:<5}{p.tiempo_inicio:<10}{p.tiempo_final:<10}{tta:<12}")
    prom = total_turnaround / len(procesos)
    print(f"\nTiempo total: {tiempo_total}")
    print(f"Promedio Turnaround: {prom:.2f}")

# ---------- Programa principal ----------
def main():
    procesos = [
        Proceso(1, 5, 2, 100),
        Proceso(2, 3, 1, 50),
        Proceso(3, 7, 3, 200)
    ]
    procesos_rr = [Proceso(p.pid, p.tiempo_irrupcion, p.prioridad_alerta, p.tam_datos) for p in procesos]
    procesos_prio = [Proceso(p.pid, p.tiempo_irrupcion, p.prioridad_alerta, p.tam_datos) for p in procesos]

    round_robin(procesos_rr, quantum=2, delay=0)
    prioridad(procesos_prio, delay=0)

    print(Color.NEGRITA + "\nSimulación completada exitosamente." + Color.RESET)

if __name__ == "__main__":
    main()
