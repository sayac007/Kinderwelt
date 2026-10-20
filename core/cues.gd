extends AudioStreamPlayer
# Original synthesized tones; no recording, speech engine or network.
func cue(success: bool = false, tone: int = -1) -> void:
	stop()
	var wav := AudioStreamWAV.new()
	wav.format = AudioStreamWAV.FORMAT_16_BITS
	wav.mix_rate = 22050
	var bytes := PackedByteArray()
	var duration := 0.35 if success else 0.18
	for i in range(int(22050 * duration)):
		var t := float(i) / 22050.0
		var frequency := 440.0 * pow(2.0, clampi(tone, 0, 7) / 12.0) if tone >= 0 else (660.0 if success else 440.0)
		var sample := int(sin(TAU * frequency * t) * 6000 * (1.0 - t / duration))
		bytes.append(sample & 255)
		bytes.append((sample >> 8) & 255)
	wav.data = bytes
	stream = wav
	play()

func _exit_tree() -> void:
	stop()
	stream = null
