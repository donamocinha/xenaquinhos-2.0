from domain import TonalSystem, Scale, TonalSystemElement, transpose_to_octave
from scamp import Session, TimeSignature, wait
import random as rd

size = 20
g = 11
max_port = 3

#TODO: PASSAR PITCH ATRAVÉS DE UM MÉTODO PITCH - OBJETO PITCH? TORNAR OBJETO TONAL SYSTEM ELEMENT "PÚBLICO"?
#TENTATIVA DE MÚSICA "ATONAL"
z = TonalSystem(size)
z.set_generator(g)
diagram = z.balzano_diagram(5,6)
diagram.show()
midi_classes = z.get_midi_pitch_classes()
bass_octave = transpose_to_octave(midi_classes, 1)
guitar_octave = transpose_to_octave(midi_classes, 2)
flute_octave = transpose_to_octave(midi_classes, 4)

def build_melody(m_size, s_size, max_port):
    initial = rd.randint(int(s_size/3), int(s_size*2/3))
    melody = [initial]
    for _ in range(m_size-1):
        melody.append(melody[-1] + rd.randint(-max_port, max_port))
    return melody

def build_arpeggio(s_size, base_note, last_notes, max_port):
    return [base_note, last_notes[0]+rd.randint(-max_port, max_port), last_notes[1]+rd.randint(-max_port, max_port)] *2

def play_part(inst, pitches, octave):
    for i in range(len(pitches[0])):
        choice = 0 if len(pitches)!=2 else rd.choice([0,1])
        p = pitches[choice][i]
        real_pitch = octave[p] if p<size else octave[p%size]+size
        inst.play_note(real_pitch, 0.8, 8/len(pitches[0]))

bass_melody = build_melody(4, size, max_port)

last_notes = [bass_melody[0] + int((g+1)/2), bass_melody[0]+g]
guitar_chords = ([bass_melody[0]] + last_notes) *2
for b in bass_melody[1:]:
    guitar_chords += build_arpeggio(size, b, guitar_chords[-2:], max_port)

flute_melody = build_melody(8, size, max_port)
flute_melody_2 = build_melody(8, size, max_port)

melodies = [[bass_melody], [guitar_chords], [flute_melody, flute_melody_2]]
octaves = [bass_octave, guitar_octave, flute_octave]

'''
s = Session()
s.print_default_soundfont_presets()
[print(m) for m in melodies]
parts = [s.new_part('fingered bass'), s.new_part('guitar'), s.new_part('clarinet')]
s.start_transcribing()
for i in range(8):
    [s.fork(play_part, args=[p, melodies[i], octaves[i]]) for i, p in enumerate(parts)]
    s.wait_for_children_to_finish()
performance = s.stop_transcribing()
'''