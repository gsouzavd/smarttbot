# Sistema de agregação de dados de cotações de criptomoedas em tempo real

## Setup

### Dependências
O código foi desenvolvido utilizando o Python 3.6.9 e as bibliotecas [Flask](https://flask.palletsprojects.com/en/2.0.x/), [Pandas](https://pandas.pydata.org), [APSScheduler](https://apscheduler.readthedocs.io/en/stable/) e [MySQL](https://dev.mysql.com/doc/connector-python/en/). Os requerimentos de projetos podem ser baixados com o código:

```sh
docker-compose up 
```

O sistema consome a API [Poloniex](https://docs.poloniex.com/#introduction) para realizar a aquisição dos dados. Todos os resultados tem como saída as candles da moeda em relação ao dólar (USDT). As moedas disponíveis para seleção podem ser encontradas no seguinte [link](https://docs.poloniex.com/#currencies). 

## Chamada do sistema

Como padrão o programa será iniciado no endereço e portas padrão da API Flask (127.0.0.1 : 5000). A chamada para pedir os resultados de uma moeda (Bitcoin no exemplo) é: http://127.0.0.1:5000/currency_sumary?currency=BTC. A reposta tem o seguinte formato:

```json
[
    {
        "currencyPair": "USDT_BTC",
        "updateDate": "2021-05-13 23:04:32.402273",
        "high1min": 49139.50002486, "low1min": 49104.12285336,
        "high5min": 48653.60019807, "low5min": 48300.0,
        "high10min": 48821.50521867, "low10min": 48300.0,
        "open1min": 49109.8906812, "close1min": 49104.12285336,
        "open5min": 48632.00583028, "close5min": 48300.0,
        "open10min": 48670.64607541, "close10min": 48300.0
    }
]
```

Os valores das Candles são calculados à partir da execução do programa. Os dados para a conexão MySQL se encontram no arquivo DatabaseMySQL.py. Como se trata de uma aplicação de teste um servidor [gratuíto](https://www.freemysqlhosting.net) foi utilizado, assim muitas requisições simultâneas podem causar instabilidade. O sistema aceita até 20 conexões ao mesmo tempo. A pool de 8 valores (16 conexões) foi criada para os testes. 

Devido às restrições do servidor de testes escolhidos apenas uma tabela foi criada para representar as 3 candles.

O log da execução é exportado para o arquivo Execution_log.log durante a execução.

## Configuração 

No arquivo app.py é possível de encontrar a lista de moedas que serão executadas. Novas moedas podem ser inseridas na lista para serem atulizadas pelo programa.

```python
# Currency list that will be used
currency_list = ['BTC', 'XMR']
```

As tarefas para cada moeda são lançadas na iniciailização do programa. A variável BASE_UPDATE_SCHEDULE_PERIOD pode ser alterada para regular o período da tarefa de aquisição de dados da API Poloniex. A mudança desse valor afetará a precisão, mas também a performance pois mais dados serão considerados nos cálculos das candles. Por padrão ela foi configurada para 2 segundos.A atualização das candles é feita a cada 1, 5 e 10 minutos respectivamente.



