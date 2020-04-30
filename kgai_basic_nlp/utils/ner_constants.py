# IOB-wikipaedia Scheme constants
# quick ref: https://spacy.io/api/annotation#named-entities , https://huggingface.co/transformers/usage.html#named-entity-recognition
OUTSIDE = "O"
BEGIN_MISC = "B-MISC"
I_MISC = "I-MISC"
BEGIN_PERSON = "B-PER"
I_PERSON = "I-PER"
BEGIN_LOCATION = "B-LOC"
I_LOCATION = "I-LOC"
BEGIN_ORG = "B-ORG"
I_ORG = "I-ORG"

# OntoNotes 5 Scheme reference
PERSON = "PERSON"  # People, including fictional.
NORP = "NORP"  # Nationalities or religious or political groups.
FAC = "FAC"  # Buildings, airports, highways, bridges, etc.
ORG = "ORG"  # Companies, agencies, institutions, etc.
GPE = "GPE"  # Countries, cities, states.
LOC = "LOC"  # Non-GPE locations, mountain ranges, bodies of water.
PRODUCT = "PRODUCT"  # Objects, vehicles, foods, etc. (Not services.)
EVENT = "EVENT"  # Named hurricanes, battles, wars, sports events, etc.
WORK_OF_ART = "WORK_OF_ART"  # Titles of books, songs, etc.
LAW = "LAW"  # Named documents made into laws.
LANGUAGE = "LANGUAGE"  # Any named language.
DATE = "DATE"  # Absolute or relative dates or periods.
TIME = "TIME"  # Times smaller than a day.
PERCENT = "PERCENT"  # Percentage, including ”%“.
MONEY = "MONEY"  # Monetary values, including unit.
QUANTITY = "QUANTITY"  # Measurements, as of weight or distance.
ORDINAL = "ORDINAL"  # “first”, “second”, etc.
CARDINAL = "CARDINAL"  # Numerals that do not fall under another type.

# simple map for IOB to OntoNotes 5 mapping
MISC = "MISC"  # keep the MISC mapping
IOB_ONTO5 = {BEGIN_PERSON: PERSON, I_PERSON: PERSON,
             BEGIN_LOCATION: LOC, I_LOCATION: LOC,
             BEGIN_ORG: ORG, I_ORG: ORG,
             BEGIN_MISC: MISC, I_MISC: MISC}  # for MISC we are not sure what this could have been
