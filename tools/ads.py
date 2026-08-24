#!/usr/bin/env python3
"""ADS/SciX access for the sci-paper skills. Python standard library only.

Five commands over the ADS v1 API:

    search '<solr query>'      metadata for a query
    refs <bibcode>             what that paper cites   -- backward snowball
    cites <bibcode>            what cites that paper   -- forward snowball
    resolve <arxiv-id|doi>     -> bibcode, preferring the refereed record
    export <bibcode> [...]     verbatim BibTeX from the ADS export endpoint

Everything but `export` prints JSON on stdout. `export` prints BibTeX exactly
as ADS returned it, because rule 2 in skills/_shared/house-rules.md says a
refs.bib entry is never composed or adjusted, and this is its only path.

Token resolution, in order, so it works on a laptop and on OzSTAR or NERSC
alike:

    macOS Keychain, service `nasa-ads-api-token`
    $ADS_API_TOKEN -> $ADS_DEV_KEY -> $SCIX_API_TOKEN
    ~/.ads/dev_key

The token travels in an Authorization header and nowhere else: never in a URL,
never on argv, and scrubbed out of every message built from something the far
end sent back.

Base URL comes from $SCI_PAPER_ADS_BASE and defaults to the ADS host. SciX
serves the same v1 surface, so moving between them is one variable.

Exit codes: 0 fine, 2 the request or the configuration failed, 3 export
returned nothing for at least one bibcode.
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE = "https://api.adsabs.harvard.edu/v1"
KEYCHAIN_SERVICE = "nasa-ads-api-token"
LOOPBACK = ("localhost", "127.0.0.1", "::1")
TIMEOUT = 30
DEFAULT_ROWS = 20
MAX_ROWS = 200

# Enough to screen a result set and then act on it. Plan section 9.1 singles
# out the abstract, the identifiers and `esources` as load-bearing rather than
# optional: without the abstract nothing can be screened, and without the
# identifiers no PDF can be found. The rest is what a shortlist has to show.
FIELDS = ("bibcode,title,author,year,property,doctype,citation_count,"
          "doi,identifier,esources,abstract")


class AdsError(Exception):
    """Anything that should reach the user as a message rather than a traceback."""


# --------------------------------------------------------------------------
# token


_TOKEN = None


def _scrub(text):
    """Strip the token out of anything the far end controls.

    A redirect Location, an HTTP reason phrase and an error body all come from
    whatever host answered, and a proxy or captive portal that echoes the
    request headers back in a debug page is an ordinary thing on a university
    or HPC network. Without this the token reaches stderr, and from there a
    log, which is exactly what "never in an error message" is meant to prevent.

    Best-effort, and worth being honest about the limit: it removes the token
    as written. A host that echoed it back base64- or percent-encoded would
    defeat it. That host is the one the token was deliberately sent to, so it
    already has the cleartext and nothing is lost by the echo -- the leak that
    matters is to a host that was never meant to see it, and that is what the
    redirect refusal above prevents.
    """
    text = str(text)
    return text.replace(_TOKEN, "<token redacted>") if _TOKEN else text


def _token():
    global _TOKEN
    if _TOKEN is not None:
        return _TOKEN
    _TOKEN = _find_token()
    return _TOKEN


def _find_token():
    if sys.platform == "darwin":
        try:
            found = subprocess.run(
                ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-w"],
                capture_output=True, text=True, timeout=10)
            if found.returncode == 0 and found.stdout.strip():
                return found.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            pass  # no keychain, or locked -- fall through to the env vars
    for var in ("ADS_API_TOKEN", "ADS_DEV_KEY", "SCIX_API_TOKEN"):
        value = os.environ.get(var, "").strip()
        if value:
            return value
    try:
        with open(os.path.expanduser("~/.ads/dev_key")) as handle:
            value = handle.read().strip()
        if value:
            return value
    except OSError:
        pass
    raise AdsError(
        "no ADS/SciX token found. Register free at https://scixplorer.org, then\n"
        f'  security add-generic-password -a "$USER" -s {KEYCHAIN_SERVICE} -w <token>\n'
        "or export ADS_API_TOKEN=<token>.")


# --------------------------------------------------------------------------
# transport


def _safe(url):
    """A URL fit to print: scheme, host and path, with the query dropped."""
    parts = urllib.parse.urlsplit(url)
    return _scrub(
        urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path, "", "")) or url)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Refuse every redirect.

    urllib follows redirects by default and re-sends the Authorization header
    while doing it, which would hand the bearer token to a host that was never
    meant to see it. The API does not redirect in normal operation, so refusing
    outright is both safe and the simplest thing that works. The target is
    reported; the token never is.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise AdsError(
            f"refused an HTTP {code} redirect to {_safe(newurl)}. The token is "
            "only ever sent to the configured API host. If ADS has genuinely "
            "moved, set SCI_PAPER_ADS_BASE to the new base URL.")


def _require_tls(base):
    """The token only ever travels over TLS to a remote host.

    Over plain HTTP the Authorization header is readable by everything on the
    path, including an `http_proxy` that was never meant to see it -- and a
    proxy is ordinary on a university or HPC network. Over HTTPS the same proxy
    sees only a CONNECT tunnel, so requiring TLS closes the exposure without
    disabling proxying, which those networks need to reach the internet at all.

    Loopback is excepted so a local stub can be pointed at; `_request` turns
    proxying off for exactly that case, where it would otherwise send a
    127.0.0.1 request, and the token with it, out to the proxy.
    """
    parts = urllib.parse.urlsplit(base)
    if parts.scheme == "https" or parts.hostname in LOOPBACK:
        return
    raise AdsError(
        f"refusing to send the token to {_safe(base)}: SCI_PAPER_ADS_BASE must "
        "use https (localhost excepted). Both api.adsabs.harvard.edu and "
        "api.scixplorer.org serve the v1 surface over https.")


def _request(path, params=None, payload=None):
    # `or`, not a default argument: `export SCI_PAPER_ADS_BASE=` leaves the
    # variable set and empty, which would otherwise build a host-less URL.
    base = (os.environ.get("SCI_PAPER_ADS_BASE") or DEFAULT_BASE).rstrip("/")
    _require_tls(base)
    url = f"{base}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {"Authorization": "Bearer " + _token(), "Accept": "application/json"}
    body = None
    if payload is not None:
        body = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    handlers = [_NoRedirect]
    if urllib.parse.urlsplit(base).hostname in LOOPBACK:
        # Never send a loopback request to a proxy. urllib's environment proxy
        # handler does not exempt 127.0.0.1, so with http_proxy set the local
        # stub the base points at -- and the token with it -- would go to the
        # proxy instead. Proxies stay enabled for every other host, because on
        # an HPC network one is how you reach the internet at all.
        handlers.append(urllib.request.ProxyHandler({}))
    opener = urllib.request.build_opener(*handlers)
    try:
        with opener.open(urllib.request.Request(url, data=body, headers=headers),
                         timeout=TIMEOUT) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        hint = {401: "  token rejected -- check it is current",
                403: "  token lacks permission for this endpoint",
                429: "  rate limit exhausted -- ADS resets daily"}.get(exc.code, "")
        # Scrub first, then truncate: truncating first can cut the token in
        # half, and half a token is still most of a token.
        detail = _scrub(exc.read().decode(errors="replace").strip())[:400]
        raise AdsError(
            f"{_safe(url)}: HTTP {exc.code} {_scrub(exc.reason)}{hint}\n{detail}")
    except urllib.error.URLError as exc:
        raise AdsError(f"{_safe(url)}: {_scrub(exc.reason)}")
    except TimeoutError:  # a read that stalls raises this bare, not as URLError
        raise AdsError(f"{_safe(url)}: no response within {TIMEOUT}s")
    except ValueError as exc:  # non-JSON body: a proxy or captive portal, usually
        raise AdsError(f"{_safe(url)}: response was not JSON ({_scrub(exc)})")


# --------------------------------------------------------------------------
# search


def _arxiv(identifiers):
    for ident in identifiers:
        if ident.startswith("arXiv:"):
            return ident[len("arXiv:"):]
    return None


def _doi(dois):
    """The publisher DOI. ADS also carries a 10.48550 DataCite DOI minted for
    the arXiv posting, which is not the published paper."""
    for doi in dois:
        if not doi.lower().startswith("10.48550/"):
            return doi
    return dois[0] if dois else None


def _shape(doc, brief):
    authors = doc.get("author") or []
    record = {
        "bibcode": doc.get("bibcode"),
        "title": (doc.get("title") or [None])[0],
        "first_author": authors[0] if authors else None,
        "n_authors": len(authors),
        "year": doc.get("year"),
        # property:REFEREED is the authoritative peer-review flag. It is never
        # inferred from whether the paper is on arXiv.
        "refereed": "REFEREED" in (doc.get("property") or []),
        "doctype": doc.get("doctype"),
        "citation_count": doc.get("citation_count"),
        "doi": _doi(doc.get("doi") or []),
        "arxiv": _arxiv(doc.get("identifier") or []),
        # Source *types*, not URLs: EPRINT_PDF, PUB_HTML and so on.
        "esources": doc.get("esources") or [],
    }
    if not brief:
        record["abstract"] = doc.get("abstract")
    return record


def _rows(requested):
    if requested < 1 or requested > MAX_ROWS:
        raise AdsError(f"--rows must be between 1 and {MAX_ROWS}; page with --start "
                       "for more, and compare `returned` against `num_found`.")
    return requested


def _search(query, rows, start, sort, brief):
    params = {"q": query, "rows": _rows(rows), "start": start,
              "fl": FIELDS.replace(",abstract", "") if brief else FIELDS}
    if sort:
        params["sort"] = sort
    response = _request("search/query", params=params).get("response", {})
    docs = response.get("docs", [])
    return {"query": query,
            "num_found": response.get("numFound"),
            "start": start,
            "returned": len(docs),
            "docs": [_shape(doc, brief) for doc in docs]}


def _year(doc):
    """ADS returns year as a string, and a stray record has none at all. Both
    have to sort against each other without raising."""
    try:
        return int(doc["year"])
    except (KeyError, TypeError, ValueError):
        return 0


def _resolve(identifier, rows):
    ident = identifier.strip()
    # People paste identifiers as URLs at least as often as bare ones, and an
    # unstripped URL produces a query that matches nothing -- which reads
    # exactly like "ADS does not have this paper".
    for host in ("doi.org/", "arxiv.org/abs/", "arxiv.org/pdf/"):
        if host in ident:
            ident = ident.split(host, 1)[1].split("?")[0].split("#")[0]
            if ident.lower().endswith(".pdf"):
                ident = ident[:-4]
            break
    for prefix in ("doi:", "arxiv:"):
        if ident.lower().startswith(prefix):
            ident = ident[len(prefix):]
            break
    if ident.startswith("10."):
        query = f'doi:"{ident}"'
    else:
        # A version suffix is not part of the identifier ADS indexes, and an
        # abs URL carries one as often as not. Only stripped on this branch: a
        # DOI is free to end in something that looks like one.
        base, sep, tail = ident.rpartition("v")
        if sep and base and tail.isdigit():
            ident = base
        query = f'identifier:"arXiv:{ident}"'
    result = _search(query, rows, 0, None, brief=True)
    docs = result["docs"]
    # Prefer the refereed record where a preprint also has a published version.
    best = max(docs, key=lambda d: (d["refereed"], d["doctype"] == "article",
                                    _year(d))) if docs else None
    return {"input": identifier,
            "query": query,
            "preferred": best["bibcode"] if best else None,
            "matches": docs}


# --------------------------------------------------------------------------
# export


def _export(bibcodes):
    """Verbatim BibTeX. Whatever ADS returns is what goes into refs.bib."""
    bibtex = _request("export/bibtex", payload={"bibcode": list(bibcodes)}).get("export", "")
    # Match the citekey, `@ARTICLE{<bibcode>,`, not the bare string: one bibcode
    # is a prefix of another often enough that a substring test would call a
    # truncated one present and drop the reference silently.
    missing = [code for code in bibcodes if "{" + code + "," not in bibtex]
    return bibtex, missing


# --------------------------------------------------------------------------
# cli


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="ads.py", description=__doc__.split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    def with_paging(sp):
        sp.add_argument("--rows", type=int, default=DEFAULT_ROWS,
                        help=f"records to return, 1-{MAX_ROWS} (default {DEFAULT_ROWS})")
        sp.add_argument("--start", type=int, default=0, help="offset, for paging")
        sp.add_argument("--sort", help="e.g. 'citation_count desc', 'date desc'")
        sp.add_argument("--brief", action="store_true",
                        help="omit abstracts -- use when listing a long reference list")
        return sp

    search = with_paging(sub.add_parser("search", help="run a Solr query"))
    search.add_argument("query")
    refs = with_paging(sub.add_parser("refs", help="what this paper cites"))
    refs.add_argument("bibcode")
    cites = with_paging(sub.add_parser("cites", help="what cites this paper"))
    cites.add_argument("bibcode")
    resolve = sub.add_parser("resolve", help="arXiv id or DOI -> bibcode")
    resolve.add_argument("identifier")
    resolve.add_argument("--rows", type=int, default=DEFAULT_ROWS,
                         help="candidate records to weigh, when an id matches more than one")
    export = sub.add_parser("export", help="verbatim BibTeX")
    export.add_argument("bibcodes", nargs="+")

    args = parser.parse_args(argv)
    try:
        if args.command == "export":
            bibtex, missing = _export(args.bibcodes)
            sys.stdout.write(bibtex)
            if missing:
                print("no BibTeX returned for: " + ", ".join(missing), file=sys.stderr)
                return 3
            return 0
        if args.command == "resolve":
            result = _resolve(args.identifier, args.rows)
        else:
            query = {"search": lambda: args.query,
                     "refs": lambda: f"references({args.bibcode})",
                     "cites": lambda: f"citations({args.bibcode})"}[args.command]()
            result = _search(query, args.rows, args.start, args.sort, args.brief)
    except AdsError as exc:
        print(f"ads.py: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
