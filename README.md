# Sistema de agregação de dados de cotações de criptomoedas em tempo real

## Setup

### Dependências
O código foi desenvolvido utilizando o Python 3.6.9 e as bibliotecas [Flask](https://flask.palletsprojects.com/en/2.0.x/), [Pandas](https://pandas.pydata.org), [APScheduler](https://apscheduler.readthedocs.io/en/stable/) e [MySQL](https://dev.mysql.com/doc/connector-python/en/). Os requerimentos de projetos podem ser baixados com o código:

```sh
docker-compose up 
```

O sistema consome a API [Poloniex](https://docs.poloniex.com/#introduction) para realizar a aquisição dos dados. Todos os resultados tem como saída as candles da moeda em relação ao dólar (USDT). As moedas disponíveis para seleção podem ser encontradas no seguinte [link](https://docs.poloniex.com/#currencies). 

## Chamada do sistema

Como padrão o programa será iniciado no endereço e portas padrão da API Flask (127.0.0.1 : 5000). A chamada para pedir os resultados de uma moeda (Bitcoin (BTC) no exemplo) é: http://127.0.0.1:5000/currency_sumary?currency=BTC. A reposta tem o seguinte formato:

```json
{
    "response": 200,
    "object": [
        {
            "currencyPair": "USDT_BTC",
            "updateDate": "2021-05-17 20:52:19.142164",
            "high1min": 44841.34726137,
            "low1min": 44798.03867676,
            "high5min": 44841.34726137,
            "low5min": 44798.03867676,
            "high10min": 44841.34726137,
            "low10min": 44798.03867676,
            "open1min": 44798.03867676,
            "close1min": 44837.61110764,
            "open5min": 44798.03867676,
            "close5min": 44837.61110764,
            "open10min": 44798.03867676,
            "close10min": 44837.61110764
        }
    ]
}
```
A http://127.0.0.1:5000/currency_sumary/all retorna todas as moedas na forma:

```json
{
    "response": 200,
    "object": [
        {
            "currencyPair": "USDT_AAVE",
            "updateDate": "2021-05-17 20:59:22.548898",
            "high1min": 582.97009103,
            "low1min": 582.97009103,
            "high5min": 582.97009103,
            "low5min": 582.97009103,
            "high10min": 582.97009103,
            "low10min": 582.97009103,
            "open1min": 582.97009103,
            "close1min": 582.97009103,
            "open5min": 582.97009103,
            "close5min": 582.97009103,
            "open10min": 582.97009103,
            "close10min": 582.97009103
        },
        ...
    ]
}
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

Caso um valor não reconhecido pelo sistema seja pedido a moeda será ignorada.

As tarefas para cada moeda são lançadas na iniciailização do programa. A variável BASE_UPDATE_SCHEDULE_PERIOD pode ser alterada para regular o período da tarefa de aquisição de dados da API Poloniex. A mudança desse valor afetará a precisão, mas também a performance pois mais dados serão considerados nos cálculos das candles. Por padrão ela foi configurada para 2 segundos.A atualização das candles é feita a cada 1 minuto.

O tratamento de erros de execução é baseado nos padrões fornecidos por APScheduler. A tarefa será executada múltiplas vezes até que ocorra o sucesso ou timeout. 



