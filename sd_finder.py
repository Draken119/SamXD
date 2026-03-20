#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sam XD — Subdomain Enumeration & OSINT Tool
Author: ! Vini
"""

import os
import sys
import json
import time
import socket
import hashlib
import argparse
import threading
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# ─── Optional deps (graceful fallback) ──────────────────────────────────────
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import dns.resolver
    import dns.query
    import dns.zone
    import dns.exception
    HAS_DNSPYTHON = True
except ImportError:
    HAS_DNSPYTHON = False


# ╔══════════════════════════════════════════════════════════════════╗
# ║                        ANSI COLOR PALETTE                       ║
# ╚══════════════════════════════════════════════════════════════════╝
class C:
    RESET        = "\033[0m"
    BOLD         = "\033[1m"
    DIM          = "\033[2m"
    WHITE        = "\033[97m"
    LIGHT_GREY   = "\033[37m"
    DARK_GREY    = "\033[90m"
    GREEN        = "\033[92m"
    DARK_GREEN   = "\033[32m"
    RED          = "\033[91m"
    DARK_RED     = "\033[31m"
    YELLOW       = "\033[93m"
    ORANGE       = "\033[33m"
    CYAN         = "\033[96m"
    DARK_CYAN    = "\033[36m"
    BLUE         = "\033[94m"
    DARK_BLUE    = "\033[34m"
    MAGENTA      = "\033[95m"
    DARK_MAGENTA = "\033[35m"
    BG_RED       = "\033[41m"
    BG_GREEN     = "\033[42m"
    BG_DARK      = "\033[40m"

    @staticmethod
    def disable():
        for attr in [a for a in dir(C) if not a.startswith('_') and isinstance(getattr(C, a), str)]:
            setattr(C, attr, "")


# ╔══════════════════════════════════════════════════════════════════╗
# ║                       LOG / PRINT HELPERS                       ║
# ╚══════════════════════════════════════════════════════════════════╝
_print_lock = threading.Lock()

def _ts() -> str:
    # LIGHT_GREY ao invés de DARK_GREY para o timestamp — legível em fundo escuro e claro
    return f"{C.LIGHT_GREY}{datetime.now().strftime('%H:%M:%S')}{C.RESET}"

def log_info(msg: str):
    with _print_lock:
        print(f"{_ts()} {C.CYAN}{C.BOLD}[*]{C.RESET} {C.WHITE}{msg}{C.RESET}")

def log_ok(msg: str):
    with _print_lock:
        print(f"{_ts()} {C.GREEN}{C.BOLD}[+]{C.RESET} {C.GREEN}{msg}{C.RESET}")

def log_found(subdomain: str, ip: str = "", source: str = ""):
    # LIGHT_GREY para a tag de fonte e CYAN (bright) para o IP — ambos legíveis
    src_tag = f" {C.LIGHT_GREY}[{source}]{C.RESET}" if source else ""
    ip_tag  = f" {C.CYAN}→ {ip}{C.RESET}" if ip else ""
    with _print_lock:
        print(f"{_ts()} {C.GREEN}{C.BOLD}[+]{C.RESET} {C.BOLD}{C.GREEN}{subdomain}{C.RESET}{ip_tag}{src_tag}")

def log_warn(msg: str):
    with _print_lock:
        print(f"{_ts()} {C.YELLOW}{C.BOLD}[!]{C.RESET} {C.YELLOW}{msg}{C.RESET}")

def log_error(msg: str):
    with _print_lock:
        print(f"{_ts()} {C.RED}{C.BOLD}[-]{C.RESET} {C.RED}{msg}{C.RESET}")

def log_question(msg: str):
    with _print_lock:
        print(f"{_ts()} {C.MAGENTA}{C.BOLD}[?]{C.RESET} {C.MAGENTA}{msg}{C.RESET}")

def log_section(title: str):
    bar = "─" * (len(title) + 4)
    with _print_lock:
        print(f"\n{C.CYAN}┌{bar}┐{C.RESET}")
        print(f"{C.CYAN}│{C.RESET}  {C.BOLD}{C.CYAN}{title}{C.RESET}  {C.CYAN}│{C.RESET}")
        print(f"{C.CYAN}└{bar}┘{C.RESET}\n")

def log_debug(msg: str, verbose=False):
    if verbose:
        with _print_lock:
            print(f"{_ts()} {C.LIGHT_GREY}[~] {msg}{C.RESET}")

def progress_bar(current: int, total: int, width: int = 30, label: str = "") -> str:
    if total == 0:
        return ""
    pct  = current / total
    done = int(pct * width)
    bar  = f"{C.GREEN}{'█' * done}{C.LIGHT_GREY}{'░' * (width - done)}{C.RESET}"
    return f"\r  {C.LIGHT_GREY}[{C.RESET}{bar}{C.LIGHT_GREY}]{C.RESET} {C.YELLOW}{pct*100:5.1f}%{C.RESET} {C.LIGHT_GREY}{label}{C.RESET}   "


# ╔══════════════════════════════════════════════════════════════════╗
# ║                    BANNER  (Sam XD — Big Money-nw)              ║
# ╚══════════════════════════════════════════════════════════════════╝
def print_banner():
    """
    'Sam XD' rendered in Big Money-nw style.
    $  → RED      /|\\_  → DARK_RED
    """
    R  = C.RED
    DR = C.DARK_RED
    W  = C.WHITE
    B  = C.CYAN
    X  = C.RESET

    # "Sam XD" in Big Money-nw
    raw_banner = [
        r"  /$$$$$$                         /$$   /$$  /$$$$$$  ",
        r" /$$__  $$                       | $$  / $$ /$$__  $$ ",
        r"| $$  \__/  /$$$$$$  /$$$$$$/$$$$ \  $$/ $$/$$  \__/  ",
        r"|  $$$$$$  |____  $$| $$_  $$_  $$ \  $$$$/| $$  /$$$$ ",
        r" \____  $$  /$$$$$$$| $$ \ $$ \ $$  >$$  $$| $$  \__/ ",
        r" /$$  \ $$ /$$__  $$| $$ | $$ | $$ /$$/\  $$\  $$  $$ ",
        r"|  $$$$$$/|  $$$$$$$| $$ | $$ | $$| $$  \ $$ \  $$$$/ ",
        r" \______/  \_______/|__/ |__/ |__/|__/  |__/  \____/  ",
    ]

    def colorize(line: str) -> str:
        out = ""
        for ch in line:
            if ch == "$":
                out += f"{R}{ch}{X}"
            elif ch in r"/|\_":
                out += f"{DR}{ch}{X}"
            elif ch == "-":
                out += f"{DR}{ch}{X}"
            elif ch in "{}[]()":
                out += f"{B}{ch}{X}"
            else:
                out += f"{W}{ch}{X}"
        return out

    print()
    for line in raw_banner:
        print("  " + colorize(line))

    tag_left  = f"{C.LIGHT_GREY}{'─' * 22}{C.RESET}"
    tag_right = f"{C.LIGHT_GREY}{'─' * 22}{C.RESET}"
    tag_mid   = f"{C.CYAN}{C.BOLD} Subdomain Enumeration & OSINT Tool {C.RESET}"
    print(f"\n  {tag_left}{tag_mid}{tag_right}")

    meta_parts = [
        f"{C.LIGHT_GREY}Author:{C.RESET} {C.MAGENTA}{C.BOLD}! Vini{C.RESET}",
        f"{C.LIGHT_GREY}Version:{C.RESET} {C.YELLOW}1.1.0{C.RESET}",
        f"{C.LIGHT_GREY}Mode:{C.RESET} {C.CYAN}OSINT + Bruteforce + DNS{C.RESET}",
    ]
    print("  " + f"  {C.LIGHT_GREY}|{C.RESET}  ".join(meta_parts))
    print(f"  {C.LIGHT_GREY}{'─' * 80}{C.RESET}\n")


# ╔══════════════════════════════════════════════════════════════════╗
# ║                     WORDLIST MANAGER                            ║
# ╚══════════════════════════════════════════════════════════════════╝
WORDLIST_CATALOG = {
    "mini": {
        "url":  "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt",
        "desc": "Top 5,000  subdomains  (SecLists)",
        "size": "~50 KB",
    },
    "medium": {
        "url":  "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-20000.txt",
        "desc": "Top 20,000 subdomains  (SecLists)",
        "size": "~190 KB",
    },
    "large": {
        "url":  "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-110000.txt",
        "desc": "Top 110k   subdomains  (SecLists)",
        "size": "~1 MB",
    },
    "dns-bitquark": {
        "url":  "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/bitquark-subdomains-top100000.txt",
        "desc": "Bitquark 100k  DNS  wordlist",
        "size": "~900 KB",
    },
    "assetnote-2m": {
        "url":  "https://wordlists-cdn.assetnote.io/data/manual/best-dns-wordlist.txt",
        "desc": "Assetnote best DNS wordlist (~2M)",
        "size": "~15 MB",
    },
    "n0kovo-3m": {
        "url":  "https://raw.githubusercontent.com/n0kovo/n0kovo_subdomains/main/n0kovo_subdomains_huge.txt",
        "desc": "n0kovo 3M — harvested from IPv4 SSL certs",
        "size": "~26 MB",
    },
}

WORDLISTS_DIR = os.path.join(os.path.expanduser("~"), ".sd_finder", "wordlists")


def _file_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read(65536))
    return h.hexdigest()[:16]

def ensure_wordlists_dir():
    os.makedirs(WORDLISTS_DIR, exist_ok=True)
    reg_path = os.path.join(WORDLISTS_DIR, "registry.json")
    if not os.path.exists(reg_path):
        with open(reg_path, "w") as f:
            json.dump({}, f)

def load_registry() -> dict:
    ensure_wordlists_dir()
    try:
        with open(os.path.join(WORDLISTS_DIR, "registry.json")) as f:
            return json.load(f)
    except Exception:
        return {}

def save_registry(reg: dict):
    with open(os.path.join(WORDLISTS_DIR, "registry.json"), "w") as f:
        json.dump(reg, f, indent=2)

def _url_to_filename(name: str) -> str:
    return f"{name}.txt"

def list_wordlists(return_data=False):
    reg  = load_registry()
    rows = []
    for name, meta in WORDLIST_CATALOG.items():
        local = os.path.join(WORDLISTS_DIR, _url_to_filename(name))
        if name in reg and os.path.exists(local):
            status     = f"{C.GREEN}✔ cached{C.RESET}"
            status_raw = "cached"
        else:
            status     = f"{C.LIGHT_GREY}✗ not cached{C.RESET}"
            status_raw = "not cached"
        rows.append({
            "name": name, "desc": meta["desc"], "size": meta["size"],
            "status": status, "status_raw": status_raw,
        })
    if return_data:
        return rows
    log_section("Available Wordlists")
    col_w = [max(len(r["name"]) for r in rows)+2, max(len(r["desc"]) for r in rows)+2, 10]
    print(f"  {C.BOLD}{C.CYAN}{'NAME':<{col_w[0]}}{'DESCRIPTION':<{col_w[1]}}{'SIZE':<{col_w[2]}}STATUS{C.RESET}")
    print(f"  {C.LIGHT_GREY}{'─'*(sum(col_w)+10)}{C.RESET}")
    for r in rows:
        print(f"  {C.YELLOW}{r['name']:<{col_w[0]}}{C.RESET}{C.WHITE}{r['desc']:<{col_w[1]}}{C.RESET}{C.LIGHT_GREY}{r['size']:<{col_w[2]}}{C.RESET}{r['status']}")
    print()

def download_wordlist(name: str, force: bool = False) -> str | None:
    if name not in WORDLIST_CATALOG:
        log_error(f"Wordlist '{name}' not in catalog. Use --list-wordlists.")
        return None
    ensure_wordlists_dir()
    reg   = load_registry()
    local = os.path.join(WORDLISTS_DIR, _url_to_filename(name))
    meta  = WORDLIST_CATALOG[name]
    if not force and name in reg and os.path.exists(local):
        log_ok(f"Wordlist '{C.BOLD}{name}{C.RESET}{C.GREEN}' already cached → {C.CYAN}{local}")
        return local
    url = meta["url"]
    log_info(f"Downloading {C.BOLD}{C.YELLOW}{name}{C.RESET} ({meta['size']})...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SamXD/1.1"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            total = int(resp.getheader("Content-Length", 0))
            downloaded = 0
            with open(local, "wb") as out:
                while True:
                    chunk = resp.read(8192)
                    if not chunk:
                        break
                    out.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        sys.stdout.write(progress_bar(downloaded, total, label=f"{downloaded//1024} KB"))
                        sys.stdout.flush()
        if total:
            print()
        fhash = _file_hash(local)
        lines = sum(1 for _ in open(local, errors="ignore"))
        reg[name] = {"path": local, "hash": fhash, "url": url,
                     "timestamp": datetime.now().isoformat(), "lines": lines}
        save_registry(reg)
        log_ok(f"Saved {C.BOLD}{lines:,}{C.RESET}{C.GREEN} entries → {C.CYAN}{local}")
        return local
    except Exception as e:
        log_error(f"Download failed: {e}")
        if os.path.exists(local):
            os.remove(local)
        return None

def load_wordlist_lines(path: str) -> list[str]:
    lines = []
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                w = line.strip()
                if w and not w.startswith("#"):
                    lines.append(w)
    except Exception as e:
        log_error(f"Cannot read wordlist: {e}")
    return lines


# ╔══════════════════════════════════════════════════════════════════╗
# ║                     DNS UTILITIES                               ║
# ╚══════════════════════════════════════════════════════════════════╝
def resolve_hostname(hostname: str, timeout: float = 2.0) -> str | None:
    if HAS_DNSPYTHON:
        try:
            resolver = dns.resolver.Resolver()
            resolver.lifetime = timeout
            answers = resolver.resolve(hostname, "A")
            return str(answers[0])
        except Exception:
            return None
    else:
        try:
            return socket.gethostbyname(hostname)
        except Exception:
            return None

def zone_transfer_attempt(domain: str) -> list[str]:
    found = []
    if not HAS_DNSPYTHON:
        log_warn("dnspython not installed — skipping zone transfer.")
        return found
    log_info(f"Attempting zone transfer on {C.BOLD}{domain}{C.RESET}...")
    try:
        ns_answers = dns.resolver.resolve(domain, "NS")
        nameservers = [str(ns).rstrip(".") for ns in ns_answers]
    except Exception:
        return found
    for ns in nameservers:
        ns_ip = resolve_hostname(ns)
        if not ns_ip:
            continue
        try:
            z = dns.zone.from_xfr(dns.query.xfr(ns_ip, domain, lifetime=5))
            for name in z.nodes.keys():
                sub = str(name)
                if sub == "@":
                    continue
                fqdn = f"{sub}.{domain}"
                found.append(fqdn)
                log_found(fqdn, source="AXFR")
            if found:
                log_ok(f"Zone transfer SUCCESS on {C.BOLD}{ns}{C.RESET}! Got {len(found)} records.")
                return found
        except Exception:
            pass
    if not found:
        log_info("Zone transfer not allowed (expected for most domains).")
    return found


# ╔══════════════════════════════════════════════════════════════════╗
# ║                     OSINT SOURCES                               ║
# ╚══════════════════════════════════════════════════════════════════╝
def _get(url: str, timeout: int = 15, headers: dict = None) -> str | None:
    h = {"User-Agent": "Mozilla/5.0 (SamXD/1.1) Security-Research"}
    if headers:
        h.update(headers)
    try:
        if HAS_REQUESTS:
            r = requests.get(url, headers=h, timeout=timeout, verify=True)
            r.raise_for_status()
            return r.text
        else:
            req = urllib.request.Request(url, headers=h)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        log_debug(f"GET {url} failed: {e}")
        return None

def _get_json(url: str, timeout: int = 15, headers: dict = None):
    text = _get(url, timeout, headers)
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None

def parse_subdomains(raw: str, domain: str) -> set[str]:
    import re
    pattern = re.compile(
        r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*" + re.escape(domain),
        re.IGNORECASE,
    )
    results = set()
    for match in pattern.findall(raw):
        sub = match.lower().strip("*. ")
        if sub and sub.endswith(domain) and sub != domain:
            results.add(sub)
    return results

def source_crtsh(domain: str) -> set[str]:
    log_info(f"{C.CYAN}[crt.sh]{C.RESET} Querying certificate transparency logs...")
    data = _get_json(f"https://crt.sh/?q=%.{domain}&output=json", timeout=20)
    if not data:
        log_warn(f"{C.CYAN}[crt.sh]{C.RESET} No data.")
        return set()
    found = set()
    for entry in data:
        for line in entry.get("name_value", "").splitlines():
            sub = line.strip().lstrip("*. ").lower()
            if sub.endswith(domain) and sub != domain:
                found.add(sub)
    log_ok(f"{C.CYAN}[crt.sh]{C.RESET} Found {C.BOLD}{C.GREEN}{len(found)}{C.RESET} subdomains.")
    return found

def source_hackertarget(domain: str) -> set[str]:
    log_info(f"{C.CYAN}[HackerTarget]{C.RESET} Querying passive DNS...")
    data = _get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=15)
    if not data or "error" in data.lower()[:30]:
        log_warn(f"{C.CYAN}[HackerTarget]{C.RESET} Rate limited or no data.")
        return set()
    found = set()
    for line in data.splitlines():
        parts = line.split(",")
        if parts:
            sub = parts[0].strip().lower()
            if sub.endswith(domain) and sub != domain:
                found.add(sub)
    log_ok(f"{C.CYAN}[HackerTarget]{C.RESET} Found {C.BOLD}{C.GREEN}{len(found)}{C.RESET} subdomains.")
    return found

def source_alienvault(domain: str) -> set[str]:
    log_info(f"{C.CYAN}[AlienVault]{C.RESET} Querying OTX passive DNS...")
    data = _get_json(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns", timeout=20)
    if not data:
        log_warn(f"{C.CYAN}[AlienVault]{C.RESET} No data.")
        return set()
    found = set()
    for entry in data.get("passive_dns", []):
        h = entry.get("hostname", "").lower().strip()
        if h.endswith(domain) and h != domain:
            found.add(h)
    log_ok(f"{C.CYAN}[AlienVault]{C.RESET} Found {C.BOLD}{C.GREEN}{len(found)}{C.RESET} subdomains.")
    return found

def source_rapiddns(domain: str) -> set[str]:
    log_info(f"{C.CYAN}[RapidDNS]{C.RESET} Querying subdomain database...")
    data = _get(f"https://rapiddns.io/subdomain/{domain}?full=1#result", timeout=15)
    if not data:
        log_warn(f"{C.CYAN}[RapidDNS]{C.RESET} No data.")
        return set()
    found = parse_subdomains(data, domain)
    log_ok(f"{C.CYAN}[RapidDNS]{C.RESET} Found {C.BOLD}{C.GREEN}{len(found)}{C.RESET} subdomains.")
    return found

def source_urlscan(domain: str) -> set[str]:
    log_info(f"{C.CYAN}[URLScan.io]{C.RESET} Querying scan database...")
    data = _get_json(f"https://urlscan.io/api/v1/search/?q=domain:{domain}&size=200", timeout=20)
    if not data:
        log_warn(f"{C.CYAN}[URLScan.io]{C.RESET} No data.")
        return set()
    found = set()
    for result in data.get("results", []):
        dom = result.get("page", {}).get("domain", "").lower().strip()
        if dom.endswith(domain) and dom != domain:
            found.add(dom)
    log_ok(f"{C.CYAN}[URLScan.io]{C.RESET} Found {C.BOLD}{C.GREEN}{len(found)}{C.RESET} subdomains.")
    return found

def source_threatminer(domain: str) -> set[str]:
    log_info(f"{C.CYAN}[ThreatMiner]{C.RESET} Querying threat intelligence...")
    data = _get_json(f"https://api.threatminer.org/v2/domain.php?q={domain}&rt=5", timeout=15)
    if not data or data.get("status_code") not in ("200", 200):
        log_warn(f"{C.CYAN}[ThreatMiner]{C.RESET} No data or rate limited.")
        return set()
    found = set()
    for sub in data.get("results", []):
        sub = sub.lower().strip()
        if sub.endswith(domain) and sub != domain:
            found.add(sub)
    log_ok(f"{C.CYAN}[ThreatMiner]{C.RESET} Found {C.BOLD}{C.GREEN}{len(found)}{C.RESET} subdomains.")
    return found

def source_wayback(domain: str) -> set[str]:
    log_info(f"{C.CYAN}[Wayback Machine]{C.RESET} Querying CDX API...")
    url  = f"https://web.archive.org/cdx/search/cdx?url=*.{domain}&output=json&fl=original&collapse=urlkey&limit=5000"
    data = _get_json(url, timeout=25)
    if not data:
        log_warn(f"{C.CYAN}[Wayback Machine]{C.RESET} No data.")
        return set()
    found = set()
    for entry in data[1:]:
        if entry:
            found.update(parse_subdomains(entry[0], domain))
    log_ok(f"{C.CYAN}[Wayback Machine]{C.RESET} Found {C.BOLD}{C.GREEN}{len(found)}{C.RESET} subdomains.")
    return found

def source_google_dork(domain: str) -> set[str]:
    log_info(f"{C.CYAN}[Google Dork]{C.RESET} Querying via DuckDuckGo — {C.YELLOW}site:{domain}{C.RESET}...")
    enc  = urllib.parse.quote(f"
