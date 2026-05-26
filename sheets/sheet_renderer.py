from pathlib import Path


def generate_html_sheet(
    musicxml_path,
    output_html,
    title="Sheet Music"
):
    musicxml_name = Path(musicxml_path).name

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">

    <title>{title}</title>

    <script src="https://cdn.jsdelivr.net/npm/opensheetmusicdisplay/build/opensheetmusicdisplay.min.js"></script>

    <style>
        body {{
            font-family: Arial;
            margin: 40px;
            background: #ffffff;
        }}

        h1 {{
            text-align: center;
        }}

        #sheet {{
            width: 100%;
        }}
    </style>
</head>

<body>

<h1>{title}</h1>

<div id="sheet"></div>

<script>
async function renderSheet() {{

    const osmd = new opensheetmusicdisplay.OpenSheetMusicDisplay("sheet");

    await osmd.load("{musicxml_name}");

    osmd.render();
}}

renderSheet();

</script>

</body>
</html>
"""

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html)