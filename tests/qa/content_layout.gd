extends SceneTree
## Measure every generated heading with the shipping font, not character counts.
## Portrait/landscape minima and both supported text sizes mirror task.gd.
func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://games/quest/tasks.json"))
	var heading := Label.new()
	root.add_child(heading)
	heading.add_theme_font_override("font",load("res://assets/quest/Nunito.ttf"))
	heading.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	var failures: Array = []
	var checks := 0
	for parent in data.tasks:
		for task in [parent,parent.bonuses[0],parent.bonuses[1]]:
			for locale in ["de","en","ru"]:
				for scale in [1.0,1.15]:
					heading.add_theme_font_size_override("font_size",roundi((18 if task.kind == "discovery" else 20)*scale))
					heading.text = task.texts[locale].prompt
					for profile in [{"width":280,"lines":6},{"width":760,"lines":3}]:
						heading.size = Vector2(profile.width,0)
						checks += 1
						if heading.get_line_count() > profile.lines:
							failures.append({"id":task.id,"locale":locale,"scale":scale,"width":profile.width,"lines":heading.get_line_count()})
	DirAccess.make_dir_recursive_absolute("res://qa-results")
	var report := FileAccess.open("res://qa-results/content-layout.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"scope":"Heading wrapping only; no manual visual or device approval"},"  ")+"\n")
	report.close()
	heading.free()
	print("Content heading layout: ",checks," measurements; ",failures.size()," overflows")
	quit(0 if failures.is_empty() else 1)
