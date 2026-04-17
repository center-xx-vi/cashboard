import json


def create_champion_website(json_file, local_gif_name):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Fehler: {json_file} nicht gefunden.")
        return
    except json.JSONDecodeError as e:
        print(f"Fehler in der JSON-Datei: {e}")
        return

    members = data[:25]
    monate_namen = ["Januar", "Februar", "März", "April", "Mai", "Juni",
                    "Juli", "August", "September", "Oktober", "November", "Dezember"]

    # --- KRONE LOGIK ---
    max_last_month_brutto = -1
    champion_name = ""
    last_data_index = -1

    for m in members[:-1]:
        blist = m.get("brutto_monate", [])
        if len(blist) > last_data_index:
            last_data_index = len(blist) - 1

    if last_data_index != -1:
        for m in members[:-1]:
            brutto_liste = m.get("brutto_monate", [])
            if len(brutto_liste) > last_data_index:
                val = brutto_liste[last_data_index]
                if val is not None and isinstance(val, (int, float)):
                    if val > max_last_month_brutto:
                        max_last_month_brutto = val
                        champion_name = m.get("name", "")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Cantata+One&display=swap" rel="stylesheet">
        <title>Cashboard Center XX/VI</title>
        <style>
            body {{
                background-image: url('{local_gif_name}');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                margin: 0;
                padding: 0;
                overflow: hidden;
                font-family: 'Cantata One', serif;
                height: 100vh;
                width: 100vw;
                color: white;
            }}

            .bg-overlay {{ 
                background-color: rgba(0, 0, 0, 0.75); 
                height: 100vh; 
                width: 100vw; 
                display: flex; 
                flex-direction: column;
                padding: 0.5vh 0.5vw;
                box-sizing: border-box;
            }}

            header {{
                text-align: center;
                height: 7vh; /* Etwas mehr Höhe für den größeren Titel */
                display: flex;
                align-items: center;
                justify-content: center;
            }}

            header h1 {{
                font-size: 3.5vh; /* DEUTLICH GRÖSSER */
                letter-spacing: 0.5em;
                margin: 0;
                font-weight: 900;
                text-transform: uppercase;
                background: linear-gradient(to bottom, #fff 40%, #ccc 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                drop-shadow: 0 0 20px rgba(0,0,0,0.5);
            }}

            .table-container {{
                flex-grow: 1;
                width: 100%;
                background: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255,255,255,0.1);
                overflow: hidden;
                margin-bottom: 0.5vh;
            }}

            table {{
                width: 100%;
                height: 100%;
                table-layout: fixed;
                border-collapse: collapse;
            }}

            th, td {{
                border: 1px solid rgba(255,255,255,0.07);
                text-align: center;
                vertical-align: middle;
                padding: 0 !important;
            }}

            .col-month {{
                width: 5.5vw;
                font-size: 1vh;
                text-transform: uppercase;
                background: rgba(0,0,0,0.5);
                color: #aaa;
                font-weight: bold;
            }}

            th div.name-label {{
                font-size: 0.62vw;
                font-weight: bold;
                text-transform: uppercase;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}

            .value-container {{
                position: relative;
                height: 100%;
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 0.75vw;
            }}

            .val-netto, .val-brutto {{
                position: absolute;
                width: 100%;
                transition: opacity 1s ease-in-out;
                font-weight: 900;
            }}

            .mode-netto .val-netto {{ opacity: 1; }}
            .mode-netto .val-brutto {{ opacity: 0; pointer-events: none; }}
            .mode-brutto .val-netto {{ opacity: 0; pointer-events: none; }}
            .mode-brutto .val-brutto {{ opacity: 1; }}

            .text-netto {{ color: #a6edd2; }} 
            .text-brutto {{ color: #ffc5ab; }}

            .champ-glow {{
                text-shadow: 0 0 10px rgba(255, 197, 171, 0.9);
                color: #fff !important;
                font-size: 0.88vw;
            }}

            .crown-icon {{
                font-size: 0.75vw;
                display: block;
                color: #fbbf24;
            }}

            .total-row {{
                background: rgba(255,255,255,0.12);
                height: 5.5vh;
            }}

            .total-row td {{
                font-size: 0.85vw;
                font-weight: 900;
                border-top: 2px solid rgba(255,255,255,0.2);
            }}

            footer {{
                height: 4vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }}

            .legend {{
                background: rgba(0,0,0,0.6);
                padding: 0.2vh 2vw;
                border-radius: 20px;
                border: 1px solid rgba(255,255,255,0.1);
                font-size: 1.2vh;
                display: flex;
                gap: 15px;
            }}
        </style>
    </head>
    <body class="mode-netto" id="main-body">
        <div class="bg-overlay">
            <header>
                <h1 class="font-black">Cashboard Center XX/VI</h1>
            </header>

            <div class="table-container">
                <table class="font-numbers">
                    <thead>
                        <tr style="height: 4.5vh;">
                            <th class="col-month">Monat</th>
                            {" ".join([f'''
                            <th class="relative {'bg-white/10' if i == len(members) - 1 else ''}">
                                {'<span class="crown-icon">👑</span>' if m['name'] == champion_name else ''}
                                <div class="name-label">{m.get('anzeigename', m['name'])}</div>
                            </th>''' for i, m in enumerate(members)])}
                        </tr>
                    </thead>
                    <tbody>
    """

    for idx, monat in enumerate(monate_namen):
        html_content += f"""
                        <tr style="height: 6.4vh;">
                            <td class="col-month">{monat}</td>
        """
        for i, m in enumerate(members):
            netto_liste = m.get("netto_monate", [])
            brutto_liste = m.get("brutto_monate", [])

            n_raw = netto_liste[idx] if idx < len(netto_liste) else None
            b_raw = brutto_liste[idx] if idx < len(brutto_liste) else None

            n_display = str(n_raw) if n_raw is not None else ""
            b_display = str(b_raw) if b_raw is not None else ""

            is_champ_cell = (m['name'] == champion_name and idx == last_data_index)
            b_class = "champ-glow" if is_champ_cell else ""
            special_col = "bg-white/5" if i == len(members) - 1 else ""

            html_content += f"""
                            <td class="{special_col}">
                                <div class="value-container">
                                    <span class="val-netto text-netto">{n_display}</span>
                                    <span class="val-brutto text-brutto {b_class}">{b_display}</span>
                                </div>
                            </td>
            """
        html_content += "</tr>"

    html_content += """
                        <tr class="total-row">
                            <td class="col-month font-black">TOTAL</td>
    """
    for i, m in enumerate(members):
        s_netto = sum(v for v in m.get("netto_monate", []) if v is not None)
        s_brutto = sum(v for v in m.get("brutto_monate", []) if v is not None)
        special_col = "bg-white/20" if i == len(members) - 1 else ""

        html_content += f"""
                            <td class="{special_col}">
                                <div class="value-container">
                                    <span class="val-netto text-netto">{s_netto}</span>
                                    <span class="val-brutto text-brutto">{s_brutto}</span>
                                </div>
                            </td>
        """

    html_content += """
                        </tr>
                    </tbody>
                </table>
            </div>

            <footer>
                <div class="legend">
                    <span id="label-brutto" style="color: #ffc5ab; font-weight: bold;">BAEH</span>
                    <span style="opacity: 0.3;">|</span>
                    <span id="label-netto" style="color: #a6edd2; font-weight: bold;">NVEH</span>
                </div>
            </footer>
        </div>

        <script>
            const body = document.getElementById('main-body');
            const lNetto = document.getElementById('label-netto');
            const lBrutto = document.getElementById('label-brutto');

            setInterval(() => {
                if (body.classList.contains('mode-netto')) {
                    body.classList.remove('mode-netto');
                    body.classList.add('mode-brutto');
                    lBrutto.style.opacity = "1";
                    lNetto.style.opacity = "0.3";
                } else {
                    body.classList.remove('mode-brutto');
                    body.classList.add('mode-netto');
                    lBrutto.style.opacity = "0.3";
                    lNetto.style.opacity = "1";
                }
            }, 10000);
        </script>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Dashboard mit vergrößertem Titel erstellt.")


LOCAL_GIF = "background.gif"
create_champion_website("data.json", LOCAL_GIF)