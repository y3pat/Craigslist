from Models.itemdata_model import Items

def format_items(all_items):
    output_lst = []
    for i in range(len(all_items)):
        item = all_items[i]
        dictionaries = {'id': item.id, 'loc': [item.long, item.lat],
                        'userId': item.userId, 'description': item.description,
                        'price': item.price, 'status': item.status}
        output_lst.append(dictionaries)

    return output_lst


def check_boolean(value: str) -> (bool, int):
    if value.lower() == 'true':
        return True, 1
    elif value.lower() == 'false':
        return False, 1
    else:
        return False, 0

criteria_dict = {
        'price': Items.price,
        'loc': Items.long,
        'userId': Items.userId,
        'id': Items.id,
        'description': Items.description,
        'status': Items.status
    }
