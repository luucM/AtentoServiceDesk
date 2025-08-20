import subprocess
import ctypes
import os
import sys
import socket
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image  # customtkinter usa PIL para CTkImage

# ---------- Função para localizar recursos (ícones, REGs, BATs) ----------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ---------- Verifica se está com privilégios de admin ----------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# ---------- Funções do launcher ----------
def restaurar_rede():
    subprocess.run("ipconfig /release", shell=True)
    subprocess.run("ipconfig /renew", shell=True)
    subprocess.run("ipconfig /flushdns", shell=True)

    comando_powershell = """
    Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } |
    ForEach-Object {
        Disable-NetAdapter -Name $_.Name -Confirm:$false;
        Start-Sleep -Seconds 3;
        Enable-NetAdapter -Name $_.Name -Confirm:$false
    }
    """
    subprocess.run(["powershell", "-Command", comando_powershell], shell=True)

def configurar_dns_automatico():
    comando_powershell = """
    Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } |
    ForEach-Object {
        Set-DnsClientServerAddress -InterfaceAlias $_.Name -ResetServerAddresses
    }
    """
    subprocess.run(["powershell", "-Command", comando_powershell], shell=True)

def desativar_teredo_ipv6_hyperv():
    subprocess.run(["powershell", "-Command", "Get-NetAdapter -Name 'vEthernet*' | Disable-NetAdapter -Confirm:$false"], shell=True)
    subprocess.run(["powershell", "-Command", "Get-NetAdapter | ForEach-Object { Disable-NetAdapterBinding -Name $_.Name -ComponentID ms_tcpip6 }"], shell=True)
    subprocess.run("bcdedit /set hypervisorlaunchtype off", shell=True)
    subprocess.run("netsh interface teredo set state disabled", shell=True)

def importar_reg(nome_arquivo_reg):
    pasta_regs = resource_path("regs")  # pega a pasta regs do EXE
    caminho_reg = os.path.join(pasta_regs, nome_arquivo_reg)
    if os.path.exists(caminho_reg):
        subprocess.run(["regedit.exe", "/s", caminho_reg], shell=True)
    else:
        messagebox.showerror("Erro", f"Arquivo {nome_arquivo_reg} não encontrado.")

def desinstalar_vpn():
    resposta = messagebox.askyesno("Confirmação", "Deseja desinstalar o FortClient VPN?")
    if not resposta:
        return
    try:
        resultado = subprocess.run(
            'wmic product where name="FortClient VPN" call uninstall',
            shell=True, capture_output=True, text=True
        )
        if "ReturnValue = 0" in resultado.stdout:
            messagebox.showinfo("Sucesso", "FortClient VPN desinstalado com sucesso.")
        elif "No instance(s) Available" in resultado.stdout:
            messagebox.showwarning("Não encontrado", "FortClient VPN não está instalado")
        else:
            messagebox.showerror("Erro", f"Falha ao desinstalar. \nSaída:\n{resultado.stdout}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao tentar desinstalar: {e}")

def limpeza_temporarios():
    resposta = messagebox.askyesno("Confirmação", "Deseja executar a limpeza de arquivos temporários?")
    if not resposta:
        return
    try:
        # Ajuste: usar resource_path para localizar o .bat no exe
        bat_path = resource_path("limpa_temporarios.bat")
        resultado = subprocess.run(
            bat_path,
            shell=True, capture_output=True, text=True
        )
        if resultado.returncode == 0:
            messagebox.showinfo("Sucesso", "Limpeza de temporários concluída.")
        else:
            messagebox.showwarning("Aviso", f"Limpeza executada com avisos. \n\nSaída:\n{resultado.stdout}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao executar limpeza.\n\n{e}")


def executar_powershell():
    subprocess.Popen("start powershell.exe -NoExit", shell=True)

# ---------- Data e Hora ----------
def data_e_hora():
    comando1 = r'net time /set \\CABRTSADC02.clienteap.br /yes'
    comando2 = 'w32tm /resync'
    try:
        resultado = subprocess.run(comando1, shell=True, capture_output=True, text=True)
        if resultado.returncode == 0:
            messagebox.showinfo("Sucesso", "Horário sincronizado com sucesso no CABRTSADC02.")
        else:
            erro1 = (resultado.stderr or "").lower()
            if "não encontrado" in erro1 or "not found" in erro1:
                resultado2 = subprocess.run(comando2, shell=True, capture_output=True, text=True)
                if resultado2.returncode == 0:
                    messagebox.showinfo("Sucesso", "Horário sincronizado com w32tm /resync.")
                else:
                    messagebox.showerror("Erro", f"Falha no segundo comando:\n{resultado2.stderr}")
            else:
                messagebox.showerror("Erro", f"Falha ao sincronizar horário:\n{resultado.stderr}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

# ---------- VPN ----------
def testar_porta(host, port, timeout=5):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except:
        return False

def verificar_vpn():
    vivo_status = "Aberta" if testar_porta("vpnvivossl.atento.com.br", 20471) else "Bloqueada"
    ml_status = "Aberta" if testar_porta("vpnmercalivrem.atento.com.br", 20445) else "Bloqueada"
    mensagem = f"Porta Vivo: {vivo_status}\nPorta Mercado Livre: {ml_status}"
    messagebox.showinfo("Status VPN", mensagem)

def gerenciador_de_tarefas():
    try:
        subprocess.Popen("taskmgr.exe", shell=True)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível abrir o Gerenciador de Tarefas:\n{e}")

# ---------- Corrige Next ----------
def corrige_next():
    try:
        jx_path = os.path.join(os.environ["LOCALAPPDATA"], "JX Browser*")
        subprocess.run(f'for /d %I in ("{jx_path}") do rmdir /s /q "%I"', shell=True)
        sun_local = os.path.join(os.environ["LOCALAPPDATA"], "Sun")
        subprocess.run(f'rmdir /s /q "{sun_local}"', shell=True)
        sun_locallow = os.path.join(os.environ["USERPROFILE"], r"AppData\\LocalLow\\Sun")
        subprocess.run(f'rmdir /s /q "{sun_locallow}"', shell=True)
        sun_roaming = os.path.join(os.environ["APPDATA"], "Sun")
        subprocess.run(f'rmdir /s /q "{sun_roaming}"', shell=True)
        messagebox.showinfo("Sucesso", "Cache do JX Browser e Sun limpo com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# ---------- Script Rede Completo ----------
def executar_script_rede():
    pasta_regs = resource_path("regs")
    if not os.path.exists(pasta_regs):
        messagebox.showerror("Erro", "Pasta de REGs não encontrada.")
        return
    try:
        restaurar_rede()
        configurar_dns_automatico()
        desativar_teredo_ipv6_hyperv()
        importar_reg("atentobr_tls.reg")
        importar_reg("clienteap_tls.reg")
        messagebox.showinfo("Sucesso", "Rede restaurada com sucesso.\nReinicie o PC para aplicar tudo.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# ---------- Interface ----------
def criar_interface():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    root.title("Atento ServiceDesk")
    root.geometry("500x490")
    root.resizable(False, False)

    icon_path = resource_path("icone.ico")
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(default=icon_path)
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")

    root.configure(fg_color="#121212")
    container = ctk.CTkFrame(root, fg_color="#121212", border_width=0)
    container.pack(padx=20, pady=20, fill="both", expand=True)

    titulo = ctk.CTkLabel(container, text="Atento ServiceDesk", font=ctk.CTkFont(size=26, weight="bold"), text_color="white")
    titulo.pack(pady=(0, 30))

    # Ícones
    icones = {name: ctk.CTkImage(light_image=Image.open(resource_path(f"icones/{name}.png")), size=(24,24))
              for name in ["rede", "bloqueio", "desinstalar", "limpeza", "terminal", "data", "next", "tarefas"]}

    # Botões
    ctk.CTkButton(container, text="Restaurar Rede", image=icones["rede"], compound="left", command=executar_script_rede, corner_radius=12, font=ctk.CTkFont(size=15)).pack(fill="x", pady=8)
    ctk.CTkButton(container, text="Teste de Bloqueio de Porta", image=icones["bloqueio"], compound="left", command=verificar_vpn, corner_radius=12, font=ctk.CTkFont(size=15)).pack(fill="x", pady=8)
    ctk.CTkButton(container, text="Desinstalar FortClient VPN", image=icones["desinstalar"], compound="left", command=desinstalar_vpn, corner_radius=12, font=ctk.CTkFont(size=15)).pack(fill="x", pady=8)
    ctk.CTkButton(container, text="Limpeza de Máquina", image=icones["limpeza"], compound="left", command=limpeza_temporarios, corner_radius=12, font=ctk.CTkFont(size=15)).pack(fill="x", pady=8)
    ctk.CTkButton(container, text="PowerShell", image=icones["terminal"], compound="left", command=executar_powershell, corner_radius=12, font=ctk.CTkFont(size=15)).pack(fill="x", pady=8)
    ctk.CTkButton(container, text="Corrige Next", image=icones["next"], compound="left", command=corrige_next, corner_radius=12, font=ctk.CTkFont(size=15)).pack(fill="x", pady=8)
    ctk.CTkButton(container, text="Sincronizar Data e Hora", image=icones["data"], compound="left", command=data_e_hora, corner_radius=12, font=ctk.CTkFont(size=15)).pack(fill="x", pady=8)
    ctk.CTkButton(container, text="Gerenciador de Tarefas", image=icones["tarefas"], compound="left", command=gerenciador_de_tarefas, corner_radius=12, font=ctk.CTkFont(size=15)).pack(fill="x", pady=8)
    
    root.mainloop()

# ---------- Execução ----------
if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, None, None, 1)
    else:
        criar_interface()
