import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from jinja2 import Environment, FileSystemLoader
import os

# Créer les dossiers si besoin
os.makedirs("output", exist_ok=True)

def generate_statut_pie_chart(data):
    target_counts = data['Target'].value_counts()
    plt.figure(figsize=(5, 5))
    plt.pie(target_counts, labels=target_counts.index, autopct='%1.1f%%',
            startangle=140, colors=['#4CAF50', '#FF7043', '#42A5F5'])
    plt.title("Répartition des étudiants par statut")
    plt.axis('equal')
    plt.tight_layout()
    path = "./statuts.png"
    plt.savefig(path)
    plt.close()
    return path


def generate_plotly_gender_chart(data):
    gender_labels = ['F', 'M']
    gender_values = data['Gender'].value_counts().tolist()
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'bar'}]], horizontal_spacing=0.25)

    fig.add_trace(go.Pie(labels=gender_labels, values=gender_values, hole=0.5,
                         marker_colors=["#4CAF50", "#2CCED2"]), row=1, col=1)

    att = data.groupby(['Gender', 'Target']).size().reset_index(name='count')
    colors = {"Graduate": "#4CAF50", "Dropout": "#FF7043", "Enrolled": "#42A5F5"}

    for target in att['Target'].unique():
        fig.add_trace(go.Bar(
            x=att[att.Target == target]['Gender'],
            y=att[att.Target == target]['count'],
            name=target,
            marker_color=colors.get(target, '#999999')
        ), row=1, col=2)

    fig.update_layout(title="Distribution par genre", height=400, showlegend=True)
    path = "./output/plotly_gender.html"
    fig.write_html(path)
    return path


def generate_math_distribution(data):
    fig, axs = plt.subplots(1, 3, figsize=(15, 4))
    for idx, col in enumerate(['G1', 'G2', 'G3']):
        axs[idx].hist(data[col], bins=20, color='skyblue', edgecolor='black')
        axs[idx].set_title(f'Distribution des notes {col}')
        axs[idx].set_xlim(0, 20)
        axs[idx].set_xlabel('Note')
        axs[idx].set_ylabel('Nombre d\'élèves')
    plt.tight_layout()
    path = "./math_notes.png"
    plt.savefig(path)
    plt.close()
    return path


def render_html_report(context):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("rapport.html")
    html_content = template.render(context)
    with open("output/rapport_final.html", "w", encoding="utf-8") as f:
        f.write(html_content)


def main():
    df = pd.read_csv("./data/etudes-superieurs.csv", sep=";", dtype={0: str})
    student_mat = pd.read_csv("./data/student/student-mat.csv", sep=";", dtype={0: str})

    statuts_img = generate_statut_pie_chart(df)
    gender_html_path = generate_plotly_gender_chart(df)
    with open(gender_html_path, "r", encoding="utf-8") as f:
        gender_plot_html = f.read()

    math_notes_img = generate_math_distribution(student_mat)

    context = {
        "statuts_img": statuts_img,
        "math_notes_img": math_notes_img,
        "plotly_html": gender_plot_html
    }

    render_html_report(context)
    print("✅ Rapport HTML généré dans: output/rapport_final.html")


if __name__ == "__main__":
    main()