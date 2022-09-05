# -*- coding:utf-8 -*-

from copy import deepcopy
from itertools import product
from numpy import random

class Stack():
    def __init__ (self):
        self.items=[]        
    def is_empty(self):
        return self.items==[]
    def push(self,item):
        self.items.append(item)        
    def pop(self):
        return self.items.pop()    
    def top(self):
        return self.items[len(self.items)-1]
    def size(self):
        return len(self.items)


class GandaGaloEngine:
    def __init__(self):
        self.linhas = 0
        self.colunas = 0
        self.tabuleiro = [] 
        self.movimentos = Stack()
        self.ancoras = Stack()
    
    def escrever_tabuleiro_ficheiro(self, filename):
        file = open(filename, "w")
        file.write(str(self.linhas) + " " + str(self.colunas) + "\n")
        for line in self.tabuleiro:
            file.write(" ".join(line) + "\n")
        file.close()
        
    def ler_tabuleiro_ficheiro(self, filename):
        '''
        Cria nova instancia do jogo numa matriz
        :param filename: nome do ficheiro a ler
        '''
        try:
            ficheiro = open(filename,"r")
            lines = ficheiro.readlines() #ler as linhas do ficheiro para a lista lines
            dim = lines[0].strip('\n').split(' ')  # obter os dois numeros da dimensao do puzzle, retirando o '\n' 
            self.linhas = int(dim[0])  # retirar o numero de linhas
            self.colunas = int(dim[1])  # retirar o numero de colunas
            self.tabuleiro=[]
            for i in range(1,len(lines)):
                self.tabuleiro.append(lines[i].split())
            ficheiro.close()
            return self.tabuleiro
        except:
            print("Erro: na leitura do tabuleiro.")
        return self.tabuleiro

    def inicializar_tabuleiro_vazio(self, linhas, colunas):
        'Gera um tabuleiro vazio de tamanho colunas x linhas'
        self.linhas = linhas
        self.colunas = colunas
        for y in range(self.linhas):
            self.tabuleiro.append([])
            for x in range(self.colunas):
                self.tabuleiro[y].append(".")

    def printpuzzle(self):
        for linha in self.tabuleiro:
            for simbolo in linha:
                print(simbolo,end=" ")
            print()
    
    def getlinhas(self):
        return self.linhas
    
    def getcolunas(self):
        return self.colunas
        
    def gettabuleiro(self):
        return self.tabuleiro

    def settabuleiro(self, t):
        self.tabuleiro = t
        
    def quadricula_ocupada(self,linha,coluna):
        return self.tabuleiro[linha-1][coluna-1]=='#' or self.tabuleiro[linha-1][coluna-1]=='X' or self.tabuleiro[linha-1][coluna-1]=='O'
        
    def jogar(self,simbolo,linha,coluna):
        if simbolo != 'X' and simbolo != 'O':
            print("Símbolo não válido!")
        if not self.quadricula_ocupada(linha, coluna):
            self.tabuleiro[linha-1][coluna-1]=simbolo
            self.movimentos.push([linha, coluna])
        else: 
            print("Casa ocupada!")
        if self.tabuleiro_cheio():
            print("O seu tabuleiro está cheio!")

    def validar(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
              if i - 1 >= 0 and i + 1 < self.linhas and j - 1 >= 0 and j + 1 < self.colunas  and self.tabuleiro[i-1][j-1] != '#' and self.tabuleiro[i-1][j-1] != '.' and self.tabuleiro[i+1][j+1] != '#' and self.tabuleiro[i+1][j+1] != '.' and self.tabuleiro[i-1][j-1] == self.tabuleiro[i+1][j+1] and self.tabuleiro[i][j]==self.tabuleiro[i+1][j+1]:
                  return False
              elif i - 1 >= 0 and i + 1 < self.linhas and j - 1 >= 0 and j + 1 < self.colunas and self.tabuleiro[i-1][j+1] != '#' and self.tabuleiro[i-1][j+1] != '.' and self.tabuleiro[i+1][j-1] != '#' and self.tabuleiro[i+1][j-1] != '.' and self.tabuleiro[i-1][j+1] == self.tabuleiro[i+1][j-1] and self.tabuleiro[i][j]==self.tabuleiro[i+1][j-1]:
                  return False
              elif j-1>=0 and j+1<self.colunas and self.tabuleiro[i][j+1] != '.' and self.tabuleiro[i][j+1] != '#' and self.tabuleiro[i][j-1] != '.' and self.tabuleiro[i][j-1] != '#' and self.tabuleiro[i][j-1] == self.tabuleiro[i][j+1] and self.tabuleiro[i][j]==self.tabuleiro[i][j+1]:
                  return False
              elif i-1>=0 and i+1<self.linhas and self.tabuleiro[i+1][j] != '.' and self.tabuleiro[i+1][j] != '#' and self.tabuleiro[i-1][j] != '.' and self.tabuleiro[i-1][j] != '#' and self.tabuleiro[i-1][j] == self.tabuleiro[i+1][j] and self.tabuleiro[i][j]==self.tabuleiro[i+1][j]: 
                  return False
              elif i+2<self.linhas and (self.tabuleiro[i+1][j] != '.' and self.tabuleiro[i+1][j] != '#' and self.tabuleiro[i+2][j] != '.' and self.tabuleiro[i+2][j] != '#' and self.tabuleiro[i+1][j] == self.tabuleiro[i+2][j] and self.tabuleiro[i][j]==self.tabuleiro[i+2][j]):
                  return False
              elif i-2>=0 and (self.tabuleiro[i-1][j] != '.' and self.tabuleiro[i-1][j] != '#' and self.tabuleiro[i-2][j] != '.' and self.tabuleiro[i-2][j] != '#' and self.tabuleiro[i-1][j] == self.tabuleiro[i-2][j] and self.tabuleiro[i][j]==self.tabuleiro[i-2][j]):
                  return False
              elif j+2<self.colunas and (self.tabuleiro[i][j+1] != '.' and self.tabuleiro[i][j+1] != '#' and self.tabuleiro[i][j+2] != '.' and self.tabuleiro[i][j+2] != '#' and self.tabuleiro[i][j+1] == self.tabuleiro[i][j+2] and self.tabuleiro[i][j]==self.tabuleiro[i][j+2]):
                  return False
              elif j-2>=0 and (self.tabuleiro[i][j-1] != '.' and self.tabuleiro[i][j-1] != '#' and self.tabuleiro[i][j-2] != '.' and self.tabuleiro[i][j-2] != '#' and self.tabuleiro[i][j-1] == self.tabuleiro[i][j-2] and self.tabuleiro[i][j]==self.tabuleiro[i][j-2]):
                   return False
              elif i+2<self.linhas and j+2<self.colunas and (self.tabuleiro[i+1][j+1]!='.' and self.tabuleiro[i+1][j+1]!='#' and self.tabuleiro[i+2][j+2]!='.' and self.tabuleiro[i+2][j+2]!='#') and self.tabuleiro[i+1][j+1]==self.tabuleiro[i+2][j+2] and self.tabuleiro[i][j]==self.tabuleiro[i+2][j+2]:
                   return False
              elif i-2>=0 and j-2>=0 and (self.tabuleiro[i-1][j-1]!='.' and self.tabuleiro[i-1][j-1]!='#' and self.tabuleiro[i-2][j-2]!='.' and self.tabuleiro[i-2][j-2]!='#') and self.tabuleiro[i-1][j-1]==self.tabuleiro[i-2][j-2] and self.tabuleiro[i][j]==self.tabuleiro[i-2][j-2]:
                   return False
              elif i+2<self.linhas and j-2>=0 and (self.tabuleiro[i+1][j-1]!='.' and self.tabuleiro[i+1][j-1]!='#' and self.tabuleiro[i+2][j-2]!='.' and self.tabuleiro[i+2][j-2]!='#') and self.tabuleiro[i+1][j-1]==self.tabuleiro[i+2][j-2] and self.tabuleiro[i][j]==self.tabuleiro[i+2][j-2]:
                   return False
              elif i-2>=0 and j+2<self.colunas and (self.tabuleiro[i-1][j+1]!='.' and self.tabuleiro[i-1][j+1]!='#' and self.tabuleiro[i-2][j+2]!='.' and self.tabuleiro[i-2][j+2]!='#') and self.tabuleiro[i-1][j+1]==self.tabuleiro[i-2][j+2] and self.tabuleiro[i][j]==self.tabuleiro[i-2][j+2]:
                   return False
        return True
   
    def undo(self):
      if self.movimentos.size()>0:
          [linha,coluna]=self.movimentos.pop()
          self.tabuleiro[linha-1][coluna-1]='.'
      else:
        print("Aviso: não existem jogadas armazenadas!")

    def ajudar(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                if i - 1 >= 0 and i + 1 < self.linhas and j - 1 >= 0 and j + 1 < self.colunas and self.tabuleiro[i][j] =='.' and self.tabuleiro[i-1][j-1] != '#' and self.tabuleiro[i-1][j-1] != '.' and self.tabuleiro[i+1][j+1] != '#' and self.tabuleiro[i+1][j+1] != '.' and self.tabuleiro[i-1][j-1] == self.tabuleiro[i+1][j+1]:
                    return i+1, j+1          
                elif i - 1 >= 0 and i + 1 < self.linhas and j - 1 >= 0 and j + 1 < self.colunas and self.tabuleiro[i][j] =='.' and self.tabuleiro[i+1][j-1] != '#' and self.tabuleiro[i+1][j-1] != '.' and self.tabuleiro[i-1][j+1] != '#' and self.tabuleiro[i-1][j+1] != '.' and self.tabuleiro[i-1][j+1] == self.tabuleiro[i+1][j-1]:
                   return i+1, j+1 
                elif j-1>=0 and j+1<self.colunas and self.tabuleiro[i][j+1] != '.' and self.tabuleiro[i][j+1] != '#' and self.tabuleiro[i][j-1] != '.' and self.tabuleiro[i][j-1] != '#' and self.tabuleiro[i][j] == '.' and self.tabuleiro[i][j-1] == self.tabuleiro[i][j+1]:
                   return i+1, j+1 
                elif i-1>=0 and i+1<self.linhas and self.tabuleiro[i+1][j] != '.' and self.tabuleiro[i+1][j] != '#' and self.tabuleiro[i-1][j] != '.' and self.tabuleiro[i-1][j] != '#' and self.tabuleiro[i][j] == '.' and self.tabuleiro[i-1][j] == self.tabuleiro[i+1][j]:
                   return i+1, j+1 
                elif i+2<self.linhas and self.tabuleiro[i][j] == '.' and (self.tabuleiro[i+1][j] != '.' and self.tabuleiro[i+1][j] != '#' and self.tabuleiro[i+2][j] != '.' and self.tabuleiro[i+2][j] != '#' and self.tabuleiro[i+1][j] == self.tabuleiro[i+2][j]):
                   return i+1, j+1 
                elif i-2>=0 and self.tabuleiro[i][j] == '.' and (self.tabuleiro[i-1][j] != '.' and self.tabuleiro[i-1][j] != '#' and self.tabuleiro[i-2][j] != '.' and self.tabuleiro[i-2][j] != '#' and self.tabuleiro[i-1][j] == self.tabuleiro[i-2][j]):
                   return i+1, j+1 
                elif j+2<self.colunas and self.tabuleiro[i][j] == '.' and (self.tabuleiro[i][j+1] != '.' and self.tabuleiro[i][j+1] != '#' and self.tabuleiro[i][j+2] != '.' and self.tabuleiro[i][j+2] != '#' and self.tabuleiro[i][j+1] == self.tabuleiro[i][j+2]):
                   return i+1, j+1 
                elif j-2>=0 and self.tabuleiro[i][j] == '.' and (self.tabuleiro[i][j-1] != '.' and self.tabuleiro[i][j-1] != '#' and self.tabuleiro[i][j-2] != '.' and self.tabuleiro[i][j-2] != '#' and self.tabuleiro[i][j-1] == self.tabuleiro[i][j-2]):
                   return i+1, j+1 
                elif i+2<self.linhas and j+2<self.colunas and self.tabuleiro[i][j] == '.' and (self.tabuleiro[i+1][j+1]!='.' and self.tabuleiro[i+1][j+1]!='#' and self.tabuleiro[i+2][j+2]!='.' and self.tabuleiro[i+2][j+2]!='#') and self.tabuleiro[i+1][j+1]==self.tabuleiro[i+2][j+2]:
                   return i+1, j+1 
                elif i-2>=0 and j-2>=0 and self.tabuleiro[i][j] == '.' and (self.tabuleiro[i-1][j-1]!='.' and self.tabuleiro[i-1][j-1]!='#' and self.tabuleiro[i-2][j-2]!='.' and self.tabuleiro[i-2][j-2]!='#') and self.tabuleiro[i-1][j-1]==self.tabuleiro[i-2][j-2]:
                   return i+1, j+1 
                elif i+2<self.linhas and j-2>=0 and self.tabuleiro[i][j] == '.' and (self.tabuleiro[i+1][j-1]!='.' and self.tabuleiro[i+1][j-1]!='#' and self.tabuleiro[i+2][j-2]!='.' and self.tabuleiro[i+2][j-2]!='#') and self.tabuleiro[i+1][j-1]==self.tabuleiro[i+2][j-2]:
                   return i+1, j+1 
                elif i-2>=0 and j+2<self.colunas and self.tabuleiro[i][j] == '.' and (self.tabuleiro[i-1][j+1]!='.' and self.tabuleiro[i-1][j+1]!='#' and self.tabuleiro[i-2][j+2]!='.' and self.tabuleiro[i-2][j+2]!='#') and self.tabuleiro[i-1][j+1]==self.tabuleiro[i-2][j+2]:
                   return i+1, j+1
    
    def tabuleiro_cheio(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.tabuleiro[i][j]=='.':
                    return False
        return True

    def create_ancora(self):
        state = [self.tabuleiro,
                 self.movimentos,
                 self.ancoras]
        self.ancoras.push(deepcopy(state))

    def undo_ancora(self):
        if self.ancoras.size() > 0:
            state = self.ancoras.pop()
            self.tabuleiro = state[0]
            self.movimentos = state[1]
            self.ancoras = state[2]
        else:
            print('Aviso: Não existem âncoras.')

    def resolvido(self):
        "Determina se o puzzle foi resolvido de forma válida"
        return self.tabuleiro_cheio() and self.validar()

    def traduz_tabuleiro_lista(self, tabuleiro):
        'traduz um tabuleiro2D para uma lista plana equivalente'
        l = []
        count_empty=0
        for y in range(self.linhas):
            for x in range(self.colunas):
                l.append(tabuleiro[y][x])
                if tabuleiro[y][x]==".":
                    count_empty+=1
        return l, count_empty

    def carrega_lista_tabuleiro(self, l):
        'Carrega a lista1D para o tabuleiro'
        for y in range(self.linhas):
            for x in range(self.colunas):
                 self.tabuleiro[y][x] = l[x + self.colunas * y] #mapping de valores da lista1D para uma matriz2D

    def resolver_forca_bruta(self):
        'Resolve o tabuleiro aplicando backtracking recursivo ate encontrar uma solução'
        self.create_ancora()
        tabuleiro1D, count_empty = self.traduz_tabuleiro_lista(self.tabuleiro)
        for opt in product('XO', repeat=count_empty):
            opt_tabuleiro = deepcopy(tabuleiro1D)
            count_vazios = 0
            for pos in range(len(opt_tabuleiro)):
                if opt_tabuleiro[pos]==".":
                    opt_tabuleiro[pos]=opt[count_vazios]
                    count_vazios+=1
            self.carrega_lista_tabuleiro(opt_tabuleiro)
            if self.validar()==True:
                print("Solução válida encontrada.")
                return
        self.undo_ancora()
        print("O tabuleiro não tem solução válida possivel!")

    def gera_forca_bruta(self, dificuldade, linhas, colunas):
        'Resolve o tabuleiro aplicando backtracking recursivo ate encontrar uma solução'
        if dificuldade==1: # facil
            pficar = 0.5
        else:              # dificil
            pficar = 0.2

        self.inicializar_tabuleiro_vazio(linhas, colunas)

        for opt in product('XO#', repeat=linhas*colunas):
            self.carrega_lista_tabuleiro(opt)
            if self.validar() == True:
                for y in range(self.linhas):
                    for x in range(self.colunas):
                        if random.choice([True, False], p=[1-pficar, pficar]):
                            if self.tabuleiro[y][x]!="#":
                                self.tabuleiro[y][x]="."
                return True
        return False

