import threading
import time
import random

NUM_FILOSOFOS = 5
TEMPO_EXECUCAO = 20  # tempo total de execução em segundos

# Semáforo (garçom) para evitar deadlock
garcom = threading.Semaphore(NUM_FILOSOFOS - 1)

# Um lock para cada garfo
garfos = [threading.Lock() for _ in range(NUM_FILOSOFOS)]

# Variável de controle
executando = True


class Filosofo(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.esquerdo = garfos[id]
        self.direito = garfos[(id + 1) % NUM_FILOSOFOS]

    def pensar(self):
        print(f"Filósofo {self.id} está pensando 🤔")
        time.sleep(random.uniform(0.5, 1.5))

    def comer(self):
        print(f"Filósofo {self.id} está comendo 🍝")
        time.sleep(random.uniform(0.5, 1.0))

    def run(self):
        global executando
        while executando:
            self.pensar()

            print(f"Filósofo {self.id} tenta pegar os garfos")

            garcom.acquire()

            self.esquerdo.acquire()
            self.direito.acquire()

            print(f"Filósofo {self.id} pegou os garfos e vai comer")

            self.comer()

            self.esquerdo.release()
            self.direito.release()

            print(f"Filósofo {self.id} devolveu os garfos")

            garcom.release()


# Criar filósofos
filosofos = [Filosofo(i) for i in range(NUM_FILOSOFOS)]

# Iniciar threads
for f in filosofos:
    f.start()

# Executa por um tempo limitado
time.sleep(TEMPO_EXECUCAO)
executando = False

# Espera todas as threads terminarem
for f in filosofos:
    f.join()

print("\nExecução finalizada com sucesso.")