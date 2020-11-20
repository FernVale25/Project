from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditNameForm, EditPasswordForm, DeviceRegistrationForm, TestUnlockForm
from app.models import User, Device, Unlock
from app.main import bp

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods= ['GET', 'POST'])
@login_required
def index():
	return render_template('index.html', title='Home', devices=current_user.devices)



@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	nameForm = EditNameForm(current_user.username)
	passForm = EditPasswordForm()

	#TODO: Fix this hacky strategy 
	if nameForm.username.validate(nameForm):
		user = User.query.filter_by(username=nameForm.username.data).first()
		if user is not None:
			flash("You must use a unique username")
			return redirect(url_for('main.edit_profile'))	
		current_user.username = nameForm.username.data
		db.session.commit()
		flash('Your username has been changed')
		return redirect(url_for('main.edit_profile'))
	elif passForm.oldpass.validate(passForm) and passForm.password.validate(passForm) and passForm.password2.validate(passForm):
		if (current_user.check_password(passForm.oldpass.data)):
			flash('Your password has been changed')
			current_user.set_password(passForm.password.data)
			db.session.commit()
		else:
			flash('Your old password must be correct')
			return redirect(url_for('main.edit_profile'))
	return render_template('editProfile.html', title='Edit Profile', nameForm=nameForm, passForm=passForm)




@bp.route('/regDevice', methods=['GET', 'POST'])
@login_required
def regDevice():
	user = User.query.filter_by(username=current_user.username).first_or_404()
	form = DeviceRegistrationForm()
	if form.validate_on_submit():
		if Device.query.filter_by(id = form.deviceID.data).scalar() is None:
			d = Device(id = form.deviceID.data)
			d.users.append(user)
			db.session.add(d)
			user.devices.append(d)
			db.session.commit()
			flash("Congragulations, you registered a device!")
			return redirect(url_for('main.index'))
		else:
			d = Device.query.filter_by(id = form.deviceID.data).first()
			d.users.append(user)
			user.devices.append(d)
			db.session.commit()
			flash("Congragulations, you registered a device!")
			return redirect(url_for('main.index'))
	return render_template('regDevice.html', title='Register Device', form = form)


@bp.route('/testUnlock', methods=['GET', 'POST'])
@login_required
def testUnlock():
	user = User.query.filter_by(username=current_user.username).first_or_404()
	form = TestUnlockForm()
	for d in current_user.devices:
		form.deviceField.choices.append(d.id)
	if form.validate_on_submit():
		unlock = Unlock(dID=form.deviceField.data, username=current_user.username)
		db.session.add(unlock)
		d = Device.query.filter_by(id=form.deviceField.data).first()
		d.unlocks.append(unlock)
		current_user
		db.session.commit()
		flash("Succesful test of unlock!")
		return redirect(url_for('main.index'))
	return render_template('testUnlock.html', title = 'Test Unlock', form = form)


#@app.route('/user/<username>')
#@login_required
