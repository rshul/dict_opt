import string
from pprint import pprint


def optimize_data(template, data):
    pieces = string.Formatter().parse(template)
    strdata = [piece[1] for piece in pieces if piece[1] is not None]
    # split placeholder into list of keys
    listkeys = [i.replace(']', '').split('[') for i in strdata]
    d = {}
    for keys in listkeys:
        temp = data
        tempd = d # temporary dictionary
        for i, el in enumerate(keys):
            if isinstance(temp, dict):
                if isinstance(el,str) and el.partition('.')[1]=='.':
                    el = el.partition('.')[0]
                temp = temp.get(el)
                if i == len(keys)-1:
                    tempd.setdefault(el, temp)
                else:
                    if not (tempd.get(el)):
                        if isinstance(temp, dict):
                            tempd.setdefault(el, {})
                        elif isinstance(temp, list):
                            tempd.setdefault(el, [None]*len(temp))
                        else:
                            tempd.setdefault(el, None)
                    tempd = tempd[el]
            elif isinstance(temp, list):
                el = int(el)
                tempd[el] = temp[el]

    return d


def main():
    template = 'Python version: {languages[python][latest_version]}'
    data = {
        'languages': {
            'python': {
                'latest_version': '3.6',
                'site': 'http://python.org',
            },
            'rust': {
                'latest_version': '1.17',
                'site': 'https://rust-lang.org',
            },
        },
    }
    print("Original data:")
    pprint(data)

    new_data = optimize_data(template, data)
    print("Optimized data:")
    pprint(new_data)


if __name__ == '__main__':
    main()
