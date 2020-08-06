from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User



class RegistrationForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
	email = StringField('Email',validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign Up')

	#custom validation for unique emails
	def validate_username(self,username):

		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username is Taken.')
	
	def validate_email(self,email):

		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is Taken.')


class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')
	

class UpdateAccountForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
	email = StringField('Email',validators=[DataRequired()])
	picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('Update')

	#custom validation for unique emails
	def validate_username(self,username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username is Taken.')
		
	def validate_email(self,email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email is Taken.')


class RequestResetForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self,email):

		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('Account not found with that email.')

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Reset Password')