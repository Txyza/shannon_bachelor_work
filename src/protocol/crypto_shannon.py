import src.protocol.src.shannon as sh


def run(input_text):
    s = sh.Shannon()
    text = s.encode(input_text)
    print('')
    text = s.decode(text)
    print('decode', text)
    output_text = 'ooo'
    return output_text


if __name__ == '__main__':
    run('hello world')
