#importing neccessary libraries
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
#universal unique ID package
import uuid,pybase64,os
from databaselibrary import getdbcur
#secure Filename
from werkzeug.utils import secure_filename
#importing mail
from flask_mail import Mail, Message
########importing database lib##########
from databaselibrary import getblogcur,getdbcur,getoutletcur
##############endlib ###############3


def homedata():
    cur = getdbcur()
    outletcur = getoutletcur()
    sql = 'select * from team'
    cur.execute(sql)
    teamdata = cur.fetchall()
    sql = 'select * from flex'
    cur.execute(sql)
    flexdata = cur.fetchall()
    session['flex_data'] = flexdata
    sql = 'select * from testimonial'
    cur.execute(sql)
    reviewdata = cur.fetchall()
    ##Getting Blogs from the blogdb ##
    blogdata = getthreeblogs()
    ###########geeting total users (oulets,producer,warehouses)##
    totalbar = []
    sql = 'select * from producer'
    cur.execute(sql)
    totalproducer = cur.rowcount
    totalbar.append(totalproducer)
    sql = 'select * from warehouse'
    cur.execute(sql)
    totalwarehouse = cur.rowcount
    totalbar.append(totalwarehouse)
    sql = 'select * from outlet'
    outletcur.execute(sql)
    totaloutlet = outletcur.rowcount
    totalbar.append(totaloutlet)
    totalbar.append(sum(totalbar))
    session['totalbar'] = totalbar
    ########################################
    return render_template('index.html',teamdata = teamdata,reviewdata = reviewdata,blogdata=blogdata)


def addmember():
    cur =getdbcur()
    app = current_app._get_current_object()
    if request.method == 'POST':
        if 'user_id' in session:
            name = request.form['name']
            position = request.form['position']
            msg = request.form['msg'].replace('\r\n','<br>')
            img = request.files['memberimg']
            path=os.path.basename(img.filename)
            file_ext=os.path.splitext(path)[1][1:]
            imgfilename=str(uuid.uuid4())+'.'+file_ext
            memberimg = secure_filename(imgfilename)
            addquery ='insert into team values (%s,%s,%s,%s) '
            cur.execute(addquery,(name,position,msg,memberimg))
            n = cur.rowcount
            if n == 1:
                img.save(os.path.join(app.config['UPLOAD_FOLDER'],memberimg))
                flash('Member Added Successully !')
                return redirect(url_for('add_member'))
            flash('There is error while adding Member !')
            return redirect(url_for('add_member'))
        flash('You must Login first to add Team Member !')
        return redirect(url_for('warehouse_login')) #Tempo put this until Admin Dash is created
    return render_template('add_teammember.html')


def addflex():
    cur =getdbcur()
    app = current_app._get_current_object()
    if request.method == 'POST':
            imageno = int(request.form['imageno'])
            heading = request.form['heading']
            body = request.form['body']
            img = request.files['fleximg']
            path=os.path.basename(img.filename)
            file_ext=os.path.splitext(path)[1][1:]
            imgfilename=str(uuid.uuid4())+'.'+file_ext
            fleximg = secure_filename(imgfilename)
            addquery = "update flex SET heading = %s , body = %s , image = %s WHERE id = %s"
            cur.execute(addquery,(heading,body,fleximg,imageno))
            n = cur.rowcount
            if n == 1:
                img.save(os.path.join(app.config['UPLOAD_FOLDER'],fleximg))
                flash('Image Added Successully !')
                return redirect(url_for('add_flex'))
            flash('There is error while adding image !')
            return redirect(url_for('add_flex'))
        #flash('You must Login first to add image !')
        #return redirect(url_for('warehouse_login')) #Tempo put this until Admin Dash is created
    return render_template('flex.html')


def clientreview():
    if 'user_id' in session:
        app = current_app._get_current_object()
        id = session['user_id']
        checksql = "select name from testimonial where clientId='"+id+"'  "
        cur =getdbcur()
        cur.execute(checksql)
        m = cur.rowcount
        if m == 0:
            if request.method == 'POST':
                name = request.form['name']
                review = request.form['review'].replace('\r\n','<br>')
                rating = request.form['rating']
                img = request.files['img']
                path=os.path.basename(img.filename)
                file_ext=os.path.splitext(path)[1][1:]
                imgfilename=str(uuid.uuid4())+'.'+file_ext
                clientimg = secure_filename(imgfilename)
                addquery ='insert into testimonial values (%s,%s,%s,%s,%s) '
                cur.execute(addquery,(id,name,clientimg,rating,review))
                n = cur.rowcount
                if n == 1:
                    img.save(os.path.join(app.config['UPLOAD_FOLDER'],clientimg))
                    flash('Review added Successfully..Thankyou for using Our services!')
                    return render_template('client_review.html')
                flash('There is error while adding review Please!')
                return redirect(url_for('add_member'))
            return render_template('client_review.html')
        flash('You have already give your review..!')
        return render_template('client_review.html')
    flash('You must Login first to give your review !')
    return redirect(url_for('warehouse_login'))

    ###########Other functions ####################
def getthreeblogs():
    cur = getblogcur()
    sql = 'select * from blogs limit 3'
    cur.execute(sql)
    n = cur.rowcount
    if n >= 1:
        data = cur.fetchall()
        cd = [list(i) for i in data]
        for i in range(0,len(cd)):
            for j in range(3,len(cd[i])):
                cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
        td = tuple(tuple(i) for i in cd)
        return td
    return None    