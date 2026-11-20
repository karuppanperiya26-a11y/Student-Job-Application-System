from pathlib import Path
import sqlite3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "analysis" / "output"

def frequencies(frame, owner, label):
    frame = frame.dropna(subset=[owner,label]).copy()
    frame[label] = frame[label].str.strip().str.casefold()
    frame = frame[frame[label].ne("")].drop_duplicates([owner,label])
    return frame.groupby(label)[owner].nunique().sort_values(ascending=False)

def plot(series, title, unit, filename, percentage=False):
    fig, ax = plt.subplots(figsize=(8,4.5), layout="constrained")
    if len(series):
        bars=ax.barh(series.index.astype(str),series.values,color="#266878")
        ax.bar_label(bars,fmt="%.1f" if percentage else "%d",padding=4)
        ax.invert_yaxis()
    else:
        ax.text(.5,.5,"No records",ha="center",transform=ax.transAxes)
    ax.set_xlim(0,110 if percentage else max([1,*series.values])*1.25)
    ax.set(title=title,xlabel=unit)
    fig.savefig(OUTPUT/filename,dpi=150)
    plt.close(fig)

def main():
    OUTPUT.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect((ROOT/"data/tracker.db").as_uri()+"?mode=ro",uri=True) as db:
        projects=pd.read_sql_query("SELECT id,domain,status FROM progress",db).drop_duplicates("id")
        technologies=pd.read_sql_query("SELECT * FROM project_tech",db)
        skills=pd.read_sql_query("SELECT * FROM student_skill",db)
    projects["domain"]=projects.domain.str.strip().str.casefold()
    rate=100 * projects.status.eq("Complete").groupby(projects.domain).mean()
    plot(rate,"Completed projects by domain","Completed projects (% of registered projects)","completion.png",True)
    plot(frequencies(technologies,"project_id","technology"),"Technology choices","Distinct projects","technologies.png")
    plot(frequencies(skills,"reg","skill"),"Recorded student skills","Distinct students","skills.png")
    print(f"{len(projects)} projects, {projects.status.eq('Complete').sum()} complete. Saved three charts.")
if __name__=="__main__":
    main()
