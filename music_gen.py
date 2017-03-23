import random
import midi
from collections import namedtuple

Node = namedtuple('Node', ['state', 'cost', 'action_path', 'node_index'])

NOTE_VELOCITY = 50
NOTE_DURATION = [110, 220, 440]

def get_initial_state():
    """
    Start at middle C
    """
    note = midi.C_5
    index = notes.index(note)
    return Node(note, 0, [note], index)


def evaluate(prev_node, nodes):
    """
    Try to pick the node with the lowest non zero distance away from previous

    NOTE: Problem if the first node is 0 distance
    """
    best = nodes[0]
    best_index = abs(best.node_index - prev_node.node_index)
    for n in nodes:
        node_diff = abs(n.node_index - prev_node.node_index)
        if node_diff < best_index and node_diff > 0:
            best = n
            best_index = node_diff

    return best



def get_successor_node(node):
    """
    Pick a random note up to 8 positions above or below the current note
    """
    index = random.randint(0, 8)
    test = random.randint(0, 1)
    if test == 0:
        index = node.node_index + index
        if index > len(notes) - 1:
            index = len(notes) -1
        note = notes[index]
    elif test == 1:
        index = node.node_index - index
        if index < 0:
            index = 0
        note = notes[index]
    return Node(note, node.cost + 1, node.action_path + [note], index)


def get_rand_duration():
    """
    This just randomly picks between eigth, quarter, and whole notes to add some
    variety
    """
    prob = random.randint(0, 100)
    if prob < 60:
        return 1
    elif prob < 90:
        return 2
    else:
        return 0



def test():
    """
    Make music!
    """
    initial = get_initial_state()
    node = get_successor_node(initial)
    for i in range(220):
        test_nodes = []
        for i in range(1000):
            test_nodes.append(get_successor_node(node))

        node = evaluate(node, test_nodes)

    pattern = midi.Pattern()
    pattern.make_ticks_abs()
    track = midi.Track()
    pattern.append(track)

    for note in node.action_path:
        on = midi.NoteOnEvent(tick=0, velocity=NOTE_VELOCITY, pitch=note)
        off = midi.NoteOffEvent(tick=NOTE_DURATION[get_rand_duration()], pitch=note)
        track.append(on)
        track.append(off)

    eot = midi.EndOfTrackEvent(tick=1)
    track.append(eot)
    print(pattern)
    midi.write_midifile("example.mid", pattern)


if __name__ == '__main__':

    # INFO: This is because I'm lazy as fuck
    a_notes = [midi.A_0, midi.A_1, midi.A_2, midi.A_3, midi.A_4, midi.A_5, midi.A_6, midi.A_7, midi.A_8, midi.A_9]
    b_notes = [midi.B_0, midi.B_1, midi.B_2, midi.B_3, midi.B_4, midi.B_5, midi.B_6, midi.B_7, midi.B_8, midi.B_9]
    c_notes = [midi.C_0, midi.C_1, midi.C_2, midi.C_3, midi.C_4, midi.C_5, midi.C_6, midi.C_7, midi.C_8, midi.C_9]
    d_notes = [midi.D_0, midi.D_1, midi.D_2, midi.D_3, midi.D_4, midi.D_5, midi.D_6, midi.D_7, midi.D_8, midi.D_9]
    e_notes = [midi.E_0, midi.E_1, midi.E_2, midi.E_3, midi.E_4, midi.E_5, midi.E_6, midi.E_7, midi.E_8, midi.E_9]
    f_notes = [midi.F_0, midi.F_1, midi.F_2, midi.F_3, midi.F_4, midi.F_5, midi.F_6, midi.F_7, midi.F_8, midi.F_9]
    g_notes = [midi.G_0, midi.G_1, midi.G_2, midi.G_3, midi.G_4, midi.G_5, midi.G_6, midi.G_7, midi.G_8, midi.G_9]

    notes = []
    for i in range(9):
        if i < len(a_notes) - 1:
            notes.append(a_notes[i])
        if i < len(b_notes) - 1:
            notes.append(b_notes[i])
        if i < len(c_notes) - 1:
            notes.append(c_notes[i])
        if i < len(d_notes) - 1:
            notes.append(d_notes[i])
        if i < len(e_notes) - 1:
            notes.append(e_notes[i])
        if i < len(f_notes) - 1:
            notes.append(f_notes[i])
        if i < len(g_notes) - 1:
            notes.append(g_notes[i])

    test()