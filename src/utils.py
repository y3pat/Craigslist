
def format_all(all_items):
    output_lst = []
    for i in range(len(all_items)):
        item = all_items[i]
        dictionaries = {}
        dictionaries['id'] = item.id
        dictionaries['loc'] = [item.long, item.lat]
        dictionaries['userId'] = item.userId
        dictionaries['description'] = item.description
        dictionaries['price'] = item.price
        dictionaries['status'] = item.status
        output_lst.append(dictionaries)

    return output_lst

def check_boolean(value: str) -> (bool, int):
    if value.lower() == 'true':
        return (True, 1)
    elif value.lower() == 'false':
        return (False, 1)
    else:
        return (False, 0)