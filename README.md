# Script-PythonLabelsVms

Um script automatizado em Python para aplicação resiliente de marcações (labels) em instâncias de Máquinas Virtuais (VMs) do Google Cloud Compute Engine, processadas em lote a partir de um arquivo CSV de inventário.

## 📋 Descrição

Este projeto foi desenvolvido para automatizar o tagueamento e a governança de VMs na GCP. O script lê um arquivo de inventário local (`vms.csv`), sanitiza os dados para cumprir as rígidas regras de sintaxe do Google Cloud (removendo maiúsculas, espaços e caracteres inválidos) e executa de forma transparente o comando de infraestrutura `gcloud compute instances add-labels` de forma resiliente por meio de subprocessos.

## 🚀 Funcionalidades

- **Sanitização Automática de Labels**: Converte os valores das colunas do CSV para letras minúsculas e substitui espaços ou caracteres proibidos por hifens (`-`), evitando erros de validação de API na nuvem.
- **Resiliência por Recurso**: Caso ocorra erro ao taguear uma VM específica (como zona incorreta ou falta de permissão), o script registra a falha no relatório final e segue para a próxima máquina sem abortar o lote.
- **Sem Dependências Externas**: Utiliza apenas módulos nativos do Python (`csv`, `subprocess`, `sys`), dispensando instalações complexas ou configurações de bibliotecas externas adicionais.
- **Relatório Final Consolidado**: Exibe um sumário detalhado ao término da execução separando o que foi concluído com sucesso e o que falhou (junto com o respectivo erro retornado pelo console).

## 📦 Pré-requisitos

1. **Python 3.6+** instalado.
2. **Google Cloud CLI (gcloud)** instalado, configurado e autenticado na sua máquina.
   - Para verificar se o `gcloud` está disponível, execute:
     ```bash
     gcloud --version
     ```
   - Lembre-se de apontar o terminal para o projeto desejado antes de rodar o script:
     ```bash
     gcloud config set project SEU-PROJETO-ID
     ```

## 🛠️ Instalação

1. Clone o repositório da organização:
```bash
git clone https://github.com/KenzoaokiTbxtech/Script-PythonLabelsVms.git
cd Script-PythonLabelsVms
```

2. Crie e ative seu ambiente virtual (boa prática):

```bash
python -m venv .venv
# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate
```

## 📄 Formato do Arquivo CSV

O arquivo `vms.csv` deve estar localizado na raiz do projeto e seguir estritamente o layout de cabeçalho abaixo:

```csv
Nome do recurso,Zona,Team,Cost Center,Country
instance-20260715-114244,us-central1-a,Infraestrutura,TI 123,Brasil
vm-ficticia-para-forçar-erro,us-east1-b,Dados,Finanças,EUA
```

### Regras de Mapeamento:

* **`Nome do recurso`**: ID/Nome exato da instância de VM na GCP.
* **`Zona`**: Zona onde a instância se encontra (ex: `us-central1-a`).
* As colunas **`Team`**, **`Cost Center`** e **`Country`** serão transformadas respectivamente nas chaves de labels `team`, `cost_center` e `country` de forma padronizada.

## 📖 Como Usar

Com o terminal autenticado no projeto da GCP e o arquivo `vms.csv` preenchido, execute o script:

```bash
python main.py
```

## 📊 Exemplo de Output no Terminal

```text
-------- Iniciando Atualização de Labels em VMs (Compute Engine) --------
Aplicando labels na VM: instance-20260715-114244 (Zona: us-central1-a)...
   ✅ Sucesso ao taguear a VM instance-20260715-114244!
Aplicando labels na VM: vm-ficticia-para-forçar-erro (Zona: us-east1-b)...
   ⚠️ Erro do gcloud na VM vm-ficticia-para-forçar-erro: ERROR: (gcloud.compute.instances.add-labels) Instance [vm-ficticia-para-forçar-erro] was not found in [us-east1-b].

-------- Relatório Final de Status (VMs) --------
Sucessos: 1
 [OK] VM: instance-20260715-114244 | Zona: us-central1-a -> Labels aplicadas.
Falhas: 1
 [ERRO] VM: vm-ficticia-para-forçar-erro | Zona: us-east1-b -> Falha: ERROR: (gcloud.compute.instances.add-labels) Instance [vm-ficticia-para-forçar-erro] was not found in [us-east1-b].
```

## 🛡️ Tratamento de Erros Comuns

* **`WinError 2 (O sistema não conseguiu localizar o ficheiro especificado)`**: O script executa o `gcloud` de forma nativa através do terminal (`shell=True`). Certifique-se de que o Google Cloud CLI está instalado e configurado nas Variáveis de Ambiente (`PATH`) do seu sistema operacional.
* **`Falha: Instance [...] was not found`**: O nome do recurso no CSV não existe ou a coluna `Zona` está indicando uma zona diferente daquela em que a VM foi criada.
