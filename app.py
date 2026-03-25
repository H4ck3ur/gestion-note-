from flask import Flask, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = 'projet2026'

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect('/dashboard')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Users hardcodés (RBAC)
        if username == 'admin' and password == 'admin':
            session['user'] = 'admin'
            session['role'] = 'admin'
        elif username == 'prof' and password == 'prof':
            session['user'] = 'prof'
            session['role'] = 'prof'
        elif username == 'eleve' and password == 'eleve':
            session['user'] = 'eleve'
            session['role'] = 'eleve'
        else:
            return 'Login échoué ! <a href="/">Retour</a>'
        
        return redirect('/dashboard')
    
    return '''
    <h1>🔐 Connexion</h1>
    <form method="POST">
        <input name="username" placeholder="Identifiant" required><br>
        <input name="password" type="password" placeholder="Password" required><br>
        <button>Login</button>
    </form>
    '''

@app.route('/dashboard')
def dashboard():
    if 'role' not in session:
        return redirect('/')
    
    role = session['role']
    html = f'<h1>Dashboard {role}</h1>'
    
    if role == 'admin':
        html += '<h2>🔧 Admin : tout accès</h2><a href="/eleves">Élèves</a> | <a href="/notes">Notes</a>'
    elif role == 'prof':
        html += '<h2>👨‍🏫 Prof : gère notes</h2><a href="/notes">Notes</a>'
    elif role == 'eleve':
        html += '<h2>👨‍🎓 Élève : voit notes</h2><p>Notes bientôt...</p>'
    
    html += '<br><a href="/logout">Logout</a>'
    return html

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
