""" See https://gist.github.com/hangtwenty/5960435#gistcomment-2796890 """
from collections import OrderedDict, namedtuple


def tupleware(obj):
    if isinstance(obj, dict):
        fields = sorted(obj.keys())
        namedtuple_type = namedtuple(
            typename='TWare',
            field_names=fields,
            rename=True,
        )
        field_value_pairs = OrderedDict(
            (str(field), tupleware(obj[field])) for field in fields)
        try:
            return namedtuple_type(**field_value_pairs)
        except TypeError:
            # Cannot create namedtuple instance so fallback to dict (invalid attribute names)
            return dict(**field_value_pairs)
    elif isinstance(obj, (list, set, tuple, frozenset)):
        return [tupleware(item) for item in obj]
    else:
        return obj
