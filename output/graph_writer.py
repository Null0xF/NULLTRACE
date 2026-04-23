"""
OSINT Graph Visualization
Genera un file HTML interattivo con un grafo dei nodi e delle relazioni trovate.
Usa pyvis per creare un network graph apribile nel browser.
"""
try:
    from pyvis.network import Network
    PYVIS_SUPPORTED = True
except ImportError:
    PYVIS_SUPPORTED = False


class GraphWriter:
    @staticmethod
    def write(data: dict, output_file: str = "nulltrace_graph.html"):
        if not PYVIS_SUPPORTED:
            print("[-] pyvis non installato. Installa con: pip install pyvis")
            return

        query = data.get("query", "target")
        results = data.get("results", {})

        net = Network(
            height="750px",
            width="100%",
            bgcolor="#0d1117",
            font_color="#c9d1d9",
            directed=False
        )
        net.set_options("""{
          "nodes": {
            "borderWidth": 2,
            "shadow": { "enabled": true }
          },
          "edges": {
            "smooth": { "type": "continuous" },
            "shadow": { "enabled": true }
          },
          "physics": {
            "forceAtlas2Based": {
              "gravitationalConstant": -80,
              "springLength": 150
            },
            "solver": "forceAtlas2Based",
            "stabilization": { "iterations": 150 }
          }
        }""")

        # Nodo centrale (il target)
        net.add_node(
            query,
            label=query,
            title=f"<b>Target:</b> {query}",
            color="#58a6ff",
            size=30,
            shape="star"
        )

        # Colori per tipo di nodo
        COLORS = {
            "platform": "#3fb950",   # verde
            "breach":   "#f85149",   # rosso
            "domain":   "#d29922",   # giallo
            "cluster":  "#bc8cff",   # viola
            "username": "#79c0ff",   # azzurro
        }

        # Aggiungi nodi per ogni fonte
        for source, source_data in results.items():
            if not isinstance(source_data, dict):
                continue

            if source == "correlation_engine":
                continue

            found = source_data.get("found", True)
            color = COLORS["platform"] if found else "#6e7681"

            tooltip = f"<b>Source:</b> {source}<br>"
            if "url" in source_data:
                tooltip += f"<b>URL:</b> {source_data['url']}<br>"
            if "public_repos" in source_data:
                tooltip += f"<b>Repos:</b> {source_data['public_repos']}<br>"
            if "link_karma" in source_data:
                tooltip += f"<b>Karma:</b> {source_data['link_karma']}<br>"

            net.add_node(source, label=source, title=tooltip, color=color, size=20, shape="dot")
            edge_label = "found_on" if found else "not_found"
            edge_color = color
            net.add_edge(query, source, label=edge_label, color=edge_color)

            # Nodi breach
            breaches = source_data.get("breaches", {})
            if isinstance(breaches, dict) and breaches.get("found"):
                for b in breaches.get("breaches", []):
                    breach_id = f"breach:{b}"
                    net.add_node(
                        breach_id, label=b,
                        title=f"<b>Breach:</b> {b}",
                        color=COLORS["breach"], size=15, shape="diamond"
                    )
                    net.add_edge(source, breach_id, label="breach_in",
                                 color=COLORS["breach"], dashes=True)

            # Nodi dominio (per email)
            if "domain" in source_data:
                domain_id = f"domain:{source_data['domain']}"
                net.add_node(
                    domain_id, label=source_data["domain"],
                    title=f"<b>Domain:</b> {source_data['domain']}",
                    color=COLORS["domain"], size=18, shape="triangle"
                )
                net.add_edge(source, domain_id, label="uses_domain", color=COLORS["domain"])

        # Nodi cluster identità
        cluster_data = results.get("identity_clusters", [])
        for i, cluster in enumerate(cluster_data):
            cluster_id = f"cluster_{i}"
            members = ", ".join(cluster.get("members", []))
            confidence = cluster.get("confidence", 0)
            net.add_node(
                cluster_id,
                label=f"Cluster {i+1} ({confidence}%)",
                title=f"<b>Identity Cluster</b><br>Members: {members}<br>Confidence: {confidence}%",
                color=COLORS["cluster"], size=22, shape="hexagon"
            )
            for member in cluster.get("members", []):
                if net.get_node(member):
                    net.add_edge(cluster_id, member, label="clustered", color=COLORS["cluster"])

        # Nodi username predetti
        predicted = results.get("predicted_usernames", [])
        for uname in predicted[:8]:  # Mostra max 8 per non affollare
            uid = f"predicted:{uname}"
            net.add_node(
                uid, label=uname,
                title=f"<b>Predicted Username:</b> {uname}",
                color=COLORS["username"], size=12, shape="ellipse"
            )
            net.add_edge(query, uid, label="predicted", color=COLORS["username"], dashes=True)

        try:
            net.write_html(output_file)
            print(f"[+] Grafo OSINT salvato: {output_file} (aprilo nel browser)")
        except Exception as e:
            print(f"[-] Errore durante la generazione del grafo: {e}")
