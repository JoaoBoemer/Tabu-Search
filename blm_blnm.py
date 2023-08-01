from typing import List
import math
import random
import time
import pandas as pd

class Resultado:
  def __init__(self, heuristica, tarefas, maquinas, replicacao, tempo, iteracoes, valor, parametro):
    self.heuristica = heuristica
    self.tarefas = tarefas
    self.maquinas = maquinas
    self.replicacao = replicacao
    self.tempo = tempo
    self.iteracoes = iteracoes
    self.valor = valor
    self.parametro = parametro

def salvar_resultados_excel(resultados, nome_arquivo):
    # Crie um dicionário com os dados dos resultados
    data = {
        'Heurística': [resultado.heuristica for resultado in resultados],
        'Tarefas': [resultado.tarefas for resultado in resultados],
        'Maquinas': [resultado.maquinas for resultado in resultados],
        'Replicacao': [resultado.replicacao for resultado in resultados],
        'Tempo (ms)': [resultado.tempo for resultado in resultados],
        'Iterações': [resultado.iteracoes for resultado in resultados],
        'Valor': [resultado.valor for resultado in resultados],
        'Parâmetro (p)': [resultado.parametro for resultado in resultados],
    }

    # Crie um DataFrame a partir do dicionário de dados
    df = pd.DataFrame(data)

    # Salve o DataFrame em um arquivo Excel
    df.to_excel(nome_arquivo, index=False)

def calculaMakespan(listaMaquinas):
  for maquina in listaMaquinas:
    total_tarefas = sum(maquina['tarefas'])
    maquina['makespan'] = total_tarefas

def buscarTarefa(listaMaquinas):
  max_value = -1
  max_index = 0

  ### Pega o indice e o makespan da máquina com maior makespan
  for i, maquina in enumerate(listaMaquinas):
    if ( maquina["makespan"] > max_value ):
      max_index = i
      max_value = maquina["makespan"]

  return max_value, max_index

def verificaMelhora(listaMaquinas):

  value, index = buscarTarefa(listaMaquinas)

  ### Itera sobre todas as máquinas e verifica se o makespan da máquina fica menor que o makespan da pior máquina.
  for maquina in listaMaquinas:
    if ( maquina["makespan"] + listaMaquinas[index]["tarefas"][-1] < listaMaquinas[index]["makespan"] ):
      return True

  ### Se nenhuma máquina fica melhor que a máquina com maior makespan, retorna falso e finaliza.
  return False

def primeiraMelhora(tarefa, listaMaquinas):

  ### Pega a última tarefa da máquina e armazena o tamanho da tarefa em ultima_tarefa
  ultima_tarefa = listaMaquinas[tarefa[1]]["tarefas"].pop()

  ### Remove o tempo da tarefa da máquina escolhida
  listaMaquinas[tarefa[1]]["makespan"] -= ultima_tarefa

  for i, maquina in enumerate(listaMaquinas):
    if (i != tarefa[1]):
      if (maquina['makespan'] + ultima_tarefa < listaMaquinas[tarefa[1]]['makespan']):
        maquina['makespan'] += ultima_tarefa
        maquina['tarefas'].append(ultima_tarefa)
        return

def PrimeiraMelhora(listaMaquinas):
  interacoes = 0
  ### Loop de verificação se é possível realizar a melhora
  while( verificaMelhora(listaMaquinas) ):
    ### Primeira melhora
    primeiraMelhora(buscarTarefa(listaMaquinas), listaMaquinas)
    interacoes = interacoes + 1

  return interacoes

def main():
  resultados = []
  m = 0
  r = 0
  cont = 0
  ### Define o número de máquinas
  for i in range(3):
    if i == 1:
      m = 10
    elif i == 2:
      m = 20
    else:
      m = 50

    ### define valor de r
    for j in range(2):
      if j == 1:
        r = 1.5
      else:
        r = 2

      #Executa 10 instancias
      for i in range(10):
        interacoes = 0
        n = math.ceil(math.pow(m, r))
        listaMaquinas = [{'tarefas': [], 'makespan': 0} for _ in range(m)] ### Inicialização das máquinas
        listaTarefas = [random.randint(1, 100) for _ in range(n)] ### Criação das tarefas
        listaMaquinas[0]['tarefas'] = listaTarefas ### Definindo as tarefas da primeira máquina
        calculaMakespan(listaMaquinas) ### Calculando o makespan das máquinas
        inicio = time.time() ### Inicia contador
        interacoes = PrimeiraMelhora(listaMaquinas) ### Primeira Melhora
        fim = time.time() ### Finaliza contador
        tempoExecucao = (fim - inicio) * 1000
        valor = buscarTarefa(listaMaquinas)[0]
        resultado = Resultado("Primeira Melhora", n, m, i, tempoExecucao, interacoes, valor, "NA")
        resultados.append(resultado)
        cont = cont + 1

  for resultado in resultados:
    print("Heurística:", resultado.heuristica)
    print("Tarefas:", resultado.tarefas)
    print("Maquinas:", resultado.maquinas)
    print("Replicacao:", resultado.replicacao)
    print("Tempo(ms):", resultado.tempo)
    print("Iterações:", resultado.iteracoes)
    print("Valor:", resultado.valor)
    print("Parâmetro:", resultado.parametro)
    print()

  print('Contador : ', cont)

  # Depois de obter os resultados, salve-os em um arquivo Excel
  nome_arquivo = 'resultados_primeira_melhora.xlsx'
  salvar_resultados_excel(resultados, nome_arquivo)

main()

from typing import List
import math
import random
import time
import pandas as pd

class Resultado:
  def __init__(self, heuristica, tarefas, maquinas, replicacao, tempo_ms, iteracoes, valor, parametro):
    self.heuristica = heuristica
    self.tarefas = tarefas
    self.maquinas = maquinas
    self.replicacao = replicacao
    self.tempo = tempo_ms
    self.iteracoes = iteracoes
    self.valor = valor
    self.parametro = parametro

class Tabu:
    def __init__(self, indexMaquina, interacoes_saida):
        self.maquina = indexMaquina
        self.cont = 0
        self.interacoes_saida = interacoes_saida

    def incrementar_contador(self):
        self.cont += 1

def salvar_resultados_excel(resultados, nome_arquivo):
    # Crie um dicionário com os dados dos resultados
    data = {
        'Heurística': [resultado.heuristica for resultado in resultados],
        'Tarefas': [resultado.tarefas for resultado in resultados],
        'Maquinas': [resultado.maquinas for resultado in resultados],
        'Replicacao': [resultado.replicacao for resultado in resultados],
        'Tempo (ms)': [resultado.tempo for resultado in resultados],
        'Iterações': [resultado.iteracoes for resultado in resultados],
        'Valor': [resultado.valor for resultado in resultados],
        'Parâmetro (p)': [resultado.parametro for resultado in resultados],
    }

    # Crie um DataFrame a partir do dicionário de dados
    df = pd.DataFrame(data)

    # Salve o DataFrame em um arquivo Excel
    df.to_excel(nome_arquivo, index=False)

def remover_tabus_expirados(lista_tabu):
    lista_tabu = [tabu for tabu in lista_tabu if tabu.cont < tabu.interacoes_saida]
    return lista_tabu

def calcula_makespan(listaMaquinas):
  for maquina in listaMaquinas:
      total_tarefas = sum(maquina['tarefas'])
      maquina['makespan'] = total_tarefas

def buscar_tarefa(listaMaquinas):
  max_value = -1
  max_index = 0

  ### Pega o indice e o makespan da máquina com maior makespan
  for i, maquina in enumerate(listaMaquinas):
    if ( maquina["makespan"] > max_value ):
      max_index = i
      max_value = maquina["makespan"]

  return max_value, max_index

def busca_tabu(listaMaquinas, max_iteracoes, p):
  lista_tabu = []
  iteracoes = 0
  iteracoesSemMelhora = 1
  while iteracoesSemMelhora < max_iteracoes:
    for tabu in lista_tabu:
      tabu.incrementar_contador()

    lista_tabu = remover_tabus_expirados(lista_tabu)
    maiorMakespan = buscar_tarefa(listaMaquinas)
    tarefa = None

    if( maiorMakespan[0] == 0 ):
      print("Error", listaMaquinas)

    if listaMaquinas[maiorMakespan[1]]["tarefas"]:
      tarefa = listaMaquinas[maiorMakespan[1]]["tarefas"][-1]
      #listaMaquinas[maiorMakespan[1]]["makespan"] -= tarefa


    if tarefa is None:
      # Se não encontrou tarefa não vazia, pular a iteração atual
      iteracoesSemMelhora += 1
      continue

    for i, maquina in enumerate(listaMaquinas):
      if (i != maiorMakespan[1]): ### Verifica se é a mesma máquina de origem
        if (any(tabu.maquina == i for tabu in lista_tabu) == False): ### Verifica se está presente na lista de tabu
          if (maquina["makespan"] + tarefa < maiorMakespan[0] - tarefa): ### Verifica se há melhora
            lista_tabu.append( Tabu(i, p) )
            maquina["tarefas"].append(tarefa)
            maquina["makespan"] += tarefa
            iteracoesSemMelhora = 0
            #if( len ( listaMaquinas[maiorMakespan[1]]["tarefas"] ) == 0 ):
              #print("Antes do error:", listaMaquinas )
            listaMaquinas[maiorMakespan[1]]["tarefas"].pop()
            listaMaquinas[maiorMakespan[1]]["makespan"] -= tarefa
            break;

          iteracoesSemMelhora += 1

    iteracoes += 1

  return listaMaquinas, iteracoes

def executar_experimento():
  resultados = []
  m = 0
  r = 0
  p = 0
  cont = 0
  max_iteracoes = 1000  # Defina o número máximo de iterações aqui

  for i in range(3):
    if i == 1:
        m = 10
    elif i == 2:
        m = 20
    else:
        m = 50

    for j in range(2):
        if j == 1:
            r = 1.5
        else:
            r = 2

        for k in range(9):
          c = (k + 1) / 100

          for _ in range(10):
            n = math.ceil(math.pow(m, r))
            p = math.ceil(n * c)
            listaMaquinas = [{'tarefas': [], 'makespan': 0} for _ in range(m)]
            listaTarefas = [random.randint(1, 100) for _ in range(n)]
            listaMaquinas[0]['tarefas'] = listaTarefas
            calcula_makespan(listaMaquinas)
            inicio = time.time()
            listaMaquinas, iteracoes = busca_tabu(listaMaquinas, max_iteracoes, p)
            fim = time.time()
            tempoExecucao = (fim - inicio) * 1000  # Convertendo para milissegundos
            valor = buscar_tarefa(listaMaquinas)[0]
            resultado = Resultado("Busca Tabu", n, m, _, tempoExecucao, iteracoes, valor, c)
            resultados.append(resultado)
            cont = cont + 1

  for resultado in resultados:
    print("Heurística:", resultado.heuristica)
    print("Tarefas:", resultado.tarefas)
    print("Maquinas:", resultado.maquinas)
    print("Replicacao:", resultado.replicacao)
    print("Tempo (ms):", resultado.tempo)
    print("Iterações:", resultado.iteracoes)
    print("Valor:", resultado.valor)
    print("Parâmetro (p):", resultado.parametro)
    print()

  print("Contador: ", cont)

  # Depois de obter os resultados, salve-os em um arquivo Excel
  nome_arquivo = 'resultados_busca_tabu.xlsx'
  salvar_resultados_excel(resultados, nome_arquivo)

executar_experimento()