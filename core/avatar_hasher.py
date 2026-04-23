"""
Avatar Hasher Module
Scarica avatar degli account trovati e li confronta con perceptual hash.
Usa Pillow e imagehash. Se due account hanno lo stesso avatar → stessa persona.
"""
import io
import requests

try:
    from PIL import Image
    import imagehash
    AVATAR_SUPPORTED = True
except ImportError:
    AVATAR_SUPPORTED = False


class AvatarHasher:
    def __init__(self):
        self.supported = AVATAR_SUPPORTED

    def collect_and_compare(self, results: dict) -> dict:
        """
        Raccoglie gli URL degli avatar dai risultati, li scarica,
        ne calcola il pHash e confronta tutti tra loro.
        """
        if not self.supported:
            return {
                "supported": False,
                "message": "Installa Pillow e imagehash: pip install Pillow imagehash"
            }

        avatar_urls = self._collect_avatar_urls(results)
        if not avatar_urls:
            return {"supported": True, "avatars_found": 0, "matches": []}

        hashes = {}
        for source, url in avatar_urls.items():
            h = self._hash_from_url(url)
            if h:
                hashes[source] = {"url": url, "hash": str(h), "_hash_obj": h}

        matches = self._find_matches(hashes)

        # Rimuovi gli oggetti hash interni prima di ritornare
        for v in hashes.values():
            v.pop("_hash_obj", None)

        return {
            "supported": True,
            "avatars_found": len(hashes),
            "hashes": {k: {"url": v["url"], "hash": v["hash"]} for k, v in hashes.items()},
            "matches": matches
        }

    def _collect_avatar_urls(self, results: dict) -> dict:
        urls = {}
        # GitHub restituisce avatar_url
        if "github" in results and results["github"].get("found"):
            # Ottieni l'avatar URL da GitHub API tramite username
            gh = results["github"]
            if "avatar_url" in gh:
                urls["github"] = gh["avatar_url"]
            elif "url" in gh:
                # Cerca di costruirlo
                username = gh["url"].rstrip("/").split("/")[-1]
                urls["github"] = f"https://github.com/{username}.png?size=200"

        return urls

    def _hash_from_url(self, url: str):
        """Scarica un'immagine e calcola il perceptual hash."""
        try:
            resp = requests.get(url, timeout=8,
                                headers={"User-Agent": "NullTrace/1.0"})
            if resp.status_code == 200:
                img = Image.open(io.BytesIO(resp.content)).convert("RGB")
                return imagehash.phash(img)
        except Exception:
            pass
        return None

    def _find_matches(self, hashes: dict) -> list:
        """Confronta tutti gli hash tra loro e trova somiglianze."""
        sources = list(hashes.keys())
        matches = []
        for i in range(len(sources)):
            for j in range(i + 1, len(sources)):
                s1, s2 = sources[i], sources[j]
                h1 = hashes[s1]["_hash_obj"]
                h2 = hashes[s2]["_hash_obj"]
                distance = h1 - h2
                similarity = max(0, 100 - (distance * 3))
                if distance < 15:
                    matches.append({
                        "source_a": s1,
                        "source_b": s2,
                        "hamming_distance": distance,
                        "similarity_percent": similarity,
                        "likely_same_person": distance < 8
                    })
        return matches
