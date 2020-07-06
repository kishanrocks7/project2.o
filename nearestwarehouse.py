#importing neccessary libraries
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
#universal unique ID package
import uuid,pybase64,os
from random import randint
#secure Filename
from werkzeug.utils import secure_filename
#importing mail
from flask_mail import Mail, Message
from geopy.distance import geodesic 
from databaselibrary import getdbcur , getoutletcur
from producer import countbar

def getnearestwarehouse(id):
    sql = 'select latitude,longitude,id from warehouse '
    cur = getdbcur()
    cur.execute(sql)
    waredata = cur.fetchall()
    sql = 'select latitude,longitude from outlet where id = %s '
    cur = getoutletcur()
    cur.execute(sql,id)
    outdata = cur.fetchone()
    mind = 9999999999999
    warehouseid = 0
    for i in waredata:
        distance = geodesic((i[0],i[1]),outdata)
        if distance < mind :
            mind = distance
            warehouseid=i[2]
    return warehouseid


def nearestone():
    if 'outlet_id' in session:
        warehouseid = getnearestwarehouse(session['outlet_id'])
        cbar = countbar(warehouseid)
        session['nearest_warehouse_id'] = warehouseid
        return render_template('Outlet/warehouse_products.html',cbar=cbar)
    flash('You must login first to view This page!')
    return redirect(url_for('outlet_login'))



def reqware():
    if 'outlet_id' in session:
        outletId = session['outlet_id']
        warehouseId = session['nearest_warehouse_id']
        if request.method == 'POST':
            fullkey = uuid.uuid4()
            requestId = fullkey.time
            name = request.form['pname']
            quantity = request.form['quantity']
            description = request.files['description']
            if description:
                path=os.path.basename(description.filename)
                file_ext=os.path.splitext(path)[1][1:]
                imgfilename=str(uuid.uuid4())+'.'+file_ext
                descriptionname = secure_filename(imgfilename)
                app = current_app._get_current_object()
                description.save(os.path.join(app.config['UPLOAD_FOLDER'],descriptionname))
            else:
                flash('Order is not placed..Please upload the description!')
                return redirect(url_for('nearest_warehouses'))
            sql = 'insert into warehousenotification(requestId,warehouseId,outletId,productName,description,quantity) values(%s,%s,%s,%s,%s,%s) '
            cur = getdbcur()
            cur.execute(sql,(requestId,warehouseId,outletId,name,descriptionname,quantity))
            n = cur.rowcount
            if n == 1:
                flash('Commodity request send to warehouse wait for response !')
                return redirect(url_for('nearest_warehouses'))
            flash('There is an error while placing Order..!')
            return redirect(url_for('nearest_warehouses'))
    flash('You must login first to view This page!')
    return redirect(url_for('outlet_login'))
    