
dictz_map = {}

# Given a dict, replies with the match or None if not found
# TODO right now exact match only supported
def search_match(dictz):
    return dictz_map[dictz] if dictz_map.has_key(dictz) else None
