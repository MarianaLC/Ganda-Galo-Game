# -*- coding:utf-8 -*-
from cmd import *
from GandaGaloWindow_vitor import GandaGaloWindow
from GandaGaloEngine_vitor import GandaGaloEngine
import copy

class GandaGaloShell(Cmd):
    intro = 'Interpretador de comandos para o GandaGalo. Escrever help ou ? para listar os comandos disponíveis.\n'
    prompt = 'GandaGalo> '
           
    def do_mostrar(self, arg):
        " -  comando mostrar que leva como parâmetro o nome de um ficheiro..: mostrar <nome_ficheiro> \n" 
        try:
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 1:
                eng.ler_tabuleiro_ficheiro(lista_arg[0])
                print("Puzzle carregado:")
                eng.printpuzzle()
                global janela  # pois pretendo atribuir um valor a um identificador global
                if janela is not None:
                    del janela  # invoca o metodo destruidor de instancia __del__()
                janela = GandaGaloWindow(40, eng.getlinhas(), eng.getcolunas())
                janela.mostraJanela(eng.gettabuleiro())
            else:
                print("Número de argumentos inválido!")
        except:
            print("Erro: ao mostrar o puzzle.")
    
    def do_abrir(self, arg):
        " - comando abrir que leva como parâmetro o nome de um ficheiro..: abrir <nome_ficheiro>  \n"
        try:
            lista_arg = arg.split()
            eng.ler_tabuleiro_ficheiro(lista_arg[0])
            print("Puzzle carregado.")
        except:
            print("Erro: ao abrir o puzzle.")
            
    def do_gravar(self, arg):
        " - comando gravar que leva como parâmetro o nome de um ficheiro..: gravar <nome_ficheiro>  \n"
        print("O seu puzzle foi gravado!")
        lista_arg = arg.split()
        eng.escrever_tabuleiro_ficheiro(lista_arg[0])
        
    def do_jogar(self, arg):    
        " - comando jogar que leva como parâmetro o caractere referente à peça a ser jogada (‘X’ ou ‘O’) e dois inteiros que indicam o número da linha e o número da coluna, respetivamente, onde jogar \n"
        lista_arg = arg.split() #aqui estou a pegar na string com os argumentos do comando e a separa-los numa lista
        num_args = len(lista_arg) #aqui tem de dar 3 pois pretende-se 3 parametros
        if num_args == 3:
            simbolo = lista_arg[0]
            linha = int(lista_arg[1])
            coluna = int(lista_arg[2])#falta validar estes parametros ...
            eng.jogar(simbolo,linha,coluna)
            eng.printpuzzle()
            global janela
            if janela is not None:
                del janela  # invoca o metodo destruidor de instancia __del__()
            janela = GandaGaloWindow(40, eng.getlinhas(), eng.getcolunas())
            janela.mostraJanela(eng.gettabuleiro())
        else:
            print("Número de argumentos inválido!")

    def do_validar(self, arg):    
        " - comando validar que testa a consistência do puzzle e verifica se o tabuleiro está válido: validar \n"
        if eng.validar():
            print("Puzzle válido.")
        else: 
            print("Puzzle inválido!")
    
    def do_ajuda(self, arg):
        " - comando ajuda que indica a próxima casa lógica a ser jogada (sem indicar a peça a ser colocada): ajuda  \n"
        i, j = eng.ajudar()
        aux1 = copy.deepcopy(eng)
        aux2 = copy.deepcopy(eng)
        aux1.jogar('X', i, j)
        aux2.jogar('O', i, j)
        if aux1.validar() or aux2.validar():
            print('Palpite: Jogar na linha ' + str(i) + ' e coluna ' + str(j))
        else:
            for i in range (eng.getlinhas()):
                for j in range (eng.getcolunas()):
                    if eng.gettabuleiro()[i][j] == '.':
                        aux1 = copy.deepcopy(eng)
                        aux2 = copy.deepcopy(eng)
                        aux1.jogar('X', i+1, j+1)
                        aux2.jogar('O', i+1, j+1)
                        if aux1.validar() or aux2.validar():
                            print('Palpite: Jogar na linha ' + str(i+1) + ' e coluna ' + str(j+1))
                            return
            print('Sem palpite de ajuda!')

    def do_undo(self, arg):    
        " - comando para anular movimentos (retroceder no jogo): undo \n"
        eng.undo()
    
    def do_resolver(self, arg):    
        " - comando para resolver o puzzle: resolver \n"
        eng.resolver_forca_bruta()

    def do_ancora(self, arg):    
        " - comando âncora que deve guardar o ponto em que está o jogo para permitir mais tarde voltar a este ponto: ancora \n"
        eng.create_ancora()
    
    def do_undoancora(self, arg):    
        " - comando undo para voltar à última ancora registada: undoancora \n"
        eng.undo_ancora()
    
    def do_gerar(self, arg):    
        " - comando gerar que gera puzzles com solução única e leva três números inteiros como parâmetros: o nível de dificuldade (1 para ‘fácil’ e 2 para ‘difícil’), o número de linhas e o número de colunas do puzzle \n"
        lista_arg = arg.split()
        if len(lista_arg)==3:
            print("A gerar um tabuleiro, espera um pouco!")
            dif = int(lista_arg[0])
            if dif not in (1, 2):
                print("A dificuldade selecionada é invalida! Irá ser gerado um puzzle com dificuldade dificil!")
                
            linhas = int(lista_arg[1])
            colunas = int(lista_arg[2])
            resultado = eng.gera_forca_bruta(dif, linhas, colunas)
            if resultado==True:
                print("Foi gerado um tabuleiro (%s, %s) com dificuldade: %s!" % (colunas, linhas, dif))
            else:
                print("O tabuleiro não tem solução valida possivel!")
        else:
            print("O numero de parametros introduzidos é invalido!")

    def do_ver(self, arg):
        " - Comando para visualizar graficamente o estado atual do GandaGalo caso seja válido: VER  \n"
        print("Puzzle atual:")
        eng.printpuzzle()
        global janela
        if janela is not None:
            del janela  # invoca o metodo destruidor de instancia __del__()
        janela = GandaGaloWindow(40, eng.getlinhas(), eng.getcolunas())
        janela.mostraJanela(eng.gettabuleiro())
        
    def do_sair(self, arg):
        "Sair do programa GandaGalo: sair"
        print('Obrigado por ter utilizado o Gandagalo, espero que tenha sido divertido!')
        global janela  # pois pretendo atribuir um valor a um identificador global
        if janela is not None:
            del janela  # invoca o metodo destruidor de instancia __del__()
        return True



if __name__ == '__main__':
    eng = GandaGaloEngine()
    janela = None
    sh = GandaGaloShell()
    sh.cmdloop()

