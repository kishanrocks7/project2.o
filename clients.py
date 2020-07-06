####################NECCESSARY IMPORTS ################
import uuid,pybase64
from random import randint
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
from flask_mail import Mail, Message

############databaselib###################
from databaselibrary import getoutletcur

def outletclients():
    if 'outlet_id' in session:
        outletid = str(session['outlet_id'])
        sql = 'select * from clients where outletid = %s'
        cur = getoutletcur()
        cur.execute(sql,outletid)
        n = cur.rowcount
        if n >= 1:
            data = cur.fetchall()
            cd = [list(i) for i in data]
            for i in range(0,len(cd)):
                for j in range(1,len(cd[i])-1):
                    cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
            td = tuple(tuple(i) for i in cd)
            return render_template('Outlet/outlet_clients.html',pdata = td)
        else:
            return render_template('Outlet/outlet_clients.html', pmsg = "currently there is NO Client information !")
    flash('You must login first to view Clients details!')
    return redirect(url_for('outlet_login'))

def addclient():
    if 'outlet_id' in session:
        if request.method == 'POST':
            outletid = str(session['outlet_id'])
            fullkey = uuid.uuid4()
            uid = fullkey.time
            name = str(pybase64.b64encode((request.form['name'].lower()).encode("utf-8")),"utf-8")
            phoneNumber = str(pybase64.b64encode((request.form['phoneNumber'].lower()).encode("utf-8")),"utf-8")
            email = str(pybase64.b64encode((request.form['email'].lower()).encode("utf-8")),"utf-8")
            gender = str(pybase64.b64encode((request.form['gender'].lower()).encode("utf-8")),"utf-8")
            age = str(pybase64.b64encode((request.form['age'].lower()).encode("utf-8")),"utf-8")
            purpose = str(pybase64.b64encode((request.form['purposevisit'].lower()).encode("utf-8")),"utf-8")
            commodityType = str(pybase64.b64encode((request.form['commoditytype'].lower()).encode("utf-8")),"utf-8")
            lastvisited = str(pybase64.b64encode((request.form['lastvisited'].lower()).encode("utf-8")),"utf-8")
            addquery ='insert into clients values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cur = getoutletcur()
            cur.execute(addquery,( uid,name,age,gender,lastvisited,email,phoneNumber,commodityType,purpose,outletid))
            n = cur.rowcount
            if (n == 1):
                flash(' New Client details added!')
                return redirect(url_for('outlet_clients'))
            else:
                flash( 'Adding new Client details failed!')
                return redirect(url_for('outlet_clients'))
        return redirect(url_for('outlet_clients'))
    flash('Direct access to this page is Not allowed !')
    return redirect(url_for('outlet_login'))
    

    
def changeclient():
    if 'outlet_id' in session:
        if request.method == 'POST':
            id =request.form['id']
            name = str(pybase64.b64encode((request.form['name'].lower()).encode("utf-8")),"utf-8")
            phoneNumber = str(pybase64.b64encode((request.form['phoneNumber'].lower()).encode("utf-8")),"utf-8")
            email = str(pybase64.b64encode((request.form['email'].lower()).encode("utf-8")),"utf-8")
            gender = str(pybase64.b64encode((request.form['gender'].lower()).encode("utf-8")),"utf-8")
            age = str(pybase64.b64encode((request.form['age'].lower()).encode("utf-8")),"utf-8")
            purpose = str(pybase64.b64encode((request.form['purposevisit'].lower()).encode("utf-8")),"utf-8")
            commodityType = str(pybase64.b64encode((request.form['commoditytype'].lower()).encode("utf-8")),"utf-8")
            lastvisited = str(pybase64.b64encode((request.form['lastvisited'].lower()).encode("utf-8")),"utf-8")
            editquery = 'update clients set name =%s,email=%s,phoneNumber=%s,commodityPurchased=%s, age=%s, gender=%s, purpose=%s,lastvisited=%s where id=%s '
            cur =getoutletcur()
            cur.execute(editquery,(name,email,phoneNumber,commodityType,age,gender,purpose,lastvisited,id))
            n =cur.rowcount
            if n == 1:
                flash('Client Details changed Successfully !')
                return redirect(url_for('outlet_clients'))
            else:
                flash('Nothing will be changed in client details !')
                return redirect(url_for('outlet_clients'))
        return redirect(url_for('outlet_clients'))
    flash('Direct access to this page is Not Alloed Login first To view this page!')
    return redirect(url_for('outlet_login'))


def deleteclient():
    if 'outlet_id' in session:
        if request.method == 'POST':
            id = request.form['id']
            delquery = 'delete from clients where id="'+id+'"   '
            cur =getoutletcur()
            cur.execute(delquery)
            n =cur.rowcount
            if n == 1:
                flash('Client Details deleted Successfully !')
                return redirect(url_for('outlet_clients'))
            else:
                flash('There is error in deleting Client details !')
                return redirect(url_for('outlet_clienst'))
        return redirect(url_for('outlet_clients'))
    flash('Direct access to this page is Not Alloed Login first To view this page!')
    return redirect(url_for('outlet_login'))


def searchclient():
    if 'outlet_id' in session:
        if request.method == 'POST':
            outletid = str(session['outlet_id'])
            si = str(pybase64.b64encode((request.form['searchinp'].lower()).encode("utf-8")),"utf-8")
            searchquery = "select * from clients where (name like  '%"+si+"%'  OR commodityPurchased like   '%"+si+"%' )  and outletid = '"+outletid+"' "
            cur =getoutletcur()
            cur.execute(searchquery)
            n =cur.rowcount
            if n >= 1:
                data = cur.fetchall()
                cd = [list(i) for i in data]
                for i in range(0,len(cd)):
                    for j in range(1,len(cd[i])-1):
                        cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
                td = tuple(tuple(i) for i in cd)
                return render_template('Outlet/outlet_clients.html',pdata = td,pmsg="Search Results!")
            else:
                return render_template('Outlet/outlet_clients.html', pmsg = "No results for search..try different key!")
        else:
            return render_template('Outlet/outlet_clients.html', pmsg = "Enter something to search!")
    flash('You must login first to view Clients!')
    return redirect(url_for('outlet_login'))