<div align="center">

```
  /$$$$$$                         /$$   /$$  /$$$$$$  
 /$$__  $$                       | $$  / $$ /$$__  $$ 
| $$  \__/  /$$$$$$  /$$$$$$/$$$$ \  $$/ $$/$$  \__/  
|  $$$$$$  |____  $$| $$_  $$_  $$ \  $$$$/| $$  /$$$$
 \____  $$  /$$$$$$$| $$ \ $$ \ $$  >$$  $$| $$  \__/ 
 /$$  \ $$ /$$__  $$| $$ | $$ | $$ /$$/\  $$\  $$  $$ 
|  $$$$$$/|  $$$$$$$| $$ | $$ | $$| $$  \ $$ \  $$$$/ 
 \______/  \_______/|__/ |__/ |__/|__/  |__/  \____/  
```

### `Subdomain Enumeration & OSINT Tool`

<br>

![Python](https://img.shields.io/badge/Python-3.10%2B-red?style=for-the-badge&logo=python&logoColor=white&labelColor=black)
![Status](https://img.shields.io/badge/Status-Active-red?style=for-the-badge&logoColor=white&labelColor=black)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge&labelColor=black)
![Threads](https://img.shields.io/badge/Threads-500%2B-red?style=for-the-badge&labelColor=black)
![Sources](https://img.shields.io/badge/OSINT_Sources-8-red?style=for-the-badge&labelColor=black)

<br>

> **Ferramenta profissional de enumeração de subdomínios** com 8 fontes OSINT passivas,  
> bruteforce DNS multithreaded, menu interativo para iniciantes e UI de terminal polida.  
> **Feito por [! Vini](https://github.com/yourusername)**

<br>

</div>

---

## ◈ Índice

- [Funcionalidades](#-funcionalidades)
- [Instalação](#-instalação)
- [Menu Interativo](#-menu-interativo)
- [Uso via CLI](#-uso-via-linha-de-comando)
- [Wordlists](#-gerenciador-de-wordlists)
- [Todas as opções](#-todas-as-opções)
- [Saída de exemplo](#-exemplo-de-saída)
- [Sistema de logs](#-sistema-de-logs)
- [Aviso legal](#-aviso-legal)

---

## ◈ Funcionalidades

<table>
<tr>
<td width="50%">

**🔍 OSINT & Recon**
- `crt.sh` — certificados SSL/TLS
- `HackerTarget` — DNS passivo
- `AlienVault OTX` — threat intelligence
- `RapidDNS` — banco de DNS público
- `URLScan.io` — páginas escaneadas
- `ThreatMiner` — threat intelligence
- `Wayback Machine` — arquivo histórico
- `DuckDuckGo Dork` — busca via dork
- `VirusTotal` — com API key

</td>
<td width="50%">

**⚙️ Engine & Performance**
- Bruteforce DNS multithreaded (até 500+ threads)
- Detecção automática de wildcard DNS
- Zone Transfer (AXFR) nos nameservers
- Resolução de IP paralela de todos os resultados
- Cache de wordlists por SHA256 (sem downloads repetidos)
- Wordlists de até **3 milhões** de entradas
- Exportação em `.txt` e `.json`
- Menu interativo com **glossário para iniciantes**

</td>
</tr>
</table>

---

## ◈ Instalação

```bash
git clone https://github.com/yourusername/sam-xd.git
cd sam-xd
pip install -r requirements.txt
```

<details>
<summary><b>📦 Dependências</b></summary>
<br>

| Pacote | Para que serve | Obrigatório? |
|--------|----------------|:------------:|
| `requests` | Requisições HTTP para as fontes OSINT | Recomendado |
| `dnspython` | Resolução DNS rápida + zone transfer | Recomendado |

> Ambos são opcionais. A ferramenta usa `urllib` e `socket` como fallback, mas instale-os para melhor performance e precisão.

```bash
pip install requests dnspython
```

</details>

---

## ◈ Menu Interativo

Roda sem argumentos e abre o menu — **ideal para quem está começando:**

```bash
python sd_finder.py
```

```
  ════════════════════════════════════════════════════════════════════════
  MENU PRINCIPAL
  ────────────────────────────────────────────────────────────────────────

  [1] ⚡  Scan Rápido          crt.sh + HackerTarget — ideal para começar
  [2] 🔬  Scan Avançado        configure tudo manualmente
  [3] 🔁  Zone Transfer (AXFR) tenta obter todos os registros DNS
  [4] 📦  Gerenciar Wordlists  baixar, listar e checar cache
  [5] 📖  Glossário            o que significa cada termo?
  [6] ℹ️   Sobre / Uso ético   créditos e avisos legais
  [0] 🚪  Sair

  ▶ Escolha uma opção:
```

<details>
<summary><b>📋 O que cada opção faz</b></summary>
<br>

| Opção | O que faz |
|-------|-----------|
| `[1] Scan Rápido` | Só pede o domínio e já roda com crt.sh + HackerTarget — zero configuração |
| `[2] Scan Avançado` | Configura fontes, bruteforce, threads, formato de saída passo a passo |
| `[3] Zone Transfer` | Tenta AXFR em todos os nameservers do domínio alvo |
| `[4] Wordlists` | Submenu para baixar, listar e atualizar as wordlists em cache |
| `[5] Glossário` | Explica Subdomínio, DNS, OSINT, Wildcard, Bruteforce, Thread e mais |
| `[6] Sobre` | Créditos, aviso de uso ético e exemplos de linha de comando |

</details>

---

## ◈ Uso via Linha de Comando

<details>
<summary><b>⚡ Scan rápido</b></summary>

```bash
# Padrão — usa crt.sh + HackerTarget
python sd_finder.py -d example.com
```

</details>

<details>
<summary><b>🌐 Todas as fontes OSINT</b></summary>

```bash
python sd_finder.py -d example.com --all-sources
```

</details>

<details>
<summary><b>💥 Todas as fontes + Bruteforce</b></summary>

```bash
# Wordlist média, 50 threads
python sd_finder.py -d example.com --all-sources --brute --wordlist medium -t 50

# Wordlist grande, 100 threads, exportar como JSON
python sd_finder.py -d example.com --brute --wordlist large -t 100 -o resultado.json --output-format json
```

</details>

<details>
<summary><b>🔁 Zone Transfer</b></summary>

```bash
python sd_finder.py -d example.com --zone-transfer --all-sources
```

</details>

<details>
<summary><b>📁 Wordlist local + VirusTotal</b></summary>

```bash
# Usar wordlist própria
python sd_finder.py -d example.com --brute --wordlist /caminho/para/lista.txt

# Com API key do VirusTotal
python sd_finder.py -d example.com --all-sources --vt-key SUA_CHAVE_AQUI
```

</details>

---

## ◈ Gerenciador de Wordlists

```bash
# Listar wordlists disponíveis e status de cache
python sd_finder.py --list-wordlists

# Baixar uma ou mais wordlists
python sd_finder.py --download-wordlist mini medium large

# Forçar re-download mesmo se já em cache
python sd_finder.py --download-wordlist large --force-download
```

```
  NAME          DESCRIPTION                                SIZE      STATUS
  ──────────────────────────────────────────────────────────────────────────
  mini          Top 5,000  subdomains  (SecLists)          ~50 KB    ✔ cached
  medium        Top 20,000 subdomains  (SecLists)          ~190 KB   ✗ not cached
  large         Top 110k   subdomains  (SecLists)          ~1 MB     ✗ not cached
  dns-bitquark  Bitquark 100k  DNS  wordlist               ~900 KB   ✗ not cached
  assetnote-2m  Assetnote best DNS wordlist (~2M)          ~15 MB    ✗ not cached
  n0kovo-3m     n0kovo 3M — harvested from IPv4 SSL certs  ~26 MB    ✗ not cached
```

> Wordlists ficam em cache em `~/.sd_finder/wordlists/` e **nunca são baixadas novamente** a não ser que você force com `--force-download`.

---

## ◈ Todas as Opções

```
Gerais:
  -d, --domain DOMAIN         Domínio alvo (ex: example.com)
  -o, --output FILE           Arquivo de saída (auto-nomeado se omitido)
  --output-format {txt,json}  Formato de saída (padrão: txt)
  --menu                      Forçar abertura do menu interativo

Fontes OSINT:
  --all-sources               Ativar todas as fontes OSINT passivas
  --crtsh                     crt.sh — certificados SSL
  --hackertarget              HackerTarget — DNS passivo
  --alienvault                AlienVault OTX
  --rapiddns                  RapidDNS
  --urlscan                   URLScan.io
  --threatminer               ThreatMiner
  --wayback                   Wayback Machine CDX API
  --dork                      DuckDuckGo dork
  --vt-key KEY                API key do VirusTotal

Bruteforce:
  --brute                     Ativar bruteforce DNS
  --wordlist NAME_OR_PATH     Nome da wordlist ou caminho para arquivo local
  --download-wordlist NAME    Baixar wordlist(s) e sair
  --force-download            Re-baixar mesmo se já em cache
  --wildcard-check            Detectar wildcard DNS antes do bruteforce (padrão: ativo)

Performance:
  -t, --threads N             Número de threads (padrão: 30, máx recomendado: 200)
  --no-resolve                Pular resolução final de IPs

Misc:
  --list-wordlists            Listar wordlists disponíveis e sair
  --zone-transfer             Tentar zone transfer (AXFR) nos nameservers
  --no-banner                 Pular o banner ASCII
  --no-color                  Desativar cores ANSI (útil para pipar output)
  -v, --verbose               Saída detalhada / debug
```

---

## ◈ Exemplo de Saída

```
  ┌────────────────────────────────────────────────┐
  │  Targeting: example.com                        │
  └────────────────────────────────────────────────┘

  19:48:01 [*] Querying certificate transparency logs...
  19:48:02 [+] api.example.com → 93.184.216.34 [crt.sh]
  19:48:02 [+] mail.example.com → 198.51.100.2 [crt.sh]
  19:48:03 [+] dev.example.com → 192.0.2.1 [HackerTarget]
  19:48:04 [*] Starting bruteforce: 5,000 words, 50 threads...
    [████████████████░░░░░░░░░░░░░░]  54.2%  2,710/5,000

  ┌──────────────────────────────────┐
  │  Resultados  (47 subdomínios)    │
  └──────────────────────────────────┘

  Subdomínios Ativos  (42)
  ──────────────────────────────────────────────────────────────
  ▸ api.example.com                              93.184.216.34
  ▸ blog.example.com                             93.184.216.34
  ▸ dev.example.com                              192.0.2.1
  ▸ mail.example.com                             198.51.100.2

  ┌──────────────────────┐
  │  Scan Summary        │
  └──────────────────────┘

  Target         : example.com
  Elapsed        : 18.42s
  Total Found    : 47
  Live (A record): 42

  Per-Source Breakdown:
  crt.sh                 ████████████████████████████████████████ 31
  HackerTarget           ████████████████████ 18
  AlienVault             ████████████ 12
  Bruteforce             ████████████████ 14
```

---

## ◈ Sistema de Logs

| Prefixo | Cor | Significado |
|---------|-----|-------------|
| `[*]` | Ciano | Informação / operação em andamento |
| `[+]` | Verde | Sucesso / subdomínio encontrado |
| `[!]` | Amarelo | Aviso importante |
| `[-]` | Vermelho | Erro ou falha |
| `[?]` | Magenta | Pergunta ao usuário |
| `[~]` | Cinza | Debug (apenas com `--verbose`) |

---

## ◈ Aviso Legal

> [!WARNING]
> Esta ferramenta é destinada **exclusivamente para testes de segurança autorizados e fins educacionais**.  
> Sempre obtenha **permissão por escrito** antes de escanear qualquer domínio que não seja seu.  
> O uso não autorizado pode configurar crime. O autor não se responsabiliza por qualquer uso indevido.

---

<div align="center">

Feito com 💻 por **! Vini**

![visitors](https://img.shields.io/badge/Happy-Hacking-red?style=for-the-badge&labelColor=black)

</div>
