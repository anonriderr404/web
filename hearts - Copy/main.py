from flask import Flask,render_template,request,redirect,send_from_directory,session,url_for
from db import *
import random,string,os

def get_preloader():
    loaders = ['https://www.eventstodayz.com/wp-content/uploads/2020/01/Kissing-gif.gif',
    'https://www.eventstodayz.com/wp-content/uploads/2020/01/I-love-you-cartoon-gif.gif',
    'https://media.tenor.com/LisG68HCRWYAAAAi/saltobears.gif',
    'https://media1.tenor.com/m/Q5qinV6Za04AAAAC/saltobears-squeeze.gif',
    'https://media1.tenor.com/m/JSc7XPKDSSoAAAAC/saltobears.gif',
    'https://media.tenor.com/CwSfh-O9DSkAAAAC/0legna-e-asuna-vc-consegue-amor.gif'
]
    return random.choice(loaders)

app = Flask(__name__)
app.secret_key = 'rmks2727919'

bg = ['https://media.tenor.com/kKmvIr30vQYAAAAj/stars-changing-colors.gif',
            'https://img1.picmix.com/output/stamp/normal/6/0/7/1/221706_5946c.gif',
            'https://img1.picmix.com/output/stamp/normal/2/2/7/1/1251722_f3c91.gif',
            'https://img1.picmix.com/output/stamp/normal/8/5/0/3/863058_a8929.gif',
            'https://img1.picmix.com/output/stamp/thumb/1/8/0/7/1257081_758f3.gif',
            'https://i.redd.it/87jgis2f4lsz.gif',
            ]
prince_img = '/static/img/' + get_record('profile','username','prince')[2]
princess_img = '/static/img/' +  get_record('profile','username','princess')[2]
def check_auth():
    if 'username' in session:
        user = get_record('users','username',session['username'])
        return user
    else:
        return None


@app.route('/')
def index_view():
    if 'username' in session:
        user = get_record('users','username',session['username'])
        if user[1] == 'princess':
            img = princess_img
        else:
            img = prince_img
        memories = retrieve_data('memories')
        memos = retrieve_data('memo')
        random.shuffle(memories)
        if len(memories) > 15:
            memories = memories[0:14]
        return render_template('index.html',person=session['username'],load=get_preloader(),img=img, memories=memories,bg=random.choice(bg),memos=memos,user=user)
    else:
        return redirect(url_for('login'))

@app.route('/download/<filename>', methods=['GET'])
def download_memory_file(filename):
    if 'username' in session:
        return send_from_directory('static/img', filename, as_attachment=True)
    else:
        return redirect(url_for('login'))


@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('query')
    memos = retrieve_data('memo')
    try:
        memories = filterFromQuery(search_query)
        return render_template('index.html',load=get_preloader(), memories=memories,bg=random.choice(bg),memos=memos)
    except:
        memories = []
        return render_template('index.html',load=get_preloader(), memories=memories,bg=random.choice(bg),memos=memos)

@app.route('/search/impression',methods=['GET'])
def search_impression():
    search_query = request.args.get('query')
    memories = retrieve_data('memories')
    try:
        memos = filterFromMemoQuery(search_query)
        return render_template('index.html',load=get_preloader(), memories=memories,bg=random.choice(bg),memos=memos)
    except:
        memos = []
        return render_template('index.html',load=get_preloader(), memories=memories,bg=random.choice(bg),memos=memos)
    

@app.route('/admin',methods=['post','get'])
def add_view():
    if 'username' in session:
        user = session['username']
        if user == 'princess':
            img = princess_img
        else:
            img = prince_img

        memos = retrieve_data('memo')
        if request.method == 'POST':
            if "memory" in request.form and "memo" in request.form:
                return render_template('add.html', message='Sorry Due to security reasons , uploading memories and impressions together is not allowed!')
            elif 'memory' in request.form:
                data = request.form
                title = data.get('title')
                description = data.get('description')
                date = data.get('date')
                place = data.get('place')
                uploaded_file = request.files['image']

                inputs = [uploaded_file.filename,title,description,date,place]
                special_chars = ['*',"'","#",'*','<','>','"','{','}','/','\\']
                for inp in inputs:
                    for char in special_chars:
                        if char in inp:
                            error = 'warning! [ YOUR ARE GOING TO BE EXTREMLY FUCKED UP WITH A THRONY DICK ] Dont even try to mess with Anon-rider 404 ! first try to fix your DNS leak noob fucking ass hole'
                            return render_template('add.html', message=error,memos=memos,load=get_preloader(), img=img)

                if title is not None and uploaded_file.filename != "":
                    filename = uploaded_file.filename
                    if os.path.exists('static/img/'+filename):
                        characters = string.ascii_letters + string.digits
                        random_string = ''.join(random.choice(characters) for _ in range(8))
                        filename = uploaded_file.filename.split('.')[0]+random_string+'.'+uploaded_file.filename.split('.')[1]
                    uploaded_file.save('static/img/'+filename)
                    add_to_memories(filename,title,description,date,place)
                else:
                    error = 'required fields are not completed'
                    return render_template('add.html', ierror=error,memos=memos,load=get_preloader(),img=img)
                
                return redirect('/')
            elif 'memo' in request.form:
                data = request.form
                title = data.get('title')
                date = data.get('date')
                uploaded_file = request.files['image']

                inputs = [uploaded_file.filename,title,date]
                special_chars = ['*',"'","#",'*','<','>','"','{','}','/','\\']
                for inp in inputs:
                    for char in special_chars:
                        if char in inp:
                            error = 'warning! [ YOUR ARE GOING TO BE EXTREMLY FUCKED UP WITH A THRONY DICK ] Dont even try to mess with Anon-rider 404 ! first try to fix your DNS leak noob fucking ass hole'
                            return render_template('add.html', message=error,memos=memos,load=get_preloader(),img=img)

                if title is not None and uploaded_file.filename != "":
                    filename = uploaded_file.filename
                    if os.path.exists('static/img/'+filename):
                        print('\n\n\n')
                        characters = string.ascii_letters + string.digits
                        random_string = ''.join(random.choice(characters) for _ in range(8))
                        filename = uploaded_file.filename.split('.')[0]+random_string+'.'+uploaded_file.filename.split('.')[1]
                    uploaded_file.save('static/img/'+filename)
                    add_to_memo(filename,title,date)
                else:
                    error = 'required fields are not completed'
                    return render_template('add.html', merror=error,memos=memos,load=get_preloader(),img=img)
                
                return redirect('/')
            else:
                return redirect('/')
        else:
            return render_template('add.html',memos=memos,img=img,load=get_preloader())
    else:
        return redirect(url_for('login'))

@app.route('/delete/memory/<int:pk>', methods=['get','post'])
def delete_memory(pk):
    user = check_auth()
    if user is None:
        return redirect(url_for('login'))
    memory = get_from_pk(pk)
    if request.method == 'POST':
        delete_record('memories','id',str(pk))
        return redirect('/')
    else:
        return render_template('delete.html', pk=pk, memory=memory,load=get_preloader())
    
@app.route('/delete/memo/<int:pk>', methods=['get','post'])
def delete_memo(pk):
    user = check_auth()
    if user is None:
        return redirect(url_for('login'))
    memo = get_memo_from_pk(pk)
    if request.method == 'POST':
        delete_record('memo','id',str(pk))
        return redirect('/')
    else:
        return render_template('delete.html', pk=pk,type='memo',memo=memo,load=get_preloader())
    

@app.route('/memorize/<int:pk>')
def memorize(pk):
    user = check_auth()
    if user is None:
        return redirect(url_for('login'))

    data = get_from_pk(pk)
    if data is not None:
        return render_template('detail.html', memory=data,load=get_preloader())
    else:
        return redirect("/")


@app.route('/alerts', methods=['POST','GET'])
def alerts():
    if 'username' in session:
        user = get_record('users','username',session['username'])
        if user[1] == 'princess':
            img = princess_img
            img2 = prince_img
        else:
            img = prince_img
            img2 = princess_img

    user = check_auth()
    if user is None:
        return redirect(url_for('login'))
    alerts = retrieve_data('alert')

    if session['username'] == 'prince':
        name = 'her'
    else:
        name = 'him'

    if alerts[0][1] == session['username']:
        my_alert = alerts[0]
        other_alert = alerts[1]
    else:
        my_alert = alerts[1]
        other_alert = alerts[0]

    
    if request.method == 'POST':
        data = request.form
        user = session['username']
        title = data.get('title')
        date = data.get('date')
        value = get_record('alert','user',user)[1]
        status = edit_record('alert','user',value,title=title,date=date)
        print(value,status)
        return redirect(url_for('alerts'))
    else:
        return render_template('alert.html',load=get_preloader(),name=name,my_alert=my_alert,other_alert=other_alert,img=img,img2=img2)

@app.route('/login', methods=['post','get'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        print(username,password)
        if authenticate(username,password):
            user = get_record('users','username',username)
            session['username'] = user[1]
            print('authenticated')
            return redirect(url_for('index_view'))
        else:
            error='you r seem to going nuts!.'
            print(error)
            return render_template('login.html', error=error,load=get_preloader())
        

    else:
        return render_template('login.html',load=get_preloader())

@app.route('/profiles', methods=['POST','GET'])
def profiles():
    user = check_auth()
    if user is None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        uploaded_file = request.files['image']
        filename = uploaded_file.filename
        if os.path.exists('static/img/'+filename):
            characters = string.ascii_letters + string.digits
            random_string = ''.join(random.choice(characters) for _ in range(8))
            filename = uploaded_file.filename.split('.')[0]+random_string+'.'+uploaded_file.filename.split('.')[1]
            uploaded_file.save('static/img/'+filename)
        else:
            uploaded_file.save('static/img/'+filename)

        edit_record('profile','username',session['username'],image=filename)
        return render_template('profile.html',load=get_preloader(),img=get_record('profile','username',session['username'])[2])
 
    else:
        return render_template('profile.html',load=get_preloader(),img=get_record('profile','username',session['username'])[2])
    

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove 'user_id' from the session if it exists
    return redirect(url_for('login'))

app.run(debug=True)
