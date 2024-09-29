import threading
import os
import numpy as np

class YourClass:
    SEEDTEMP = 423234
    SEEDALTU = 6782342390
    SEEDHUME = 54342321
    CHUNK_SIZE = 128

    def getNoise(self, seed, x, y, scale, size):
        return np.random.rand(size, size)

    def getBioma(self, hume, altu, temp):
        return int(hume + altu + temp)

    def getChunk(self, x, y):
        if os.path.exists(f"./Chunks/T_{hex(self.SEEDTEMP).replace('0x','')}A_{hex(self.SEEDTEMP).replace('0x','')}H_{hex(self.SEEDTEMP).replace('0x','')}/{x}/{y}.npy"):
            return np.load(f"./Chunks/T_{hex(self.SEEDTEMP).replace('0x','')}A_{hex(self.SEEDTEMP).replace('0x','')}H_{hex(self.SEEDTEMP).replace('0x','')}/{x}/{y}.npy")
        else:
            temp = self.getNoise(self.SEEDTEMP, x, y, 3, 128)
            altu = self.getNoise(self.SEEDALTU, x, y, 6, 256)
            hume = self.getNoise(self.SEEDHUME, x, y, 3, 256)
            array_biomas = np.zeros(dtype=np.uint8, shape=(self.CHUNK_SIZE, self.CHUNK_SIZE))
            for i in range(self.CHUNK_SIZE):
                for j in range(self.CHUNK_SIZE):
                    array_biomas[i, j] = self.getBioma(hume[i, j], altu[i, j], temp[i, j])
            os.makedirs(f"./Chunks/T_{hex(self.SEEDTEMP).replace('0x','')}A_{hex(self.SEEDTEMP).replace('0x','')}H_{hex(self.SEEDTEMP).replace('0x','')}/{x}", exist_ok=True)
            np.save(f"./Chunks/T_{hex(self.SEEDTEMP).replace('0x','')}A_{hex(self.SEEDTEMP).replace('0x','')}H_{hex(self.SEEDTEMP).replace('0x','')}/{x}/{y}", array_biomas)
            return array_biomas

    def getChunkThreaded(self, x, y, results, index):
        def target():
            results[index] = self.getChunk(x, y)
        thread = threading.Thread(target=target)
        thread.start()
        return thread

# Ejemplo de uso
obj = YourClass()
threads = []
results = [None] * 9  # Lista para almacenar los resultados de los chunks

# Generar 9 chunks en una cuadrícula 3x3
index = 0
for x in range(3):
    for y in range(3):
        thread = obj.getChunkThreaded(x, y, results, index)
        threads.append(thread)
        index += 1

# Esperar a que todos los hilos terminen
for thread in threads:
    thread.join()

# Imprimir los chunks generados
for i, chunk in enumerate(results):
    print(f"Chunk {i}:")
    print(chunk)