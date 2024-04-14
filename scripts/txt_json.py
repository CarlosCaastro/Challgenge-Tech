import os
import sys
import shutil

projeto_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(projeto_path)

from utils.transform_data import split_file, txt_to_json
from credentials.paths import PATH_JSON_EQUIPMENT_FAILURE, FILE_NAME_TXT, PATH_TXT_ORIGINAL, PATH_TXT_DESTINO

os.makedirs(PATH_JSON_EQUIPMENT_FAILURE)
shutil.move(PATH_TXT_ORIGINAL, PATH_JSON_EQUIPMENT_FAILURE)

split_file(input_file=PATH_JSON_EQUIPMENT_FAILURE+FILE_NAME_TXT,num_parts=10)

shutil.move(PATH_TXT_DESTINO,PATH_TXT_ORIGINAL)

path = 'C:/Users/User\Desktop/Challgenge-Tech/txt_part_10'
for arquivo in os.listdir(PATH_JSON_EQUIPMENT_FAILURE):
    if arquivo.startswith('equpment_failure_sensors') and arquivo.endswith('.txt'):
        txt_file = os.path.join(path, arquivo)
        json_file = os.path.splitext(txt_file)[0] + '.json'
        txt_to_json(txt_file, json_file)

print("Arquivo JSON gerado com sucesso!")

for arquivo in os.listdir(PATH_JSON_EQUIPMENT_FAILURE):
    if arquivo.endswith('.txt'):
        caminho_arquivo = os.path.join(PATH_JSON_EQUIPMENT_FAILURE, arquivo)
        os.remove(caminho_arquivo)

print("Arquivos TXTs apagados.")



