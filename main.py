import csv
import subprocess
import sys

planilha_vms = 'vms.csv'

def read_csv_vms(caminho_arquivo):
    data = []
    try:
        with open(caminho_arquivo, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row_limpa = {k.strip(): v.strip() for k, v in row.items() if k is not None}
                data.append(row_limpa)
        return data
    except FileNotFoundError:
        print(f"❌ Erro: O arquivo '{caminho_arquivo}' não foi encontrado na raiz.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado ao ler o CSV: {e}")
        sys.exit(1)

def sanitizar_label(valor):
    return str(valor).strip().lower().replace(" ", "-").replace(":", "-")

def executar_tagueamento_vms():
    dados_vms = read_csv_vms(planilha_vms)
    
    print("\n-------- Iniciando Atualização de Labels em VMs (Compute Engine) --------")
    
    sucessos = []
    falhas = []

    for linha in dados_vms:
        nome_vm = linha.get('Nome do recurso')
        zona = linha.get('Zona')
        team = linha.get('Team')
        cost_center = linha.get('Cost Center')
        country = linha.get('Country')

        if not nome_vm or not zona:
            print(f"⚠️ Ignorando linha inválida no CSV (Nome ou Zona ausentes).")
            continue

        label_team = sanitizar_label(team)
        label_cost_center = sanitizar_label(cost_center)
        label_country = sanitizar_label(country)

        string_labels = f"team={label_team},cost_center={label_cost_center},country={label_country}"

        print(f"Aplicando labels na VM: {nome_vm} (Zona: {zona})...")

        comando_gcloud = [
            "gcloud", "compute", "instances", "add-labels", nome_vm,
            f"--zone={zona}",
            f"--labels={string_labels}"
        ]

        try:
            resultado = subprocess.run(comando_gcloud, capture_output=True, text=True, check=True, shell=True)
            
            print(f"   ✅ Sucesso ao taguear a VM {nome_vm}!")
            sucessos.append(f"VM: {nome_vm} | Zona: {zona} -> Labels aplicadas.")

        except subprocess.CalledProcessError as erro_gcloud:
            print(f"   ⚠️ Erro do gcloud na VM {nome_vm}: {erro_gcloud.stderr.strip()}")
            falhas.append(f"VM: {nome_vm} | Zona: {zona} -> Falha: {erro_gcloud.stderr.strip()}")
            continue
            
        except Exception as erro_inesperado:
            print(f"   ⚠️ Erro inesperado na VM {nome_vm}: {erro_inesperado}")
            falhas.append(f"VM: {nome_vm} | Zona: {zona} -> Falha: {erro_inesperado}")
            continue

    print("\n-------- Relatório Final de Status (VMs) --------")
    print(f"Sucessos: {len(sucessos)}")
    for s in sucessos:
        print(f" [OK] {s}")
        
    print(f"Falhas: {len(falhas)}")
    for f in falhas:
        print(f" [ERRO] {f}")

if __name__ == "__main__":
    executar_tagueamento_vms()