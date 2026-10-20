extends RefCounted
# Pure simulation: reusable in a stationary puzzle UI. No scene/audio/save access.
const VARIANTS := {
 "Entdecker": {"budget":6,"heat":9,"fuse":24,"surplus":99},
 "Tüftler": {"budget":5,"heat":4,"fuse":18,"surplus":99},
 "Meister": {"budget":5,"heat":3,"fuse":15,"surplus":3}}
const SOURCES := {"sun":{"power":8,"cost":1,"heat":1},"wind":{"power":9,"cost":2,"heat":3},"battery":{"power":6,"cost":3,"heat":0}}
var difficulty := "Tüftler"
var sources := {"sun":false,"wind":false,"battery":false}
var circuits := {"relay":false,"door":false,"lamp":false}

func toggle(key: String) -> bool:
	if sources.has(key): sources[key] = not sources[key]
	elif circuits.has(key): circuits[key] = not circuits[key]
	else: return false
	return true

func evaluate() -> Dictionary:
	var power := 0
	var cost := 0
	var heat := 0
	for key in SOURCES:
		if sources[key]:
			power += SOURCES[key].power
			cost += SOURCES[key].cost
			heat += SOURCES[key].heat
	var demand := (4 if circuits.relay else 0)+(8 if circuits.door else 0)+(3 if circuits.lamp else 0)
	var limits: Dictionary = VARIANTS[difficulty]
	var safe: bool = cost<=limits.budget and heat<=limits.heat and power<=limits.fuse
	var supplied: bool = safe and power>=demand
	var solved: bool = supplied and circuits.relay and circuits.door and power-demand<=limits.surplus
	var message := "Schalte Quellen ein. Relais (4) und Tor (8) brauchen zusammen 12 Energie."
	if cost>limits.budget: message = "Material reicht nicht: %d von %d. Probiere andere Quellen." % [cost,limits.budget]
	elif heat>limits.heat: message = "Zu warm: %d von %d. Der Akku erzeugt keine Wärme." % [heat,limits.heat]
	elif power>limits.fuse: message = "Sicherung schützt die Anlage: %d über %d. Eine Quelle abschalten." % [power,limits.fuse]
	elif power<demand: message = "Es fehlen %d Energie. Mehr erzeugen oder einen Verbraucher abschalten." % (demand-power)
	elif not circuits.relay: message = "Das Relais ist aus. Es steuert das Tor und braucht 4 Energie."
	elif not circuits.door: message = "Das Relais läuft. Schalte jetzt die Torleitung ein."
	elif power-demand>limits.surplus: message = "Zu viel ungenutzte Energie: %d. Höchstens %d erlaubt. Nutze die Werkstattlampe oder andere Quellen." % [power-demand,limits.surplus]
	elif solved: message = "Die Anlage läuft! Das Tor zur Sternwarte ist offen. Geh hinein!"
	return {"power":power,"cost":cost,"heat":heat,"demand":demand,"safe":safe,"supplied":supplied,"solved":solved,"message":message}

func snapshot() -> Dictionary:
	return {"difficulty":difficulty,"sources":sources.duplicate(),"circuits":circuits.duplicate()}

func restore(value: Variant) -> bool:
	# Transactional validation: malformed saves cannot partially mutate a model.
	if not value is Dictionary or not VARIANTS.has(value.get("difficulty", "")): return false
	for field in ["sources","circuits"]:
		if not value.get(field) is Dictionary: return false
		var expected: Dictionary = sources if field=="sources" else circuits
		if value[field].size()!=expected.size(): return false
		for key in expected:
			if not value[field].get(key) is bool: return false
	difficulty = value.difficulty
	sources = value.sources.duplicate()
	circuits = value.circuits.duplicate()
	return true
