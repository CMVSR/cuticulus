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
    'rough': 1,
    'smooth': 2,
}

INT_RS_LABEL_MAP = {v: k for k, v in RS_LABEL_MAP.items()}

# for all cuticle
ALL_LABEL_MAP = {
    '_background_': 0,
    'rough dimpled': 1,
    'rough netted': 2,
    'rough ridged': 3,
    'rough T': 4,
    'smooth gritty': 5,
    'smooth smooth': 6,
}

INT_ALL_LABEL_MAP = {v: k for k, v in ALL_LABEL_MAP.items()}
