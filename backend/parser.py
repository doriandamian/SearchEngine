
class Parser:
    def parseQuery(query: str):
        qualifiers = {}
        for part in query.strip().split():
            if ':' in part:
                key, value = part.split(':', 1)
                if key in qualifiers:
                    qualifiers[key].append(value.lower())
                else:
                    qualifiers[key] = [value.lower()]
        return qualifiers
    