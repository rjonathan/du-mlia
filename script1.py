import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def load_data():
    etude_sup = pd.read_csv('./data/etudes-superieurs.csv', sep=';', dtype={0: str})
    student_mat = pd.read_csv('./data/student/student-mat.csv', sep=';', dtype={0: str})
    student_por = pd.read_csv('./data/student/student-por.csv', sep=';', dtype={0: str})
    return etude_sup, student_mat, student_por


def pie_chart_target(data):
    target_counts = data['Target'].value_counts()
    plt.figure(figsize=(5, 5))
    plt.pie(
        target_counts,
        labels=target_counts.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=['#4CAF50', '#FF7043', '#42A5F5']
    )
    plt.title("Répartition des étudiants par statut")
    plt.axis('equal')
    plt.show()


def gender_distribution_plot(data):
    gender_labels = ['F', 'M']
    gender_values = data['Gender'].value_counts().tolist()
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'bar'}]], horizontal_spacing=0.25)

    fig.add_trace(go.Pie(labels=gender_labels, values=gender_values, name='Gender Distribution',
                         marker_colors=["#4CAF50", "#2CCED2"], hole=0.5), row=1, col=1)

    att = data.groupby(['Gender', 'Target']).agg(count=('Target', 'count')).reset_index()

    for target, color in zip(['Graduate', 'Dropout', 'Enrolled'], ["#4CAF50", "#FF7043", "#42A5F5"]):
        fig.add_trace(go.Bar(x=att[att.Target == target]['Gender'], y=att[att.Target == target]["count"],
                             name=target, marker=dict(color=color)), row=1, col=2)

    fig.update_layout(
        height=500, width=850, bargap=0.1,
        title_text="<b>Distribution par genre</b>",
        paper_bgcolor="#F4F6FB", plot_bgcolor="#F4F6FB",
        title_font=dict(size=20, family='Verdana', color='#003566'),
        hoverlabel=dict(font_size=13),
        legend=dict(orientation="h", yanchor="top", y=1.133, xanchor="right", x=1.1),
        shapes=[dict(type="line", xref='paper', yref='paper', x0=-0.06, y0=1.121, x1=0.435, y1=1.121)],
        xaxis=dict(tickmode='array', tickvals=['0', '1'], ticktext=['Femme', 'Homme'])
    )

    fig.show()


def plot_notes_distribution(data, dataset_name):
    fig, axs = plt.subplots(1, 3, figsize=(15, 4))
    for idx, col in enumerate(['G1', 'G2', 'G3']):
        axs[idx].hist(data[col], bins=20, color='skyblue', edgecolor='black')
        axs[idx].set_title(f'{dataset_name} - Notes {col}')
        axs[idx].set_xlim(0, 20)
        axs[idx].set_xlabel('Note')
        axs[idx].set_ylabel('Nombre d\'élèves')
    plt.tight_layout()
    plt.show()


def plot_dropout_percentages(data, dataset_name):
    total = len(data)
    zero_percentages = {
        'G1': (data['G1'] == 0).sum() / total * 100,
        'G2': (data['G2'] == 0).sum() / total * 100,
        'G3': (data['G3'] == 0).sum() / total * 100
    }
    plt.plot(list(zero_percentages.keys()), list(zero_percentages.values()),
             marker='o', linestyle='-', color='darkred', linewidth=2)
    plt.title(f"{dataset_name} - Pourcentage de décrochage (note = 0)")
    plt.xlabel("Période")
    plt.ylabel("Pourcentage d'élèves avec 0 (%)")
    plt.ylim(0, max(zero_percentages.values()) + 5)
    plt.grid(True)
    plt.show()


def main():
    etude_sup, student_mat, student_por = load_data()
    pie_chart_target(etude_sup)
    gender_distribution_plot(etude_sup)
    plot_notes_distribution(student_mat, "Mathématiques")
    plot_dropout_percentages(student_mat, "Mathématiques")
    plot_notes_distribution(student_por, "Portugais")
    plot_dropout_percentages(student_por, "Portugais")


if __name__ == "__main__":
    main()