from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField
from wtforms.validators import Email, DataRequired, Length


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
	phone_no = StringField('Mobile no.', validators=[Length(min=10, max=13)])

	dob = DateField('DOB', validators=[DateField])
	submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
	submit = SubmitField('Login')


class SearchForm(FlaskForm):
	chr = StringField('Chromosome')
	start = StringField('Start')
	end = StringField('End')
	var_type = StringField('Variant_type', validators=[DataRequired()])
	submit = SubmitField('Search')
	output = TextAreaField('Area')


class RegionForm(FlaskForm):
	chr = StringField('Chromosome', validators=[DataRequired()])
	start = StringField('Start', validators=[DataRequired()])
	end = StringField('End', validators=[DataRequired()])
	submit = SubmitField('Search')
	output = TextAreaField('Area')


class ContactForm(FlaskForm):
	fname =StringField('First Name', validators=[DataRequired])
	lname=StringField('Last Name', validators=[DataRequired])
	country=StringField('Country', validators=[DataRequired])
	email = StringField('Email', validators=[DataRequired()])
	message=StringField('Message',validators=[DataRequired])
	submit=SubmitField('Submit')


class MethylForm(FlaskForm):
	start = StringField('Start', validators=[DataRequired()])
	end = StringField('End', validators=[DataRequired()])
	submit = SubmitField('Search')
	output = TextAreaField('Area')


class FusionForm(FlaskForm):
	h_gene = StringField('H-gene', validators=[DataRequired()])
	submit = SubmitField('Search')
	output = TextAreaField('Area')