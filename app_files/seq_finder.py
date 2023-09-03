
def process_centers(centers, img_dims):
    hflag = False
    if img_dims[1]>img_dims[0]:
        hflag = True
    scores = []
    if hflag == True:
        for center in centers:
            score = center[0]*img_dims[0]
            scores.append(score)
    else:
        for center in centers:
            score = center[1]*img_dims[1]
            scores.append(score)
    return scores

def init_seq(img_dims, red_centers, pink_centers, blue_centers):
    scores = []
    sequence = []
    seq_string = ''
    if pink_centers != []:
        ps = process_centers(pink_centers, img_dims)
        for i in range(len(ps)):
            sequence.append('P')
            seq_string+= 'P'
        for val in ps:
            scores.append(val)

    if red_centers != []:
        rs = process_centers(red_centers, img_dims)
        for i in range(len(rs)):
            sequence.append('R')
            seq_string += 'R'
        for val in rs:
            scores.append(val)

    if blue_centers != []:
        bs = process_centers(blue_centers, img_dims)
        for i in range(len(bs)):
            sequence.append('B')
            seq_string += 'B'
        for val in bs:
            scores.append(val)

    print('init sequence', sequence)
    return seq_string, sequence, scores
    #   bubble sort implementation (couldn't use the inbuilt sort() function 
    #   because of the operation required to be done to the sequence string)

def sort_seq(scores, sequence, img_dims):
    n = len(scores)

    for i in range(n):
        swapped = False

        for j in range(0, n-i-1):

            if scores[j] > scores[j+1]:
                scores[j], scores[j+1] = scores[j+1], scores[j]
                sequence[j], sequence[j+1] = sequence[j+1], sequence[j]
                # seq_string[j], seq_string[j+1] = seq_string[j+1], seq_string[j]
                swapped = True
        if (swapped == False):
            break
    seq_string_temp = ''.join(sequence)

    distances = []
    for i in range(1, len(scores)):
        distances.append(scores[i]-scores[i-1])
    
    dist_thresh_max = max(img_dims[0], img_dims[1])/3.5
    
    chk_gap = [i for i, dist in enumerate(distances) if dist > dist_thresh_max]
    if chk_gap != []:
        for ind in chk_gap:
            seq_string = ' '.join([seq_string_temp[:ind], seq_string_temp[ind:]])
    else:
        seq_string = seq_string_temp
    print('sorted sequence: ', sequence)
    print('sorted sequence string: ', seq_string)
    print('sorted scores: ', scores)
    return sequence, seq_string

def find_type(sequence, seq_string):
    
    # classifier_key = {
    #     'normal'    : [['B','B','R','R'], ['R','R','B','B']],
    #     'cco'       : [['R','B','R','B'], ['B','R','B','R'], ['B','R','R','B'], ['R','B','B','R']],
    #     'mi_ndj'    : [['B','R'], ['R', 'B'],['P', 'P'], ['P']],
    #     'mi_rs'     : [['R','B','P'], ['B','R','P'], ['P','R','B'], ['P','B','R']],
    #     'mi_pssc'   : [['R','B','B'], ['B','R','B'], ['R','B','R'], ['B','B','R'], ['B','R','R'], ['R','R','B'],['R','P','B'],['B','P','R']],
    #     'mii_pssc'  : [['R','B'], ['B','R']]
    # }
    string_class_key = {
        'normal'    : ['BBRR', 'RRBB','RR BB','BB RR'],
        'cco'       : ['RBRB', 'BRBR', 'BRRB', 'RBBR'],
        'mi_ndj'    : ['RB ', 'BR ','PP ', 'P'],
        'mi_rs'     : ['RB P', 'BRP', 'PRB', 'PBR', 'RBP', 'BR P', 'P RB', 'P BR'],
        'mi_pssc'   : ['RBB','RB B','R BB', 'BRB','BR B','B RB','RBR','RB R','R BR', 'BBR','B BR','BB R', 'BRR','B RR','BR R', 'RRB', 'R RB', 'RR B'],
        'mii_pssc'  : ['R B', 'B R', 'RB', 'BR', ' RB', 'RB ', ' BR', 'BR ']
    }

    cell_type = ''
    found = False
    for key, val in string_class_key.items():
        for seq in val:
            if seq == seq_string:
                cell_type = key
                found = True
                break
        if found:
            break
        else:
            subset_key = ''

            for key, val in string_class_key.items():
                for seq in val:
                    half_n_flag = 0
                    if (seq in seq_string) and (cell_type == ''):
                        subset_key = key
                        if subset_key == 'normal':
                            return 'normal'
                        elif subset_key == 'RR' or subset_key == 'BB':
                            half_n_flag += 0.5
                    if half_n_flag == 1:
                        return 'normal'
                
    if cell_type == '':
        print('other')
        print('subset_key: ', subset_key)
        return 'others'
    else:  
        print(cell_type)
        return cell_type
    

