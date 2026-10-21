extends RefCounted
const ITEMS := {
 "wiener_blut": {
  "title": "Wiener Blut",
  "composer": "J. Strauss II",
  "detail": "Walzerauszug",
  "path": "res://assets/music/wiener_blut.ogg",
  "color": "e9bd60",
  "icon": "sun"
 },
 "babbino": {
  "title": "O mio babbino caro",
  "composer": "G. Puccini",
  "detail": "Themenauszug",
  "path": "res://assets/music/babbino.ogg",
  "color": "ddb4ba",
  "icon": "leaf"
 },
 "french_song": {
  "title": "Altes französisches Lied",
  "composer": "P. I. Tschaikowski",
  "detail": "Klavier",
  "path": "res://assets/music/french_song.ogg",
  "color": "b8bfdc",
  "icon": "moon"
 },
 "consolation": {
  "title": "Consolation Nr. 1",
  "composer": "F. Liszt",
  "detail": "Klavier",
  "path": "res://assets/music/consolation.ogg",
  "color": "bed39a",
  "icon": "leaf"
 },
 "elise": {
  "title": "Für Elise",
  "composer": "L. v. Beethoven",
  "detail": "Klavier",
  "path": "res://assets/music/elise.ogg",
  "color": "e9bd60",
  "icon": "leaf"
 },
 "bach_prelude": {
  "title": "Präludium C-Dur · BWV 846",
  "composer": "J. S. Bach",
  "detail": "Klavier",
  "path": "res://assets/music/bach_prelude.ogg",
  "color": "ddb4ba",
  "icon": "moon"
 },
 "gymnopedie": {
  "title": "Gymnopédie Nr. 1",
  "composer": "E. Satie",
  "detail": "Klavier",
  "path": "res://assets/music/gymnopedie.ogg",
  "color": "b8bfdc",
  "icon": "sun"
 },
 "clair": {
  "title": "Clair de lune",
  "composer": "C. Debussy",
  "detail": "Klavier",
  "path": "res://assets/music/clair.ogg",
  "color": "bed39a",
  "icon": "leaf"
 },
 "nocturne": {
  "title": "Nocturne · Op. 9 Nr. 2",
  "composer": "F. Chopin",
  "detail": "Klavier",
  "path": "res://assets/music/nocturne.ogg",
  "color": "e9bd60",
  "icon": "moon"
 },
 "traeumerei": {
  "title": "Träumerei · Op. 15 Nr. 7",
  "composer": "R. Schumann",
  "detail": "Klavier",
  "path": "res://assets/music/traeumerei.ogg",
  "color": "ddb4ba",
  "icon": "sun"
 },
 "mozart_sonata": {
  "title": "Sonata facile · Allegro",
  "composer": "W. A. Mozart",
  "detail": "Klavier",
  "path": "res://assets/music/mozart_sonata.ogg",
  "color": "b8bfdc",
  "icon": "leaf"
 },
 "arabesque": {
  "title": "Arabesque Nr. 1",
  "composer": "C. Debussy",
  "detail": "Klavier",
  "path": "res://assets/music/arabesque.ogg",
  "color": "bed39a",
  "icon": "moon"
 },
 "brahms_waltz": {
  "title": "Walzer · Op. 39 Nr. 15",
  "composer": "J. Brahms",
  "detail": "Klavier",
  "path": "res://assets/music/brahms_waltz.ogg",
  "color": "e9bd60",
  "icon": "sun"
 },
 "canon": {
  "title": "Kanon in D",
  "composer": "J. Pachelbel",
  "detail": "Klavier",
  "path": "res://assets/music/canon.ogg",
  "color": "ddb4ba",
  "icon": "leaf"
 },
 "impromptu": {
  "title": "Impromptu · D 899 Nr. 3",
  "composer": "F. Schubert",
  "detail": "Klavier",
  "path": "res://assets/music/impromptu.ogg",
  "color": "b8bfdc",
  "icon": "moon"
 },
 "invention": {
  "title": "Invention Nr. 1 · BWV 772",
  "composer": "J. S. Bach",
  "detail": "Klavier",
  "path": "res://assets/music/invention.ogg",
  "color": "bed39a",
  "icon": "sun"
 },
 "chopin_prelude": {
  "title": "Prélude e-Moll · Op. 28 Nr. 4",
  "composer": "F. Chopin",
  "detail": "Klavier",
  "path": "res://assets/music/chopin_prelude.ogg",
  "color": "e9bd60",
  "icon": "leaf"
 },
 "minuet": {
  "title": "Menuett G-Dur · BWV Anh. 114",
  "composer": "C. Petzold",
  "detail": "Klavier",
  "path": "res://assets/music/minuet.ogg",
  "color": "ddb4ba",
  "icon": "moon"
 },
 "turca": {
  "title": "Rondo alla turca",
  "composer": "W. A. Mozart",
  "detail": "Klavier",
  "path": "res://assets/music/turca.ogg",
  "color": "b8bfdc",
  "icon": "sun"
 },
 "moonlight": {
  "title": "Mondscheinsonate · Adagio sostenuto",
  "composer": "L. v. Beethoven",
  "detail": "Klavier",
  "path": "res://assets/music/moonlight.ogg",
  "color": "bed39a",
  "icon": "leaf"
 }
}
const DEFAULT := "wiener_blut"
const WORLDS := {"math":"wiener_blut","german":"babbino","logic":"french_song","success":"consolation"}
static func resolve(world: String) -> String:
	return WORLDS.get(world,world)
static func next(id: String,direction := 1,shuffle := false,repeat := false) -> String:
	var ids := ITEMS.keys()
	if repeat and ITEMS.has(id): return id
	if shuffle and direction>0:
		ids.erase(id)
		return ids.pick_random()
	return ids[posmod(ids.find(id)+direction,ids.size())]
