#!/usr/bin/env bash
# usage: bash mix.sh PROJECT_DIR STYLE [1=with music|0=no music]
# MUSIC_DB=-8 sets the bed level before ducking (default -12)
# voice chain -> duck music under voice -> add sfx -> two-pass linear loudnorm to -14 LUFS / -1.5 dBTP
set -e; P=$1; ST=$2; MUS=${3:-1}; HERE=$(cd "$(dirname "$0")" && pwd); cd "$P"
ffmpeg -v error -y -i voice.wav -af "$(cat $HERE/voice_chain.txt)" -ar 48000 voice_proc.wav
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 voice.wav)
if [ "$MUS" = 1 ]; then
FC="[0:a]pan=stereo|c0=c0|c1=c0,asplit[v][vk];[1:a]volume=${MUSIC_DB:--12}dB[m];[m][vk]sidechaincompress=threshold=0.04:ratio=3:attack=40:release=380:makeup=1[md];[2:a]volume=-3dB[s];[v][md][s]amix=inputs=3:normalize=0:duration=first"; OUT=mix_$ST.wav
else
FC="[0:a]pan=stereo|c0=c0|c1=c0[v];[2:a]volume=-3dB[s];[v][s]amix=inputs=2:normalize=0:duration=first"; OUT=mix_${ST}_nomusic.wav
fi
ffmpeg -v error -y -i voice_proc.wav -i music.wav -i sfx_$ST.wav -filter_complex "$FC" -ar 48000 pre.wav
J=$(ffmpeg -hide_banner -i pre.wav -af loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i pre.wav -af "loudnorm=I=-14:TP=-1.5:LRA=9:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true" -ar 48000 $OUT
ffmpeg -hide_banner -i $OUT -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | grep -E "I:|Peak:" | tr -s ' ' | tr '\n' ' '; echo " -> $P/$OUT"
