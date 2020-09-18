import requests
import sqlite3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from flask import redirect, render_template, request, session
from functools import wraps

inicio = 2000
fim = 2021
						
def deputados_update():
	# Setup error handling when fetching data via requests	
	sessao_deputados = requests.Session()
	retry = Retry(connect=5, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries=retry)
	sessao_deputados.mount('http://', adapter)
	sessao_deputados.mount('https://', adapter)
	
	sessao_deputado = requests.Session()
	retry = Retry(connect=5, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries=retry)
	sessao_deputado.mount('http://', adapter)
	sessao_deputado.mount('https://', adapter)
	
	# Connects to the database
	db = sqlite3.connect('database.db')
	db_cursor = db.cursor()
	
	# Fetches the information from the deputados api, loops throught it and stores it in the database
	resp_deputados = sessao_deputados.get('https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome')
	json_deputados = resp_deputados.json()
	deputados = json_deputados['dados']
	
	for deputados in deputados:
		resp_deputado = sessao_deputado.get('https://dadosabertos.camara.leg.br/api/v2/deputados/'+str(deputados['id']))
		json_deputado = resp_deputado.json()
		deputado = json_deputado['dados']
		db_cursor.execute("""INSERT INTO deputados (id, nomeCivil, nomeEleitoral, sexo, partido, uf, foto, cpf, email, telefone, predio, andar, sala, situacao, dataNascimento, dataFalecimento, ufNascimento, municipioNascimento, escolaridade) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (deputado['id'], deputado['nomeCivil'], deputado['ultimoStatus']['nomeEleitoral'], deputado['sexo'], deputado['ultimoStatus']['siglaPartido'], deputado['ultimoStatus']['siglaUf'], deputado['ultimoStatus']['urlFoto'], deputado['cpf'], deputado['ultimoStatus']['email'], deputado['ultimoStatus']['gabinete']['telefone'], deputado['ultimoStatus']['gabinete']['predio'], deputado['ultimoStatus']['gabinete']['andar'], deputado['ultimoStatus']['gabinete']['sala'], deputado['ultimoStatus']['situacao'], deputado['dataNascimento'], deputado['dataFalecimento'], deputado['ufNascimento'], deputado['municipioNascimento'], deputado['escolaridade']))
		db.commit()

def proposicoes_update():
	# Setup error handling when fetching data via requests
	sessao_proposicoes = requests.Session()
	retry = Retry(connect=5, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries=retry)
	sessao_proposicoes.mount('http://', adapter)
	sessao_proposicoes.mount('https://', adapter)
	
	sessao_proposicao = requests.Session()
	retry = Retry(connect=5, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries=retry)
	sessao_proposicao.mount('http://', adapter)
	sessao_proposicao.mount('https://', adapter)
	
	# Connects to the database
	db = sqlite3.connect('database.db')
	db_cursor = db.cursor()
	
	# Fetches the information from the votacoes api, loops throught it and stores it in the database
	for i in range(inicio, fim, 1):
		k = 0
		for j in range(1, 13, 1):
			if j == 1 or j == 3 or j == 5 or j == 7 or j == 8 or j == 10 or j == 12:
				k = 31
			elif j == 2:
				k = 28
			else:
				k = 30
			if j < 10:
				j = "{0:0=2d}".format(j)
			resp_proposicoes = sessao_proposicoes.get('https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio='+str(i)+'-'+str(j)+'-01&dataFim='+str(i)+'-'+str(j)+'-'+str(k)+'&ordenarPor=id')
			json_proposicoes = resp_proposicoes.json()
			proposicoes = json_proposicoes['dados']
			for proposicoes in proposicoes:
				resp_proposicao = sessao_proposicao.get('https://dadosabertos.camara.leg.br/api/v2/proposicoes/'+str(proposicoes['id']))
				json_proposicao = resp_proposicao.json()
				proposicao = json_proposicao['dados']
				db_cursor.execute("""INSERT INTO proposicoes (id, siglaTipo, descricaoTipo, ano, dataApresentacao, ementa, ementaDetalhada, descricaoSituacao, descricaoTramitacao, keywords, urlInteiroTeor) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (proposicoes['id'], proposicoes['siglaTipo'], proposicao['descricaoTipo'], proposicoes['ano'], proposicao['dataApresentacao'], proposicoes['ementa'], proposicao['ementaDetalhada'], proposicao['statusProposicao']['descricaoSituacao'], proposicao['statusProposicao']['descricaoTramitacao'], proposicao['keywords'], proposicao['urlInteiroTeor']))
				db.commit()

def votacoes_update():
	# Setup error handling when fetching data via requests
	sessao_votacoes = requests.Session()
	retry = Retry(connect=5, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries=retry)
	sessao_votacoes.mount('http://', adapter)
	sessao_votacoes.mount('https://', adapter)
	
	# Connects to the database
	db = sqlite3.connect('database.db')
	db_cursor = db.cursor()
	
	# Fetches the information from the votacoes api, loops throught it and stores it in the database
	for i in range(inicio, fim, 1):
		k = 0
		for j in range(1, 13, 1):
			if j == 1 or j == 3 or j == 5 or j == 7 or j == 8 or j == 10 or j == 12:
				k = 31
			elif j == 2:
				k = 28
			else:
				k = 30
			if j < 10:
				j = "{0:0=2d}".format(j)
			resp_votacoes = sessao_votacoes.get('https://dadosabertos.camara.leg.br/api/v2/votacoes?dataInicio='+str(i)+'-'+str(j)+'-01&dataFim='+str(i)+'-'+str(j)+'-'+str(k)+'&ordenarPor=dataHoraRegistro')
			json_votacoes = resp_votacoes.json()
			votacoes = json_votacoes['dados']
			for votacoes in votacoes:
				db_cursor.execute("""INSERT INTO votacoes (id, data, descricao, aprovacao) VALUES(?, ?, ?, ?)""", (votacoes['id'], votacoes['data'], votacoes['descricao'], votacoes['aprovacao']))
				db.commit()

def autores_proposicoes_update():
	# Setup error handling when fetching data via requests
	sessao_proposicoes = requests.Session()
	retry = Retry(connect=5, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries=retry)
	sessao_proposicoes.mount('http://', adapter)
	sessao_proposicoes.mount('https://', adapter)
	
	sessao_autores_proposicao = requests.Session()
	retry = Retry(connect=5, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries=retry)
	sessao_autores_proposicao.mount('http://', adapter)
	sessao_autores_proposicao.mount('https://', adapter)
	
	# Connects to the database
	db = sqlite3.connect('database.db')
	db_cursor = db.cursor()
	
	# Fetches the information from the votacoes api, loops throught it and stores it in the database
	for i in range(inicio, fim, 1):
		k = 0
		for j in range(1, 13, 1):
			if j == 1 or j == 3 or j == 5 or j == 7 or j == 8 or j == 10 or j == 12:
				k = 31
			elif j == 2:
				k = 28
			else:
				k = 30
			if j < 10:
				j = "{0:0=2d}".format(j)
			resp_proposicoes = sessao_proposicoes.get('https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio='+str(i)+'-'+str(j)+'-01&dataFim='+str(i)+'-'+str(j)+'-'+str(k)+'&ordenarPor=id')
			json_proposicoes = resp_proposicoes.json()
			proposicoes = json_proposicoes['dados']
			for proposicoes in proposicoes:
				resp_autores_proposicao = sessao_autores_proposicao.get('https://dadosabertos.camara.leg.br/api/v2/proposicoes/'+str(proposicoes['id'])+'/autores')
				json_autores_proposicao = resp_autores_proposicao.json()
				autores_proposicao = json_autores_proposicao['dados']
				if autores_proposicao == []:
					continue
				else:
					for autores_proposicao in autores_proposicao:
						db_cursor.execute("""INSERT INTO autoresProposicoes (idProposicao, nome) VALUES(?, ?)""", (proposicoes['id'], autores_proposicao['nome']))
						db.commit()

def votacoes_proposicoes_update():
	# Setup error handling when fetching data via requests
	sessao_proposicoes = requests.Session()
	retry = Retry(connect=5, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries=retry)
	sessao_proposicoes.mount('http://', adapter)
	sessao_proposicoes.mount('https://', adapter)
	
	sessao_votacao_proposicao = requests.Session()
	retry = Retry(connect=5, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries=retry)
	sessao_votacao_proposicao.mount('http://', adapter)
	sessao_votacao_proposicao.mount('https://', adapter)
	
	# Connects to the database
	db = sqlite3.connect('database.db')
	db_cursor = db.cursor()
	
	# Fetches the information from the votacoes api, loops throught it and stores it in the database
	for i in range(inicio, fim, 1):
		k = 0
		for j in range(1, 13, 1):
			if j == 1 or j == 3 or j == 5 or j == 7 or j == 8 or j == 10 or j == 12:
				k = 31
			elif j == 2:
				k = 28
			else:
				k = 30
			if j < 10:
				j = "{0:0=2d}".format(j)
			resp_proposicoes = sessao_proposicoes.get('https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio='+str(i)+'-'+str(j)+'-01&dataFim='+str(i)+'-'+str(j)+'-'+str(k)+'&ordenarPor=id')
			json_proposicoes = resp_proposicoes.json()
			proposicoes = json_proposicoes['dados']
			for proposicoes in proposicoes:
				resp_votacao_proposicao = sessao_votacao_proposicao.get('https://dadosabertos.camara.leg.br/api/v2/proposicoes/'+str(proposicoes['id'])+'/votacoes?ordem=ASC&ordenarPor=dataHoraRegistro')
				json_votacao_proposicao = resp_votacao_proposicao.json()
				votacao_proposicao = json_votacao_proposicao['dados']
				if votacao_proposicao == []:
					continue
				else:
					for votacao_proposicao in votacao_proposicao:
						db_cursor.execute("""INSERT INTO votacoesProposicoes (idProposicao, idVotacao) VALUES(?, ?)""", (proposicoes['id'], votacao_proposicao['id']))
						db.commit()

def resultados_votacoes_update():
	# Setup error handling when fetching data via requests
	sessao_votacao = requests.Session()
	retry = Retry(connect=5, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries=retry)
	sessao_votacao.mount('http://', adapter)
	sessao_votacao.mount('https://', adapter)
	
	sessao_voto = requests.Session()
	retry = Retry(connect=5, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries=retry)
	sessao_voto.mount('http://', adapter)
	sessao_voto.mount('https://', adapter)
	
	# Connects to the database
	db = sqlite3.connect('database.db')
	db_cursor = db.cursor()
	
	for i in range(inicio, fim, 1):
		k = 0
		for j in range(1, 13, 1):
			if j == 1 or j == 3 or j == 5 or j == 7 or j == 8 or j == 10 or j == 12:
				k = 31
			elif j == 2:
				k = 28
			else:
				k = 30
			if j < 10:
				j = "{0:0=2d}".format(j)
			# Returns the information regading the votacoes, loops through it and store info in database table
			resp_resultado_votacao = sessao_votacao.get('https://dadosabertos.camara.leg.br/api/v2/votacoes?dataInicio='+str(i)+'-'+str(j)+'-01&dataFim='+str(i)+'-'+str(j)+'-'+str(k))
			json_resultado_votacao = resp_resultado_votacao.json()
			resultado_votacao = json_resultado_votacao['dados']
			
			for resultado_votacao in resultado_votacao:
				resp_resultado_voto = sessao_voto.get('https://dadosabertos.camara.leg.br/api/v2/votacoes/'+resultado_votacao['id']+'/votos')
				json_resultado_voto = resp_resultado_voto.json()
				resultado_voto = json_resultado_voto['dados']
				if resultado_voto == []:
					continue
				else:
					for resultado_voto in resultado_voto:
						db_cursor.execute("""INSERT INTO resultadoVotacoes (idCandidato, 		idVotacao, data, voto) VALUES(?, ?, ?, ?)""", 								(resultado_voto['deputado_']['id'], resultado_votacao['id'], 				resultado_votacao['data'], resultado_voto['tipoVoto']))
						db.commit()

def login_required(f):
    # Decorate routes to require login. http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function