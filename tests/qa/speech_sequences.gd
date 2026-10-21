extends "res://tests/qa/speech_playback.gd"
# Capture every actual recording in multilingual learning sequences.
func sequence_paths(id: String) -> Array[String]:
 var paths: Array[String]=[app.narration.resolve(id,app.store.data.locale)]
 if app.store.data.locale!="de":paths.append(app.narration.resolve(id,"de"))
 paths.append(app.narration.resolve("praise_1",app.store.data.locale))
 return paths
func total_length(paths: Array[String]) -> float:
 var seconds:=0.0
 for path in paths:
  var stream: AudioStream=load(path)
  seconds+=stream.get_length()
 return seconds
func run() -> void:
 app=load("res://core/quest/main.tscn").instantiate();root.add_child(app)
 app.store.reset();app.store.data.muted=false;app.store.data.music_volume=0;app.store.data.effects_volume=0;app.store.data.voice_volume=1;app.store.data.quest.hero_chosen=true
 app.audio.sync_settings();app.narration.cancel()
 AudioServer.add_bus()
 var index:=AudioServer.bus_count-1
 AudioServer.set_bus_name(index,"SequenceVerification")
 capture=AudioEffectCapture.new();capture.buffer_length=2
 AudioServer.add_bus_effect(index,capture);app.narration.bus="SequenceVerification"
 for locale in ["de","en","ru"]:
  app.store.data.locale=locale
  for id in ["german_sun","german_robot_hint"]:
   var paths:=sequence_paths(id)
   check(app.narration.play_clip("quest/"+id),"Native German question or syllable hint loads")
   app.narration.speak_feedback("quest/praise_1")
   check(app.narration.pending_feedback=="praise_1","Fast response preserves every remaining native target")
   await completed(total_length(paths),["quest/"+id,"quest/praise_1"],paths)
   check(not app.audio.music.ducked,"Music restores only after the complete learning sequence")
 # Exercise the same notifications Android sends, using the real desktop mixer.
 app.store.data.locale="de"
 app.narration.play_clip("quest/area_physics")
 await create_timer(.15).timeout
 app.narration._notification(Node.NOTIFICATION_APPLICATION_PAUSED)
 var paused_position: float=app.narration.get_playback_position()
 await create_timer(.35).timeout
 check(app.narration.stream_paused,"Application pause suspends narration")
 check(absf(app.narration.get_playback_position()-paused_position)<.08,"Pause does not consume spoken word duration")
 app.narration._notification(Node.NOTIFICATION_APPLICATION_RESUMED)
 check(not app.narration.stream_paused,"Resume unpauses narration")
 await completed(maxf(.1,length("area_physics")-paused_position),["quest/area_physics"],[app.narration.resolve("area_physics","de")])
 app.store.data.locale="ru"
 app.narration.play_clip("quest/german_sun")
 app.narration.speak_feedback("quest/praise_1")
 app.store.data.muted=true;app.narration.sync_settings()
 check(not app.narration.playing and app.narration.stream==null,"Mute stops the actual stream")
 check(app.narration.queue.is_empty() and app.narration.pending_feedback.is_empty(),"Mute clears native targets and queued feedback")
 check(not app.audio.music.ducked,"Mute releases music ducking")
 app.store.data.muted=false
 check(app.narration.play_clip("quest/area_physics"),"Manual repeat works after unmute")
 app.narration.cancel();app.audio.music.shutdown();app.audio.stop();app.free()
 AudioServer.remove_bus(index)
 var output:=OS.get_environment("KINDERWELT_SEQUENCE_REPORT")
 if not output.is_empty():FileAccess.open(output,FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"scope":"Actual desktop mixer; simulated application notifications, no Android device or human listening claim","results":results},"  "))
 print("SPEECH SEQUENCES: ",checks," checks, ",failures," failures")
 await create_timer(.2).timeout
 quit(0 if failures==0 else 1)
