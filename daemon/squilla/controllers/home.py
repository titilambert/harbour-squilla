from flask import make_response, render_template

from squilla import app


from squilla.libs.authentication import requires_auth

#@app.route('/')
#def basic_pages(**kwargs):
#    return make_response(open('squilla/templates/index.html').read())


@app.route('/')
@requires_auth
def home(**kwargs):
    modules = app.module_list.get('loaded', [])
    return render_template('/index.html', modules=modules)
