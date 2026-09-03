from __future__ import annotations

import ipaddress
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import tarfile
import threading
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
from itertools import islice
from typing import Any
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from uuid import uuid4


_TOOL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".tools")
_TOOL_REPOSITORIES = {
	"amass": "owasp-amass/Amass",
	"subfinder": "projectdiscovery/subfinder",
	"gau": "lc/gau",
	"hakrawler": "hakluke/hakrawler",
}
_TOOL_LOCK = threading.Lock()


@dataclass
class DiscoveryResult:
	hosts: set[str] = field(default_factory=set)
	urls: set[str] = field(default_factory=set)
	sources: dict[str, set[str]] = field(default_factory=dict)
	statuses: dict[str, int] = field(default_factory=dict)
	titles: dict[str, str] = field(default_factory=dict)
	technologies: set[str] = field(default_factory=set)


def _now() -> str:
	return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _tool_executable(name: str) -> str:
	filename = f"{name}.exe" if os.name == "nt" else name
	return os.path.join(os.path.abspath(_TOOL_DIR), filename)


def _release_asset(name: str, assets: list[dict[str, Any]]) -> dict[str, Any] | None:
	system = {"windows": "windows", "linux": "linux", "darwin": "darwin"}.get(platform.system().lower(), "")
	machine = platform.machine().lower()
	architecture = "amd64" if machine in {"amd64", "x86_64", "x64"} else "arm64" if "arm64" in machine or "aarch64" in machine else machine
	architecture_tokens = {"amd64", "x86_64", "x64"} if architecture == "amd64" else {"arm64", "aarch64"} if architecture == "arm64" else {architecture}
	for asset in assets:
		asset_name = asset.get("name", "").lower()
		if system in asset_name and any(token in asset_name for token in architecture_tokens) and asset_name.endswith((".zip", ".tar.gz", ".tgz")):
			return asset
	return None


def _install_tool(name: str) -> str | None:
	executable = _tool_executable(name)
	if os.path.isfile(executable):
		return executable
	with _TOOL_LOCK:
		if os.path.isfile(executable):
			return executable
		repository = _TOOL_REPOSITORIES.get(name)
		if not repository:
			return None
		try:
			api_request = Request(
				f"https://api.github.com/repos/{repository}/releases/latest",
				headers={"Accept": "application/vnd.github+json", "User-Agent": "ReconPilot/1.0"},
			)
			with urlopen(api_request, timeout=30) as response:
				release = json.loads(response.read().decode("utf-8"))
			asset = _release_asset(name, release.get("assets", []))
			if not asset:
				return None
			with urlopen(Request(asset["browser_download_url"], headers={"User-Agent": "ReconPilot/1.0"}), timeout=120) as response:
				archive = response.read()
			os.makedirs(_TOOL_DIR, exist_ok=True)
			archive_path = os.path.join(_TOOL_DIR, asset["name"])
			with open(archive_path, "wb") as output:
				output.write(archive)
			if asset["name"].lower().endswith(".zip"):
				with zipfile.ZipFile(archive_path) as package:
					member = next((item for item in package.namelist() if os.path.basename(item).lower() in {name, f"{name}.exe"}), None)
					if not member:
						return None
					with package.open(member) as source, open(executable, "wb") as output:
						output.write(source.read())
			else:
				with tarfile.open(archive_path, "r:*") as package:
					member = next((item for item in package.getmembers() if os.path.basename(item.name).lower() == name), None)
					if not member:
						return None
					with package.extractfile(member) as source, open(executable, "wb") as output:
						if source is None:
							return None
						output.write(source.read())
			if os.name != "nt":
				os.chmod(executable, 0o755)
			try:
				os.remove(archive_path)
			except OSError:
				pass
			return executable if os.path.isfile(executable) else None
		except (OSError, ValueError, KeyError, json.JSONDecodeError, zipfile.BadZipFile, tarfile.TarError):
			return None


def _command(name: str, args: list[str], target: str, timeout: int = 90) -> list[str]:
	executable = shutil.which(name) or _install_tool(name)
	if executable is None:
		return []
	try:
		completed = subprocess.run(
			[executable, *args],
			input=f"{target}\n" if name == "hakrawler" else None,
			capture_output=True,
			text=True,
			timeout=timeout,
			check=False,
		)
	except (OSError, subprocess.TimeoutExpired):
		return []
	return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def _extract_asns(lines: list[str]) -> set[str]:
	return {f"AS{match}" for match in re.findall(r"(?i)(?:^|\W)AS(\d{1,10})(?:$|\W)", "\n".join(lines))}


def _extract_networks(lines: list[str]) -> set[str]:
	return set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b", "\n".join(lines)))


def _reverse_dns(networks: set[str], target: str) -> list[str]:
	hosts: set[str] = set()
	for network in networks:
		try:
			addresses = ipaddress.ip_network(network, strict=False).hosts()
		except ValueError:
			continue
		# Avoid turning a broad ASN allocation into an unbounded scan.
		for address in islice(addresses, 65536):
			try:
				hosts.add(socket.gethostbyaddr(str(address))[0])
			except (OSError, socket.herror):
				continue
	return list(hosts)


def _hostname(value: str) -> str | None:
	candidate = value.strip().lower().rstrip(".")
	if candidate.startswith("*."):
		candidate = candidate[2:]
	try:
		parsed = urlsplit(candidate if "://" in candidate else f"//{candidate}")
		host = parsed.hostname
	except ValueError:
		return None
	return host.rstrip(".") if host else None


def _is_in_scope(host: str, target: str) -> bool:
	target_host = _hostname(target)
	if not target_host:
		return False
	try:
		return ipaddress.ip_address(host) == ipaddress.ip_address(target_host)
	except ValueError:
		return host == target_host or host.endswith(f".{target_host}")


def _add_host(result: DiscoveryResult, value: str, source: str, target: str) -> None:
	host = _hostname(value)
	if host and _is_in_scope(host, target):
		result.hosts.add(host)
		result.sources.setdefault(host, set()).add(source)


def _add_url(result: DiscoveryResult, value: str, source: str, target: str) -> None:
	try:
		parsed = urlsplit(value.strip())
	except ValueError:
		return
	if parsed.scheme not in {"http", "https"} or not parsed.hostname:
		return
	if not _is_in_scope(parsed.hostname, target):
		return
	normalized = value.strip().split("#", 1)[0]
	result.urls.add(normalized)
	_add_host(result, parsed.hostname, source, target)


def _wayback_urls(target: str) -> list[str]:
	target_host = _hostname(target)
	if not target_host or "." not in target_host:
		return []
	url = (
		"https://web.archive.org/cdx/search/cdx?"
		f"url=*.{target_host}/*&output=json&fl=original&collapse=urlkey&filter=statuscode:200"
	)
	try:
		with urlopen(Request(url, headers={"User-Agent": "ReconPilot/1.0"}), timeout=20) as response:
			payload = json.loads(response.read().decode("utf-8"))
	except (OSError, ValueError, json.JSONDecodeError):
		return []
	return [item[0] for item in payload[1:] if isinstance(item, list) and item]


def _crt_hosts(target: str) -> list[str]:
	target_host = _hostname(target)
	if not target_host or "." not in target_host:
		return []
	try:
		with urlopen(
			Request(f"https://crt.sh/?q=%25.{target_host}&output=json", headers={"User-Agent": "ReconPilot/1.0"}),
			timeout=20,
		) as response:
			payload = json.loads(response.read().decode("utf-8"))
	except (OSError, ValueError, json.JSONDecodeError):
		return []
	names: set[str] = set()
	for entry in payload:
		for name in entry.get("name_value", "").splitlines():
			if name:
				names.add(name)
	return list(names)


def _probe(result: DiscoveryResult, host: str) -> None:
	for scheme in ("https", "http"):
		url = f"{scheme}://{host}"
		try:
			request = Request(url, headers={"User-Agent": "ReconPilot/1.0"}, method="GET")
			with urlopen(request, timeout=8) as response:
				body = response.read(4096).decode("utf-8", errors="ignore")
				result.statuses[host] = response.status
				title = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
				if title:
					result.titles[host] = " ".join(title.group(1).split())[:255]
				server = response.headers.get("Server")
				if server:
					result.technologies.add(server.split("/", 1)[0].strip())
				return
		except (OSError, ValueError):
			continue


def discover(target: str) -> DiscoveryResult:
	result = DiscoveryResult()
	target_host = _hostname(target)
	if not target_host:
		return result
	_add_host(result, target_host, "target", target)
	_add_url(result, f"https://{target_host}", "target", target_host)

	if "." in target_host and not _is_ip(target_host):
		# Run independent OSINT sources concurrently; a missing or slow tool does not block the others.
		sources = {
			"amass-passive": lambda: _command("amass", ["enum", "-passive", "-d", target_host], target_host),
			"amass-active": lambda: _command("amass", ["enum", "-active", "-d", target_host], target_host),
			"amass-intel": lambda: _command("amass", ["intel", "-d", target_host, "-whois"], target_host),
			"subfinder": lambda: _command("subfinder", ["-silent", "-d", target_host], target_host),
			"crt.sh": lambda: _crt_hosts(target_host),
			"wayback": lambda: _wayback_urls(target_host),
		}
		intel_lines: list[str] = []
		with ThreadPoolExecutor(max_workers=len(sources)) as pool:
			futures = {pool.submit(task): source for source, task in sources.items()}
			for future in as_completed(futures):
				source = futures[future]
				try:
					lines = future.result()
				except Exception:
					lines = []
				if source == "amass-intel":
					intel_lines = lines
				for line in lines:
					if source == "wayback":
						_add_url(result, line, source, target_host)
					else:
						_add_host(result, line, source, target_host)

		asns = _extract_asns(intel_lines)
		with ThreadPoolExecutor(max_workers=max(1, min(8, len(asns)))) as pool:
			asn_futures = {
				pool.submit(_command, "amass", ["intel", "-asn", asn.removeprefix("AS")], target_host): asn
				for asn in asns
			}
			for future in as_completed(asn_futures):
				asn = asn_futures[future]
				try:
					asn_lines = future.result()
				except Exception:
					asn_lines = []
				for line in asn_lines:
					_add_host(result, line, f"amass-asn:{asn}", target_host)
				for host in _reverse_dns(_extract_networks(asn_lines), target_host):
					_add_host(result, host, f"reverse-dns:{asn}", target_host)

	for source, lines in (
		("gau", _command("gau", [target_host], target_host)),
		("hakrawler", _command("hakrawler", ["-d", "3"], f"https://{target_host}")),
	):
		for line in lines:
			_add_url(result, line, source, target_host)

	for host in sorted(result.hosts):
		try:
			socket.gethostbyname_ex(host)
		except socket.gaierror:
			continue
		_probe(result, host)
	return result


def _is_ip(value: str) -> bool:
	try:
		ipaddress.ip_address(value)
		return True
	except ValueError:
		return False


def build_records(result: DiscoveryResult, project_id: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
	timestamp = _now()
	assets: list[dict[str, Any]] = []
	for host in sorted(result.hosts):
		try:
			addresses = sorted({item[4][0] for item in socket.getaddrinfo(host, None)})
		except socket.gaierror:
			addresses = []
		assets.append({
			"id": f"asset-{uuid4().hex}", "projectId": project_id, "hostname": host,
			"url": f"https://{host}", "type": "ip" if _is_ip(host) else "subdomain",
			"statusCode": result.statuses.get(host), "alive": host in result.statuses,
			"title": result.titles.get(host, host), "technologies": sorted(result.technologies),
			"ips": addresses, "ports": [443] if host in result.statuses else [],
			"source": sorted(result.sources.get(host, {"discovery"})), "discoveredAt": timestamp,
		})
	endpoints = []
	javascript = []
	for url in sorted(result.urls):
		parsed = urlsplit(url)
		endpoint = {
			"id": f"ep-{uuid4().hex}", "projectId": project_id, "host": parsed.hostname or "",
			"method": "GET", "path": parsed.path or "/", "url": url, "category": "general",
			"priority": "info", "authRequired": False, "parameterCount": len(parsed.query.split("&")) if parsed.query else 0,
			"parameters": [part.split("=", 1)[0] for part in parsed.query.split("&") if part],
			"statusCode": result.statuses.get(parsed.hostname or ""), "sources": ["gau", "wayback", "hakrawler"],
			"lastSeenAt": timestamp,
		}
		endpoints.append(endpoint)
		if parsed.path.lower().endswith(".js"):
			javascript.append({
				"id": f"js-{uuid4().hex}", "projectId": project_id, "host": parsed.hostname or "",
				"url": url, "filename": parsed.path.rsplit("/", 1)[-1], "size": 0,
				"endpointsFound": 0, "secretsFound": 0, "source": "discovery",
				"statusCode": result.statuses.get(parsed.hostname or ""), "lastSeenAt": timestamp,
			})
	technologies = [{"id": f"tech-{uuid4().hex}", "projectId": project_id, "name": name, "category": "server", "assets": len(assets), "confidence": 50, "sources": ["http-header"]} for name in sorted(result.technologies)]
	return assets, endpoints, javascript, technologies
