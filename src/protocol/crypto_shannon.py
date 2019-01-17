from .src.shannon import Shannon


def run(input_text):
    s = Shannon()
    text = s.encode(input_text)
    print('')
    text = s.decode(text)
    print('decode', text)
    output_text = 'ooo'
    return output_text

