#! /usr/bin/env python
# _*_coding:utf-8 -*_

from flask_wtf import FlaskForm
from wtforms import StringField,  SelectField,SubmitField
from wtforms.validators import DataRequired, URL, Regexp,Length


class NewScanTaskForm(FlaskForm):
    Name = StringField(
        "任务名称",
        validators=[
            Length(4, 32),
            DataRequired(),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '任务名称必须有字母数字或下划线组成')
        ],
        default="Task_Name"
    )
    StartURL = StringField("起始URL", validators=[DataRequired(), URL()], default="http://www.demo.net")
    # ScanPolicy = SelectField("扫描策略", validators=[DataRequired])
    # Select类型，下拉单选框，choices里的内容会在Option里，里面每个项是(值，显示名)对
    ScanPolicy = SelectField('扫描策略', choices=[
        ('Normal', 'Normal'),
        ('Quick', 'Quick'),
        ('Full', 'Full'),
    ], validators=[DataRequired()], default='Normal')
    submit_new = SubmitField('新建任务')
    submit_new_and_start = SubmitField('新建任务并运行')
    #
    # def __init__(self, name="", url="", policy="Normal"):
    #     pass
    #     # NewScanTaskForm.Name.data = name
    #     # NewScanTaskForm.StartURL.data = url
    #     # NewScanTaskForm.ScanPolicy.data = policy



