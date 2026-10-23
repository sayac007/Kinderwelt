extends "res://tests/qa/speech_playback.gd"
func run() -> void:
 app=load("res://core/quest/main.tscn").instantiate();root.add_child(app)
 app.store.reset();app.store.data.muted=false;app.store.data.music_volume=0;app.store.data.effects_volume=0;app.store.data.voice_volume=1;app.store.data.quest.hero_chosen=true
 app.audio.sync_settings();app.narration.cancel()
 AudioServer.add_bus();var index:=AudioServer.bus_count-1
 AudioServer.set_bus_name(index,"WorldSpeechVerification")
 capture=AudioEffectCapture.new();capture.buffer_length=2
 AudioServer.add_bus_effect(index,capture);app.narration.bus="WorldSpeechVerification"
 for example in [["de","tree"],["en","seabed"],["ru","city"],["de","moon"]]:
  app.store.data.locale=example[0];app.store.data.subject_sceneries.physics=example[1]
  app.hub();app.game_view.switch_subject("physics")
  var hint: String="world_"+example[1]
  check(app.narration.clip=="quest/area_physics" and app.narration.pending_feedback==hint,"World tutorial waits until complete subject announcement")
  await completed(length("area_physics")+length(hint),["quest/area_physics","quest/"+hint],[app.narration.resolve("area_physics",example[0]),app.narration.resolve(hint,example[0])])
  check(not app.audio.music.ducked,"Complete world tutorial restores music")
 app.store.data.voice_auto=false;app.game_view.switch_subject("physics")
 check(not app.narration.playing and app.narration.pending_feedback.is_empty(),"Disabling automatic voice also disables world hints")
 app.store.data.voice_auto=true;app.store.data.muted=true;app.game_view.switch_subject("physics")
 check(not app.narration.playing and app.narration.pending_feedback.is_empty(),"Mute also disables queued world tutorials")
 app.narration.cancel();app.audio.music.shutdown();app.audio.stop();app.free();AudioServer.remove_bus(index)
 var output:=OS.get_environment("KINDERWELT_WORLD_SPEECH_REPORT")
 if output.is_empty():output="res://qa-results/world-speech.json"
 FileAccess.open(output,FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"scope":"Actual desktop mixer and complete scene hints; no human listening or Android speaker claim","results":results},"  "))
 print("WORLD SPEECH: ",checks," checks, ",failures," failures")
 await create_timer(.2).timeout
 quit(1 if failures else 0)
