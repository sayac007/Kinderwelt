extends SceneTree
# Capture the actual Godot audio bus, not only an Ogg header or a timer mock.
var failures := 0
var checks := 0
var results := []
var capture: AudioEffectCapture
var app: Control
func check(value: bool,message: String) -> void:
 checks+=1
 if not value:failures+=1;push_error(message)
func _initialize() -> void:call_deferred("run")
func drain() -> Dictionary:
 var samples:=capture.get_buffer(capture.get_frames_available())
 var peak:=0.0
 for frame in samples:peak=maxf(peak,maxf(absf(frame.x),absf(frame.y)))
 return {"frames":samples.size(),"peak":peak}
func completed(expected_seconds: float,ids: Array[String],expected_paths: Array[String]=[]) -> void:
 capture.clear_buffer()
 var frames:=0;var peak:=0.0
 var seen: Array[String]=[]
 var paths: Array[String]=[]
 var start:=Time.get_ticks_msec()
 while app.narration.playing or not app.narration.queue.is_empty() or not app.narration.pending_feedback.is_empty() or not app.narration.clip.is_empty():
  if not app.narration.clip.is_empty() and app.narration.clip not in seen:seen.append(app.narration.clip)
  if app.narration.stream!=null:
   var path: String=app.narration.stream.resource_path
   if paths.is_empty() or paths[-1]!=path:paths.append(path)
  await process_frame
  var block:=drain();frames+=block.frames;peak=maxf(peak,block.peak)
  if Time.get_ticks_msec()-start>int((expected_seconds+3)*1000):
   check(false,"Speech playback timed out");app.narration.cancel();break
 var elapsed:=(Time.get_ticks_msec()-start)/1000.0
 # The mixer may buffer a fraction of a second; allow its documented latency.
 check(elapsed>=expected_seconds-.25,"Actual playback preserves the complete duration: "+str(ids))
 check(float(frames)/AudioServer.get_mix_rate()>=expected_seconds-.35,"Audio bus contains the complete recording sequence")
 check(peak>.01,"Audio bus contains audible speech, not just silence")
 for id in ids:check(id in seen,"Actual playback reaches "+id)
 if not expected_paths.is_empty():check(paths==expected_paths,"Actual recording order matches localized instruction, German target and feedback")
 results.append({"stream_paths":paths,"locale":app.store.data.locale,"expected_seconds":expected_seconds,"elapsed_seconds":elapsed,"captured_seconds":float(frames)/AudioServer.get_mix_rate(),"peak":peak,"clips":seen})
func length(id: String) -> float:
 var stream: AudioStream=load(app.narration.resolve(id,app.store.data.locale))
 return stream.get_length()
func run() -> void:
 app=load("res://core/quest/main.tscn").instantiate();root.add_child(app)
 app.store.reset();app.store.data.muted=false;app.store.data.music_volume=0;app.store.data.effects_volume=0;app.store.data.voice_volume=1;app.store.data.quest.hero_chosen=true
 app.audio.sync_settings();app.narration.cancel()
 AudioServer.add_bus()
 var index:=AudioServer.bus_count-1
 AudioServer.set_bus_name(index,"SpeechVerification")
 capture=AudioEffectCapture.new();capture.buffer_length=2
 AudioServer.add_bus_effect(index,capture)
 app.narration.bus="SpeechVerification"
 for locale in ["de","en","ru"]:
  app.store.data.locale=locale;app.hub()
  app.game_view.switch_subject("physics")
  await completed(length("area_physics"),["quest/area_physics"])
  app.praise_cursor=1
  app.game_view.open_task(0)
  var id: String=app.game_view.task_panel.task.id
  app.game_view.task_panel.answer(app.game_view.task_panel.task.answer)
  check(app.narration.pending_feedback=="praise_1","Quick answer queues praise instead of cutting off the instruction")
  await completed(length(id)+length("praise_1"),["quest/"+id,"quest/praise_1"])
  app.game_view.close_task()
 app.narration.cancel();app.audio.music.shutdown();app.audio.stop();app.free()
 AudioServer.remove_bus(index)
 var output:=OS.get_environment("KINDERWELT_SPEECH_REPORT")
 if not output.is_empty():FileAccess.open(output,FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"scope":"Actual desktop Godot mixer capture; no Android speaker or human listening claim","results":results},"  "))
 print("SPEECH PLAYBACK: ",checks," checks, ",failures," failures")
 await create_timer(.2).timeout
 quit(0 if failures==0 else 1)
