CODEC_MAP = {
    'mp4': ['-c:v', 'libx264', '-c:a', 'aac'],
    'webm': ['-c:v', 'libvpx', '-c:a', 'libvorbis'],
    'avi': ['-c:v', 'mpeg4', '-c:a', 'mp3'],
    'mov': ['-c:v', 'prores', '-c:a', 'pcm_s16le'],
    'flv': ['-c:v', 'libx264', '-c:a', 'aac'],
    'mkv': ['-c:v', 'libx264', '-c:a', 'aac'],
}