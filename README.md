# Sumário:

- [Introdução](#introdução)
- [Start](#inicialização)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Testes](#testes)
- [Arquitetura da Solução](#arquitetura-da-solução)
- [Modelo de Dados](#modelo-de-dados)
- [Perguntas](#perguntas)

## Introdução
O projeto Challenge-Tech é uma iniciativa voltada para a construção de um pipeline de dados automatizado, empregando tecnologias como MySQL e Airflow. A essência deste projeto reside na automatização do fluxo de dados, desde a extração, tratamento até o carregamento dos dados em um banco de dados MySQL.

Para facilitar a gestão e a escalabilidade, o ambiente de desenvolvimento utiliza contêineres Docker. O MySQL é implantado em um contêiner Docker dedicado, garantindo flexibilidade e portabilidade no gerenciamento do banco de dados. Da mesma forma, Airflow é implantado em um ambiente isolado, permitindo a orquestração e o agendamento de tarefas de forma eficiente e confiável.

O processo de automatização é conduzido por Directed Acyclic Graphs (DAGs) no Airflow. As DAGs são responsáveis por definir o fluxo de trabalho, desde a identificação das fontes de dados até a carga dos dados tratados no banco de dados MySQL. Uma parte que vale ressaltar+ deste processo é a integração com volumes Docker, onde os dados são armazenados como volumes nos containers do Airflow, permitindo uma interação fluida entre os dados e o pipeline de processamento.

No âmbito técnico, o projeto engloba várias etapas, incluindo a extração de dados dos volumes Docker, o tratamento e limpeza dos dados, bem como a inserção eficiente no banco de dados MySQL. Cada DAG foi projetado para garantir a integridade e consistência dos dados.

## Inicialização

### MySQL

```
docker-compose -f docker-compose.MySQL.yml up -d --build
```

### Airflow

```
docker-compose -f docker-compose.Airflow.yml up -d airflow-init

docker-compose -f docker-compose.Airflow.yml up -d
```

## Estrutura do Projeto

```
Challenge-Tech/
├── config/
├── dados/
│   ├── equipment_sensors.json
│   ├── equipment.json
│   └── equpment_failure_sensors.json
├── dags/
│   ├── clases/
│   │   ├── conn.py
│   │   ├── extract.py
│   │   ├── load.py
│   │   └── mysql_conn.py
│   ├── credentials/
│   │   ├── credential.py
│   │   ├── paths.py
│   │   └── tables.py
│   ├── ddls/
│   │   ├── equipment_failure_sensors.sql
│   │   ├── equipment_sensors.sql
│   │   └── equipment.sql
│   ├── scripts/
│   │   ├── equipment_failure_sensors_mysql.py
│   │   ├── equipment_mysql.py
│   │   ├── equipment_sensors_mysql.py
│   │   ├── tabelas_raw.py
│   │   └── txt_json.py
│   ├── dag_equipment_failure_sensors.py
│   ├── dag_equipment_sensors.py
│   ├── dag_equipment.py
│   └── dag_teste.py
├── logs/
├── plugins/
├── img/
├── .env
├── .gitignore
├── docker-compose.Airflow.yml
├── docker-compose.MySQL.yml
├── Dockerfile
└── README.md
```
```
config/: Esta pasta é usada para armazenar as configurações que são montadas como volume pelo docker-compose.Airflow.

dados/: Outra pasta que é montada como volume pelo Airflow. É usada para armazenar dados necessários para os DAGs, como arquivos JSON.

logs/: Pasta usada para armazenar logs gerados durante a execução dos DAGs. 

plugins/: Pasta usada para armazenar plugins personalizados que estendem a funcionalidade do Airflow.

img/: Guarda as imagens usadas na documentação do projeto.

dags/: Esta pasta contém os DAGs, que são fluxos de trabalho automatizados escritos em Python para o Apache Airflow.

dags/clases/: Esta pasta contém classes Python criadas para uso no projeto. C

dags/credentials/: Pasta que armazena constantes do projeto, como caminhos de arquivos, nomes de tabelas e credenciais de acesso ao MySQL.

dags/ddls/: Pasta que contém os DDLs (Data Definition Language) das tabelas do banco de dados. 

dags/scripts/: Esta pasta contém scripts manuais criados para realizar operações de extração, transformação e carga (ETL) de dados. 

dags/utils/: Contém arquivos com funções que podem ser uteis em diferentes partes do projeto.

.env: Arquivo de configuração do Apache Airflow que contém variáveis de ambiente e configurações específicas do ambiente de execução.

.gitignore: Arquivo usado pelo Git para determinar quais arquivos e pastas devem ser ignorados ao versionar o projeto.

docker-compose.Airflow.yml e docker-compose.MySQL.yml: Arquivos de configuração do Docker Compose que definem os serviços necessários para executar o Apache Airflow e o MySQL em contêineres Docker.

Dockerfile: Arquivo contendo informações para a dockerização do Apache Airflow.
```
## Testes

Utilizei para validar os testes a dag [dag_equipment_sensor.py](/dags/dag_equipment_sensors.py), pois possui uma estrutura completa que serviu de base para as outras duas dags.

Temos então o gráfico de execução da dag.
![Execução completa da dag](/img/dag_equipment_sensors.png)

E a tabela com os dados carregados no database MySQL.
![Tabela com os dados carregados](/img/tabela_equipment_sensors.png)

## Arquitetura da Solução
![Arquitetura de Dados](/img/Arquitetura.png)

Ambos os serviços, Airflow e MySQL, foram implementados via Docker.

### Fluxo do Processo  

        +----------------------------------+
        |          Apache Airflow          |
        +---------------|------------------+
                        |            
          +-------------v-------------------+
          |       Python Scripts            |
          |       (ETL, Classes, etc.)      |
          +-------|-----|------|------------+
                  |     |      |
      +-----------v---+ |   +--v---------------+
      |   Data Files  | |   |   Credentials    |
      |   .JSON       | |   |  (credentials.py)|
      +---------------+ |   +------------------+
                        |       
        +---------------v-----------------+
        |        MySQL Database           |
        +---------------------------------+


## Modelo de Dados

![Modelo de Dados](/img/modelo.png)

| Nome da Tabela        | Descrição                                   |
|-----------------------|---------------------------------------------|
| equipment             | Tabela que contém informações sobre os equipamentos e seus grupo. Chave Primária é o campo equipment_id. |
| equipment_sensors     | Tabela que armazena dados dos sensores dos equipamentos. Um mesmo equipamento pode ter vários sensores, chave da tabela é uma chave composta pelos campos equipment_id e sensor_id. |
| equipment_failure_sensors | Tabela que contém o registro de falhas dos sensores. Contém os campos de hora da falha, se realmente foi uma falha ou uma atenção, qual a temperatura registrada, a vibração e qual sensor registrou isso. De posse da informação do sensor é possível saber qual o equipamento falhou, pois um sensor só pode está relacionado a um equipamento. A chave dessa tabela é a uma chave composta formada pelos campos timestamp, sensor_id, temperatura e vibration. Pois um mesmo sensor, em um mesmo instante registra apenas uma temperatura e uma vibração.|

### Validação das Chaves

Query 1:
```
SELECT
    equipment_id , 
    COUNT(*) AS count
FROM
    equipment e
GROUP BY
    equipment_id 
HAVING
    COUNT(*) > 1
ORDER BY
    COUNT(*) DESC;
```
Não retornou resultado validando a chave primária da tabela.

Query 2:

```
SELECT
    sensor_id, 
    COUNT(*) AS count
FROM
    equipment_sensors es
GROUP BY
    sensor_id
HAVING
    COUNT(*) > 1
ORDER BY
    COUNT(*) DESC;
```
Não retornou resultado validando a chave primária da tabela.

Query 3:
```
SELECT
    `timestamp`  ,
    sensor_id ,
    temperature ,
    vibration ,
    COUNT(*) AS count
FROM
    equipment_failure_sensors efs 
GROUP BY
    1,2,3,4
HAVING
    COUNT(*) > 1
ORDER BY
    COUNT(*) DESC;
```
Não retornou resultado validando a chave primária da tabela.

## Perguntas

### Total de falhas de equipamento que ocorreram?

```
SELECT 
	count(*)
FROM
	equipment_failure_sensors efs
WHERE 
	log_level = 'ERROR';
```
A consulta retorna um total de 4.749.474 falhas registradas. Para fins deste contexto, consideramos como falha todo registro marcado como ERROR. Além disso, é importante ressaltar que, na perspectiva do autor, um equipamento que entre em falha em um determinado instante pode acionar todos os sensores associados a ele. Portanto, cada registro de falha é representado por um sensor específico e contabilizado individualmente.

### Qual nome de equipamento teve mais falhas?

```
SELECT 
	e.equipment_id,
	e.name, 
	count(*) as num_failures
FROM 
	equipment_failure_sensors efs 
LEFT JOIN 
	equipment_sensors es ON efs.sensor_id  = es.sensor_id 
LEFT JOIN 
	equipment e ON e.equipment_id = es.equipment_id 
WHERE 
	efs.log_level = 'ERROR'
GROUP BY 
	e.equipment_id, e.name 
ORDER BY 
	num_failures DESC
LIMIT 2;
```

A consulta resultou no equipamento de nome 2C195700 e ID 14. Foi posto a condição de `log_level = 'ERROR'` pois no entendimento do autor essa é a validação que houve uma falha.

### Média de falhas por grupo de equipamentos, ordenada pelo número de falhas em ordem crescente?

```
SELECT 
    e.group_name,
    COUNT(efs.item) AS contagem_de_falhas,
    COUNT(efs.item)/COUNT(DISTINCT e.equipment_id) as avg_falhas
FROM 
    equipment_failure_sensors efs
LEFT JOIN 
    equipment_sensors es ON efs.sensor_id = es.sensor_id
LEFT JOIN 
    equipment e ON es.equipment_id = e.equipment_id
WHERE 
	efs.log_level = 'ERROR'
GROUP BY 
    e.group_name
ORDER BY
	2;
```

![Q3](/img/q3.png)

### Classifique os sensores que apresentam o maior número de erros por nome de equipamento em um grupo de equipamentos.

```
SELECT *
FROM (
    SELECT 
        base.*,
        (@row_number := CASE WHEN @prev_group = base.equipment_group THEN @row_number + 1 ELSE 1 END) AS rn,
        @prev_group := base.equipment_group
    FROM (
        SELECT 
            e.group_name AS equipment_group,
            e.name,
            efs.sensor_id,
            COUNT(efs.item) AS total_failures
        FROM 
            equipment_failure_sensors efs
        LEFT JOIN 
            equipment_sensors es ON efs.sensor_id = es.sensor_id
        LEFT JOIN 
            equipment e ON es.equipment_id = e.equipment_id
        WHERE 
            efs.log_level = 'ERROR'
        GROUP BY 
            e.group_name, e.name, efs.sensor_id
        ORDER BY 
            e.group_name, total_failures DESC
    ) AS base
    CROSS JOIN (SELECT @row_number := 0, @prev_group := NULL) AS vars
) AS ranked
WHERE rn = 1;
```
![q4](/img/q4.png)

Na versão do MySQL Database utilizada no projeto, que é a [5.7](https://dev.mysql.com/doc/refman/5.7/en/functions.html), as funções QUALIFY e ROW_NUMBER não estão disponíveis. Por esse motivo, a consulta foi elaborada utilizando uma abordagem alternativa. É importante observar que ambas as funções foram introduzidas na versão [8.0](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html) do MySQL.

