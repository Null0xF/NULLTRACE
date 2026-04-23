"""
Identity Clustering Module
Raggruppa account che sembrano appartenere alla stessa persona,
basandosi su attributi condivisi tra i diversi moduli.
"""

class IdentityCluster:
    def __init__(self):
        self.clusters = []

    def build(self, results: dict) -> list:
        """
        Analizza i risultati raccolti e raggruppa le identità per attributi condivisi.
        Restituisce una lista di cluster con confidence score.
        """
        identity_attrs = self._extract_attributes(results)
        clusters = self._cluster(identity_attrs)
        return clusters

    def _extract_attributes(self, results: dict) -> list:
        """Estrae attributi normalizzati da ogni fonte trovata."""
        attrs = []

        for source, data in results.items():
            if not isinstance(data, dict) or not data.get("found"):
                continue

            entry = {"source": source, "attributes": {}}

            if "url" in data:
                entry["attributes"]["url"] = data["url"]
            if "name" in data and data["name"]:
                entry["attributes"]["name"] = data["name"].lower().strip()
            if "location" in data and data["location"]:
                entry["attributes"]["location"] = data["location"].lower().strip()
            if "company" in data and data["company"]:
                entry["attributes"]["company"] = data["company"].lower().strip()
            if "blog" in data and data["blog"]:
                entry["attributes"]["website"] = data["blog"].lower().strip()
            if "avatar_hash" in data:
                entry["attributes"]["avatar_hash"] = data["avatar_hash"]

            if entry["attributes"]:
                attrs.append(entry)

        return attrs

    def _cluster(self, entries: list) -> list:
        """
        Raggruppa entries per attributi in comune.
        Algoritmo greedy: ogni entry entra nel primo cluster compatibile,
        oppure crea un cluster nuovo.
        """
        clusters = []

        for entry in entries:
            matched = False
            for cluster in clusters:
                if self._is_compatible(cluster, entry):
                    cluster["members"].append(entry["source"])
                    cluster["shared_attributes"] = self._merge_attrs(
                        cluster["shared_attributes"], entry["attributes"]
                    )
                    cluster["confidence"] = min(100, cluster["confidence"] + 20)
                    matched = True
                    break

            if not matched:
                clusters.append({
                    "members": [entry["source"]],
                    "shared_attributes": dict(entry["attributes"]),
                    "confidence": 50  # baseline for a single-source cluster
                })

        # Filter out single-member clusters with no meaningful attributes
        clusters = [c for c in clusters if len(c["members"]) > 1 or
                    len(c["shared_attributes"]) > 1]

        return clusters

    def _is_compatible(self, cluster: dict, entry: dict) -> bool:
        """
        Due identità sono compatibili se condividono almeno un attributo non banale.
        """
        shared = cluster["shared_attributes"]
        attrs = entry["attributes"]

        for key in ["name", "location", "company", "website"]:
            if key in shared and key in attrs:
                if shared[key] and attrs[key] and shared[key] == attrs[key]:
                    return True

        if "avatar_hash" in shared and "avatar_hash" in attrs:
            # Hamming distance < 10 = avatar molto simile
            try:
                dist = bin(int(shared["avatar_hash"], 16) ^
                           int(attrs["avatar_hash"], 16)).count("1")
                if dist < 10:
                    return True
            except Exception:
                pass

        return False

    def _merge_attrs(self, base: dict, new: dict) -> dict:
        """Unisce due dizionari di attributi mantenendo i valori condivisi."""
        merged = {}
        for key in set(list(base.keys()) + list(new.keys())):
            if key in base and key in new and base[key] == new[key]:
                merged[key] = base[key]
            elif key in base:
                merged[key] = base[key]
            else:
                merged[key] = new[key]
        return merged
