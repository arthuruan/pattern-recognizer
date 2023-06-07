def encoder(k, data_list):
    maximum_table_size = pow(2, int(k))

    dictionary_size = 256
    dictionary = {chr(i): i for i in range(dictionary_size)}
    string = ""
    compressed_data = []

    for data in data_list:
        for symbol in data:
            string_plus_symbol = string + chr(symbol)
            if string_plus_symbol in dictionary:
                string = string_plus_symbol
            else:
                compressed_data.append(dictionary[string])
                if(len(dictionary) <= maximum_table_size):
                    dictionary[string_plus_symbol] = dictionary_size
                    dictionary_size += 1
                string = chr(symbol)

        if string in dictionary:
            compressed_data.append(dictionary[string])

    return dictionary, compressed_data