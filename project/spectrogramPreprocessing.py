from pydub import AudioSegment
# This requires ffmpeg!!!

import matplotlib.pyplot as plt
from scipy.io import wavfile
from tempfile import mktemp



# A significant poriton of this comes from https://stackoverflow.com/questions/15311853/plot-spectogram-from-mp3 

# mp3_audio = AudioSegment.from_file('./data/kaggle_debate/us_election_2020_vice_presidential_debate.mp3', format="mp3")  # read mp3
# mp3_audio = AudioSegment.from_file('./data/kaggle_debate/us_election_2020_1st_presidential_debate.mp3', format="mp3")  # read mp3

mp3_audio = AudioSegment.from_file('./data/kaggle_debate/us_election_2020_2nd_presidential_debate.mp3', format="mp3")  # read mp3

print("data loaded")
# mp3_audio = pyaudio.
# mp3_audio = sa.WaveObject.from_wave_file(".\data\kaggle_debate")
wname = mktemp('.wav')  # use temporary file
print("makes copy")
mp3_audio.export(wname, format="wav")  # convert to wav
print("at this step....")
FS, data = wavfile.read(wname)  # read wav file
print(FS)
# data = data + 0.001
print("next is spect plot")


for i in range(0,len(data),882000):
    if (i + 882000) >= len(data)-1:
        end = len(data)-1
    else :
        end = i + 882000
    #Plot
    plt.figure(figsize=(28.00,4.80))                           
    plt.specgram(data[i:end,0], Fs=FS, NFFT=1024, noverlap=128, cmap='gray')
    plt.ylim((0,5000))
    plt.xlabel('Time in Seconds')
    plt.ylabel('Frequency in Hz')
    plt.title('Debate Spectrogram')
    time = int(i/44100)
    plt.savefig(f'./data/spectrograms/p2Debate{time}.jpg', format='jpg') #jpg was the best choice
    #i = end
    if (i + 882000) >= len(data)-1:
        break
    print(i)





mp3_audio = AudioSegment.from_file('./data/kaggle_debate/us_election_2020_1st_presidential_debate.mp3', format="mp3")  # read mp3


print("data loaded")
wname = mktemp('.wav')  # use temporary file
print("makes copy")
mp3_audio.export(wname, format="wav")  # convert to wav
print("at this step....")
FS, data = wavfile.read(wname)  # read wav file
print(FS)
# data = data + 0.001
print("next is spect plot")


for i in range(0,len(data),882000):
    if (i + 882000) >= len(data)-1:
        end = len(data)-1
    else :
        end = i + 882000
    #Plot
    plt.figure(figsize=(28.00,4.80))                           
    plt.specgram(data[i:end,0], Fs=FS, NFFT=1024, noverlap=128, cmap='gray')
    plt.ylim((0,5000))
    plt.xlabel('Time in Seconds')
    plt.ylabel('Frequency in Hz')
    plt.title('Debate Spectrogram')
    time = int(i/44100)
    plt.savefig(f'./data/spectrograms/pDebate{time}.jpg', format='jpg') #jpg was the best choice
    #i = end
    if (i + 882000) >= len(data)-1:
        break
    print(i)



mp3_audio = AudioSegment.from_file('./data/kaggle_debate/us_election_2020_vice_presidential_debate.mp3', format="mp3")  # read mp3


print("data loaded")
wname = mktemp('.wav')  # use temporary file
print("makes copy")
mp3_audio.export(wname, format="wav")  # convert to wav
print("at this step....")
FS, data = wavfile.read(wname)  # read wav file
print(FS)
# data = data + 0.001
print("next is spect plot")


for i in range(0,len(data),882000):
    if (i + 882000) >= len(data)-1:
        end = len(data)-1
    else :
        end = i + 882000
    #Plot
    plt.figure(figsize=(28.00,4.80))                           
    plt.specgram(data[i:end,0], Fs=FS, NFFT=1024, noverlap=128, cmap='gray')
    plt.ylim((0,5000))
    plt.xlabel('Time in Seconds')
    plt.ylabel('Frequency in Hz')
    plt.title('Debate Spectrogram')
    time = int(i/44100)
    plt.savefig(f'./data/spectrograms/vpDebate{time}.jpg', format='jpg') #jpg was the best choice
    #i = end
    if (i + 882000) >= len(data)-1:
        break
    print(i)


