"""
Username Predictor Module
Data un'email, predice username probabili da cercare sui social.
Usa pattern analysis e euristica, nessuna dipendenza ML pesante.
"""
import re


class UsernamePredictor:
    def predict(self, email: str) -> list:
        """
        Genera una lista di username probabili a partire da un'email.
        Gestisce sia email con separatori (salvatore.scribano2004@gmail.com)
        che senza (salvatorescribano2004@gmail.com).
        """
        if "@" not in email:
            return []

        local = email.split("@")[0].lower()
        candidates = set()

        # Sempre includi il local part originale
        candidates.add(local)

        # Estrai parti con separatori espliciti
        parts = re.split(r'[._\-+]', local)
        words = [p for p in parts if p and not p.isdigit()]
        numbers = re.findall(r'\d+', local)
        year = numbers[0] if numbers else ""

        # Se ci sono separatori: combinazioni standard
        if len(parts) > 1:
            if len(words) >= 2:
                candidates.add("".join(words))
                candidates.add("_".join(words))
                candidates.add(".".join(words))
                candidates.add(words[0][0] + words[1])
                candidates.add(words[0][0] + "_" + words[1])
                candidates.add(words[0] + words[1][0])
            if year:
                for w in words:
                    candidates.add(w + year)
                if len(words) >= 2:
                    candidates.add("".join(words) + year)
                    candidates.add(words[0] + "_" + words[1] + year)
        else:
            # Nessun separatore: euristica su confini anno (es. salvatorescribano2004)
            # Estrai la parte numerica finale (anno)
            m = re.match(r'^([a-z]+?)(\d{2,4})$', local)
            if m:
                text_part, num_part = m.group(1), m.group(2)
                candidates.add(text_part)
                candidates.add(text_part + num_part)
                candidates.add(text_part + "_" + num_part)
                # Prova a spezzare la parte testuale in nome+cognome
                # (se è lunga abbastanza — minimo 8 char)
                if len(text_part) >= 8:
                    mid = len(text_part) // 2
                    for split_at in range(max(3, mid - 2), min(len(text_part) - 3, mid + 4)):
                        nome    = text_part[:split_at]
                        cognome = text_part[split_at:]
                        candidates.add(nome)
                        candidates.add(cognome)
                        candidates.add(nome + cognome)
                        candidates.add(nome + "_" + cognome)
                        candidates.add(nome + "." + cognome)
                        candidates.add(nome[0] + cognome)
                        candidates.add(nome + cognome + num_part)
                        candidates.add(nome + "_" + cognome + num_part)
            else:
                # Nessun numero finale: prova split al punto mediano
                if len(local) >= 8:
                    mid = len(local) // 2
                    for split_at in range(max(3, mid - 2), min(len(local) - 3, mid + 4)):
                        candidates.add(local[:split_at])
                        candidates.add(local[split_at:])

        # Pulizia: rimuovi troppo corti, ridondanti o con caratteri strani
        candidates = {c for c in candidates if len(c) >= 3 and re.match(r'^[\w.\-\|!]+$', c)}

        return sorted(candidates)
