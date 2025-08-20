# Atento ServiceDesk

![Python](https://img.shields.io/badge/python-3.x-blue)
![License](https://img.shields.io/badge/license-MIT-green)

O **Atento ServiceDesk** é um launcher desenvolvido para agilizar o atendimento técnico dos analistas, automatizando scripts de manutenção, rede e VPN, otimizando o TMA e padronizando procedimentos.  

---

## 🎬 Demonstração da Interface

![Interface do Atento ServiceDesk](docs/interface_screenshot.png)  

> Tela principal do launcher com botões para scripts e manutenção.

![Exemplo de execução de script](docs/script_execution.gif)  

> Demonstração de execução automática de um script de limpeza de temporários.

---

## 📌 Índice

- [Sobre o Projeto](#sobre-o-projeto)  
- [Funcionalidades](#funcionalidades)  
- [Instalação](#instalação)  
- [Uso](#uso)  
- [Arquitetura Técnica](#arquitetura-técnica)  
- [Contribuições](#contribuições)  
- [Licença](#licença)  

---

## 📝 Sobre o Projeto

O **Atento ServiceDesk** centraliza scripts administrativos e de manutenção em uma interface gráfica intuitiva, permitindo executar rotinas críticas de forma automatizada e segura.  

O launcher é modular, permitindo a inclusão de novos scripts e funcionalidades conforme novas demandas surgirem.

---

## ⚙ Funcionalidades

| Botão | Ação Executada | Lógica Técnica |
|-------|----------------|----------------|
| **Restaurar Rede** | Libera e renova IP, limpa DNS e reconfigura adaptadores. | Executa `ipconfig /release`, `renew`, `flushdns` e PowerShell para reiniciar adaptadores. |
| **Teste de Bloqueio de Porta** | Verifica portas da VPN Vivo e Mercado Livre. | Usa `socket.create_connection()` para testar portas 20471 e 20445, retornando "Aberta" ou "Bloqueada". |
| **Desinstalar FortClient VPN** | Remove FortClient VPN, se instalado. | Executa `wmic product where name="FortClient VPN" call uninstall` e retorna mensagens de sucesso/falha. |
| **Limpeza de Máquina** | Limpa arquivos temporários e logs. | Executa script `limpa_temporarios.bat` embutido no instalador. |
| **PowerShell** | Abre terminal PowerShell interativo. | `subprocess.Popen("start powershell.exe -NoExit")`. |
| **Corrige Next** | Corrige erros do sistema Next, apagando caches corrompidos. | Remove pastas **JX Browser** e **Sun** em `%LOCALAPPDATA%`, `%APPDATA%` e `LocalLow`. |
| **Sincronizar Data e Hora** | Sincroniza o relógio do sistema com servidor interno. | `net time /set \\CABRTSADC02.clienteap.br /yes` ou `w32tm /resync` como fallback. |
| **Gerenciador de Tarefas** | Abre o Task Manager do Windows. | `subprocess.Popen("taskmgr.exe")`. |

---

## 💻 Instalação

1. Clone o repositório:  
```bash
git clone https://github.com/luucM/AtentoServiceDesk.git
