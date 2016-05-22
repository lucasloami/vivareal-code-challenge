# Code Challenge - Viva Real

Esse projeto é uma API RESTful que adiciona e busca imóveis dentro do reino de Spottipos. Você pode conhecer a [Lenda de Spottipos](http://vivareal.github.io/historia/) também.

A API foi construída em Python 2.7.6, usando [Flask](http://flask.pocoo.org/) e sua extensão [Flask RESTful](http://flask-restful-cn.readthedocs.io/en/0.3.4/).

# Pré requisitos
Você vai encontrar todas as dependências no arquivo `requirements.txt`. Para instalá-las, basta executar o comando `pip install -r requirements.txt`

# Banco de Dados
Não foi utilizado nenhum SGBD para esse projeto. O "banco de dados" utilizado são os arquivos `.json` presentes na pasta `databases`. Todas as ações que envolvem _fetch_ ou _save_ dos dados são realizadas em cima desses arquivos.

# Estrutura do Projeto
```
|-project/
|--- __init__.py
|--- run.py
|--- run_tests.py
|--- requirements.txt
|--- api/
|------- __init__.py
|------- api.py
|------- api_test.py
|------- databases/
|------- models/
|------- resources/
```
# Executar a API
```sh
$ git clone [URL_DO_PROEJTO] NOME_DA_PASTA
$ cd NOME_DA_PASTA
$ python run.py
```

Quando o server estiver executando, você pode testar as respostas da API usando `curl`. Alguns exemplos abaixo:

```sh
$ curl -X GET "http://127.0.0.1:5000/properties?ax=88&ay=200&bx=100&by=200"
$ curl -X GET "http://127.0.0.1:5000/properties/30"
$ curl -H "Content-Type: application/json" -X POST "http://127.0.0.1:5000/properties" -d '{ "x": 222, "y": 444, "beds": 4, "baths": 3, "squareMeters": 210}'
```

# Testes
Uma suite de testes foi criada dentro do arquivo `api_test.py`. Para realizar os testes na aplicação, execute o comando `python run_tests.py` a partir da pasta raiz do projeto.