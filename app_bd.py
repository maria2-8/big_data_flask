import sqlalchemy
from flask import Flask, render_template, request
import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy import text
import json

app = Flask(__name__)
@app.route('/')

def index():
    title = 'Site'
    return render_template('main_bd.html', title=title)

table_df = pd.read_csv("C:/Users/79215/Dropbox/ПК/Downloads/inton_units_with_f0.csv")

@app.route('/table', methods=("POST", "GET"))
def table_print():
    engine = create_engine('sqlite:///:memory:', echo=False)
    table_sql = table_df.to_sql('syntagmas_inf', engine)
    with engine.connect() as conn:
        synt_types = list(conn.execute(text('SELECT DISTINCT unit FROM syntagmas_inf')).fetchall())
        new_types = []
        for el in synt_types:
            el1 = el[0]
            new_types.append(el1)
        filenames = list(conn.execute(text('SELECT DISTINCT filename FROM syntagmas_inf')).fetchall())
        new_filenames = []
        for fn in filenames:
            fn1 = fn[0]
            new_filenames.append(fn1)
        return render_template('table.html', tables=[table_df.to_html(columns=['filename', 'unit', 'start', 'end', 'duration', 'words', 'transcription', 'f0_values'], classes='data', index=False, index_names=False)], caption = 'CORPRESS Files', new_types=new_types, new_filenames=new_filenames)

@app.route('/synt_type_sample', methods=["POST"])
def synt_type_sample():
    engine = create_engine('sqlite:///:memory:', echo=False)
    table_sql = table_df.to_sql('syntagmas_inf', engine)
    with engine.connect() as conn:
        selected_file = request.form.get('new_types')
        query = 'SELECT * FROM syntagmas_inf WHERE unit=:param'
        params = {'param': selected_file}
        res = conn.execute(text(query), params).fetchall()
        df_file = DataFrame(res)
        df_file.columns = conn.execute(text(query), params).keys()
        return render_template('res_table.html', tables = [df_file.to_html(columns=['filename', 'unit', 'start', 'end', 'duration', 'words', 'transcription', 'f0_values'], classes='data', index=False, index_names=False)], caption=f'Intonation Unit: {selected_file}')


@app.route('/filename_sample', methods=["POST"])
def filename_sample():
    engine = create_engine('sqlite:///:memory:', echo=False)
    table_sql = table_df.to_sql('syntagmas_inf', engine)
    with engine.connect() as conn:
        selected_file = request.form.get('new_filenames')
        query = 'SELECT * FROM syntagmas_inf WHERE filename=:param'
        params = {'param': selected_file}
        probe = conn.execute(text(query), params).fetchall()
        df_file = DataFrame(probe)
        df_file.columns = conn.execute(text(query), params).keys()
        return render_template('res_table.html', tables = [df_file.to_html(columns=['filename', 'unit', 'start', 'end', 'duration', 'words', 'transcription', 'f0_values'], classes='data', index=False, index_names=False)], caption=f'File: {selected_file}')

@app.route('/count_synts', methods=['POST'])
def count_synts():
    engine = create_engine('sqlite:///:memory:', echo=False)
    table_sql = table_df.to_sql('syntagmas_inf', engine)
    with engine.connect() as conn:
        count_synts = conn.execute(text('SELECT COUNT(unit) FROM syntagmas_inf')).fetchall()
        count_res = [tuple(row) for row in count_synts]
        json_string = json.dumps(count_res[0][0])
        return json_string

@app.route('/avg_duration', methods=['POST'])
def avg_dur_synts():
    engine = create_engine('sqlite:///:memory:', echo=False)
    table_sql = table_df.to_sql('syntagmas_inf', engine)
    with engine.connect() as conn:
        avg_dur = conn.execute(text('SELECT AVG(duration) FROM syntagmas_inf')).fetchall()
        avg_dur_res = [tuple(row) for row in avg_dur]
        json_string = json.dumps(avg_dur_res[0][0])
        return json_string

if __name__ == '__main__':
    app.run(debug=True)  # Запускаем сервер