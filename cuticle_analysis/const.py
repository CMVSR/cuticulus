DATASET = 'dataset'
DATASET_ALL = 'all'
DATASET_BG = 'background'
DATASET_RS = 'rough_smooth'

LABEL_MAP = {
    '_background_': 0,
    'antenna_base': 1,
    'cuticle': 2,
    'cuticle_extra': 3,
    'eye': 4
}

DS_MAP = {
    DATASET_BG: 'bg',
    DATASET_RS: 'rs'
}

BG_LABEL_MAP = {
    '_background_': 0,
    'cuticle': 1,
}

RS_LABEL_MAP = {
    '_background_': 0,
    'Rough': 1,
    'Smooth': 2,
}

INT_RS_LABEL_MAP = {v: k for k, v in RS_LABEL_MAP.items()}

# for all cuticle
ALL_LABEL_MAP = {
    '_background_': 0,
    'Rough Dimpled': 1,
    'Rough Netted': 2,
    'Rough Ridged': 3,
    'Rough Tuberous': 4,
    'Smooth': 5,
}

INT_ALL_LABEL_MAP = {v: k for k, v in ALL_LABEL_MAP.items()}
