def ler_ddl_arquivo(path):
    with open(path, "r") as arquivo:
        ddl = arquivo.read()
    return ddl
