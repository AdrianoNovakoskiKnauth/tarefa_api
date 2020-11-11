from flask import Flask, jsonify, request
import json
app = Flask(__name__)

banco_de_dados=[
    {"id":0,"responsavel":"Adriano","tarefa":[{"descricao":{"tarf":"Plantar aipim","status":"PENDENTE"}},
                                              {"descricao":{"tarf":"Plantar BATATA","status":"CONCLUIDO"}},]},
    {"id":1,"responsavel":"Samuel","tarefa":[{"descricao":{"tarf":"Lavar a MOTO","status":"PENDENTE"}},
                                              {"descricao":{"tarf":"Lavar o CARRO","status":"CONCLUIDO"}},]}
]
@app.route('/tarefa/', methods=['GET','POST'])      #Consulta todos, adiciona novo ID na lista
def nova_responsavel_banco_de_dados_lista():
    if request.method == 'GET':
        return jsonify(banco_de_dados)
    elif request.method == 'POST':
        dados = json.loads(request.data)
        dados["id"] = len(banco_de_dados)
        banco_de_dados.append(dados)
        return jsonify(banco_de_dados)

@app.route('/tarefa/<int:id>/', methods=['GET','DELETE'])       #Consulta e deleta por ID
def delete_responsavel_get (id):
    if request.method == "GET":
        dados = banco_de_dados[id]
        return jsonify(dados)
    elif request.method == "DELETE":              #Arrumar para deletar tarefa
        banco_de_dados.pop(id)
        mensagem = "Responsavel excluida com sucesso"
        return jsonify({"status":mensagem},banco_de_dados)

@app.route('/tarefa/<int:id>/', methods=['PUT'])    #Adiciona nova tarefa a um ID
def nova_tarefa(id):
    if request.method == 'PUT':             #PUT altera registro
        dados = json.loads(request.data)            #recebido
        dados = dados["tarefa"]                     #recebido
        num = len(dados)
        seq = 0
        while seq < num:
            banco_de_dados[id]["tarefa"].append(dados[seq])            #banco de dados
            seq += 1
        return jsonify(banco_de_dados)

@app.route('/tarefa/<int:id>/<int:tr>/', methods=['PUT','DELETE'])  #Altera e deleta uma unica tarefa
def taresa_put_delete(id,tr):
    if request.method == 'PUT':                   #Permite apenas alterar o status de pendente/concluido
        num_taref = len(banco_de_dados[id]['tarefa'])
        if tr < num_taref:
            if banco_de_dados[id]['tarefa'][tr]["descricao"]["status"] == "PENDENTE":
                banco_de_dados[id]['tarefa'][tr]["descricao"]["status"] = "CONCLUIDO"
                return jsonify({"status": "CONCLUIDO"})
            else:
                banco_de_dados[id]['tarefa'][tr]["descricao"]["status"] = "PENDENTE"
                return jsonify({"status":"PENDENTE"})
        else:
            return jsonify({"mensagem":"Não existe esse numero de tarefa"})
    if request.method == 'DELETE':                   #Permite apenas alterar o status de pendente/concluido
        num_taref = len(banco_de_dados[id]['tarefa'])
        if tr < num_taref:
            banco_de_dados[id]['tarefa'].pop(tr)
            return jsonify({'mensagem':"Tarefa excluida com sucesso"})
        else:
            return jsonify({"mensagem":"Tarefa não existe"})

if __name__ == '__main__':
    app.run(debug=True)