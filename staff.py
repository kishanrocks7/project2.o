####################NECCESSARY IMPORTS ################
import uuid,pybase64
from random import randint
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
from flask_mail import Mail, Message

############databaselib###################
from databaselibrary import getoutletcur

def staffhome():
    if 'outlet_id' in session:
        outletid = str(session['outlet_id'])
        sql = 'select * from staff where outletid = %s'
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
            return render_template('Outlet/staff.html',pdata = td)
        else:
            return render_template('Outlet/staff.html', pmsg = "currently there is NO Staff information !")
    flash('You must login first to view Staff List!')
    return redirect(url_for('outlet_login'))

def addstaff():
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
            address = str(pybase64.b64encode((request.form['address'].lower()).encode("utf-8")),"utf-8")
            post = str(pybase64.b64encode((request.form['post'].lower()).encode("utf-8")),"utf-8")
            aadharNumber = str(pybase64.b64encode((request.form['aadharNumber'].lower()).encode("utf-8")),"utf-8")
            addquery ='insert into staff values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cur = getoutletcur()
            cur.execute(addquery,( uid,name,phoneNumber,email,gender,age,address,post,aadharNumber,outletid ))
            n = cur.rowcount
            if (n == 1):
                flash(' New Staff added!')
                return redirect(url_for('staff_crud'))
            else:
                flash(' There is some problem with server. Try again Later !!')
                return redirect(url_for('staff_crud'))
        return redirect(url_for('staff_crud'))
    flash('Direct access to this page is Not allowed !')
    return redirect(url_for('outlet_login'))

def searchstaff():
    if 'outlet_id' in session:
        if request.method == 'POST':
            outletid = str(session['outlet_id'])
            si = str(pybase64.b64encode((request.form['searchinp'].lower()).encode("utf-8")),"utf-8")
            searchquery = "select * from staff where (name like  '%"+si+"%'  OR post like  '%"+si+"%') and outletid = '"+outletid+"' "
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
                return render_template('Outlet/staff.html',pdata = td,pmsg="Search Results!")
            else:
                return render_template('Outlet/staff.html', pmsg = "No results for search..try different key!")
        else:
            return render_template('Outlet/staff.html', pmsg = "Enter something to search!")
    flash('You must login first to view Staff List!!')
    return redirect(url_for('outlet_login'))

def deletestaff():
    if 'outlet_id' in session:
        if request.method == 'POST':
            id = request.form['id']
            delquery = 'delete from staff where id="'+id+'"   '
            cur =getoutletcur()
            cur.execute(delquery)
            n =cur.rowcount
            if n == 1:
                flash('Staff Details deleted Successfully !')
                return redirect(url_for('staff_crud'))
            else:
                flash('There is error in deleting Staff details !')
                return redirect(url_for('staff_crud'))
        return redirect(url_for('staff_crud'))
    flash('Direct access to this page is Not Alloed Login first To view this page!')
    return redirect(url_for('outlet_login'))

def changestaff():
    if 'outlet_id' in session:
        if request.method == 'POST':
            id =request.form['id']
            name = str(pybase64.b64encode((request.form['name'].lower()).encode("utf-8")),"utf-8")
            email = str(pybase64.b64encode((request.form['email'].lower()).encode("utf-8")),"utf-8")
            number = str(pybase64.b64encode((request.form['phoneNumber'].lower()).encode("utf-8")),"utf-8")
            gender = str(pybase64.b64encode((request.form['gender'].lower()).encode("utf-8")),"utf-8")
            age = str(pybase64.b64encode((request.form['age'].lower()).encode("utf-8")),"utf-8")
            address = str(pybase64.b64encode((request.form['address'].lower()).encode("utf-8")),"utf-8")
            post = str(pybase64.b64encode((request.form['post'].lower()).encode("utf-8")),"utf-8")
            aadharNumber = str(pybase64.b64encode((request.form['aadharNumber'].lower()).encode("utf-8")),"utf-8")
            editquery = 'update staff set name =%s,email=%s,phone=%s,post=%s, age=%s, gender=%s, address=%s,aadhar=%s where id=%s '
            cur =getoutletcur()
            cur.execute(editquery,(name,email,number,post,age,gender,address,aadharNumber,id))
            n =cur.rowcount
            if n == 1:
                flash('Staff Details changed Successfully !')
                return redirect(url_for('staff_crud'))
            else:
                flash('Nothing will be changed in staff details !')
                return redirect(url_for('staff_crud'))
        return redirect(url_for('staff_crud'))
    flash('Direct access to this page is Not Alloed Login first To view this page!')
    return redirect(url_for('outlet_login'))