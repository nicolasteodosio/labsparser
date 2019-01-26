
[![Build Status](https://travis-ci.org/nicolasteodosio/labsparser.svg?branch=master)](https://travis-ci.org/nicolasteodosio/labsparser)

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
Vou deixar aqui o motivo de algumas decisões nesse projeto.
* Primeiramente minha opção pelo Mongo no parser, foi primeiro para praticar a implementação de um banco NOSQL,
 e outro foi pra esse projeto ficar mais próximo de uma aplicação em produção, claro que eu poderia salvar o resultado
 em um arquivo, que poderia subir para o S3 ou algo similar, ou até mesmo deixar só como print mesmo. Pra isso deixei a 
 opção de "printar" o resultado caso queira, mas sempre salvando no mongo.
* Outra coisa que gostaria de citar é o usa da biblioteca [rows](https://github.com/turicas/rows) , que além de ser 
open source, que sempre gosto de utilizar projetos open source, é feito por um brasileiro o Turicas. 
Soube desse projeto em uma palestra na python sudeste 2017. 
* A escolha do `Flask` para a api, foi por ser um framework bem enxuto e de rápido desenvolvimento.
 Considerei até usar outros como o django, mas descartei por causa de toda a estrutura qeu ele tem, 
 e o Vibora que é um framework feito por um brasileiro também, 
 mas descartei por não saber como um framework assincrono funcionaria com o mongo, 
 já que o Flask tem uma integrção muito boa com o mongo.
* Uma consideração sobre as view da api é que o tratamento de exceções que fiz não é o ideal. 
Fiz de uma maneira onde não retorno a exceção em si , como resposta da view, e isso já garante uma certa segurança.
Porém dificulta a resolução de bug, pois só acessando a máquina e ver os logs para descobrir o que aconteceu, 
ou adicionar um sistema de capturar exceptions, como o `Sentry` ou o `Rollbar` . Uilizar um desses seria minha escolha.
* Utilizei o `Travis`, pra fazer o CI, mas ele só está rodando os testes. 
Faltando ele executar o build para o deploy, caso a aplicação estivesse em produção.
