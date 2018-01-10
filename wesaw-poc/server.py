from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import summarizer

app = FlaskAPI(__name__)


notes = {
    0: ["Facebook","fr","IOT on aura un QCM jeudi",["qcm","jeudi","IOT"]]
}

def summarize(source,lang,content):
    return summarizer.main(source,lang,content)

def note_repr(key):
    return {
        'url': request.host_url.rstrip('/') + url_for('notes_detail', key=key),
        'origin': notes[key][0],
        'lang': notes[key][1],
        'summary': notes[key][2],
        'tags': notes[key][3]
    }


@app.route("/", methods=['GET', 'POST'])
def node_list():
    """
    Lister ou créer des notes
    """
    if request.method == 'POST':
        source = str(request.data.get('source', ''))
        lang = str(request.data.get('lang', ''))
        content = str(request.data.get('content', ''))
        origin = str(request.data.get('origin', ''))
        idx = max(notes.keys()) + 1
        summary = summarize(source,lang,content)
        notes[idx] = [origin,lang,summary[0],summary[1]]
        return note_repr(idx), status.HTTP_201_CREATED

    # request.method == 'GET'
    return [note_repr(idx) for idx in sorted(notes.keys())]


@app.route("/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def notes_detail(key):
    """
    Retirer, mettre à jour ou supprimer des notes.
    """
    if request.method == 'PUT':
        source = str(request.data.get('source', ''))
        lang = str(request.data.get('lang', ''))
        content = str(request.data.get('content', ''))
        origin = str(request.data.get('origin', ''))
        summary = summarize(source,lang,content)
        notes[key] = [origin,lang,summary[0],summary[1]]
        return note_repr(key)

    elif request.method == 'DELETE':
        notes.pop(key, None)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    if key not in notes:
        raise exceptions.NotFound()
    return note_repr(key)


if __name__ == "__main__":
    app.run(debug=True)