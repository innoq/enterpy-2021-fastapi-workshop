# TODO: Einen eigenen APIRouter erzeugen
#  Erzeuge einen APIRouter der Anfragen auf dem Pfad '/keys' entgegen nimmt

# TODO: GET-Request mit Query-Parametern beantworten
#  Liefere auf dem Pfad '/' des APIRouters die Liste 'all_keys' zurück.
#  Werte dabei den Query-Parameter 'limit' aus. Ist er gesetzt liefere nur n-Datensätze aus 'all_keys'
#  zurück, wobei n = 'limit' (Wert des Query-Parameters).

# TODO: GET-Request mit Pah-Parametern beantworten
#  Liefere auf dem Pfad '/{country}' des APIRouters nur Datensätze aus der Liste 'all_keys' zurück,
#  bei denen 'origin' == {country} (Wert des Path-Parameters)

# Wird vom Test automatisch befüllt. Nicht ändern!
# Einträge sind Dicts in der Form {id: '...', origin: '...', timestamp: '...'}
all_keys = []
