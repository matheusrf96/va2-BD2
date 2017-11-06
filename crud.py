#coding: utf-8

from appJar import gui
import MySQLdb

def entrar(btn):
	global cursor
	global conexao

	host = login.getEntry("host")
	usuario = login.getEntry("usuario")
	senha = login.getEntry("senha")

	try:
		conexao = MySQLdb.connect(host, usuario, senha, "mundo")
		cursor = conexao.cursor()

	except MySQLdb.Error as err:
		print err

	login.stop()

login = gui("Login", "300x150")

login.addLabelEntry("host")
login.addLabelEntry("usuario")
login.addSecretLabelEntry("senha")

login.addButton("Entrar", entrar)

login.go()

#conexao = MySQLdb.connect("192.168.56.102", "aluno", "aluno2017", "mundo")
#cursor = conexao.cursor()


app = gui("CRUD de MySQL", "600x400")

def pesquisar(btn):
	termo = app.getEntry("txtBusca")

	if termo == '':
		app.errorBox("Erro", 'Informe um termo para pesquisar!')
	else:
		cursor.execute(
			"SELECT Cidade.Nome, Estado.Nome FROM Cidade " +
			"INNER JOIN Estado ON Estado.id = Cidade.Estado_id " +
			"WHERE Cidade.Nome LIKE '%" + termo + "%'"
		)

		rs = cursor.fetchall()

		app.clearListBox("lBusca")

		for x in rs:
			app.addListItem("lBusca", x[0] + ' - ' + x[1])

def exibir(btn):
	cursor.execute(
		"SELECT Cidade.Nome, Estado.Nome, Pais.Nome FROM Cidade " +
		"INNER JOIN Estado ON Cidade.Estado_id = Estado.id " +
		"INNER JOIN Pais ON Estado.Pais_id = Pais.id;"
	)

	rs = cursor.fetchall()

	app.clearListBox("lBusca")

	for x in rs:
		app.addListItem("lBusca", x[0] + ' - ' + x[1] + ' - ' + x[2])

def inserir(btn):
	app.showSubWindow('janela_inserir')

def salvar_estado(btn):
	cidade = app.getEntry('txtcidade')
	idestado = app.getEntry('txtestado')
	cursor.execute("INSERT INTO Cidade (Nome, Estado_id) VALUES('{}',{})".format(cidade,idestado))
	#cursor.execute("INSERT INTO Cidade (NomeCidade, Estado_idEstado) VALUES('%s',%s)" % (cidade,idestado))
	conexao.commit()

	app.clearListBox("lBusca")
	app.addListItem("lBusca", "A cidade " + cidade + " foi inserida com sucesso!")

	app.hideSubWindow('janela_inserir')

def deletar(btn):
	app.showSubWindow("delete_cidade")

def deletar_estado(btn):
	nome_cidade_delete = app.getEntry("cidade2")

	cursor.execute(
		"SELECT id, Nome FROM Cidade WHERE Nome LIKE '%" + nome_cidade_delete + "%'"
	)

	rs = None
	rs = cursor.fetchone()

	app.clearListBox("lBusca")

	app.addListItem("lBusca", "A cidade " + rs[1] + " foi deletada!")

	cursor.execute(
		"DELETE FROM Cidade WHERE id = %s" % (rs[0])
	)

	conexao.commit()

	app.hideSubWindow("delete_cidade")

def atualizar(btn):
	app.showSubWindow("atualizar_cidade")

def atualizar_estado(btn):
	nome_antigo = app.getEntry("nome_antigo")
	nome_novo = app.getEntry("nome_novo")
	id_novo = app.getEntry("id_novo")

	cursor.execute(
		"SELECT id, Nome FROM Cidade WHERE Nome LIKE '%" + nome_antigo + "%'"
	)

	rs = cursor.fetchone()

	app.clearListBox("lBusca")

	app.addListItem("lBusca", "A cidade " + rs[1] + " foi atualizada para " + nome_novo + " com o ID Estado" + id_novo + " !")

	cursor.execute(
		"UPDATE Cidade "+
		"SET Estado_id = " + id_novo + ", Nome = '" + nome_novo + "'"
		"WHERE id = " + str(rs[0])
	)

	conexao.commit()

	app.hideSubWindow("atualizar_cidade")

#Janela Inserir ----------------
app.startSubWindow("janela_inserir", modal=True)
app.addLabel("l1", "Inserindo dados...")
app.addEntry('txtestado')
app.addEntry('txtcidade')
app.addButton('Salvar cidade',salvar_estado)
app.setEntryDefault("txtestado", "ID do Estado")
app.setEntryDefault("txtcidade", "Nome da cidade")
app.stopSubWindow()

# Janela Deletar ---------------
app.startSubWindow("delete_cidade", modal=True)

app.addLabel("lDelete", "Deletar cidade: ")

app.addEntry("cidade2")
app.addButton("Deletar Cidade", deletar_estado)
app.setEntryDefault("cidade2", "Nome Cidade")

app.stopSubWindow()

#Janela Atualizar ---------------
app.startSubWindow("atualizar_cidade", modal=True)

app.addLabel("lUpdate", "Atualizar cidade: ")

app.addEntry("nome_antigo")
app.addEntry("nome_novo")
app.addEntry("id_novo")

app.addButton("Atualizar Cidade", atualizar_estado)

app.setEntryDefault("nome_antigo", "Nome Antigo")
app.setEntryDefault("nome_novo", "Nome Novo")
app.setEntryDefault("id_novo", "Novo ID Estado")

app.stopSubWindow()

# Menu principal ----------------
app.addLabel("lNome", '', 0, 0, 2)

app.addButton("Exibir dados", exibir, 1, 0)
app.addButton("Inserir dados", inserir, 1, 1)
app.addButton("Atualizar dados", atualizar, 2, 0)
app.addButton("Excluir dados", deletar, 2, 1)

app.addEntry("txtBusca", 3, 0, 2)
app.setEntryDefault("txtBusca", "Digite o termo...")

app.addButton("Pesquisar", pesquisar, 4, 0, 2)

app.addListBox("lBusca", [], 5, 0, 2)
app.setListBoxRows("lBusca", 5)

app.go()
