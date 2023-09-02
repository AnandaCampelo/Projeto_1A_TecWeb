from utils import load_data, load_template, build_response
from database import Database
from database import Note
from urllib.parse import unquote_plus

db = Database('notehtml')

def delete(request):
    request = request.replace('\r', '')  
    partes = request.split('\n\n')
    corpo = partes[1]
    note_id = corpo.split('=')[1]
    
    db.delete(note_id)

    return build_response(code=303, headers='Location: /')

def edit(request):
    request = request.replace('\r', '') 
    partes = request.split('\n\n')
    corpo = partes[1]
    note_id = corpo.split('=')[1]
    note = db.get(note_id)
    return build_response(body=load_template('edit.html').format(id=note.id, title=note.title, content=note.content))

def update(request):
    request = request.replace('\r', '') 
    partes = request.split('\n\n')
    corpo = partes[1]
    note_id = corpo.split('&')[0].split('=')[1]
    title = unquote_plus(corpo.split('&')[1].split('=')[1])
    content = unquote_plus(corpo.split('&')[2].split('=')[1])
    db.update(Note(id=note_id, title=title, content=content))
    return build_response(code=303, reason='See Other', headers='Location: /')

def not_found(request):
    return build_response(code=404, body=load_template('404.html'))

def index(request):
    if request.startswith('POST'):
        request = request.replace('\r', '')  
        partes = request.split('\n\n')
        corpo = partes[1]
        itens = [0,0]
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            if chave == 'titulo':
                itens[0] = unquote_plus(valor)
            elif chave == 'detalhes':
                itens[1] = unquote_plus(valor)


        db.add(Note(title=itens[0], content=itens[1]))
        return build_response(code=303, reason='See Other', headers='Location: /')
                    
    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    '''note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados['titulo'], details=dados['detalhes'])
        for dados in load_data('notes.json')
    ]
    notes = '\n'.join(notes_li)

    return build_response(body=load_template('index.html').format(notes=notes))'''

    notes = db.get_all()
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=note.title, details=note.content, id=note.id)
        for note in notes
    ]
    notes = '\n'.join(notes_li)
    return build_response(body=load_template('index.html').format(notes=notes))