# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class GeneratorForm(FlaskForm):
    h = StringField("Distance between the center of the coordinate system and the center of the facet eye (mm)",
                    validators=[DataRequired()])
    l = StringField("Facet eye radius (mm)", validators=[DataRequired()])
    m = StringField("The number of ommatidia in the facet eye", validators=[DataRequired()])
    g_min = StringField("Minimal radius of the object (mm)", validators=[DataRequired()])
    g_max = StringField("Maximal radius of the object (mm)", validators=[DataRequired()])
    fi_min = StringField("Minimal azimuth of the object (rad, > 0)", validators=[DataRequired()])
    fi_max = StringField("Maximal azimuth of the object (rad, < 3.14)", validators=[DataRequired()])
    r_min = StringField("Minimal distance between the center of the coordinate system and the center of the object (mm)",
                    validators=[DataRequired()])
    r_max = StringField("Maximal distance between the center of the coordinate system and the center of the object (mm)",
                    validators=[DataRequired()])
    n = StringField("Number of precedents to generate", validators=[DataRequired()])
    lambd = StringField("Lambda", validators=[DataRequired()])
    gamma = StringField("Gamma", validators=[DataRequired()])
