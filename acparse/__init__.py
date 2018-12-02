def parse(file_name, transform=lambda x: x):
    with open(file_name) as file:
        for line in file:
            yield transform(line)