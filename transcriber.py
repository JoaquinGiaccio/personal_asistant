import whisper

def load_model(model):
    
    model_used = whisper.load_model(model)

    return model_used

def get_language(model, audio_file):

    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    #print(f"Detected language: {max(probs, key=probs.get)}")
    lang_set = {max(probs, key=probs.get)}
    
    for i in lang_set:
        lang = str(i)

    return lang, mel

def transcriber(model, mel):

    # decode the audio
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)

    transcription = result.text

    return transcription
