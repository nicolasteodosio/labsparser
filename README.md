### Instalação ###
* Clone o projeto `git clone git@github.com:nicolasteodosio/labsparser.git`
* Projeto foi criando unsando python 3.6, então cria um virtualenv com python 3.6
* Recomendo o uso do  [pyenv](https://github.com/pyenv/pyenv-installer) e [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv#installation)
* Ative seu virtualenv
* [Instale o docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository)
* [Instale o docker-compose](https://docs.docker.com/compose/install/#install-compose)
* Se utilizar `pipenv` execute: `pipenv sync`
* Caso não, na raiz do projeto execute `pip install -r requirements-dev.txt`

### Rodando Parser ###
* Execute o `docker-compose up -d` , que irá subir um `MONGODB`
* Adicione o log_file no diretório `parser/samples`
* Execute o comando `python parser/main.py --log samples/games.log` 
    * Esse comando fará a analise do log e salvará o resultado no `MONGODB`
* Também é possível executar o comando `python parser/main.py --log samples/games.log --print True`
    * Esse comando além de salvar no mongo ele faz um `print`do resultado da análise.

### Rodando a API ###
* Execute o `docker-compose up -d` , que irá subir um MONGODB
* Execute o comando `python api/wsgi.py` 
* Aplicação estará rodando em: `http://localhost:9001`
* `http://localhost:9001/api/gamelog/games`
    * Endpoint onde mostra a listagem de todos as partidas.
    * Só espera método `GET`
* `http://localhost:9001/api/gamelog/games/<id>`
    * Endpoint onde mostra uma partida especificada pelo id.
    * Só espera método `GET`
    
### Rodando os testes ###
* Para executar todos os testes `python run_tests.py`
* Para executar um teste específico `python run_tests.py -k nome_do_teste_ou_classe_do_teste`
   
### Observações ###
