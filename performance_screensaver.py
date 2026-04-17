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

    # Wir nehmen die ersten 25 Mitglieder
    members = data[:25]
    monate_namen = [
        "Januar", "Februar", "März", "April", "Mai", "Juni",
        "Juli", "August", "September", "Oktober", "November", "Dezember"
    ]

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
                # Wir prüfen auf Not None und Zahl
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
        <title>Team Cashboard Center XX/VI</title>
        <style>
            body {{
                background-image: url('{local_gif_name}');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                margin: 0;
                overflow: hidden;
                font-family: 'Cantata One', serif;
            }}
            .bg-overlay {{ 
                background-color: rgba(0, 0, 0, 0.65); 
                height: 100vh; width: 100vw; 
                display: flex; flex-direction: column;
                justify-content: center; align-items: center;     
            }}
            .compact-cell {{ 
                width: calc(100vw / {len(members) + 3}); 
                min-width: 0; position: relative; height: 40px;
            }}
            .value-container {{
                position: relative; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
            }}
            .val-netto, .val-brutto {{
                position: absolute;
                transition: opacity 1.5s ease-in-out, transform 1.5s ease-in-out;
                width: 100%;
            }}
            .mode-netto .val-netto {{ opacity: 1; transform: translateY(0); }}
            .mode-netto .val-brutto {{ opacity: 0; transform: translateY(5px); pointer-events: none; }}
            .mode-brutto .val-netto {{ opacity: 0; transform: translateY(-5px); pointer-events: none; }}
            .mode-brutto .val-brutto {{ opacity: 1; transform: translateY(0); }}
            .text-netto {{ color: #a6edd2; text-shadow: 0 0 15px rgba(166, 237, 210, 0.4); }} 
            .text-brutto {{ color: #ffc5ab; text-shadow: 0 0 15px rgba(255, 197, 171, 0.4); }}
            .crown {{
                position: absolute; top: 0px; left: 50%;
                transform: translateX(-50%) rotate(-10deg);
                font-size: 16px; color: #f59e0b;
                text-shadow: 0 0 12px rgba(245, 158, 11, 0.9);
                z-index: 50;
            }}
            .font-numbers {{ font-variant-numeric: tabular-nums; }}
            * {{ font-style: normal !important; }}
        </style>
    </head>
    <body class="text-white mode-netto" id="main-body">
        <div class="bg-overlay p-4">
            <header class="mb-6">
                <h1 class="text-5xl font-black uppercase tracking-[0.3em] text-white/90 drop-shadow-[0_0_30px_rgba(0,0,0,0.8)] text-center">
                    Cashboard Center XX/VI
                </h1>
            </header>

            <div class="w-[98vw] bg-black/30 backdrop-blur-md rounded-xl border border-white/10 shadow-2xl overflow-hidden mb-8">
                <table class="w-full table-fixed border-collapse">
                    <thead>
                        <tr class="bg-white/5">
                            <th class="w-24 pt-6 pb-4 border-r border-white/10 uppercase font-bold text-gray-400 text-[11px] tracking-widest">Monat</th>
                            {" ".join([f'''
                            <th class="pt-6 pb-4 border-r border-white/10 text-center compact-cell relative {'bg-white/10' if i == len(members) - 1 else ''}">
                                {'<div class="crown">👑</div>' if m['name'] == champion_name else ''}
                                <div class="text-[10px] font-bold uppercase truncate px-1 text-gray-200 tracking-tighter">
                                    {m.get('anzeigename', m['name'])}
                                </div>
                            </th>''' for i, m in enumerate(members)])}
                        </tr>
                    </thead>
                    <tbody class="font-numbers">
    """

    for idx, monat in enumerate(monate_namen):
        html_content += f"""
                        <tr class="border-b border-white/5 hover:bg-white/10 transition-all">
                            <td class="p-1 font-bold border-r border-white/10 bg-black/10 text-center text-gray-200 text-[14px] tracking-tight">
                                {monat}
                            </td>
        """
        for i, m in enumerate(members):
            netto_liste = m.get("netto_monate", [])
            brutto_liste = m.get("brutto_monate", [])

            n_raw = netto_liste[idx] if idx < len(netto_liste) else None
            b_raw = brutto_liste[idx] if idx < len(brutto_liste) else None

            # Logik: null (None) -> "", 0 -> "0"
            n_display = str(n_raw) if n_raw is not None else ""
            b_display = str(b_raw) if b_raw is not None else ""

            is_champ_cell = (m['name'] == champion_name and idx == last_data_index)
            glow_style = "filter: drop-shadow(0 0 12px rgba(255, 197, 171, 0.9)); font-size: 20px;" if is_champ_cell else ""

            special_style = "bg-white/5 font-black" if i == len(members) - 1 else "font-bold"
            border_style = "" if i == len(members) - 1 else "border-r border-white/10"

            html_content += f"""
                            <td class="p-1.5 {border_style} text-center compact-cell {special_style} text-[16px]">
                                <div class="value-container">
                                    <span class="val-netto text-netto">{n_display}</span>
                                    <span class="val-brutto text-brutto" style="{glow_style}">{b_display}</span>
                                </div>
                            </td>
            """
        html_content += "</tr>"

    html_content += """
                        <tr class="bg-white/10 border-t-2 border-white/20">
                            <td class="p-2 font-bold border-r border-white/10 text-center text-white uppercase tracking-tighter text-[13px]">
                                TOTAL
                            </td>
    """
    for i, m in enumerate(members):
        # Sicher summieren (null/None Werte ignorieren)
        s_netto = sum(v for v in m.get("netto_monate", []) if v is not None)
        s_brutto = sum(v for v in m.get("brutto_monate", []) if v is not None)

        special_style = "bg-white/20 font-black text-[18px]" if i == len(
            members) - 1 else "font-bold text-[17px] border-r border-white/10"

        html_content += f"""
                            <td class="p-1.5 text-center compact-cell {special_style}">
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
            <div class="flex gap-6 items-center bg-black/50 px-10 py-3 rounded-full border border-white/10 backdrop-blur-md shadow-lg">
                <span id="label-brutto" class="uppercase font-bold tracking-[0.2em] transition-all duration-[1500ms] text-sm" style="color: #ffc5ab;">BAEH</span>
                <span class="text-gray-600 font-thin text-xl">|</span>
                <span id="label-netto" class="uppercase font-bold tracking-[0.2em] transition-all duration-[1500ms] text-sm" style="color: #a6edd2;">NVEH</span>
            </div>
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
                    lNetto.style.opacity = "0.2";
                } else {
                    body.classList.remove('mode-brutto');
                    body.classList.add('mode-netto');
                    lBrutto.style.opacity = "0.2";
                    lNetto.style.opacity = "1";
                }
            }, 10000);
        </script>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Dashboard mit Null-Differenzierung erstellt.")

LOCAL_GIF = "background.gif"
create_champion_website("data.json", LOCAL_GIF)